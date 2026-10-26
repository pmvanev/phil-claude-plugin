# lambda-web-app-speed — Self-Test

The measurement is only as good as its count of cold starts, and two kinds of cold start carry no
`Init Duration`. These fixtures hand the timing scripts recorded log lines and state the split each
must reach.
Run them whenever `SKILL.md`, a script under `scripts/`, a file under `references/`,
`commands/lambda-web-app-speed.md` or the Principles of `rules/lambda-web-app-speed.md` change.

## What the fixtures pin

| Fixture | Situation | Expected outcome |
|---|---|---|
| `01-cold-path-split/` | 31 recorded platform lines from six execution environments of one web API, renamed: four cold starts with `Init Duration`, two after a failed INIT (both timeouts), two suppressed inits after invoke timeouts, and a memory change mid-window | 8 cold starts in 29 invokes, in three kinds; 21 warm; INIT owns the cold path; the memory change named |
| `02-init-phases/` | 12 recorded cold-start lines in Embedded Metric Format from the same API, renamed: three phases, and ten checks run concurrently, six of them waiting on one database | `ColdStartChecks` the largest phase, at 66% of the time the code timed; the ten checks reported beside it, never summed (their medians sum to 4.99 s inside 0.92 s); the six that wait alike marked |
| `03-rank-replay/` | beatrix's cold `GET /` at two points of its speed work, each candidate's estimate drawn only from what was measured before the fix | before the build moved into INIT, nothing ranked and both large gains listed as experiments; after memory, concurrent checks above bytecode — the order the real gains fell — and the target not reached |

## How to drive it

`python3 -m pytest -q tests/test_lambda_cold_path.py tests/test_lambda_init_phases.py
tests/test_lambda_rank.py` drives fixture 01 through `cold-path.py`, fixture 02 through `phases.py` and
fixture 03 through `rank.py`, with no model in the loop. The skill's prose — the window, the read-only
limits, the layer to look inside, Step 4's choice between a cause and the next instrument, and Step 5's
candidates and their estimates — has no driver; drive it by hand against a real function, as the
feature delta's slice records do.
