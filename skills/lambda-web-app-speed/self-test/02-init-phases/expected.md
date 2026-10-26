# Expected outcome — fixture 02 (INIT phases)

`events.json` holds the last twelve cold-start lines one web API wrote on 2026-10-25 and 26, as the AWS
CLI's `filter-log-events` returned them for the filter pattern `"ColdStartImport"`, renamed: the
namespace reads `reports`. Each line is one cold start's INIT, in CloudWatch's Embedded Metric Format:
three phases — `ColdStartImport`, `ColdStartBuild`, `ColdStartChecks` — and ten checks run concurrently
on a thread pool, `ColdStartCheck.<name>`.

**Expected**, pinned by `tests/test_lambda_init_phases.py`, every figure hand-counted from the raw lines:

- One group, `function=api phase=init`, of 12 lines.
- Totals across the window: checks 35,655.17 ms, imports 12,803.91 ms, build 5,675.85 ms. The largest
  phase is `ColdStartChecks`, 66% of the time the code timed — though imports are larger at p50
  (1,109.93 ms against 922.97 ms): five cold starts spent 5–8 s in the checks.
- The code timed itself at p50 2,329.36 ms: the sum of each line's three phases, never its checks.
- The ten checks' medians sum to 4,991.75 ms inside a phase whose median the clock timed at 922.97 ms.
- Six checks — `access`, `accounts.reader`, `accounts.rows`, `database`, `model_versions`,
  `version_catalog`, every one that opens a Postgres connection — reach 90% of the phase's p95, and are
  marked as waiting alike. `inputs`, `manifests`, `jobs` and `results` finish within 0.21 s.

**The hard assertion.** No member is added into the time the code timed. Summing them would report an
INIT of seven seconds where the clock saw two.
