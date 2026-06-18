# Critic / Gate Self-Test

The refactor-loop gate is software under test. A gate bug is silent — a critic stuck on
`accept`, or a hard gate that fails to revert, looks exactly like fast convergence. These
fixtures feed the loop deliberately-bad refactorings and assert each is **rejected**. If any
bad refactoring is *accepted*, the gate is decorative.

This suite is the **regression gate for the frozen rubric** (`refactor/rubric.md`). Run it
whenever the rubric or a loop prompt changes — every such edit is non-monotonic, so the
rubric is never changed and eyeballed; it is changed and regression-tested here.

## The fixtures — each MUST be rejected

| Fixture | The bad refactoring | Must be caught by | Expected outcome |
|---|---|---|---|
| `01-breaks-test/` | A diff that changes observable behavior so a test fails. | **G3** (hard-gate-red) at TEST | `REVERT` |
| `02-broadens-api/` | A diff that adds a public export while the manifest claims `public_api_touched: false`. | **G4** (manifest-mismatch) at TEST | `REVERT` |
| `03-no-span-praise/` | A critic verdict of generic praise (`"perfect refactor!"`) with no `span`. | Anti-flattery clause (rubric §Scoring) | coerced to `CANNOT_ASSESS`, never `accept` |

## Layout

Each fixture is self-contained:

- `before.py` — the starting code (its test passes: this is the green baseline).
- `test_before.py` — the behavioral test that pins the contract.
- `bad-diff.patch` — the deliberately-bad refactoring to apply.
- `manifest.json` — the proposer's predicted-impact manifest for the bad diff.
- `expected.md` — the outcome the gate must produce, and the guard that must produce it.

Fixture `03` also carries `verdict.json` — the flattering, span-less critic output that the
anti-flattery clause must coerce.

## How to run it as the rubric regression gate

For each fixture:

1. Establish the green baseline: run `test_before.py` against `before.py` and confirm it
   passes (mirrors INIT / G1).
2. Apply `bad-diff.patch`.
3. Drive the gate the loop would drive:
   - **01:** run the test suite, read the exit code. Assert non-zero → the loop must REVERT
     (G3). A green result here means the gate is broken.
   - **02:** compute the public-API diff (Python: `__all__` + top-level defs), compare to
     `manifest.json`'s `public_api_touched: false`. Assert mismatch → REVERT (G4).
   - **03:** feed `verdict.json` to the verdict router. Assert the span-less praise is
     coerced to `CANNOT_ASSESS`, not accepted.
4. Compare against the fixture's `expected.md`. Any fixture that is *accepted* is a gate
   failure — block the rubric change.

These are metamorphic/differential tests on the gate itself, not on the target code.
