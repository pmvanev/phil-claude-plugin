# Expected outcome — fixture 01 (walking skeleton)

**Expected decision:** `CONFORMS`.

`ask.md` is the verbatim framing emitted during this feature's own DISCUSS wave on 2026-08-21, before any
artifact was written. It is the baseline the three failing fixtures in slice 02 are measured against.

## What is asserted mechanically

- **143 words**, against a ceiling of 200. Counted by `tests/test_decision_request_fixtures.py`, not by
  reading.
- **Zero forbidden tokens.** No wave label, issue number, slice id, decision number, skill name, command
  name-as-noun, or file path appears in the ask.

Both are re-computed on every run rather than trusted from `manifest.json`. A fixture that recorded a
count and never re-derived it would drift silently the first time anyone edited `ask.md` — which is the
whole class of defect this repo keeps finding.

## What is asserted by reading, and is not automated

- The framing states **what is being decided** and **what turns on it** before any option appears. Each of
  the three parts does both: the depth question says the fuller version maps the malformed case *"which is
  the actual complaint"*; the persona question says the alternative is *"an existing one wearing a
  different hat"*; the ceiling question says a target means *"the standard becomes advice"*.
- Each option in the accompanying `AskUserQuestion` call named its own cost, not only its benefit.

`expected_decision` is `CONFORMS` on the mechanical half. The reading half is recorded here so a later
session can check it rather than re-derive it.

## Gate failures

- Recording `measured_words` and never recomputing it. The number in `manifest.json` is documentation; the
  test is the authority. If they disagree the test wins and the manifest is stale.
- Treating this fixture as proof the ceiling works. **One instance is not a distribution.** It proves the
  ceiling is not *obviously* wrong, which is what it needed to survive DISCUSS. Slice 02 is where it meets
  input designed to break it.
- Adding a forbidden token to `ask.md` to make it read more precisely. The ask is a fixture now; edit it
  and the baseline is gone.
