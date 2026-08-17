---
name: board-setup
description: Use when recording a repo's issue-board constants in its `CLAUDE.md` on GitHub — the forge and repo, the project and Status field ids, every single-select option id, the enabled built-in workflows, the tier, the docs root and whether the repo is nWave — or when asked to "record the board constants", "write the issue board section", "probe the board", or "why grooming cannot evaluate rule 4". Writes probed facts into a delimited region and labels every line with where it came from. Never infers a declaration from the labels in use, and never writes to the forge.
---

# Board setup — probe, label, write

Discover a repo's board constants and write them down **before** they are learned by contact. This
plugin's own `CLAUDE.md` is the evidence: most of the hazards in its `## Issue board` section were
written *after* the thing they document had already gone wrong — two of them still carry the date
they were learned. Each was paid for by a call that reported success while doing something else.

So probe everything discoverable, ask for what is not, and **label every line with where it came
from**. A line whose origin cannot be told is the defect here — not a line that is missing.

## Three categories, and every line carries one

| Category | Means | Where it is written |
|---|---|---|
| **probed** | the forge returned it | **inside** the markers |
| **assumed** | the forge returned *half* of it | inside the markers, labelled — **slice 04** |
| **declared** | only a human can say it | **outside** the markers, attributed — **slice 03** |

The third category is not decoration. `projectV2 { workflows { name enabled } }` returns
`Auto-close issue: enabled`, so the hazard is discoverable — but `ProjectV2Workflow` exposes
`createdAt, enabled, fullDatabaseId, id, name, number, project, updatedAt` and **no field for the
configured trigger statuses**. "A status→close workflow is on" is probed; "`Done` fires it" is
assumed. A block saying *"Auto-close on Done is ENABLED"* is one confident sentence spanning a fact
and a guess.

## The probe is a script, and that is the point

Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/probe-board.py --repo OWNER/REPO`. It emits JSON: every
value paired with the exact query that produced it, in a fixed field order.

**Never type a value this script could return, and never fill a gap it left.** The script exists
because AC1 — *no value inside the markers was typed by a human* — is a property code can hold and
prose can only request. In the finished file a remembered id is indistinguishable from a probed one,
which is this feature's own failure mode turned on itself. A value that did not come out of the
JSON does not go inside the markers.

**Read `status` first.** On `refused`, **write nothing** and report `refusal.reason`, then
`refusal.fix` **when it is non-null** — `fix` is nullable, and printing `None` at a reader is worse
than saying no fix is known. A refusal whose reason names an unbuilt slice is reported as *not
available yet*, never as an instruction: there is no flag that names a board, and relaying advice the
product cannot honour is its own defect.

A partial block is worse than none: a block silently missing its Status field id reads exactly like
one whose board has no Status field.

## The region

```markdown
## Issue board

<!-- phil:board-setup:v1:begin -->
generated 2026-08-17T14:44Z · do not edit inside these markers

- Forge: GitHub at github.com — use `gh -R owner/repo` on every call *(probed · Q1)*
- Board: project `PVT_…` · number 3 · "phil plugin" *(probed · Q2)*
- Status is a project **field**, id `PVTSSF_…` — not a label *(probed · Q3)*
- Status options (4) *(probed · Q3)*: Todo `f75ad846` · In Progress `47fc9ee4` · …

**Queries**

- `Q1` — `gh repo view owner/repo --json nameWithOwner,defaultBranchRef,isFork,isPrivate`
- `Q2` — `{ repository(owner:"…", name:"…"){ projectsV2(first:20){ … } } }`

<!-- phil:board-setup:v1:end -->
```

**The markers are bare and versioned; the timestamp is the first line inside.** This follows
`nwave-issue-board`'s generated-block convention, and the reason is mechanical: the marker is the
string slice 05 must match on to find the region again, so it must not be the string that changes
every run. A version token lets a later slice recognise a region written by an earlier one.

**Every bullet names the query that produced it**, with the queries listed once each at the foot —
several constants come from one call, and repeating a GraphQL document per bullet buries the values
it exists to source. Two shapes need a rule:

- A fact whose `query` is a cross-reference (`"(see project-discovery)"`) cites the **referenced
  fact's** Q-number.
- A compound `query` — two calls joined because the first returned nothing — becomes **two** named
  entries, with what the first returned recorded.

**Everything outside the markers belongs to a human, permanently.**

### The facts with no template field still get written

Five facts carry no `template_field`: `default-branch`, `fork`, `project-discovery`, `board-view`,
`other-single-select-fields`. They are not surplus and must not be dropped — *how* the board was
found is itself a constant, and a repo whose project is unlinked is a repo where
`gh project item-add` is the only way a card ever arrives. Write them as bullets in the same region,
after the template-shaped ones, each carrying its provenance and Q-number like any other. `fork` and
`other-single-select-fields` appear only when the forge returned them.

## The flow

1. **CONFIRM the forge target.** Enumerate the candidates mechanically — it makes no forge call:

   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/probe-board.py --list-targets
   ```

   Then **confirm with the human before any call**, on every `status`:

   | `status` | Do |
   |---|---|
   | `ok` | one candidate — confirm it anyway. `confirm_required` is always true |
   | `ambiguous` | **ask** which board, presenting the candidates. Never pick, and never prefer `origin` |
   | `none` | no parseable remote — ask for the target |

   Never infer: issue `#12` exists in every repo, so an inferred remote reads — and would mutate —
   the wrong one successfully. **A fork is the case that looks fine and is not**: `origin` and
   `upstream` are two repos with two boards, and the one that matters is usually not the one you
   pushed to. This is the only question slice 01 may ask, and it happens before the probe runs.
2. **PROBE.** One pass of the script. Report each value beside the call that found it.
3. **PLACE.** Slice 01 targets a `CLAUDE.md` with **no** `## Issue board` section. Append the
   section containing only the region. Create the file if absent, and say which happened.
4. **WRITE**, then **REPORT** — naming what was left out and who owns it. In slice 01 the declared
   and assumed totals are **necessarily zero**, because neither is built; say so rather than
   printing a bare `0` that invites filling.

**Scope is the repo you are in** — one `CLAUDE.md`, the one in the working tree, never a sibling
checkout. Confirming the forge target is required; the file target is not negotiable.

## What the probe reaches, and what it cannot

Measured against `phil:issue-board`'s *Per-project setup* template, which owns the block's content:
the probe reaches every field except **`label-families`** and **`local-task-system`**, both slice
03's, both correctly *declared* rather than guessed. The slice brief owns the KPI-1 reading; the
durable fact is which two fields no forge can answer.

`phil:issue-board` owns the template and the forge mechanics; `phil:nwave-issue-board` owns the
artifact→issue mapping. On GitHub the **tier comes out of the probe as *not applicable*** — the
bullet exists because GitLab gates scoped labels and real `blocks` links behind Premium, and GitHub
gates neither, so there is no GitHub tier call to make and none to invent. When GitLab lands
(slice 06) the probe calls `phil:issue-board`'s tier check rather than restating it.

**`/phil:claude-md` does not know this region exists.** It revises `CLAUDE.md` against a checklist
including line budgets and "no long explanations", so running it over a configured repo can compress
or delete probed ids — silently. Until that skill learns to treat a marked region as off-limits,
re-run this command after any `/phil:claude-md` pass and check the region survived.

## Decision outcomes

Report the outcome by name, every run. Exactly one:

`WROTE` · `AMBIGUOUS-TARGET` · `REFUSED` · `SECTION-EXISTS` · `REPORTED-NOT-WRITTEN`

The discriminator is **who stopped it**, because the script has one failure state and the model has
another:

- **`WROTE`** — names the file and the field count.
- **`AMBIGUOUS-TARGET`** — resolved by the model at CONFIRM, *before* the script runs: two remotes,
  or a fork. A question, never a guess.
- **`REFUSED`** — the script returned `status: refused`. Report `refusal.reason` verbatim and
  `refusal.fix` when non-null. Includes every case the script cannot resolve: a missing `project`
  scope, more than one candidate project, no board at all, a project with no `Status` field, a forge
  error. The file is byte-unchanged.
- **`SECTION-EXISTS`** — the target already has an `## Issue board` section. Slice 02 owns coexisting
  with prose; until it ships this stops, changing nothing.
- **`REPORTED-NOT-WRITTEN`** — accompanies `WROTE` for the half-probed values: reported to the
  human, kept out of the file until slice 04 ships the labelling that would make them honest.

## What this skill must never do

- **Type a value the script could have returned**, or fill a gap it left.
- **Write a half-probed value.** Report it; slice 04 owns the `assumed` label and its confirm offer.
- **Infer a label family from the labels in use.** Nothing on a forge records whether a family is
  single- or multi-valued. The labels in use may be shown as *evidence beside a question*; they may
  never be adopted as the answer. Inferring one makes the board's habits audit themselves and mints
  precisely the declaration `phil:groom-issues` rule 4 exists to read.
- **Write to the forge.** This command reads the forge and writes one local file. It creates no
  project, no field, no option, no label. `updateProjectV2Field`'s full-replacement hazard is a
  reason to *record* a field's shape, never to modify it.
- **Touch anything outside the markers**, on any path including failure.
- **Guess a region's extent.** A `begin` marker with no `end` is refused, file unchanged. (S2 AC4 —
  slice 02's criterion, kept here as defence; its presence is not evidence that placement among
  prose is built.)
- **Relay a fix the product cannot honour**, or print a null `fix`.
- **Restate `phil:issue-board`'s template or its tier probe.** That skill owns both.
- **Claim a re-run is safe.** Slice 05 owns re-run behaviour; running twice is undefined until it
  ships.

## Slice boundary — what is not built yet

Slice 01 ships CONFIRM → PROBE → PLACE → WRITE against a `CLAUDE.md` with no `## Issue board`
section. Deliberately absent, and not an oversight to improvise:

| Not built | Owner | Consequence today |
|---|---|---|
| Coexisting with hand-written prose; drift reporting | slice 02 | The target must have no such section |
| Eliciting label families | slice 03 | Grooming keeps reporting rule 4 **unevaluated**, and the report says so |
| The `assumed` label and confirm offer | slice 04 | Half-probed values are reported, never written |
| Safe re-run, staleness, vanished option ids | slice 05 | Running twice is undefined |
| GitLab (`glab`) | slice 06 | GitHub only; a GitLab repo is refused, not half-served |

**A question in slice 01 is a defect** beyond confirming the forge target — the whole measurement is
what comes out with none.

## Acceptance

Two halves, automated to different degrees, and the difference matters:

- **The script is tested.** `tests/test_probe_board.py` covers the refusal paths, `project` scope
  detection, and both ambiguity directions — including AC4, which is otherwise unverifiable without
  stripping the operator's live `gh` scope.
- **The prose is model-driven.** There is no CI runner in this plugin. `self-test/` holds the
  fixtures; drive each by giving this skill the situation in its `manifest.json` and comparing the
  decision reached against its `expected.md`. Do that whenever this file or the command loader
  changes.

AC3 splits across the two halves, and the split is the point: **detecting** ambiguity is tested
(`--list-targets` over a real two-remote checkout returns `ambiguous` with both candidates), while
**asking** is prose and stays unverified until the command runs as a command. Detection was moved out
of prose for exactly the reason the probe is a script: a property code holds beats one a model is
asked to honour.

`docs/feature/board-setup-block/slices/slice-01-probe-and-write.md` holds the criteria and the KPI-1
reading.

Every failure mode here is silent. A block with a remembered id looks exactly like a probed one, and
a partial block looks more complete than a refusal.
