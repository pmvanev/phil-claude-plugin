# phil:rank-issues — Acceptance Self-Test

The **ranking session** is the software under test: what it asks, what it writes, and — mostly — what
it refuses to write. Its bugs are silent. An order written into a description alongside the real
positions looks *more* documented. A reversed order on GitLab looks like a completed reorder. A
dependency encoded as position looks like a ranked board. Every one of them reports success.

These fixtures feed the session known situations and assert the correct **decision outcome**:

`GROUP` · `MERGE-GOALS` · `LEAVE-UNASSIGNED` · `ORDER-DIRECT` · `PAIRWISE-FALLBACK` ·
`REGROUP-INTRANSITIVE` · `WRITE-BASIS-NOT-ORDER` · `WRITE-DEPENDENCY` · `INCREMENTAL-PLACE`

Format and intent mirror `skills/edd/self-test/` and `skills/session-handoff/self-test/` — this
plugin's established way to test a skill. Forge state and user answers are supplied by
`manifest.json` so the suite runs unattended; in live use they come from a real board and a real
person.

## What the fixtures pin

| Fixture | Situation | Guard under test | Expected |
|---|---|---|---|
| `01-goals-then-order/` | 7 unranked issues, 2 natural goals (**walking skeleton**) | the two-level scheme end to end | `GROUP` → `ORDER-DIRECT` → milestones + positions |
| `02-basis-not-order/` | user states why a goal ranks first | record the why, never the order | `WRITE-BASIS-NOT-ORDER` — description holds reasoning, position holds sequence |
| `03-dependency-not-position/` | "B is pointless until A lands" | a dependency is not an ordering | `WRITE-DEPENDENCY` — forge link + `## Chain` on both, *and* the order |
| `04-one-goal-per-issue/` | 8 issues, user proposes 7 goals | goals are outcomes, not tasks | `MERGE-GOALS` — say so and offer to merge |
| `05-intransitive-pairwise/` | pairwise returns A>B, B>C, C>A | do not average a contradiction | `REGROUP-INTRANSITIVE` — the goal is mis-cut; back to grouping |
| `06-new-issue-arrives/` | one new issue on an already-ranked board | two levels exist to avoid re-cutting | `INCREMENTAL-PLACE` — one goal + one position, no re-rank |
| `08-feature-is-the-ranked-unit/` | eight of eleven cards are slice cards on an nWave board | ranking a unit that is about to become a table row | stop at READ; consolidate first |
| `09-story-card-is-a-ranked-unit/` | a feature card and a **story** card, both open and unranked | ranks both; the story gets one position and its four members get none; does **not** stop | `RANKED` |
| `10-story-and-member-both-open/` | a story card **and one of its own members** both carded | stops, names `/phil:groom-set`, ranks nothing; reuses grooming's detector rather than writing a second | `STOP-NAMING-GROOM-SET` |
| `07-homeless-issue/` | an issue fits no goal | unassigned is visible; a wrong goal is not | `LEAVE-UNASSIGNED` |

## The two sharpest

**`02` is the one that matters most.** Writing the resulting order into the milestone description
alongside the real positions is the single most tempting mistake here — it looks like thorough
documentation and it creates a second authority over the same fact. The copy is the one that goes
stale, and this repo has spent a lot of effort on exactly that failure. The rule is narrow: the
description holds *why this goal ranks here*; position holds *which issue comes third*.

**`03` and `06` protect the scheme from opposite ends.** `03` stops a dependency being flattened into
a mere order, which throws away the reason. `06` stops a single arrival re-cutting a whole board,
which is the flat-order failure the two levels exist to prevent. A session that gets one right by a
rule that gets the other wrong has not understood the design.

## Running

Drive each fixture by giving the session the situation in `manifest.json` and comparing the decisions
it reaches against `expected.md`. Model-driven — there is no CI runner in this plugin, and
`tests/test_self_test_fixtures.py` does not cover these.
