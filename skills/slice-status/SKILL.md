---
name: slice-status
description: Use when orienting in an nWave feature before resuming work — "how many steps are in this slice", "which ones are done", "which one are we on", "what's next", "is slice 03 next", "what was the point of slice 02". Renders a read-only step table from the feature's own artifacts and stops. Never launches a wave, dispatches a step, or runs tests.
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

Parse `$ARGUMENTS`. It may contain a feature id, a slice number, both, or nothing.

| Input | What to do |
|-------|-----------|
| Empty | Use the most recently modified `docs/feature/*/`. Name it in the output so the user can correct you. |
| `admin-triage` | That feature; all slices. |
| `03` or `slice 03` | Slice 03 of the resolved feature. |
| `admin-triage 03` | Both. |
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
| `docs/feature/<id>/slices/slice-NN-*.md` | `**Goal.**` plus IN/OUT scope prose, one file per slice | The most reliable slice roster, and the best source for the intent line. Often present when `roadmap.json` is not. |
| `docs/feature/<id>/deliver/roadmap.json` | `phases[].steps[]` — `id`, `name`, `criteria[]`, sometimes `status` | Step structure within a slice, when it exists. |
| `docs/feature/<id>/deliver/progress.md` | A narrative record, sometimes containing a step table | **Read carefully — see below.** |
| `docs/feature/<id>/deliver/execution-log.json` | COMMIT/PASS records per step | **Read it with the Read tool.** A `des-hook:pre-bash` hook blocks any Bash command whose text contains `execution-log`, and routing around that hook is not acceptable. |
| `.develop-progress.json` | Last failure point | Only when present. |

**`progress.md` is not reliably a step table.** In practice it is prose with several unrelated
tables in it — authored-artifact tables, self-test *fixture* tables (`Fixture | Expected | Result`),
adversarial-review *findings* tables (`# | Severity | Finding | Fix`). Only treat a table as the step
record when its header carries a `Step` or `Slice` column. When no such table exists, take status
from the per-slice section headings and their prose, and say in Notes that the record is narrative.
Rendering a fixture table as a step table produces a confident, entirely wrong answer.

**A slice may legitimately have one step.** Where the roadmap gives a phase a single step, or where
there is no roadmap at all, report the slice as one row. Do not manufacture sub-steps to fill a table.

Precedence when sources disagree: **name the disagreement in the Notes column rather than silently
picking a winner.** A step marked `done` in `progress.md` and absent from the execution log is
exactly the fact the user needs to see.

---

## Step 3 — Decide each step's status

Statuses are `done`, `current`, `next`, `not started`, and `unknown`.

Take done-ness from the recorded evidence — the execution log, `progress.md`, or the per-step
`status` field, whichever the project actually maintains. Then **cross-check with git**: run
`git log --oneline -- <step's test_file and implementation_scope paths>` and note a step recorded
done with no commit touching its files.

`current` is the first step that is not done. Everything after it is `next` (the immediate one) or
`not started`.

Use `unknown` honestly. A `roadmap.json` whose every step has `status: null` and no other record
means you do not know — say `unknown`, not `not started`. Those are different claims, and reporting
untouched work as "not started" when you cannot tell is a lie the user will act on.

---

## Step 4 — Write the descriptions

Steps carry **no description field** — only `name` and `criteria[]`. Synthesize 1–2 sentences per
step from `name`, `criteria[]`, and `implementation_notes` when present. Say what the step delivers,
not how it is tested. Keep each under ~20 words; the table is for scanning.

For the intent line above the table, prefer the `**Goal.**` sentence from `slices/slice-NN-*.md`.
Falling back, use the phase `name` from `roadmap.json`. This is what answers *"what was the point of
slice 03?"*.

---

## Step 5 — Output

Exactly this shape, nothing else:

```
Feature: admin-field-triage · Slice 03 — Triage feed and bulk actions
Goal: admins see a live triage feed and can dismiss items in bulk.

| Step  | What it does              | Status  | Notes             |
|-------|---------------------------|---------|-------------------|
| 03-05 | Triage queue reader       | done    |                   |
| 03-06 | Feed pagination           | done    | ⚠ no commit found |
| 03-07 | Triage feed group         | current |                   |
| 03-08 | Bulk dismiss              | next    |                   |

5 of 9 done · resume with: /nw-continue admin-field-triage
```

Notes stays empty when the sources agree. Put drift, missing artifacts, and ambiguity there — one
short clause each, not a paragraph.

Then **stop**. No summary of the table, no offer to start the next step, no commentary on progress.
The user asked where they are; they can see it.

---

## Degrade honestly

- **No `roadmap.json` and no `progress.md`** — say the feature has no step-level record, list the
  wave directories that do exist, and suggest `/nw-roadmap`. Do not invent steps from commit history.
- **Roadmap present, no progress record of any kind** — render the table with every status `unknown`
  and one line saying why. Do not silently mean "not started".
- **Layout unrecognized** — say "layout not recognized", show the paths you checked, and stop.
  These are nWave's paths, not this plugin's; they move between versions, and guessing at a
  half-matched layout produces a plausible table that is wrong.
