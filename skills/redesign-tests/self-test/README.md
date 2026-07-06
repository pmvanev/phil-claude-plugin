# redesign-tests — Acceptance Self-Test

The `redesign-tests` **safety loop** is the software under test. Its bugs are silent: a gate that
fails to revert, a tool that redesigns on red, or a rewrite committed without the human validating
its coverage-equivalence claim all look exactly like a smooth run. These fixtures feed the loop
known situations and assert each produces the correct **gate outcome** (`STOP` / `REVERT` /
`COMMIT` / `SKIP`) or the correct **backlog**. A fixture that produces the wrong outcome means a
safety guard is decorative.

This suite is the **acceptance + regression gate** for `skills/redesign-tests/SKILL.md`. Run it
whenever the skill or the command loader changes — every such edit is non-monotonic, so the skill
is never changed and eyeballed; it is changed and regression-tested here. Format and intent mirror
`skills/refactor-tests/self-test/` and `refactor/self-test/` — the plugin's established way to test
a skill/gate.

**What makes this suite different from refactor-tests':** the moves are behaviour-CHANGING. A green
suite therefore proves *less* here — it cannot prove the rewrite preserved coverage. So the
human-gated fixtures (03, 04) pin the extra element that makes the human the oracle: the proposal
carries a **coverage-equivalence claim** (before/after "what it caught then / catches now"), and
the human decision is a judgment on that claim (ADR-004).

## What the fixtures pin

| Fixture | Situation | Pins (feature-delta AC) | Guard under test | Expected outcome |
|---|---|---|---|---|
| `01-baseline-red-stop/` | baseline suite already red | AC1.7 | never-redesign-on-red (DDD5) | `STOP` — nothing applied, nothing committed |
| `02-postapply-red-autorevert/` | a rewrite gets the new assertion wrong and reds the suite | AC1.3 | post-apply auto-revert (DDD5) | `REVERT` — `git checkout`, item `blocked`, no human prompt |
| `03-approve-commit-on-green/` | coupling rewrite, suite green, human approves the coverage-equivalence claim | AC1.1, AC1.2, AC1.5, AC1.6 (**walking skeleton, S1**) | human gate + coverage-equivalence claim (ADR-004) | `COMMIT` — one commit, suite green |
| `04-reject-reverts-clean/` | coupling rewrite, suite green, human rejects the claim | AC1.5 | human is the oracle, not the suite (D2) | `REVERT` — clean tree, nothing written |
| `05-review-seeds-backlog/` | file with behavioural smells (coupling, over-mock, flaky, private-method) | AC2.1, AC2.2, AC2.4 | behavioural-only detector (ADR-003) | backlog matching `expected-backlog.md` |
| `06-missing-fake-skips/` | over-mock rewrite would need a fake that does not exist | AC3.2 | skip-not-scaffold (S3) | `SKIP` — item skipped, no test scaffolding invented |

Deterministic safety mechanics (01, 02, 03-commit, 04-revert, 06-skip) are the driveable core. The
**human decision itself** (approve vs reject in 03/04) is supplied by the fixture manifest so the
suite can run unattended; in live use it comes from the developer at the AskUserQuestion gate (D2).
Detection precision (05) is validated by dogfood audit against the KPI (≤20% false positives), not
by byte-exact line matching.

**Deferred (documented gap):** a dedicated flakiness-rewrite fixture with the N-run stability check
(S4, AC4.2) is NOT in v1 — S4 is the most tentative slice and its go/no-go depends on real-loop
data (empirical over speculative). The behaviour is specified in `acceptance.feature`
(`@us-S4 @flakiness`) and the flaky smell is exercised by fixture 05's detection. Add the fixture
when S4 is committed.

## Layout

Each fixture is self-contained and dependency-free (`python -m pytest` runs it):

- `orders.py` — the tiny SUT (NOT the thing rewritten — the *test file* is). Kept green. It has a
  real in-memory repository so a behavioural rewrite can assert on observable persisted state.
- `test_orders.py` / `test_orders_smells.py` — the test file the loop scopes to.
- `move.patch` — the proposed behaviour-changing rewrite (fixtures 02–04). Applies with `git apply`.
- `manifest.json` — the proposal metadata (smell family, target span, rationale, the
  **coverage_equivalence_claim**) and, for the human-gated fixtures, the `human_decision` the
  driver should supply.
- `expected.md` — the gate outcome the loop must produce, and the guard that must produce it.
- `expected-backlog.md` — fixture 05 only: the backlog `--review` must write.

## How to drive it (as the skill acceptance/regression gate)

For each fixture:

1. **Baseline.** Run `python -m pytest -q` in the fixture dir.
   - `01`: expect **red** — this IS the precondition.
   - `02`–`04`, `06`: expect **green** — the loop's baseline check must pass here.
2. **Drive the loop** exactly as `/phil:redesign-tests` would, using `manifest.json`:
   - `01`: red baseline → must **STOP**. Assert the tree is unchanged and no commit was made.
   - `02`: apply `move.patch`, run the suite (red) → must **REVERT** (`git checkout`), mark
     `blocked`. Assert no commit and no human prompt.
   - `03`: apply `move.patch`, run the suite (green), surface the diff + rationale +
     `coverage_equivalence_claim`, supply `human_decision: approve` → must **COMMIT** exactly one
     item. Assert nothing was committed before approval and the claim was surfaced.
   - `04`: apply `move.patch`, run the suite (green), surface the claim, supply
     `human_decision: reject` → must **REVERT**. Assert clean tree, no commit.
   - `05`: run `--review .` → compare the written `.test-redesign-backlog.md` against
     `expected-backlog.md` on the `(smell, rewrite-intent)` pairs (see its `expected.md`).
   - `06`: consider the over-mock rewrite named in the manifest; the required fake is absent →
     must **SKIP** the item. Assert no test file was written and no fake class was invented.
3. **Compare** against each fixture's `expected.md`. Any fixture that produces the wrong outcome is
   a gate failure — **block the skill change**.

Until `skills/redesign-tests/SKILL.md` exists (DELIVER), there is nothing to drive: the suite is
RED for the right reason — the implementation is missing. See
`docs/feature/redesign-tests/distill/red-classification.md`.

These are metamorphic/differential tests on the **loop's safety behaviour**, not on the target test
code.
