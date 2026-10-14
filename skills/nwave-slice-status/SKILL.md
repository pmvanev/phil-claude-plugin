---
name: nwave-slice-status
description: Use when the user asks where an nWave feature stands — "how many steps are in this slice", "which ones are done", "which one are we on", "what's next", "is slice 03 next", "what was the point of slice 02". Renders a read-only step table from the feature's own artifacts and stops. Prefer over `/nw-continue`, which computes the same thing and then launches the next wave, and over `/nw-buddy`, which answers in prose — this produces a table and starts nothing. Also folds a feature-level state over every slice on request — "what state is this feature in", "which column does this card belong in" — and a story-level state over every feature in a story — "what state is this story in", "how far through the story are we" — for a caller placing the card on a board. For what a finished stage DECIDED rather than where it stands, use phil:nwave-wave-summary instead.
---

# Slice Status

Answer one question — **where does this feature stand right now?** — by reading the feature's own
artifacts, rendering a table, and stopping.

**Read-only.** `/nw-continue` computes similar data and then *launches the next wave*; this skill
exists to look without starting anything. Print the resume command as text; never run it. Pass `git log`
neither `--output`, which writes any path, nor `-p` or `--ext-diff`, which run a repo's configured diff
filters.

Three hard rules:

1. **Report what the artifacts say; run no test suite.** "Where are we?" must stay cheap.
2. **Write nothing** — no status updates, no progress-file edits, no commits.
3. **Detect the layout, and ask when detection is ambiguous.** Layouts differ per project; never guess
   one.

---

## Step 1 — Resolve the feature and the slice

Resolve scope from the user's request — `$ARGUMENTS` when invoked as `/phil:nwave-slice-status`, otherwise
the feature id or slice number named in the question itself. **Most invocations arrive as prose**,
where `$ARGUMENTS` is empty but "is slice 03 next?" plainly names a slice. Treat scope as empty only
when neither carries one.

| Scope | What to do |
|-------|-----------|
| Empty | Use the feature directory containing the most recently modified file — not the newest directory mtime, which only changes when an entry is added or removed. Name the feature in the output so the user can correct it. |
| `admin-field-triage` | That feature; all slices. |
| `03` or `slice 03` | Slice 03 of the resolved feature. |
| `admin-field-triage 03` | Both. |
| `--feature-state` | Emit the feature-level state instead of the tables — see *The feature-level state, on request*, in `references/states.md`. Combines with a feature id; a slice number alongside it is a contradiction, because the fold always reads the whole roster. Say so and ask. |
| `--story-state <slug>` | Emit the story-level state — see *The story-level state, on request*, in `references/states.md`. Takes a story slug, never a feature id. A slice number or a feature id alongside it is a contradiction, for the same reason: the fold reads the whole story. Say so and ask. |
| both `--feature-state` and `--story-state` | Two different questions at two scopes. Do not guess which was meant, and do not emit both. Say so and ask. |
| No `docs/feature/` at all | Say so and stop. Suggest `/nw-new`. Do not search elsewhere. |

**Before emitting a feature-level or story-level state, read `references/states.md` whole, and decide
the scope there.** That is, on `--feature-state` or `--story-state <slug>`, on a question that plainly
asks what state a feature is in or which column its card belongs in, and on any question scoped to a
story rather than a feature — what state it is in, or how far through it the work is. Each state is a
fold over every slice or every member feature, in a fixed order, and the order is the content. A story
question routed through the `Empty` row above answers for the wrong scope, confidently.

**"Slice" means one of two things; detect which, and assume neither:**

- **A roadmap phase.** Step ids are `<phase>-<step>`, so `03-07` is phase `03`, step `07`, and
  "slice 03" scopes to `phases[id="03"]`. Commit subjects in such repos read `DELIVER slice 03 <feature>`.
- **A feature directory of its own**, named `slice-NN-*`.

If both readings fit, or the number matches nothing, list what was found and ask which. A wrong
scope produces a confidently wrong table.

---

## Step 2 — Read the artifacts

Look for these, in this order. Not every project has all of them, and **no single file is
guaranteed** — the layout varies by project and by nWave version. Establish the slice roster first,
then its steps, then their status.

| Artifact | Holds | Notes |
|---|---|---|
| `docs/feature/<id>/feature-delta.md` header | `Story: <slug> · position NN` — the feature's declaration that it belongs to a story | **Read only for `--story-state`.** One authority per fact: a feature declares its own membership and nothing declares it for that feature. Absent means the feature is in no story, which is the normal case. |
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

**A slice file may declare itself out of scope.** Look for a `**Status:**` line, or a `DEFERRED` / `OUT of
v<N>` / `RETIRED` / `SUBSUMED BY <slice>` marker in the heading, **or a `Retired <date>` / `Superseded by
<slice>` line in the first few lines of the body**. **That marker overrides every other source.** Wound: a
scan matching only `**Status:**` and `DEFERRED` missed an H1 `— SUBSUMED BY SLICE 07`, with the same
retirement in body prose, and folded a shipped feature to `in progress` (2026-09-04). Report the slice
`deferred` and never as `next` — telling the user to build something its own slice file says to skip is
the most actively harmful output this skill can produce. A slice present in `slices/` but absent from
`roadmap.json` is `deferred` when marked and `unknown` otherwise; never `next`, never `not started`.

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
means the status is not known — say `unknown`, not `not started`. Those are different claims, and
reporting work as "not started" when the record cannot tell is a lie the user will act on.

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

Then **stop** — after any of the three outputs, the table, the feature state or the story state. No
summary, no offer to start the next step, no commentary on progress. The user asked where they are;
they can see it.

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
- **Layout unrecognized** — say "layout not recognized", show the paths checked, and stop.
  These are nWave's paths, not this plugin's; they move between versions, and guessing at a
  half-matched layout produces a plausible table that is wrong.

---

## Self-test (regression gate)

`self-test/README.md` is the fixture register: what each fixture pins and how to drive it. Drive the
fixtures whenever this skill, its `references/` or `commands/nwave-slice-status.md` changes. Every failure mode here is
silent: the wrong answer arrives as a clean, confident table.

**Fixtures `14` and `17` are the two whose failure mutates rather than misinforms**: each failure
answers `done` over an unassessed roster, and auto-close closes the card — one feature in `14`, **N** in `17`.
Keep both; the README says why neither covers the other.
