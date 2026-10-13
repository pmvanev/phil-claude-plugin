---
name: nwave-slice-status
description: Use when the user asks where an nWave feature stands — "how many steps are in this slice", "which ones are done", "which one are we on", "what's next", "is slice 03 next", "what was the point of slice 02". Renders a read-only step table from the feature's own artifacts and stops. Prefer over `/nw-continue`, which computes the same thing and then launches the next wave, and over `/nw-buddy`, which answers in prose — this produces a table and starts nothing. Also folds a feature-level state over every slice on request — "what state is this feature in", "which column does this card belong in" — and a story-level state over every feature in a story — "what state is this story in", "how far through the story are we" — for a caller placing the card on a board. For what a finished stage DECIDED rather than where it stands, use phil:nwave-wave-summary instead.
---

# Slice Status

Answer one question — **where does this feature stand right now?** — by reading the feature's own
artifacts, rendering a table, and stopping.

**Read-only.** `/nw-continue` computes similar data and then *launches the next wave*; this skill
exists to look without starting anything. Print the resume command as text; never run it.

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
| `--feature-state` | Emit the feature-level state instead of the tables — see *The feature-level state, on request*. Combines with a feature id; a slice number alongside it is a contradiction, because the fold always reads the whole roster. Say so and ask. |
| `--story-state <slug>` | Emit the story-level state — see *The story-level state, on request*. Takes a story slug, never a feature id. A slice number or a feature id alongside it is a contradiction, for the same reason: the fold reads the whole story. Say so and ask. |
| both `--feature-state` and `--story-state` | Two different questions at two scopes. Do not guess which was meant, and do not emit both. Say so and ask. |
| No `docs/feature/` at all | Say so and stop. Suggest `/nw-new`. Do not search elsewhere. |

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

### The feature-level state, on request

A count is not a state. `5 of 9 done` says how much is finished; it does not say what the feature *is*,
which is what a caller placing it in a board column needs. **Emit a feature-level state only when asked
for one** — by the `--feature-state` flag, or by a question that plainly asks for one (*"what state is
this feature in"*, *"which column does this card belong in"*) — and derive it by this fold, in this order,
because the order is the content:

| Test, applied in order | State |
|---|---|
| The roster is empty — no slice files and no roadmap phases | `unknown` |
| The current slice is `blocked` | `blocked` |
| Every slice that is not `deferred` is `done` | `done` — note any deferred slices |
| Any slice is `done` or `current` | `in progress` |
| Every slice is `deferred` | `deferred` |
| Any slice is `unknown`, and none is `done` or `current` | `unknown` |
| Otherwise — every slice `not started` or `next` | `to do` |

**Order matters most at the `in progress` row.** A feature with five of six slices `done` and the
sixth `not started` folds to `in progress`; reading only the current slice gives `to do`, reporting
nearly-finished work as untouched.

**`unknown` sits below `done`/`current` deliberately.** A feature with three slices done and one
unrecorded is in progress, not unknown; the unrecorded slice is a `Notes` entry, not a verdict on the
feature. But where nothing is known, `unknown` is the answer and **never `to do`** — the cardinal rule of
this skill applied to the fold.

**The empty-roster row is the one place `unknown` outranks everything**, because every universal below
it is vacuously true over an empty roster. A feature never decomposed would otherwise fold to `done`;
`phil:nwave-issue-board` maps `done` to the Done column, and on a board with auto-close the card closes.
An empty roster is a fact about the record, not about the work.

**Render the state as one line, with the count beside it** — `Feature: <id> — <state> · N of M slices
done · current slice NN` — because a state and a count answer different questions and a caller placing a
card needs both. **The empty roster is the one case that carries no count:** `0 of 0 done` reads as
completion, which is the same lie arithmetically. Say what is missing there and name the command that
fixes it.

This state is a derivation, so it belongs here rather than in whatever publishes it. Two derivations over
the same files drift apart, and a publisher that folds locally is inventing a status while claiming to
delegate one. `phil:nwave-issue-board` consumes this and renders it; it does not compute it.

Notes stays empty when the sources agree. Put drift, missing artifacts, and ambiguity there — one
short clause each, not a paragraph.

Then **stop** — after any of the three outputs, the table, the feature state or the story state. No
summary, no offer to start the next step, no commentary on progress. The user asked where they are;
they can see it.

---

### The story-level state, on request

A **story** is several nWave features worked as one piece by one owner, carried on one card. Emit a
story-level state only when asked — by `--story-state <slug>`, or by a question that plainly asks for
one (*"what state is this story in"*). `phil:nwave-issue-board` renders this value; it must never
compute it.

**Build the roster from the features' own declarations.** Scan `docs/feature/*/feature-delta.md` for
`Story: <slug> · position NN` — **anchored at column 0, in the file's header region, at most one per
file**. The story's roster is every feature declaring that slug, in `position` order.

**The anchor is load-bearing.** A feature delta may discuss the convention as well as use it, so an
unanchored match finds decoys that parse as conflicting declarations, and `**Story:**` appears in
slice briefs for an unrelated concept. **A file matching twice at column 0 is a defect** — name both
and do not pick.

- **A feature with no `Story:` line is in no story.** That is the normal case and never an error.
- **A missing `position` sorts last**, and Notes says the order was not declared.
- **A position collision is named in Notes, never resolved.** Two features claiming position 02 is a
  fact about the record; picking one invents an order the artifacts do not contain.
- **Nothing here reads a forge.** Membership lives in `docs/feature/`, so this derivation stays a pure
  read of artifacts — which is what lets the publisher stay a renderer.

**The fold is the feature fold with features substituted for slices. It is not a second table, and
must never become one** — two tables over the same seven tests drift, and preventing that drift is why
this skill owns both folds. Apply *The feature-level state, on request* with exactly these
substitutions:

| In the feature fold, read | As |
|---|---|
| "slice" | "feature" |
| a slice's status (seven values) | a feature's state, from the feature fold itself (six values) |
| `current` | `in progress` |
| `not started` | `to do` — the feature fold returns `to do`, never `not started`; without this row the final test's condition is unmatchable |
| `next` | **absent** — the feature vocabulary has no such value, so no test can match it |
| the roster is empty (no slice files, no roadmap phases) | **no feature declares this slug** — the guard row does not survive a literal substitution, and it is the row that matters most |

Each member's state therefore comes from running the feature fold over that feature's own roster. A
story fold is M feature folds and one application of the same table.

**Render as one line, with the count beside it:**

```
Story: <slug> — <state> · N of M features done · current feature <id>
Notes: <one short clause per defect, one per line; omitted entirely when the sources agree>
```

**`current feature` is the first member, in `position` order, whose state is not `done`.** Omit it
entirely when every member is `done`.

**Where the position order is contested, the ordinal does not resolve — say so in its place:**

```
Story: <slug> — <state> · N of M features done · current feature contested — position NN claimed by <a> and <b>
```

The state is quantified over members, not over their order, so a collision cannot change it. What a
collision *does* change is `current feature`, the field a reader acts on when asking what to work on
next. Emitting a winner there — by directory name, by mtime, by discovery order — invents the one fact
the artifacts do not contain, and the result is indistinguishable from a story whose positions were
declared correctly. Report the state, withhold the ordinal.

**The guard matters more here, and it must be tested on its conjunction.** The empty-roster row exists
because every universal below it is vacuously true over an empty set, so an unguarded fold answers
`done`, `phil:nwave-issue-board` maps `done` to Done, and auto-close turns the rendering into a closed
issue. One level up, that closed card holds **N features**. Two emptinesses are distinct and resolve
differently:

- **No feature declares the slug** — the roster is empty. `unknown`, **no count**, and say the slug
  matched nothing. Guard row.
- **Features declare the slug but every one folds to `unknown`** — the roster is populated. `unknown`
  **with a count**, from the existential row, and Notes names the unreadable members.

A guard weakened to one clause stays green on the other, which is why both are pinned.

**A story is never `next`, and never inherits a slice's status directly.** Reading a member's *slice*
status where its *feature* state is required crosses two vocabularies and produces a value the six-state
table cannot render.

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
fixtures whenever this skill or `commands/nwave-slice-status.md` changes. Every failure mode here is
silent: the wrong answer arrives as a clean, confident table.

**Fixtures `14` and `17` are the two whose failure mutates rather than misinforms**: each failure
answers `done` over an unassessed roster, and auto-close closes the card — one feature in `14`, **N** in `17`.
Keep both; the README says why neither covers the other.
