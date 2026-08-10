---
name: slice-status
description: Use when the user asks where an nWave feature stands — "how many steps are in this slice", "which ones are done", "which one are we on", "what's next", "is slice 03 next", "what was the point of slice 02". Renders a read-only step table from the feature's own artifacts and stops. Prefer over `/nw-continue`, which computes the same thing and then launches the next wave, and over `/nw-buddy`, which answers in prose — this produces a table and starts nothing.
---

# Slice Status

You are answering one question: **where does this feature stand right now?** You read the feature's
own artifacts, render a table, and stop.

This is a **read-only** skill. `/nw-continue` already computes similar data and then *launches the
next wave*. That side effect is the reason this skill exists — the user often wants to look without
starting anything. Print the resume command as text. Never run it.

Three hard rules:

1. **Never run the test suite.** "Where are we?" must stay cheap. Report what the artifacts say.
2. **Never write anything.** No status updates, no progress-file edits, no commits.
3. **Never guess a layout.** Layouts differ per project. When detection is ambiguous, ask.

---

## Step 1 — Resolve the feature and the slice

Resolve scope from the user's request — `$ARGUMENTS` when invoked as `/phil:slice-status`, otherwise
the feature id or slice number named in the question itself. **Most invocations arrive as prose**,
where `$ARGUMENTS` is empty but "is slice 03 next?" plainly names a slice. Treat scope as empty only
when neither carries one.

| Scope | What to do |
|-------|-----------|
| Empty | Use the feature directory containing the most recently modified file — not the newest directory mtime, which only changes when an entry is added or removed. Name the feature in the output so the user can correct you. |
| `admin-field-triage` | That feature; all slices. |
| `03` or `slice 03` | Slice 03 of the resolved feature. |
| `admin-field-triage 03` | Both. |
| No `docs/feature/` at all | Say so and stop. Suggest `/nw-new`. Do not search elsewhere. |

**"Slice" means one of two things, and you must detect which.** Do not assume:

- **A roadmap phase.** Step ids are `<phase>-<step>`, so `03-07` is phase `03`, step `07`, and
  "slice 03" scopes to `phases[id="03"]`. Commit subjects in such repos read `DELIVER slice 03 <feature>`.
- **A feature directory of its own**, named `slice-NN-*`.

If both readings fit, or the number matches nothing, list what you found and ask which. A wrong
scope produces a confidently wrong table.

---

## Step 2 — Read the artifacts

Look for these, in this order. Not every project has all of them, and **no single file is
guaranteed** — the layout varies by project and by nWave version. Establish the slice roster first,
then its steps, then their status.

| Artifact | Holds | Notes |
|---|---|---|
| `docs/feature/<id>/slices/slice-NN-*.md` | A goal line plus IN/OUT scope prose, one file per slice | The most reliable slice roster, and the best source for the intent line. Often present when `roadmap.json` is not. |
| `docs/feature/<id>/deliver/roadmap.json` | `phases[].steps[]` — `id`, `name`, `criteria[]`, sometimes `status` | Step structure within a slice, when it exists. |
| `docs/feature/<id>/deliver/progress.md` | A narrative record, sometimes containing a step table | **Read carefully — see below.** |
| `docs/feature/<id>/deliver/execution-log.json` | COMMIT/PASS records per step | **Read it with the Read tool.** A `des-hook:pre-bash` hook blocks any Bash command whose text contains `execution-log`, and routing around that hook is not acceptable. |
| `.develop-progress.json` | Last failure point | Only when present. |

**`progress.md` is not reliably a step table.** In practice it is prose with several unrelated
tables in it — authored-artifact tables, self-test *fixture* tables (`Fixture | Expected | Result`),
adversarial-review *findings* tables (`# | Severity | Finding | Fix`). Only treat a table as the step
record when its header carries a `Step` or `Slice` column. When no such table exists, take status
from the per-step or per-slice section headings and their prose — both shapes occur, sometimes in
sibling features — and say in Notes that the record is narrative.
Rendering a fixture table as a step table produces a confident, entirely wrong answer.

**A slice may legitimately have one step.** Where the roadmap gives a phase a single step, or where
there is no roadmap at all, report the slice as one row. Do not manufacture sub-steps to fill a table.

**A slice file may declare itself out of scope.** Look for a `**Status:**` line, or a `DEFERRED` /
`OUT of v<N>` marker in the heading. **That marker overrides every other source.** Report the slice
`deferred` and never as `next` — telling the user to build something its own slice file says to skip
is the most actively harmful output this skill can produce. A slice present in `slices/` but absent
from `roadmap.json` is `deferred` when marked and `unknown` otherwise; never `next`, never
`not started`.

Precedence when sources disagree: **name the disagreement in the Notes column rather than silently
picking a winner.** A step marked `done` in `progress.md` and absent from the execution log is
exactly the fact the user needs to see.

---

## Step 3 — Decide each step's status

Statuses are `done`, `current`, `next`, `not started`, `blocked`, `deferred`, and `unknown`.

Take done-ness from the recorded evidence — the execution log, `progress.md`, or the per-step
`status` field, whichever the project actually maintains.

Then **cross-check with git** where it can actually discriminate: run
`git log --oneline -- <the step's own paths>` and note a step recorded done with no commit touching
its files. **`implementation_scope` is usually roadmap-level, not per-step, and `test_file` is often
the same string for every step in the feature.** When neither resolves to step-distinct paths, skip
the cross-check and say so in Notes. A log that returns the same commits for every row cannot detect
drift, and reporting its output silently reads as corroboration it never provided.

`current` is the first step that is not done. Everything after it is `next` (the immediate one) or
`not started`. When `.develop-progress.json` records a failure at that step, mark it `blocked`
instead and put the failure point in Notes — a step that died mid-run is the one fact a returning
user most needs.

**When every step is done**, omit `current` and `next` entirely and replace the resume line with
`slice complete`, or `feature complete` when no slice remains. Offering to resume a finished feature
is a wrong answer with a confident format.

Use `unknown` honestly. A `roadmap.json` whose every step has `status: null` and no other record
means you do not know — say `unknown`, not `not started`. Those are different claims, and reporting
untouched work as "not started" when you cannot tell is a lie the user will act on.

---

## Step 4 — Write the descriptions

Steps carry **no description field** — only `name` and `criteria[]`. Synthesize 1–2 sentences per
step from `name`, `criteria[]`, and `implementation_notes` when present. Say what the step delivers,
not how it is tested. Keep each under ~20 words; the table is for scanning.

For the intent line above the table, prefer the goal sentence from `slices/slice-NN-*.md`. **Match a
line beginning `**Goal`, whatever follows it** — `**Goal.**`, `**Goal:**`, and
`**Goal (one sentence):**` are all in use, sometimes across sibling features in one repo — and take
the sentence after it. Falling back, use the phase `name` from `roadmap.json`; falling back again,
the slice-file heading. This is what answers *"what was the point of slice 03?"*, so exhaust the
sources before leaving it out.

---

## Step 5 — Output

One block per slice, in this shape, and nothing else. A single slice:

```
Feature: admin-field-triage · Slice 03 — Triage feed and bulk actions
Goal: admins see a live triage feed and can dismiss items in bulk.

| Step  | What it does              | Status  | Notes             |
|-------|---------------------------|---------|-------------------|
| 03-05 | Triage queue reader       | done    |                   |
| 03-06 | Feed pagination           | done    | ⚠ no commit found |
| 03-07 | Triage feed group         | current |                   |
| 03-08 | Bulk dismiss              | next    |                   |

Slice 03: 2 of 4 done · resume with: /nw-continue admin-field-triage
```

**Whole feature — the default when no slice is named** — repeats that block per slice under a
`## Slice NN — <name>` heading with its own goal line and table, then closes with one feature-level
count:

```
Feature: admin-field-triage

## Slice 01 — Queue ingestion
Goal: …

| Step | What it does | Status | Notes |
…
Slice 01: 3 of 3 done · slice complete

## Slice 02 — Triage feed and bulk actions
…

Feature: 5 of 9 done · resume with: /nw-continue admin-field-triage
```

Always label what a count counts. A bare "5 of 9" above a four-row table cannot be reconciled with
what the reader sees.

Notes stays empty when the sources agree. Put drift, missing artifacts, and ambiguity there — one
short clause each, not a paragraph.

Then **stop**. No summary of the table, no offer to start the next step, no commentary on progress.
The user asked where they are; they can see it.

---

## Degrade honestly

- **No `roadmap.json` and no `progress.md`, but `slices/` exists** — render one row per slice with
  status `unknown` and its goal line, then say the feature has no step-level record and suggest
  `/nw-roadmap`. The roster is real even when the step record is missing; discarding it throws away
  the most reliable source this skill has.
- **None of the three** — say the feature has no step-level record, list the wave directories that do
  exist, and suggest `/nw-roadmap`. Do not invent steps from commit history.
- **Roadmap present, no progress record of any kind** — render the table with every status `unknown`
  and one line saying why. Do not silently mean "not started".
- **Layout unrecognized** — say "layout not recognized", show the paths you checked, and stop.
  These are nWave's paths, not this plugin's; they move between versions, and guessing at a
  half-matched layout produces a plausible table that is wrong.

---

## Self-test (regression gate)

`skills/slice-status/self-test/` holds golden fixtures that pin these behaviors: the table rendered
from agreeing sources (01, walking skeleton), a narrative `progress.md` whose fixture and findings
tables must never be read as step records (02), `unknown` reported instead of `not started` when the
record is empty (03), disagreeing sources named rather than resolved and a deferred slice never
called `next` (04), read-only discipline under maximum temptation to launch (05), an ambiguous slice
argument asked rather than guessed (06), no table at all when no step record exists (07), drift
surfaced without overriding the record (08), a finished feature offered no resume command (09), a
slice roster kept when the step record is missing (10), a git cross-check skipped when it cannot
discriminate (11), and a failed step reported `blocked` rather than `current` (12).

Fixtures 03 and 07 pin the honesty of absence in both directions — an empty record versus no record —
because collapsing either into "not started" makes a claim about the work from a fact about the
evidence.

Fixture 04 is the one actively harmful case: positionally the deferred slice *is* next, and its own
file says not to build it. Every other failure misinforms; that one directs.

Whenever this skill or `commands/slice-status.md` changes, drive the fixtures per
`self-test/README.md` and confirm each produces its `expected.md` decision. Every failure mode here
is silent: the wrong answer arrives as a clean, confident table.
