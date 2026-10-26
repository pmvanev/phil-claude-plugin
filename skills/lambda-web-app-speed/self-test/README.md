# lambda-web-app-speed — Self-Test

The measurement is only as good as its count of cold starts, and two kinds of cold start carry no
`Init Duration`. These fixtures hand the timing script recorded log lines and state the split it must
reach. Run them whenever `SKILL.md`, `scripts/cold-path.py`, `commands/lambda-web-app-speed.md` or the
Principles of `rules/lambda-web-app-speed.md` change.

## What the fixtures pin

| Fixture | Situation | Expected outcome |
|---|---|---|
| `01-cold-path-split/` | 31 recorded platform lines from six execution environments of one web API, renamed: four cold starts with `Init Duration`, two after a failed INIT (both timeouts), two suppressed inits after invoke timeouts, and a memory change mid-window | 8 cold starts in 29 invokes, in three kinds; 21 warm; INIT owns the cold path; the memory change named |

## How to drive it

`python3 -m pytest -q tests/test_lambda_cold_path.py` drives fixture 01 through the script, with no
model in the loop. The skill's prose — the window, the read-only limits, the layer to look inside — has
no driver; drive it by hand against a real function, as the feature delta's slice 02 record does.
