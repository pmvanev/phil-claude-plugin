#!/usr/bin/env python3
"""Divide a Lambda function's cold path from its own platform log lines: how many invokes were cold,
how long INIT and the first invoke took, and which layer to look inside first.

Used by `/phil:lambda-web-app-speed`, in two calls. First the window, from the function's
`LastModified`:

    python3 cold-path.py --window 2026-10-26T14:37:09.000+0000

prints the window's start and end in epoch milliseconds: from the last change, or from fourteen days
ago where the change is older. Then the measurement, from what the AWS CLI returns, as a file or on
stdin:

    aws logs filter-log-events --log-group-name /aws/lambda/<function> \\
        --start-time <ms> --end-time <ms> --max-items 200000 \\
        --filter-pattern '?"REPORT RequestId" ?INIT_REPORT' --output json \\
      | python3 cold-path.py -

It reads the `REPORT` and `INIT_REPORT` lines and nothing else, so an application line the filter let
through is dropped unread. It needs no access to AWS and writes nothing.

**Three kinds of cold start, and only one carries `Init Duration`.** Read 2026-10-26 from a real
function's logs:

- **Recorded**: the `REPORT` carries `Init Duration`, and `Duration` is the first invoke alone.
- **After a failed INIT**: `INIT_REPORT ... Status: timeout` (or `error`) ends INIT; Lambda retries it
  inside the first invoke, whose `REPORT` has no `Init Duration` and whose `Duration` holds the retried
  INIT and the invoke together.
- **Suppressed init**: after an invoke that timed out or crashed (`Status: timeout` or `error` on its
  `REPORT`), Lambda resets the environment, and the next `REPORT` in that stream folds a fresh INIT
  into `Duration` the same way.

A count of `Init Duration` misses the last two, and their durations land among the warm invokes. Each
log stream is one execution environment, so the kinds are told apart by reading each stream in time
order. **At the window's edges** a stream is read without what came before it: a suppressed init whose
failed invoke fell before the start counts as warm, and a failed INIT whose retry fell after the end
counts to INIT with no cold start beside it.

**The owner is named from recorded splits only.** INIT's share is every `Init Duration` plus every
failed INIT's logged duration; the first invoke's is the `Duration` of each recorded cold start. A
`Duration` that folds INIT in cannot be divided from the logs, so it is reported as unsplit and
assigned to neither.

**Percentiles are nearest rank**: a value some line carries. Logs Insights' `pct()` matched nearest rank
exactly over 96 values, and approximated it over 7,876 (V2, 2026-10-26). Over twenty values or fewer,
nearest-rank p95 is the maximum.

**What it refuses.** A SnapStart restore, whose `REPORT` carries `Restore Duration` in place of
`Init Duration`: this version does not divide restores, and counting them warm would hide them. And a
line in the JSON log format, should one pass the filter; the skill's configuration read is the real
guard, since the filter matches text lines only.
"""
import argparse
import json
import math
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

FAILED = ("timeout", "error")
WINDOW_DAYS = 14
NEAR_CEILING_MS = 9000  # an INIT this long left its person waiting almost as long as a timeout


@dataclass(frozen=True)
class Line:
    stream: str
    time: int
    kind: str  # "report" or "init_report"
    duration: float
    init: Optional[float]
    status: Optional[str]
    memory: Optional[int]


class Refused(ValueError):
    pass


def _number(pattern, message):
    m = re.search(pattern, message)
    return float(m.group(1)) if m else None


def _status(message):
    m = re.search(r"Status: (\w+)", message)
    return m.group(1) if m else None


def _parse(event):
    message = event["message"]
    if message.lstrip().startswith("{") and '"platform.' in message:
        raise Refused("the function uses the JSON log format; this script reads the text format only")
    if message.startswith("REPORT RequestId:"):
        if "Restore Duration" in message:
            raise Refused("SnapStart restores are in the window; this version does not divide them")
        duration = _number(r"\tDuration: ([\d.]+) ms", message)
        if duration is None:
            return None
        memory = _number(r"Memory Size: (\d+) MB", message)
        return Line(event["logStreamName"], event["timestamp"], "report", duration,
                    _number(r"Init Duration: ([\d.]+) ms", message), _status(message),
                    int(memory) if memory is not None else None)
    if message.startswith("INIT_REPORT"):
        duration = _number(r"Init Duration: ([\d.]+) ms", message)
        if duration is None:
            return None
        return Line(event["logStreamName"], event["timestamp"], "init_report", duration, None,
                    _status(message), None)
    return None


def load(payload):
    """The platform lines in a `filter-log-events` response, grouped by stream and in time order."""
    streams = defaultdict(list)
    for event in payload.get("events", []):
        line = _parse(event)
        if line:
            streams[line.stream].append(line)
    for lines in streams.values():
        lines.sort(key=lambda l: l.time)
    return dict(streams)


def percentile(values, p):
    ordered = sorted(values)
    return ordered[max(0, math.ceil(p / 100 * len(ordered)) - 1)]


def _spread(values):
    if not values:
        return {"count": 0, "p50": None, "p95": None, "max": None}
    return {"count": len(values), "p50": percentile(values, 50), "p95": percentile(values, 95),
            "max": max(values)}


def _times(n, noun):
    return f"{n} {noun}{'' if n == 1 else 's'}"


def look_inside(summary):
    """The layer to look inside first, by these tests in order, with the reason."""
    owner, failed_init = summary["owner"], summary["init_failures"]
    if not summary["cold"]["total"]:
        return {"layer": None, "because": "no cold start in the window"}
    if failed_init["timeout"]:
        return {"layer": "INIT",
                "because": f"INIT reached its 10 s ceiling {_times(failed_init['timeout'], 'time')}"}
    owned = owner["init_ms"] if owner["layer"] == "INIT" else owner["first_invoke_ms"]
    if owner["layer"] is None or owner["unsplit_ms"] > owned:
        folded = []
        if failed_init["error"]:
            folded.append(_times(failed_init["error"], "failed INIT"))
        if summary["invoke_failures"]:
            folded.append(_times(summary["invoke_failures"], "failed invoke"))
        return {"layer": None,
                "because": f"{owner['unsplit_ms'] / 1000:.2f} s of cold-start time folds INIT into Duration, "
                           f"after {' and '.join(folded)}, and outweighs the "
                           f"{owner['layer'] or 'recorded'} share"}
    share = owned / (owner["init_ms"] + owner["first_invoke_ms"]) * 100
    return {"layer": owner["layer"], "because": f"it took {share:.0f}% of the split cold-start time"}


def summarize(streams):
    init, first, warm, unsplit = [], [], [], []
    cold = {"recorded": 0, "after_failed_init": 0, "suppressed": 0}
    failed_init_ms, init_failures, invoke_failures, memory = [], {"timeout": 0, "error": 0}, 0, set()
    for lines in streams.values():
        init_failed = previous_failed = False
        for line in lines:
            if line.kind == "init_report":
                if line.status in FAILED:
                    init_failed = True
                    init_failures[line.status] += 1
                    failed_init_ms.append(line.duration)
                continue
            if line.memory:
                memory.add(line.memory)
            if line.init is not None:
                cold["recorded"] += 1
                init.append(line.init)
                first.append(line.duration)
            elif init_failed:
                cold["after_failed_init"] += 1
                unsplit.append(line.duration)
            elif previous_failed:
                cold["suppressed"] += 1
                unsplit.append(line.duration)
            else:
                warm.append(line.duration)
            init_failed = False
            previous_failed = line.status in FAILED
            invoke_failures += previous_failed
    cold["total"] = sum(cold.values())
    init_ms, first_ms = sum(init) + sum(failed_init_ms), sum(first)
    summary = {
        "invokes": cold["total"] + len(warm),
        "cold": cold,
        "init_failures": init_failures,
        "invoke_failures": invoke_failures,
        "init": _spread(init),
        "first_invoke": _spread(first),
        "cold_wait": _spread([a + b for a, b in zip(init, first)]),
        "warm": _spread(warm),
        "unsplit": _spread(unsplit),
        "near_ceiling": sum(1 for ms in init if ms >= NEAR_CEILING_MS),
        "memory_sizes": sorted(memory),
        "environments": len(streams),
        "last_line_ms": max((l.time for lines in streams.values() for l in lines), default=None),
        "owner": {
            "layer": None if not (init_ms or first_ms) else "INIT" if init_ms >= first_ms else "first invoke",
            "init_ms": round(init_ms, 2),
            "first_invoke_ms": round(first_ms, 2),
            "unsplit_ms": round(sum(unsplit), 2),
        },
    }
    summary["look_inside"] = look_inside(summary)
    return summary


def _s(ms):
    return "—" if ms is None else f"{ms / 1000:.2f} s"


def _iso(ms):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def report(summary, truncated=False):
    cold, owner, failed_init = summary["cold"], summary["owner"], summary["init_failures"]
    share = cold["total"] / summary["invokes"] * 100
    lines = []
    if truncated:
        lines.append(f"⚠ truncated: the fetch stopped at its item cap, at {_iso(summary['last_line_ms'])}; "
                     "these numbers cover only the lines before it")
    if len(summary["memory_sizes"]) > 1:
        sizes = " and ".join(f"{m} MB" for m in summary["memory_sizes"])
        lines.append(f"⚠ the window mixes memory sizes ({sizes}): it spans a configuration change")
    lines += [
        f"Invokes: {summary['invokes']} in {summary['environments']} execution environments",
        f"Cold starts: {cold['total']} ({share:.1f}%) — {cold['recorded']} with Init Duration, "
        f"{cold['after_failed_init']} after a failed INIT, {cold['suppressed']} suppressed init(s)",
        f"Failed INITs: {failed_init['timeout']} timed out, {failed_init['error']} errored; "
        f"{summary['near_ceiling']} within a second of the 10 s ceiling · "
        f"invokes that timed out or crashed: {summary['invoke_failures']}",
        "",
        "| Slice | Count | p50 | p95 | Max |",
        "|---|---|---|---|---|",
    ]
    for label, key in (("INIT (recorded)", "init"), ("First invoke after INIT", "first_invoke"),
                       ("Cold wait: INIT and its first invoke", "cold_wait"),
                       ("INIT and invoke, unsplit", "unsplit"), ("Warm invoke", "warm")):
        s = summary[key]
        p95 = "p95 is the max" if 0 < s["count"] <= 20 else _s(s["p95"])
        lines.append(f"| {label} | {s['count']} | {_s(s['p50'])} | {p95} | {_s(s['max'])} |")
    lines.append("")
    if owner["layer"]:
        total = owner["init_ms"] + owner["first_invoke_ms"]
        part = owner["init_ms"] if owner["layer"] == "INIT" else owner["first_invoke_ms"]
        failed = ", counting each failed INIT's logged time to INIT" if any(failed_init.values()) else ""
        lines.append(f"{owner['layer']} owns the cold path: {_s(part)} of the {_s(total)} split between INIT "
                     f"and the first invoke ({part / total * 100:.0f}%){failed}")
    if owner["unsplit_ms"]:
        lines.append(f"Unsplit: {_s(owner['unsplit_ms'])} in {summary['unsplit']['count']} cold start(s) "
                     "fold INIT into Duration and are assigned to neither layer")
    choice = summary["look_inside"]
    if choice["layer"]:
        lines.append(f"Look inside: {choice['layer']}, because {choice['because']}")
    else:
        lines.append(f"Look inside: no layer can be named, because {choice['because']}")
    return "\n".join(lines)


def _utc(stamp):
    moment = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    if moment.utcoffset() is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment


def window(last_change=None, now=None, days=None):
    """The measurement window: from the last change, or from fourteen days ago where it is older; or,
    given `days`, that many days whatever changed."""
    end = _utc(now) if now else datetime.now(timezone.utc)
    floor = end - timedelta(days=days or WINDOW_DAYS)
    if not days and _utc(last_change) > floor:
        start, starts_at = _utc(last_change), "last change"
    else:
        start, starts_at = floor, f"{days or WINDOW_DAYS} days ago"
    return {"start_ms": int(start.timestamp() * 1000), "end_ms": int(end.timestamp() * 1000),
            "start": _iso(start.timestamp() * 1000), "end": _iso(end.timestamp() * 1000),
            "starts_at": starts_at}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--window", metavar="LAST_MODIFIED",
                        help="print the measurement window for a function last changed then, and stop")
    parser.add_argument("--days", type=int, help="a window of this many days, ignoring the last change")
    parser.add_argument("--now", help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true", help="print the summary as JSON")
    parser.add_argument("file", nargs="?", help="a filter-log-events JSON response, or - for stdin")
    args = parser.parse_args(argv)
    if args.window or args.days:
        print(json.dumps(window(args.window, args.now, args.days)))
        return 0
    if not args.file:
        parser.error("give a filter-log-events response, or --window")
    try:
        payload = json.load(sys.stdin if args.file == "-" else open(args.file))
    except (OSError, ValueError) as err:
        print(f"cold-path: {args.file} is not a complete filter-log-events response ({err}); the fetch "
              "was cut off, so move the window's start later and fetch again", file=sys.stderr)
        return 1
    try:
        streams = load(payload)
    except Refused as err:
        print(f"cold-path: {err}", file=sys.stderr)
        return 1
    except (KeyError, TypeError, AttributeError) as err:
        print(f"cold-path: {args.file} is not a filter-log-events response: {err}", file=sys.stderr)
        return 1
    if not any(l.kind == "report" for lines in streams.values() for l in lines):
        print("cold-path: no REPORT line in the window; the function served no request in it",
              file=sys.stderr)
        return 1
    summary = summarize(streams)
    truncated = "NextToken" in payload or "nextToken" in payload
    print(json.dumps({**summary, "truncated": truncated}, indent=2) if args.json else report(summary, truncated))
    return 0


if __name__ == "__main__":
    sys.exit(main())
