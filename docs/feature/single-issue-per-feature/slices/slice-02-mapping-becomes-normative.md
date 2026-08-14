# Slice 02 — The mapping becomes normative

**Goal:** Rewrite `phil:nwave-issue-board` so the feature is the card and slices and steps are rows,
and realign the fixtures that currently pin the opposite.

**Stories:** S1 (the format it now asserts)
**Flagged:** this is the slice most likely to exceed a day. See *Effort*.

## Learning hypothesis

**Disproves** the claim that this change is containable in one skill — if the rewrite forces edits to
`phil:issue-board`'s forge mechanics, then the delegation boundary between the two skills was drawn in
the wrong place, and that is a bigger finding than the paradigm itself.
**Confirms**, if it holds, that `issue-board` needs only *Choosing what becomes an issue* touched.

## IN scope

- **The mapping table** (`SKILL.md:28-36`): feature → card; slice → row; step → row. Replace the
  rationale with [D2]'s premise correction, stated as a correction rather than a fresh assertion.
- **Ordering** (`:102-129`): slice order becomes a table fact. Retire the two-orders-on-GitHub
  problem and the GitLab second-pass roster; keep the provisional-order rule, which slice 01 exercised.
- **Two-stage fill** (`:220-236`): now one description filling in two stages rather than N issues.
- **The roster** (`:43-58`): the ban on a hand-written roster is scoped to the sub-issue case it was
  written for, and a **generated** roster is permitted — with the reasoning, so the next reader does
  not re-derive it as a contradiction.
- **The projection contract** from slice 01, promoted to normative prose: glyphs ([D8]), bounded to
  the current slice ([D9]), delimited, timestamped.
- **Fixtures.** Realign 09 (native sub-issues), 13 (order follows roadmap), 14 (guessed order says
  so). Add a fixture for the bounded projection and one for glyphs-not-checkboxes. Keep 15 — it gets
  *more* load-bearing, not less.
- `plugin-dev:skill-development` consulted **before** writing, then `plugin-dev:skill-reviewer` and
  `plugin-dev:plugin-validator` over the result. The commit says which ran.

## OUT scope

- Wave columns (slice 03), the stack (slice 04), grooming and ranking (slice 05).
- `phil:nwave-slice-status`'s feature-level fold. It is [D10]'s and lands with slice 03, which is the
  first slice that needs a column state.
- Any restructure of `issue-board`'s sixteen flat sections. That proposal is already deferred
  (`docs/evolution/2026-08-10-issue-board.md:358-363`) and bundling it here would hide this change
  inside a reorganisation.

## Acceptance criteria

1. The mapping table reads feature → card, and its rationale names the premise correction rather than
   asserting the new shape bare.
2. No fixture in the suite still asserts that a slice gets its own card; every realigned fixture states
   what it used to assert and why that changed.
3. The retired ordering machinery is **removed, not left standing** — a skill that documents both
   orders is a skill that licenses either.
4. `plugin-dev:skill-reviewer` returns no finding of a restated rule that belongs to `issue-board` —
   the fault this skill shipped in its first draft and the reason it exists separately.
5. `issue-board` changes only in *Choosing what becomes an issue* (the concurrency reading) and its
   per-project template. Any further edit is the hypothesis failing, and gets recorded as such.

## Dependencies

Slice 01 passed. If KPI-1 failed, this slice does not start — the format is wrong and rewriting the
skill to assert a wrong format is the most expensive possible ordering.

## Effort

**~1.5 days — over the one-day taste test, and kept whole deliberately.** The rules and their fixtures
must ship together: this repo's fold-back rule requires the fixture that would have caught the gap, and
fixture 15 caught its own skill in the same commit it shipped in. Splitting would ship a skill whose
own suite contradicts it.

If it runs long, the honest split is by *fixture*, not by rules-then-fixtures: land the mapping plus
its two new fixtures, then the three realignments.

Reference class: the 2026-08-12 amendment, which touched both skills and moved the suite from fourteen
fixtures to fifteen in one pass.

## Result — 2026-08-14

**Hypothesis CONFIRMED: the change is containable.** `phil:issue-board` needed exactly the two edits this
brief permitted — the concurrency reading in *Choosing what becomes an issue*, and a column-families entry
in the per-project template. No forge mechanic moved, and the delegation boundary held.

**More fixtures were affected than this brief predicted.** It named 09, 13 and 14. The actual set:

| Fixture | Change |
|---|---|
| `01` | Amended — the skeleton creates no slice issue |
| `07` | Amended — added the branch where `/nw-roadmap` never runs |
| `08` | **Renamed and inverted** — `deferred-slice-not-a-card` → `deferred-slice-is-a-row` |
| `09` | **Renamed and inverted** — `native-hierarchy-no-roster` → `generated-roster-no-subissues` |
| `10` | **Retired** — no second pass exists to get wrong |
| `13` | Renamed — the assertion moved from the board column to the roster rows |
| `14` | Amended — no slice issues created; added the "order is final" form |
| `15` | Amended — forge-neutral now, and glyphs are the stated alternative |
| `16` | Amended — added the wave-with-no-routing-row branch |
| `17` | **New** — the projection bounded at 94 steps |

Ten of sixteen touched against three predicted. The under-estimate has one cause worth naming: **the brief
counted fixtures that assert the mapping, and missed the ones that assert something else *through* it.**
`15` is about hand-ticked state, not hierarchy — but it reached that subject via a GitLab roster of bare
`#N` references, and those references only existed because slices were issues. A fixture's subject and its
scaffolding are different things, and only the subject is obvious from its name.

**Numbering has a deliberate gap at 10.** Retired rather than renumbered, so the gap is a question a reader
can answer from the suite README instead of a silent renumbering that invalidates every prior reference.

**Estimate:** the brief said ~1.5 days and flagged it as the over-the-one-day failure. Landed in one
session, because the fixture work turned out to be mechanical once the mapping was settled — the ratio the
brief got wrong was rules-to-fixtures, not the total.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | Borderline — one skill rewritten, three fixtures realigned, two added. Counted as one surface with its own suite, not five components. |
| Depends on a new abstraction? | No. Consumes the projection format slice 01 already shipped. |
| Disproves a pre-commitment? | Yes — that the change is containable in one skill. Any forced edit to `issue-board`'s mechanics is the hypothesis failing. |
| Synthetic data only? | Fixtures are constructed by nature; the rules they pin were derived from slice 01's real card. Noted rather than claimed clean. |
| ≤1 day? | **NO — ~1.5 days. Documented failure, kept whole deliberately.** Rules and fixtures must ship together: this repo's fold-back rule requires the fixture that would have caught the gap, and fixture 15 caught its own skill in the same commit. Splitting would ship a skill whose suite contradicts it. If it runs long, split by *fixture*, never rules-then-fixtures. |
