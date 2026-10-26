#!/usr/bin/env python3
"""Order the fixes for one measured path by the time each saves, and draw the line where the path meets
its target.

Used by `/phil:lambda-web-app-speed` after it has measured and drilled. Give it one JSON document, as a
file or on stdin (`-`):

    {"path": {"name": "cold wait: INIT and its first invoke", "now_ms": 6000,
              "target_ms": 2500, "noise_ms": 320},
     "candidates": [
       {"name": "...", "kind": "removes", "effort": "M", "standard": true,
        "saves": [{"basis": "removes", "low": 1200, "high": 1250}],
        "evidence": "the measurement every figure rests on"},
       {"name": "...", "kind": "experiment", "effort": "S", "standard": true, "evidence": "..."}]}

    python3 rank.py - < candidates.json

**A candidate that removes measured work** states how, part by part, with the measured low and high —
the p50 and the p95 its measurement reported — and the script computes the saving, summing the parts:

| `basis` | The part | Saves |
|---|---|---|
| `removes` | a call or phase taken off the path: `low`, `high` | `low` to `high` |
| `concurrent` | calls run one after another, made concurrent: `sum` and `slowest`, each `low`/`high` | the sum less the slowest: `sum.low − slowest.high` to `sum.high − slowest.low` |
| `batch` | N calls made one: `calls`, and one call's `low`, `high` | N − 1 calls |
| `scaled` | a time a fix shrinks by a measured fraction: `low`, `high`, `fraction` [low, high] | the time times the fraction |

**An experiment** changes the machine rather than the work — more memory, work moved into INIT — and no
measurement this skill takes predicts its saving: try it, measure, keep or revert.

**The order** (D17, 2026-10-26): the largest midpoint saving first. Savings within 10% of each other are
near-ties, broken by effort (S, then M, then L) and then by the standard, documented pattern (D13). A
range that starts at nothing, or whose top is more than three times its bottom, is listed as too wide to
rank. A saving whose top lies inside `noise_ms`, the spread of repeated measurements, falls below the
line; with no `noise_ms`, nothing does.

**The stopping line** walks the ranked fixes, subtracting each midpoint from `now_ms`, and falls after the
first that brings the path to `target_ms` (D16) — at once where the path already meets it. With no
`target_ms` there is no line: the script borrows no target the project did not state.

It needs no access to AWS and writes nothing.
"""
import argparse
import json
import sys

EFFORT = {"S": 1, "M": 2, "L": 3}
KINDS = ("removes", "experiment")
NEAR_TIE = 0.1
TOO_WIDE = 3


class Refused(ValueError):
    pass


def _pair(part, where):
    low, high = part.get("low"), part.get("high")
    if not all(isinstance(v, (int, float)) for v in (low, high)) or low < 0 or low > high:
        raise Refused(f"{where}: low and high are milliseconds, 0 ≤ low ≤ high")
    return low, high


def _part(part):
    basis = part.get("basis")
    if basis == "removes":
        return _pair(part, "removes")
    if basis == "concurrent":
        total, slowest = _pair(part.get("sum", {}), "concurrent sum"), _pair(part.get("slowest", {}), "slowest")
        return max(total[0] - slowest[1], 0), total[1] - slowest[0]
    if basis == "batch":
        calls = part.get("calls")
        if not isinstance(calls, int) or calls < 2:
            raise Refused("batch: calls is a whole number of at least 2")
        low, high = _pair(part, "batch")
        return (calls - 1) * low, (calls - 1) * high
    if basis == "scaled":
        low, high = _pair(part, "scaled")
        fraction = part.get("fraction")
        if (not isinstance(fraction, list) or len(fraction) != 2
                or not 0 <= fraction[0] <= fraction[1] <= 1):
            raise Refused("scaled: fraction is [low, high], each between 0 and 1")
        return round(low * fraction[0], 2), round(high * fraction[1], 2)
    raise Refused(f"basis {basis!r} is none of removes, concurrent, batch, scaled")


def saving(parts):
    """The range a candidate saves: the sum of its parts' ranges."""
    ranges = [_part(p) for p in parts]
    return round(sum(r[0] for r in ranges), 2), round(sum(r[1] for r in ranges), 2)


def _mid(candidate):
    low, high = candidate["range"]
    return (low + high) / 2


def _check(candidate):
    name = candidate.get("name", "?")
    for field in ("name", "kind", "effort", "evidence"):
        if not candidate.get(field):
            raise Refused(f"candidate {name!r} has no {field}; every estimate names the measurement behind it")
    if candidate["kind"] not in KINDS:
        raise Refused(f"candidate {name!r}: kind is removes or experiment")
    if candidate["effort"] not in EFFORT:
        raise Refused(f"candidate {name!r}: effort is S, M or L")
    if not isinstance(candidate.get("standard"), bool):
        raise Refused(f"candidate {name!r}: standard is true or false")
    if candidate["kind"] == "removes":
        if not candidate.get("saves"):
            raise Refused(f"candidate {name!r}: saves lists the parts it removes")
        try:
            candidate["range"] = saving(candidate["saves"])
        except Refused as err:
            raise Refused(f"candidate {name!r}: {err}") from None


def _order(fixes):
    fixes = sorted(fixes, key=lambda c: -_mid(c))
    ordered = []
    while fixes:
        lead = _mid(fixes[0])
        cluster = [c for c in fixes if _mid(c) >= lead * (1 - NEAR_TIE)]
        fixes = [c for c in fixes if c not in cluster]
        ordered += sorted(cluster, key=lambda c: (EFFORT[c["effort"]], not c["standard"], -_mid(c)))
    return ordered


def plan(spec):
    path = spec["path"]
    if not isinstance(path.get("now_ms"), (int, float)):
        raise Refused("path: now_ms is the path's present time in milliseconds")
    target, noise = path.get("target_ms"), path.get("noise_ms") or 0
    ranked, experiments, too_wide, inside_noise = [], [], [], []
    for candidate in spec["candidates"]:
        _check(candidate)
        if candidate["kind"] == "experiment":
            experiments.append(candidate)
            continue
        low, high = candidate["range"]
        if high < noise:
            inside_noise.append(candidate)
        elif low <= 0 or high > TOO_WIDE * low:
            too_wide.append(candidate)
        else:
            ranked.append(candidate)
    ranked = _order(ranked)
    remaining, stop_after, reaches = path["now_ms"], None, None
    if target is not None:
        stop_after, reaches = len(ranked), False
        if remaining <= target:
            stop_after, reaches = 0, True
        else:
            for i, fix in enumerate(ranked, 1):
                remaining -= _mid(fix)
                if remaining <= target:
                    stop_after, reaches = i, True
                    break
    return {
        "path": path,
        "ranked": ranked,
        "stop_after": stop_after,
        "expected_ms": remaining,
        "reaches_target": reaches,
        "experiments": sorted(experiments, key=lambda c: (EFFORT[c["effort"]], not c["standard"])),
        "too_wide": too_wide,
        "inside_noise": inside_noise,
    }


def _s(ms):
    return f"{ms / 1000:.2f} s"


def report(p):
    path = p["path"]
    target = path.get("target_ms")
    lines = [f"Path: {path['name']} — now {_s(path['now_ms'])}, "
             + (f"target {_s(target)}" if target is not None else "no target stated")
             + (f", noise {_s(path['noise_ms'])}" if path.get("noise_ms") else ""), ""]
    if p["stop_after"] == 0:
        lines.append("The path is already within the target: no fix is needed for it.")
    lines.append("Ranked by time saved:")
    if not p["ranked"]:
        lines.append("  none: no fix's saving can be read off the measurement")
    for i, fix in enumerate(p["ranked"], 1):
        low, high = fix["range"]
        lines.append(f"  {i}. {fix['name']} — −{_s(_mid(fix))} ({_s(low)} to {_s(high)}) · effort {fix['effort']}"
                     f"{' · standard' if fix['standard'] else ''}")
        lines.append(f"     from: {fix['evidence']}")
        if p["reaches_target"] and i == p["stop_after"]:
            lines.append(f"  — stop here: expected {_s(p['expected_ms'])}, within the target —")
    if target is None and p["ranked"]:
        lines.append("  — no target stated, so no stopping line —")
    elif p["reaches_target"] is False and p["ranked"]:
        lines.append(f"  — the ranked fixes do not reach the target: expected {_s(p['expected_ms'])} after all "
                     f"{len(p['ranked'])} —")
    if p["experiments"]:
        lines += ["", "Experiments — try, measure, keep or revert:"]
        lines += [f"  - {c['name']} · effort {c['effort']} — {c['evidence']}" for c in p["experiments"]]
    if p["too_wide"]:
        lines += ["", "Too wide to rank — measure further, or try as an experiment:"]
        lines += [f"  - {c['name']} · range too wide to rank: {_s(c['range'][0])} to {_s(c['range'][1])} — "
                  f"{c['evidence']}" for c in p["too_wide"]]
    if p["inside_noise"]:
        lines += ["", "Inside the noise — not worth making for speed:"]
        lines += [f"  - {c['name']} · up to {_s(c['range'][1])} — {c['evidence']}" for c in p["inside_noise"]]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--json", action="store_true", help="print the plan as JSON")
    parser.add_argument("file", help="the candidates, as a file or - for stdin")
    args = parser.parse_args(argv)
    try:
        if args.file == "-":
            spec = json.load(sys.stdin)
        else:
            with open(args.file) as f:
                spec = json.load(f)
        p = plan(spec)
    except Refused as err:
        print(f"rank: {err}", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, TypeError) as err:
        print(f"rank: cannot read {args.file}: {err}", file=sys.stderr)
        return 1
    print(json.dumps(p, indent=2) if args.json else report(p))
    return 0


if __name__ == "__main__":
    sys.exit(main())
