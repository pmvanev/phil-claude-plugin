---
name: refactor-tests-critic
description: Skill bundle for the refactor-tests-critic agent — the frozen test-refactoring correctness rubric, the assertion-normalization method, and worked examples
---

# Refactor-Tests Critic — Frozen Rubric

The knowledge the `refactor-tests-critic` agent applies when judging a proposed **test**
refactoring diff. Authored once, frozen, and applied identically to every diff so verdicts
are order-invariant. The agent reads this and applies it as written — it does not
re-improvise a standard per call.

Scope: the structure-only test moves from the `refactor-tests` feature (decision D5) —
Extract Fixture/Helper, reorder into Arrange-Act-Assert, Rename, Extract Test Helper. It
references the test standards in `~/.claude/rules/testing.md` (F.I.R.S.T., AAA,
one-concept-per-test, "test code is production code") and the behavior-preservation frame in
`~/.claude/rules/refactoring.md`.

## The load-bearing idea

A production refactoring is safe when the test suite is green before and after. A **test**
refactoring has no such external oracle — the thing being changed is the oracle. So the
critic's central job is to prove one thing from the diff alone:

> **The set of assertions is identical after the change.**

If an assertion was added, removed, loosened, or its expected value changed, the test now
verifies something different — that is a behavior change to the oracle, and it is a `reject`
regardless of how clean the diff looks.

## Assertion-normalization method

To compare assertions before and after, reduce each test's assertions to a canonical multiset:

1. **Locate assertions.** Match the language's assertion forms — Python `assert`,
   `self.assertEqual/assertTrue/...`, `pytest.raises`; TS/JS `expect(...).toBe/toEqual/...`,
   `assert.equal`. Include exception-expectation blocks.
2. **Canonicalize each.** Reduce to `(actual-expression, matcher, expected-value)`. Strip
   reformatting and whitespace. A pure rename of a **local** variable is allowed **only** if
   the asserted expression and expected value are otherwise identical after substitution.
3. **Build the multiset per test** and compare before-set to after-set.
   - Identical multisets → `assertion-set-preserved: met`.
   - Any assertion added / removed / matcher weakened (`assertEqual`→`assertTrue`, a tight
     matcher→a looser one) / expected value changed → `not met` → `reject`.
4. **Relocated ≠ changed.** When a move extracts setup into a fixture/helper, the assertions
   may move location but their canonical multiset must be unchanged. Relocation alone never
   fails this criterion; a changed canonical form always does.
5. **When you cannot parse the assertions** (macro-generated, metaprogrammed, unfamiliar
   framework), abstain: mark the criterion `CANNOT_ASSESS`. Never guess `met`.

## The rubric

Scoring rules match `refactor/rubric.md`: binary where possible; behavioral anchors, not
adjectives; per-criterion justification written before the verdict; `CANNOT_ASSESS` over a
guess; anti-pattern criteria carry negative weight and block a clean `accept`.

| Criterion | Type | Behavioral anchor | Kind |
|---|---|---|---|
| `assertion-set-preserved` | correctness | The canonical assertion multiset (method above) is identical before and after, per test. | binary |
| `behavior-preserved` | correctness | Setup, act, and teardown produce the same calls and values in the same order; no test logic added or removed. | binary |
| `single-named-move` | scope | The diff is exactly one D5 move, not a bundle and not a behavior change disguised as structure. | binary |
| `test-count-preserved` | scope | The number of test cases (and their ids) is unchanged — no test added, split, merged, or removed. | binary |
| `no-behavior-change-smuggled` *(anti-pattern, negative weight)* | correctness | No determinism edit (`datetime.now()`→fixed, seeding, injected clock), no tightening/loosening, no new control flow. Those are out of scope for structure-only. | binary |
| `no-assertion-weakened` *(anti-pattern, negative weight)* | correctness | No assertion is removed, relaxed, or has its expected value broadened. | binary |
| `no-test-deleted` *(anti-pattern, negative weight)* | correctness | No test function is deleted, `skip`/`xfail`/`.only`/`.skip` added, or body commented out. | binary |
| `fixture-extraction-faithful` | structure | An extracted fixture/helper reproduces the original setup exactly — same objects, args, and order. | graded (3) |
| `name-reveals-behavior` | structure | For a Rename move, the new test name describes the behavior verified (testing.md naming), not the implementation. | graded (3) |
| `coverage-not-narrowed` | correctness | The move does not drop a branch/case the test exercised. Usually not decidable from the diff alone → abstain. | binary / CANNOT_ASSESS |

Graded anchors:

- `fixture-extraction-faithful` — **met**: setup reproduced exactly; **partial**: reproduced
  but with an incidental reordering that does not change values (route `revise`); **not-met**:
  setup differs in a way that could change a value (route `reject`).
- `name-reveals-behavior` — **met**: behavior-revealing name; **partial**: renamed but still
  weak/encoded (route `revise`); **not-met**: no improvement or less clear (route `revise`).

## Verdict mapping

| Condition | Verdict |
|---|---|
| All active criteria `met`, no anti-pattern present | `accept` |
| A fixable criterion fails, a behavior-preserving version exists | `revise` |
| Wrong in kind: any assertion changed, a test deleted, behavior smuggled, or not a D5 move | `reject` |
| The critic cannot point to a span supporting its judgment | `CANNOT_ASSESS` |

The human approval gate (decision D2) consumes the verdict: `reject`/blocking-`major`
withholds or red-flags the diff; `accept`/`revise` still goes to the human for final
approval. The critic augments the human; it never certifies on its own authority.

## Worked examples

**Faithful fixture extraction — accept**
Two tests repeat the same three setup lines. The diff extracts them into a fixture; both
tests now consume it. Canonical assertion multisets are unchanged; test count unchanged.
`assertion-set-preserved: met`, `fixture-extraction-faithful: met` → `verdict: accept`,
cite the moved setup lines and the unchanged assertions.

**Loosened assertion hidden in a rename — reject**
The diff renames a test and, in passing, changes `assertEqual(total, 42)` to
`assertTrue(total)`. Normalization shows the matcher weakened and the expected value dropped.
`no-assertion-weakened: not met` (`major`), `span` on the changed line → `verdict: reject`.

**Determinism fix smuggled as cleanup — reject**
The diff replaces `datetime.now()` with a fixed timestamp while "extracting a helper." That
is a behavior change to the test and out of scope. `no-behavior-change-smuggled: not met`
(`major`) → `verdict: reject`; name the determinism edit in `mechanism`.

**Test split — reject (out of scope)**
One test with two asserts becomes two tests with one assert each. `test-count-preserved:
not met`. Assert-splitting is out of scope for structure-only. `verdict: reject`.

**Unparseable framework — CANNOT_ASSESS**
The assertions run through a custom macro the diff does not show. You cannot build the
canonical multiset. Mark `assertion-set-preserved: CANNOT_ASSESS` and set
`verdict: "CANNOT_ASSESS"` rather than guessing `accept`.

**Empty praise coerced**
Tempted to write "clean extraction!" with no span. That is not a verdict — set
`verdict: "CANNOT_ASSESS"` and state what you could not point to.
