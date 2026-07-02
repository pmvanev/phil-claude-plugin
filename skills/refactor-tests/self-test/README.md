# refactor-tests — Acceptance Self-Test

The `refactor-tests` **safety loop** is the software under test. Its bugs are silent: a gate
that fails to revert, or a tool that refactors on red, looks exactly like a smooth run. These
fixtures feed the loop known situations and assert each produces the correct **gate outcome**
(`STOP` / `REVERT` / `COMMIT`) or the correct **backlog**. A fixture that produces the wrong
outcome means a safety guard is decorative.

This suite is the **acceptance + regression gate** for `skills/refactor-tests/SKILL.md`. Run it
whenever the skill or the command loader changes — every such edit is non-monotonic, so the
skill is never changed and eyeballed; it is changed and regression-tested here. Format and
intent mirror `refactor/self-test/` (the refactor-loop gate self-test) — the plugin's
established way to test a skill/gate.

## What the fixtures pin

| Fixture | Situation | Pins (feature-delta AC) | Guard under test | Expected outcome |
|---|---|---|---|---|
| `01-baseline-red-stop/` | baseline suite already red | AC2.5 | never-refactor-on-red (D7/DD6) | `STOP` — nothing applied, nothing committed |
| `02-postapply-red-autorevert/` | a move silently reds the suite | AC2.3 | post-apply auto-revert (D7/DD6) | `REVERT` — `git checkout`, item `blocked`, no human prompt |
| `03-approve-commit-on-green/` | correct move, suite green, human approves | AC2.1, AC2.2 (**walking skeleton**) | human-approval port (DD4) + commit-only-on-green | `COMMIT` — one commit, suite green |
| `04-reject-reverts-clean/` | correct move, suite green, human rejects | AC2.4 | human is the oracle, not the suite (D2) | `REVERT` — clean tree, nothing written |
| `05-review-seeds-backlog/` | file with all four D5 smells | AC1.1, AC1.2, AC1.3 | D5-only detector (DD3) | backlog matching `expected-backlog.md` |

Deterministic safety mechanics (01, 02, 03-commit, 04-revert) are the driveable core. The
**human decision itself** (approve vs reject in 03/04) is supplied by the fixture manifest so
the suite can run unattended; in live use it comes from the developer at the AskUserQuestion
gate (D2). Detection precision (05) is validated by dogfood audit against the KPI (≤20% false
positives), not by byte-exact line matching.

## Layout

Each fixture is self-contained and dependency-free (`python -m pytest` runs it):

- `cart.py` — the tiny SUT (NOT the thing refactored — the *test file* is). Kept green.
- `test_cart.py` / `test_cart_smells.py` — the test file the loop scopes to.
- `move.patch` — the proposed structure-only move (fixtures 02–04). Applies with `git apply`.
- `manifest.json` — the proposal metadata (named D5 move, target span, rationale) and, for the
  human-gated fixtures, the `human_decision` the driver should supply.
- `expected.md` — the gate outcome the loop must produce, and the guard that must produce it.
- `expected-backlog.md` — fixture 05 only: the backlog `--review` must write.

## How to drive it (as the skill acceptance/regression gate)

For each fixture:

1. **Baseline.** Run `python -m pytest -q` in the fixture dir.
   - `01`: expect **red** — this IS the precondition.
   - `02`–`04`: expect **green** — the loop's baseline check must pass here.
2. **Drive the loop** exactly as `/phil:refactor-tests` would, using `manifest.json`:
   - `01`: the loop sees red baseline → must **STOP**. Assert the tree is unchanged and no
     commit was made.
   - `02`: apply `move.patch`, run the suite (red) → must **REVERT** (`git checkout`), mark
     `blocked`. Assert no commit and no human prompt.
   - `03`: apply `move.patch`, run the suite (green), supply `human_decision: approve` → must
     **COMMIT** exactly one item. Assert the diff/named-move/rationale were surfaced and nothing
     was committed before approval.
   - `04`: apply `move.patch`, run the suite (green), supply `human_decision: reject` → must
     **REVERT**. Assert clean tree, no commit.
   - `05`: run `--review .` → compare the written `.test-refactoring-backlog.md` against
     `expected-backlog.md` on the `(smell, move)` pairs (see its `expected.md`).
3. **Compare** against each fixture's `expected.md`. Any fixture that produces the wrong
   outcome is a gate failure — **block the skill change**.

Until `skills/refactor-tests/SKILL.md` exists (DELIVER), there is nothing to drive: the suite
is RED for the right reason — the implementation is missing. See
`docs/feature/refactor-tests/distill/red-classification.md`.

These are metamorphic/differential tests on the **loop's safety behaviour**, not on the target
test code.
