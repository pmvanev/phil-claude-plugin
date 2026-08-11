# phil:nwave-issue-board — Acceptance Self-Test

The `phil:nwave-issue-board` **publisher** is the software under test. Its bugs are worse than its
sibling's, and for one reason: `nwave-slice-status` renders a wrong table into a terminal, where one
person reads it and moves on. This skill writes the wrong table into an issue description, where the
team reads it, for as long as it stands.

Every failure here ships as a clean, well-formed, timestamped table. A dropped `Notes` column looks
tidier than the honest version. A regenerated block that erased "blocked — waiting on Sam" reads as
healthy progress. A wave label that accumulated instead of swapping still renders. None of these look
like failures. They look like a board that is up to date.

These fixtures feed the skill known project and forge states and assert each produces the correct
**decision outcome** (`PUBLISHED` / `NOTES-PRESERVED` / `UNKNOWN-PUBLISHED` / `HUMAN-STATE-KEPT` /
`BLOCK-DELIMITED` / `WAVE-SWAPPED` / `NO-ROWS-BEFORE-ROADMAP` / `DEFERRED-NOT-A-CARD` /
`NATIVE-HIERARCHY` / `TWO-PASS-BARE-REFS` / `ONE-WAY` / `OWNER-DECIDES`).

This suite is the **acceptance + regression gate** for `skills/nwave-issue-board/SKILL.md`. Run it
whenever that file changes, and whenever either skill it delegates to changes — `phil:issue-board`
or `phil:nwave-slice-status` — because this skill's correctness is defined partly by theirs. Format
and intent mirror `skills/nwave-slice-status/self-test/`.

## What the fixtures pin

| Fixture | Situation | Guard under test | Expected outcome |
|---|---|---|---|
| `01-publish-happy-path/` | feature, two slices, roadmap and log agree; GitHub (**walking skeleton**) | publishes the block, attaches slices natively, writes nothing back | `PUBLISHED` |
| `02-notes-column-survives/` | a step is recorded done with no commit touching its files | the `Notes` drift marker reaches the forge, not just the terminal | `NOTES-PRESERVED` |
| `03-unknown-published-as-unknown/` | roadmap present, no status recorded anywhere | publishes `unknown`; never `not started` | `UNKNOWN-PUBLISHED` |
| `04-human-state-outranks-refresh/` | issue says *awaiting input — waiting on Sam*; log says the step ran | preserves the human state; does not overwrite with a derived one | `HUMAN-STATE-KEPT` |
| `05-no-markers-append/` | issue description is hand-written prose, no `nwave:status` markers | appends the block; never rewrites the description | `BLOCK-DELIMITED` |
| `06-wave-swaps-not-accumulates/` | feature moves DISTILL → DELIVER on a forge without scoped labels | removes the old wave in the same call that adds the new | `WAVE-SWAPPED` |
| `07-no-rows-before-roadmap/` | feature is in DESIGN; `slices/` exists, `roadmap.json` does not | opens slice issues, invents no step rows | `NO-ROWS-BEFORE-ROADMAP` |
| `08-deferred-slice-not-a-card/` | slice 03 is marked DEFERRED and is positionally next | opens no card for it | `DEFERRED-NOT-A-CARD` |
| `09-native-hierarchy-no-roster/` | GitHub, where the parent rolls up its children | attaches sub-issues; writes no duplicate roster table | `NATIVE-HIERARCHY` |
| `10-gitlab-roster-second-pass/` | GitLab, four slices created in one run | roster written after numbers exist, as bare `#N` | `TWO-PASS-BARE-REFS` |
| `11-forge-never-writes-back/` | issue was hand-edited to `done`; the log disagrees | treats the artifacts as authoritative; changes no file | `ONE-WAY` |
| `12-owner-decides-status/` | `roadmap.json` carries a per-step `status` field (**the real edd-loop case**) | publishes what `nwave-slice-status` returns, not a local fold | `OWNER-DECIDES` |

`01` is the single walking-skeleton scenario. The **safety core** is `02`, `03`, `04`, `05`, `11`,
`12` — the bug classes that ship silently because the published artifact is indistinguishable from a
correct one: honesty stripped on the way out, missing knowledge published as known absence, a human's
escalation erased by a refresh, hand-written prose destroyed by a whole-body write, artifacts
corrupted from the forge, and a status computed here instead of asked for.

Fixture `08` carries the only actively harmful failure in the suite. Slices 01 and 02 are done, so
positionally slice 03 *is* next — and its own file says not to build it. A card on the board for
deferred work does not misinform someone; it assigns them.

Fixtures `03` and `04` pin the two directions in which this skill can lie about *why* a status is what
it is. `03` is the machine having nothing to say. `04` is a person having said something the machine
cannot represent. Collapsing either into a derived value is a gate failure, because both are claims
about the evidence, not about the work.

## Layout

Each fixture is self-contained and manifest-driven — no sample repository is checked out and no forge
is contacted. The `manifest.json` describes the situation: the local artifacts, the existing forge
state, the invocation, and the `expected_outcome`. The `expected.md` states the decision the skill
must produce, the guard that produces it, the checkable assertions, and the gate-failure condition
that blocks the skill change.

Forge state is described, not created. A fixture asserting "removes the old wave label" is satisfied
by a command that would do so — no fixture requires a live GitLab or GitHub.

## How to drive it

For each fixture, run `skills/nwave-issue-board/SKILL.md` against the situation in `manifest.json`,
and compare the intended forge writes and rendered block against `expected.md`. Any fixture that
produces the wrong outcome is a gate failure — **block the skill change**.

Three assertions apply to every fixture and are not repeated in each file:

1. **Nothing under `docs/feature/` is written.** The projection is one-way.
2. **No status is derived here.** The value published is the one `phil:nwave-slice-status` returns.
3. **Every forge command names its target** with `-R`, per `phil:issue-board`.

Any fixture that violates one is a gate failure regardless of whether its table is correct.
