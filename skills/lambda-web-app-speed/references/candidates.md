# Candidates for the Ranking

The JSON `scripts/rank.py` reads on stdin, built in Step 5 of the skill from Steps 1, 3 and 4.

```
python3 -I ${CLAUDE_PLUGIN_ROOT}/skills/lambda-web-app-speed/scripts/rank.py - <<'JSON'
{"path": {"name": "cold wait: INIT and its first invoke", "now_ms": <cold wait p50>,
          "target_ms": <budget, or null>, "noise_ms": <spread of repeated runs, or null>},
 "candidates": [
  {"name": "<the fix>", "kind": "removes", "effort": "S|M|L", "standard": true,
   "saves": [{"basis": "removes", "low": <p50>, "high": <p95>}],
   "evidence": "<the report lines the figures come from>"},
  {"name": "<the machine change>", "kind": "experiment", "effort": "S|M|L", "standard": true,
   "evidence": "<why no measurement predicts it>"}]}
JSON
```

## A fix that removes measured work

`"kind": "removes"` lists, under `saves`, each part the fix removes, with the part's measured p50 as
`low` and its p95 as `high`. The script computes the saving from the basis and sums the parts:

| `basis` | Use it for | Give |
|---|---|---|
| `removes` | a call or phase taken off the path | `low`, `high` |
| `concurrent` | calls run one after another, made concurrent | `sum` and `slowest`, each with `low` and `high` |
| `batch` | N calls made one | `calls`, and one call's `low` and `high` |
| `scaled` | a time a fix shrinks by a fraction the person measured | `low`, `high`, and `fraction` as `[low, high]` |

## A fix that changes the machine

`"kind": "experiment"` — more memory, work moved from the first invoke into INIT — carries no `saves`:
no measurement the skill takes predicts what it saves.

## Every candidate

- **`effort`**: `S` within hours, `M` about a day, `L` longer.
- **`standard`**: `true` where the fix is a documented pattern — AWS's guidance, or a Preferred form of
  the rule's rows; `false` otherwise.
- **`evidence`**: the numbers the figures rest on, as Steps 3 and 4 reported them, or the person's own
  measurement, cited. `rank.py` refuses a candidate without it.
