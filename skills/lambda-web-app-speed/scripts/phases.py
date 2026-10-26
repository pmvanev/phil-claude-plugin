#!/usr/bin/env python3
"""Divide a slice of a Lambda cold start one level down, from a timing line the function itself writes:
which phase took the time, and what ran inside it.

Used by `/phil:lambda-web-app-speed` to drill into the slice `cold-path.py` names. Give it what the AWS
CLI returns for the timing line's own records, as a file or on stdin:

    aws logs filter-log-events --log-group-name /aws/lambda/<function> \\
        --start-time <ms> --end-time <ms> --max-items 200000 \\
        --filter-pattern '"<one of the line's metric names>"' --output json \\
      | python3 phases.py -

**The line is CloudWatch's Embedded Metric Format** (EMF): a JSON record whose `_aws.CloudWatchMetrics`
names each metric, its unit and its dimensions, with the values as top-level keys. The script reads the
metrics whose unit is `Milliseconds` and ignores every other line and metric. Records that share their
dimension values — `function=api phase=init` — form one group.

**Two kinds of metric, told apart by name.** A name without a dot is a **phase**: phases run one after
another, so together they divide the time the code timed itself. A name with a dot is a **member** of
the phase whose name starts with the part before the first dot — `ColdStartCheck.database` is a member
of `ColdStartChecks`. Members ran concurrently inside their phase, so the script reports them beside it
and never adds them: the phase's own value is the time by the clock.

**Members that wait alike.** In the slow cold starts — those whose phase took at least its median — a
member that reaches 90% of its phase in at least half of them waits on whatever bounds the phase. Where
several do and the rest finish early, what those several share — a connection, a service — is the next
level to time. The test runs record by record, since a member's tail and its phase's tail can come
from different cold starts.

**The convention is checked where a check can see it.** A phase within 10% of the sum of two or more
other phases in every record is their total, not a phase, and the script refuses the line. A member
whose prefix starts two phases' names is listed unattached, never guessed. Other breaks — phases that
overlap without summing — only the line's code shows.

**The largest phase is the one with the most time across the window**, the sum over every record, since
a person pays every cold start and not the median one. Percentiles are nearest rank, as in
`cold-path.py`.

It needs no access to AWS and writes nothing.
"""
import argparse
import json
import math
import sys
from collections import defaultdict
from datetime import datetime, timezone

MILLISECONDS = "Milliseconds"
ALIKE = 0.9  # a member this close to its phase, in the same cold start, waits on what bounds the phase
TOTAL = 0.1  # a phase within this share of the others' sum, in every record, is their total


class BrokenConvention(ValueError):
    pass


def _metrics(record):
    """The record's millisecond metrics and its group key, or nothing where it is not EMF."""
    aws = record.get("_aws") if isinstance(record, dict) else None
    if not isinstance(aws, dict):
        return None, {}
    names, dimensions = [], []
    for directive in aws.get("CloudWatchMetrics", []):
        names += [m["Name"] for m in directive.get("Metrics", [])
                  if m.get("Unit") == MILLISECONDS and isinstance(m.get("Name"), str)]
        for dimension_set in directive.get("Dimensions", []):
            dimensions += [d for d in dimension_set if d not in dimensions]
    values = {n: float(record[n]) for n in names if isinstance(record.get(n), (int, float))}
    key = " ".join(f"{d}={record.get(d)}" for d in dimensions)
    return key, values


def load(payload):
    """Each group's records, as lists of {metric: milliseconds}."""
    groups = defaultdict(list)
    for event in payload.get("events", []):
        try:
            record = json.loads(event["message"])
        except ValueError:
            continue
        key, values = _metrics(record)
        if values:
            groups[key].append(values)
    return dict(groups)


def percentile(values, p):
    ordered = sorted(values)
    return ordered[max(0, math.ceil(p / 100 * len(ordered)) - 1)]


def _spread(values):
    return {"p50": percentile(values, 50), "p95": percentile(values, 95), "max": max(values),
            "total_ms": sum(values)}


def _parent(member, phases):
    """The one phase whose name starts with the member's prefix; none where no phase or two do."""
    prefix = member.split(".", 1)[0]
    claims = [p for p in phases if p.startswith(prefix)]
    return claims[0] if len(claims) == 1 else None


def _check_convention(records, phase_names):
    for name in phase_names:
        others = [p for p in phase_names if p != name]
        if len(others) < 2:
            continue
        spans = [r for r in records if name in r and all(o in r for o in others)]
        if spans and all(abs(r[name] - sum(r[o] for o in others)) <= TOTAL * r[name] for r in spans):
            raise BrokenConvention(
                f"{name} equals the sum of {', '.join(others)} in every record: it is their total, and the "
                "line breaks the phase convention, so its phases cannot be added")


def _waits_with(records, phase, member):
    slow_floor = percentile([r[phase] for r in records if phase in r], 50)
    slow = [r for r in records if r.get(phase, 0) >= slow_floor and member in r]
    near = [r for r in slow if r[member] >= ALIKE * r[phase]]
    return bool(slow) and len(near) * 2 >= len(slow)


def _group(records):
    names = {n for r in records for n in r}
    phase_names = sorted(n for n in names if "." not in n)
    _check_convention(records, phase_names)
    members = defaultdict(list)
    for name in sorted(n for n in names if "." in n):
        members[_parent(name, phase_names)].append(name)
    phases = []
    for name in phase_names:
        spread = _spread([r[name] for r in records if name in r])
        inside = [{"name": m, **_spread([r[m] for r in records if m in r])} for m in members.get(name, [])]
        for member in inside:
            member["waits_with_phase"] = _waits_with(records, name, member["name"])
        inside.sort(key=lambda m: -m["p50"])
        phases.append({"name": name, **spread, "members": inside, "members_concurrent": bool(inside),
                       "members_p50_sum_ms": sum(m["p50"] for m in inside)})
    phases.sort(key=lambda p: -p["total_ms"])
    timed = [sum(r.get(p, 0.0) for p in phase_names) for r in records if any(p in r for p in phase_names)]
    if not timed:
        return {"lines": len(records), "phases": [], "largest": None, "timed_ms": None,
                "unattached": [{"name": m} for m in sorted(names)]}
    return {
        "lines": len(records),
        "phases": phases,
        "largest": phases[0]["name"] if phases else None,
        "timed_ms": {"p50": percentile(timed, 50), "p95": percentile(timed, 95), "total_ms": sum(timed)},
        "unattached": [{"name": m} for m in members.get(None, [])],
    }


def summarize(groups):
    return {key: _group(records) for key, records in groups.items()}


def _s(ms):
    return f"{ms / 1000:.2f} s"


def _iso(ms):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _plural(n, noun):
    return f"{n} {noun}{'' if n == 1 else 's'}"


def report(summary, truncated_at=None, init_p50_ms=None, cold_starts=None):
    lines = []
    if truncated_at is not None:
        lines.append(f"⚠ truncated: the fetch stopped at its item cap, at {_iso(truncated_at)}; these numbers "
                     "cover only the lines before it")
    for key, g in summary.items():
        title = f"## {key or 'no dimensions'} — {_plural(g['lines'], 'cold-start line')}"
        if not g["phases"]:
            lines += [title, "no phase: every metric in this group has a dot, so nothing divides the slice — "
                      + ", ".join(m["name"] for m in g["unattached"]), ""]
            continue
        timed = g["timed_ms"]
        small = g["lines"] <= 20
        lines += [title, f"Timed by the code: p50 {_s(timed['p50'])}, p95 {_s(timed['p95'])}"]
        largest = next(p for p in g["phases"] if p["name"] == g["largest"])
        if init_p50_ms is not None:
            untimed = init_p50_ms - timed["p50"]
            lines.append(f"INIT p50 {_s(init_p50_ms)}; untimed: {_s(untimed)} at p50 — the runtime's own start, "
                         "any extension's, and whatever runs before the import clock starts")
            if untimed > largest["p50"]:
                lines.append("The untimed gap outweighs the largest phase: look first at what the code does not "
                             "time.")
        if cold_starts is not None:
            if g["lines"] > cold_starts:
                why = ("more lines than cold starts: a line whose cold start fell outside the window, or an INIT "
                       "that wrote twice")
            else:
                why = ("a timed-out INIT attempt writes no line, though its retry may; a cold start that wrote "
                       "none is missing here")
            lines.append(f"{_plural(g['lines'], 'line')} for {cold_starts} cold starts: {why}")
        lines += ["", "| Phase | p50 | p95 | Max | Total | Share |", "|---|---|---|---|---|---|"]
        for p in g["phases"]:
            share = p["total_ms"] / timed["total_ms"] * 100 if timed["total_ms"] else 0
            p95 = "p95 is the max" if small else _s(p["p95"])
            lines.append(f"| {p['name']} | {_s(p['p50'])} | {p95} | {_s(p['max'])} | "
                         f"{_s(p['total_ms'])} | {share:.0f}% |")
        share = largest["total_ms"] / timed["total_ms"] * 100 if timed["total_ms"] else 0
        lines += ["", f"Largest phase: {largest['name']}, {share:.0f}% of the time the code timed"]
        if len(g["phases"]) == 1 and not largest["members"]:
            lines.append("The line holds one undivided phase, so it divides nothing: treat the layer as having no "
                         "timing line.")
        if largest["members"]:
            lines += [f"Inside it, {len(largest['members'])} members ran concurrently: their medians sum to "
                      f"{_s(largest['members_p50_sum_ms'])} inside a phase the clock timed at "
                      f"{_s(largest['p50'])}, so read each against the phase, never their sum.",
                      "", "| Member | p50 | p95 | Max | Waits with the phase |", "|---|---|---|---|---|"]
            lines += [f"| {m['name']} | {_s(m['p50'])} | {'p95 is the max' if small else _s(m['p95'])} | "
                      f"{_s(m['max'])} | {'yes' if m['waits_with_phase'] else ''} |" for m in largest["members"]]
            alike = [m["name"] for m in largest["members"] if m["waits_with_phase"]]
            if 1 < len(alike) < len(largest["members"]):
                lines.append(f"{len(alike)} members wait alike, near the phase's p95, while the rest finish "
                             "early: what they share is the next level to time.")
        if g["unattached"]:
            lines.append("Members no phase's name claims: " + ", ".join(m["name"] for m in g["unattached"]))
        lines.append("")
    return "\n".join(lines).rstrip()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--json", action="store_true", help="print the summary as JSON")
    parser.add_argument("--init-p50", type=float, metavar="SECONDS",
                        help="the recorded INIT p50 cold-path.py reported, to name the untimed gap")
    parser.add_argument("--cold-starts", type=int, metavar="N",
                        help="the cold starts cold-path.py counted, to set the lines against")
    parser.add_argument("file", help="a filter-log-events JSON response, or - for stdin")
    args = parser.parse_args(argv)
    try:
        payload = json.load(sys.stdin if args.file == "-" else open(args.file))
        groups = load(payload)
    except (OSError, ValueError) as err:
        print(f"phases: {args.file} is not a complete filter-log-events response ({err}); the fetch was "
              "cut off, so move the window's start later and fetch again", file=sys.stderr)
        return 1
    except (KeyError, TypeError, AttributeError) as err:
        print(f"phases: {args.file} is not a filter-log-events response: {err}", file=sys.stderr)
        return 1
    if not groups:
        print("phases: no Embedded Metric Format line with a Milliseconds metric in the window; check the "
              "filter pattern names one of the line's metrics", file=sys.stderr)
        return 1
    try:
        summary = summarize(groups)
    except BrokenConvention as err:
        print(f"phases: {err}", file=sys.stderr)
        return 1
    truncated_at = None
    if "NextToken" in payload or "nextToken" in payload:
        truncated_at = max((e["timestamp"] for e in payload.get("events", [])), default=0)
    init_ms = args.init_p50 * 1000 if args.init_p50 is not None else None
    print(json.dumps({**summary, "truncated": truncated_at is not None}, indent=2) if args.json
          else report(summary, truncated_at, init_ms, args.cold_starts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
