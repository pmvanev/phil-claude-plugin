# Slice 02 — Measure the cold path and divide its time

**Goal.** `/phil:lambda-web-app-speed` reads a function's own logs and says which layer owns its cold
path, citing the query behind every number.

**Story:** US-02 · **Job:** make-a-lambda-web-app-load-fast

## IN scope
- `commands/lambda-web-app-speed.md` and `skills/lambda-web-app-speed/SKILL.md`, v1: measure only.
- Logs Insights queries over `REPORT` and `INIT_REPORT` lines, filtered on `@type` first: cold-start
  count and share, INIT and first-invoke percentiles, INIT timeouts, suppressed inits.
- The rule's measuring Principles: measure, then divide the time; name the path (cold, warm, repeat).
- A fixture of recorded log lines and the split it must yield.

## OUT scope
- Instrumenting deeper (slice 03); ranking, warmth and the browser (slice 04).
- Any write to AWS (D12).

## Learning hypothesis
Disproves "a function's existing logs are enough to name the layer that owns its cold path" **if** the
modive run cannot tell INIT from first invoke without new instrumentation.

## Acceptance criteria
See US-02 in `feature-delta.md`.

## Dependencies
- Slice 01 (the rule file exists). V2 closed before the queries ship.

## Effort / reference class
≤ 1 day. Reference class: `build-ci --speed`'s `pipeline-timings.py`.

## Production data
One read-only run against modive's simulation API, whose INIT hit the 10 s ceiling on 2026-10-26.
