# The Cold-Start Line

One record per cold start, in CloudWatch's Embedded Metric Format (EMF), timing the code's own share of
INIT one level down: its imports, its build, and its startup checks, each check on its own. `phases.py`
reads it. Propose it only where the layer `cold-path.py` named has no timing line already, or one that
times the layer as a single undivided phase.

## What it times, and how

- **Phases run one after another**, so they divide the code's share of INIT: `ColdStartImport`,
  `ColdStartBuild`, `ColdStartChecks`. Name each without a dot.
- **Checks run concurrently**, each on its own thread, so each is a member of `ColdStartChecks`:
  `ColdStartCheck.<name>`, with a dot. `ColdStartChecks` is the clock's time for all of them together;
  summing the members would count the overlap twice.
- **Time with a monotonic clock** (`time.perf_counter`), never wall time.
- **Start the import clock at the top of the handler's package**, before its first import, so the
  import phase includes the libraries.
- **Write the line from INIT, with a `phase` dimension** of `init`; a line timing the first request
  writes `first_request` (below).
- The gap between the code's total and `Init Duration` is the runtime's own start and any extension's,
  which the code cannot time; `phases.py --init-p50` reports it.
- **A timed-out INIT attempt writes nothing**: Lambda stops it before the line is written. Its retry,
  inside the first invoke, writes an ordinary `init` line where the code builds there too.

**Cost at INIT.** One clock read per phase and per check, about 50 ns each, and one JSON line, about
6 µs to format (measured 2026-10-26): well under a millisecond. EMF needs no agent and no extension;
CloudWatch extracts the metrics from the log line. **Cost in CloudWatch**: each metric name with each
dimension value is one custom metric, billed monthly — three phases and ten checks over two `phase`
values make 26.

## Reference, Python

```python
# <package>/__init__.py — first lines, before any other import
import time

IMPORT_STARTED = time.perf_counter()
```

```python
# <package>/cold_start.py
import json
import time
from concurrent.futures import ThreadPoolExecutor


def _ms(since):
    return (time.perf_counter() - since) * 1000


def run_checks(checks):
    """Every check at once, each timed; build every client a check uses before calling this."""
    def timed(check):
        started = time.perf_counter()
        check()
        return _ms(started)

    started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=max(len(checks), 1)) as pool:
        each = dict(zip(checks, pool.map(timed, checks.values())))
    return _ms(started), each


def write_line(namespace, phase, import_ms, build_ms, checks_ms, each_check_ms):
    metrics = {"ColdStartImport": import_ms, "ColdStartBuild": build_ms, "ColdStartChecks": checks_ms,
               **{f"ColdStartCheck.{name}": ms for name, ms in each_check_ms.items()}}
    print(json.dumps({
        "_aws": {"Timestamp": int(time.time() * 1000), "CloudWatchMetrics": [{
            "Namespace": namespace, "Dimensions": [["phase"]],
            "Metrics": [{"Name": name, "Unit": "Milliseconds"} for name in metrics]}]},
        "phase": phase, **metrics}))
```

```python
# <package>/handler.py — at module scope, so INIT runs it
import time

from . import IMPORT_STARTED
from .app import build_app, startup_checks  # imports above this line count as import time
from .cold_start import run_checks, write_line

import_ms = (time.perf_counter() - IMPORT_STARTED) * 1000
build_started = time.perf_counter()
app = build_app()                          # clients, pool, app object: LWS-1
checks_ms, each = run_checks(startup_checks(app))
build_ms = (time.perf_counter() - build_started) * 1000 - checks_ms
write_line("<app>", "init", import_ms, build_ms, checks_ms, each)
```

## When the first invoke owns the path

Where `cold-path.py` names the first invoke, the time is the handler's own work on its first request:
a lazy connection, a cache filled on first use. Time that request's steps the same way, from the
handler, once per environment, with `phase` set to `first_request`: each step a phase, and any
concurrent calls members of the step that awaits them.

## Read it back

Step 4 of the skill runs, over the measured window:

```
aws logs filter-log-events --log-group-name <group> --start-time <ms> --end-time <ms> \
  --max-items 200000 --filter-pattern '"ColdStartImport"' --output json [--profile <p>] [--region <r>] \
  | python3 -I ${CLAUDE_PLUGIN_ROOT}/skills/lambda-web-app-speed/scripts/phases.py \
      --init-p50 <seconds> --cold-starts <n> -
```

Lineage: modive's ADR-026 cold-start line, which split a 7 s INIT into imports, build and ten checks
on 2026-10-26, and beatrix's per-phase pass under its issue 254.
