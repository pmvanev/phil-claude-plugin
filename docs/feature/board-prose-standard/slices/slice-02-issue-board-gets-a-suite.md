# Slice 02 — `issue-board` gets a suite

**Goal:** Create `skills/issue-board/self-test/` from scratch and land its first fixture on the one
sentence that skill composes — the clause after the dash on a `## Chain` line.

**Stories:** S1 (the fixture half), S3 (the chain convention it owns)
**Answers:** issue #40's done-condition 3, the load-bearing half of [D2]

## Learning hypothesis

**Disproves the cost estimate if creating this repo's first board-skill suite from scratch needs a
harness that does not exist.** Five siblings carry suites (29, 44, 11, 14, 27 entries at 0.82.0), so the
pattern is presumed copyable — but presumed is the word, because none of them was created after the
harness settled, and `self-test/README.md` conventions may be per-skill rather than shared.

**Confirms**, if it is copyable, that [D9] costs a fixture rather than an infrastructure slice — which is
what lets slice 03 cite four surfaces in a paragraph each.

**Why this slice is separate from 01.** [D9] is the mechanism that keeps [D2] from being a bare mention,
so it must not be optional; and its cost is the one unknown that is not about prose at all. Bundling it
with 01 would let a prose failure and a harness failure arrive as one ambiguous result.

## IN scope

- `skills/issue-board/self-test/`, created — directory, `README.md` naming how to drive it, matching
  whichever sibling convention slice 02 finds to be shared rather than local.
- **The first fixture: the chain clause.** `issue-board:456` already ships a tight real example —
  *"Blocked by #47 — token refresh must land first or the retry test can't be written"*. The fixture pins
  a padded variant failing against it, so the assertion is anchored on shipped text rather than on
  invented text.
- `skills/issue-board/SKILL.md` at *Leave a chain when you pivot*: name the standard for the clause after
  the dash, and state that it applies to that clause and not to the edge the forge records.
- Version bump.

## OUT scope

- The other five surfaces — 01 and 03.
- **Backfilling a full suite for `issue-board`.** One fixture satisfies [D9]. A suite sized to its
  siblings is a separate card, and inventing it here would hide the cost this slice exists to measure.
- Self-tests for `eos`, `ai-eos` or `red-team-prose`. Out of scope for the feature.
- `rank-issues`' chain lines. It cites this convention; the citation lands in slice 03.

## Acceptance criteria

1. `skills/issue-board/self-test/` exists with a `README.md` that a reader can drive without asking.
   **KPI-2: ≥ 1 entry.**
2. The fixture asserts the shipped `:456` clause passes and a named padded variant fails, and the failure
   reason is the standard rather than an incidental difference.
3. The skill names the standard at the chain clause, scoped to the clause and not the edge.
4. **The harness finding is recorded either way** — whether sibling conventions were shared or local.
   That answer is what slice 03 and every future board fixture depends on.

## Dependencies

Slice 01 confirmed [D2], or reported it disproven and the feature re-scoped. Creating a suite to pin a
mechanism that does not work is the ordering mistake this dependency exists to prevent.

## Dogfood moment

Same day: drive the new suite by hand from its own `README.md`, without consulting a sibling. A suite
whose README needs a sibling open beside it has not been created, only started.

## Effort

Half a day, dominated by the harness question rather than the fixture.

## Reference class

The five sibling suites. **Their entry counts are the estimate and their creation history is not** —
none was created after the harness settled, which is exactly the uncertainty above.

## Taste tests

| Test | Verdict |
|---|---|
| Ships 4+ new components? | No — one directory, one README, one fixture, one citation |
| Depends on a new abstraction? | **Possibly — the shared harness may not exist. That is the hypothesis** |
| Disproves a pre-commitment? | Yes — the "a fixture is cheap" estimate underneath [D9] |
| Synthetic data only? | No — the fixture is anchored on shipped text at `issue-board:456` |
| Identical to another slice but for scale? | No — the only slice that creates infrastructure |
