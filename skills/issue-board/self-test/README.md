# phil:issue-board — Acceptance Self-Test

**Created 2026-09-04** (issue #40, feature `board-prose-standard`, slice 02). This was the only
board-family skill with no suite; every sibling had one. (A fixture tally stood here and was wrong —
see this skill's `SKILL.md` for what it said and what the suites actually hold.)

`phil:issue-board` is a **reference skill**: it owns forge mechanics — naming the target, tier gating,
label swaps versus board lists, ordering a column, dependency links, chains, two-pass seeding, reading
the end state. It defines rules, not a workflow, so unlike its siblings **it had no decision-outcome
vocabulary at all.** This suite introduces one, and the vocabulary **grows with the suite** rather than
being designed up front — an outcome is added when a fixture needs it, never in advance.

Its failures are the ones `--help` does not warn about, where **a wrong guess reports success**: a
mutation against the wrong repository, a label swap that accumulated, a column write that silently
dropped an option. Nothing errors.

## Decision outcomes

| Outcome | Meaning |
|---|---|
| `CHAIN-COMPOSED` | Both ends of a pivot are written, under the fixed heading, and the clause after the dash says why the work stopped |

One outcome, one fixture. A suite that shipped a vocabulary ahead of its fixtures would be asserting
coverage it does not have.

## Fixtures

| Fixture | Situation | Guard under test | Expected outcome |
|---|---|---|---|
| `01-chain-clause-composed/` | mid-work pivot: the blocker is discovered and no candidate text is supplied | composes both chain lines, and the clause after the dash carries the reasoning the forge edge cannot | `CHAIN-COMPOSED` |

## Which manifest scheme this suite uses, and why

**The repo has two, and this is the finding slice 02 was built to produce.** Measured across all
suites at 0.83.0: `situation` (158 uses, 8 skills) and `expected_guard` (145, 11 skills) are genuinely
shared. Past those the convention forks —

- `fixture_id` + `expected_decision` — 6 skills (`board-setup`, `edd`, `groom-issues`, `rank-issues`,
  `session-handoff`, `work`)
- `fixture` + `expected_outcome` — 5 skills (`adversarial-review`, `nwave-issue-board`,
  `nwave-slice-status`, `rank-issues`, `ux-review`)

**`rank-issues` uses both.** So "match the sibling convention" was not an instruction that could be
followed; there was no single one to match.

**This suite uses `fixture_id` + `expected_decision`**, for a mechanical reason rather than a taste one:
the only copyable *driver* in the repo, `tests/test_board_setup_fixtures.py`, is written against that
scheme, and matching it means the driver ports with almost no change. **Stated because
`phil:nwave-issue-board` — the skill that depends on this one — uses the other scheme**, so a reader
moving between the two suites meets the switch. That inconsistency is issue #42, not something this
suite resolves.

## Layout

Each fixture is self-contained and manifest-driven: no repository is checked out and **no forge is
contacted**. `manifest.json` carries the situation, the forge state, and `expected_decision`.
`expected.md` states the decision, the guard that produces it, the checkable assertions, and the
gate-failure condition.

**No fixture supplies candidate prose to choose between.** Selecting the shorter of two given strings is
not composing, and a suite that tested selection would be satisfied by a word ceiling — which
`board-prose-standard` [D5] refuses. Where a fixture tests composed text it supplies the situation plus
`enumerable_facts`, and the assertions are properties of the output.

## How to drive it

For each fixture, apply `skills/issue-board/SKILL.md` to the situation in `manifest.json` and compare
the result against `expected.md`. **Judging whether a run reached the right decision is not
automatable** — these are prose fixtures over a prose skill.

`tests/test_issue_board_fixtures.py` checks what *is* automatable: that every fixture stays well-formed,
that `expected_decision` names exactly one outcome this README defines, and that every defined outcome
has a fixture. It does not pretend to judge a run, and it says so in its own docstring.

**Run it whenever `skills/issue-board/SKILL.md` changes**, and whenever `phil:nwave-issue-board` or
`phil:nwave-slice-status` changes, since both build on this skill's mechanics.
