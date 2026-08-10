# phil:slice-status — Acceptance Self-Test

The `phil:slice-status` **status renderer** is the software under test. Its bugs are silent: every
one of them produces a clean, confident, well-formatted table that the user reads and acts on. A
table built from the wrong markdown table, a step reported `not started` when nothing is actually
known, two disagreeing sources quietly resolved in favour of one — none of these look like failures.
They look like answers.

That is the whole risk. The user asks this question *to decide what to do next*, so a wrong table is
worse than no table.

These fixtures feed the skill known project layouts and assert each produces the correct **decision
outcome** (`STATUS-TABLE` / `NARRATIVE-RECORD` / `UNKNOWN` / `DISAGREEMENT-NAMED` / `READ-ONLY` /
`ASK-DONT-GUESS` / `NO-STEP-RECORD` / `DRIFT-NOTED` / `COMPLETE` / `ROSTER-ONLY` /
`CROSS-CHECK-SKIPPED` / `BLOCKED`).

This suite is the **acceptance + regression gate** for `skills/slice-status/SKILL.md` and
`commands/slice-status.md`. Run it whenever either changes. Format and intent mirror
`skills/adversarial-review/self-test/`, `skills/edd/self-test/`, and `skills/work/self-test/` — the
plugin's established way to test a skill.

## What the fixtures pin

| Fixture | Situation | Guard under test | Expected outcome |
|---|---|---|---|
| `01-status-table-happy-path/` | roadmap + execution log agree; slice is a roadmap phase (**walking skeleton**) | renders the table, reads the log with the Read tool, stops without launching | `STATUS-TABLE` |
| `02-narrative-progress-not-step-table/` | `progress.md` is prose whose only tables are fixture and findings tables | requires a `Step`/`Slice` column before trusting a table | `NARRATIVE-RECORD` |
| `03-unknown-is-not-not-started/` | `roadmap.json` present, every step `status: null`, no other record | reports `unknown`, never `not started` | `UNKNOWN` |
| `04-disagreeing-sources-named/` | 3 slice files, 2 roadmap phases, third slice marked deferred (**the real edd-loop case**) | names the disagreement; a deferred slice is never `next` | `DISAGREEMENT-NAMED` |
| `05-read-only-never-launches/` | next step is obvious and the wave is ready to run | prints the resume command as text; runs nothing | `READ-ONLY` |
| `06-ambiguous-slice-asks/` | "03" matches both a roadmap phase and a `slice-03-*` feature directory | asks which; does not pick the likelier one | `ASK-DONT-GUESS` |
| `07-no-step-record-degrades/` | feature has discuss/design artifacts only — no roadmap, no progress file | says there is no step-level record; invents nothing from git | `NO-STEP-RECORD` |
| `08-drift-recorded-done-no-commit/` | a step is recorded done but no commit touches its files | surfaces the drift in Notes without overriding the record | `DRIFT-NOTED` |
| `09-feature-complete-no-resume/` | every step done — no first-not-done step exists | omits `current`/`next`; prints no resume command | `COMPLETE` |
| `10-slices-only-roster-kept/` | `slices/` present, no `deliver/` at all (**the real mobile-web-standards case**) | keeps the roster instead of discarding it as "no record" | `ROSTER-ONLY` |
| `11-inert-cross-check-skipped/` | roadmap-level `implementation_scope`, one shared `test_file` (**the real phil-work case**) | skips a git check that cannot discriminate, and says so | `CROSS-CHECK-SKIPPED` |
| `12-blocked-step-surfaced/` | `.develop-progress.json` records a failure at the current step | reports `blocked`, never re-runs the failing test | `BLOCKED` |

`01` is the single walking-skeleton scenario. The **safety core** is `02`, `03`, `04`, `07`, `08`,
`11` — the bug classes that ship silently because their output is indistinguishable from a correct
answer: a table built from the wrong source, missing knowledge reported as known absence, deferred
work scheduled as next, fabricated structure, unreported drift, and a cross-check whose silence is
mistaken for corroboration.

Fixture `04` carries the only actively harmful failure in the suite. Slices 01 and 02 are done, so
positionally slice 03 *is* next — while its own file says "do NOT build in this cycle". Every other
failure misinforms; this one directs.

Fixtures `03` and `07` pin the honesty of *absence* in both directions: a record that exists but is
empty (`unknown`) versus no record at all (`NO-STEP-RECORD`). Collapsing either into "not started" is
a gate failure, because "not started" is a claim about the work, not about the evidence.

## Layout

Each fixture is self-contained and manifest-driven — no sample repository is checked out. The
`manifest.json` describes the situation: which artifacts exist, their relevant contents, the
arguments the skill is invoked with, and the `expected_outcome`. The `expected.md` states the
decision the skill must produce, the guard that produces it, the checkable assertions, and the
gate-failure condition that blocks the skill change.

## How to drive it

For each fixture, run `skills/slice-status/SKILL.md` against the situation in `manifest.json` as
`/phil:slice-status` would, and compare the rendered output against `expected.md`. Any fixture that
produces the wrong outcome is a gate failure — **block the skill change**.

Two assertions apply to every fixture and are not repeated in each file:

1. **Nothing is written.** No file created or modified, no commit, no status update.
2. **No test suite is run**, and no wave, step, or command is launched.

Any fixture that violates either is a gate failure regardless of whether its table is correct.
