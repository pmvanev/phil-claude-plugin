---
name: board-setup
description: Use when recording a repo's issue-board constants in its `CLAUDE.md` on GitHub — the forge and repo, the project and Status field ids, every single-select option id, the enabled built-in workflows, the tier, the docs root and whether the repo is nWave — or when asked to "record the board constants", "write the issue board section", "probe the board", "add the board block to a repo that already documents its board", "check whether the hand-written board notes match the forge" (for a repo not yet carrying a generated region — re-checking a configured one is slice 05), or "why grooming cannot evaluate rule 4". Writes probed facts into a delimited region beside hand-written prose without altering a byte of it, reports where that prose agrees with the forge, disagrees, or cannot be judged, and labels every generated line with where it came from. Never infers a declaration from the labels in use, and never writes to the forge.
---

# Board setup — probe, label, write

Discover a repo's board constants and write them down **before** they are learned by contact.

Probe everything discoverable, ask for what is not, and **label every line with where it came
from**. A line whose origin cannot be told is the defect here — not a line that is missing.

Why that is the thesis, and why this plugin's own `CLAUDE.md` is the evidence for it:
`${CLAUDE_PLUGIN_ROOT}/skills/board-setup/references/provenance-model.md`.

## Three categories, and every line carries one

| Category | Means | Where it is written |
|---|---|---|
| **probed** | the forge returned it | **inside** the markers |
| **assumed** | the forge returned *half* of it | inside the markers, labelled — **slice 04** |
| **declared** | only a human can say it | **outside** the markers, attributed — **slice 03** |

The third category is not decoration: *"Auto-close on Done is ENABLED"* is one confident sentence
spanning a fact and a guess, because the forge reports that the workflow is on and never which
status fires it. The field-level derivation is in `${CLAUDE_PLUGIN_ROOT}/skills/board-setup/references/provenance-model.md`.

## The probe is a script, and that is the point

Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/probe-board.py --repo OWNER/REPO`. It emits JSON: every
value paired with the exact query that produced it, in a fixed field order.

**Never type a value this script could return, and never fill a gap it left.** A value that did not
come out of the JSON does not go inside the markers, because in the finished file a remembered id is
indistinguishable from a probed one.

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

**The markers are bare and versioned; the timestamp is the first line inside.** The marker is the
string slice 05 must match on to find the region again, so it must not be the string that changes
every run.

**Every bullet names the query that produced it**, with the queries listed once each at the foot —
several constants come from one call, and repeating a GraphQL document per bullet buries the values
it exists to source. Two shapes need a rule:

- A fact whose `query` is a cross-reference (`"(see project-discovery)"`) cites the **referenced
  fact's** Q-number.
- A compound `query` — two calls joined because the first returned nothing — becomes **two** named
  entries, with what the first returned recorded.

**Everything outside the markers belongs to a human, permanently.**

## Where the region goes, and why it looks tight

**Immediately after the `## Issue board` heading, contributing no blank line of its own.** The line
that already followed the heading terminates the `end` marker, so excising the region returns the
file byte-for-byte. A blank line inserted for readability is a byte outside the markers that was not
there before, so the `end` marker sits directly above the first hand-written line with no breathing
room. That cost is accepted: readability outside the markers is not this command's to spend.

Placement is **deterministic** — the position derives from the heading's line number and nothing
else. No scan for a "good spot", no reading of the prose.

## The reader, the placer and the drift report are a script

`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/region-place.py` owns classification, placement, line
arithmetic and the diff. Same reasoning as the probe: **AC1 is a property code can hold and prose
can only request.** A region placed one line off still looks placed, and a reflowed bullet still
reads as English — every failure here is silent.

| Call | Does | Writes? |
|---|---|---|
| `--file F --classify` | names the state, returns the region extent and a `sha256` | no |
| `--file F --drift PROBE.json` | the three buckets | no |
| `--file F --place REGION.md --expect-sha S` | inserts, re-checking `S` first | yes |
| `--file F --retire N --expect-sha S` | deletes exactly one whole line | yes |

The `sha256` from `--classify` is passed back to every writing call, so a file that moved between
read and write is refused rather than overwritten.

**`PROBE.json` and `REGION.md` are intermediates, and they never touch the target repo.** Write both
to the session's scratch directory and pass absolute paths. Left unqualified they default into the
repo root, which contradicts this command's whole contract — *one local file changes* — and leaves
untracked litter in someone else's tree. The target repo gains exactly one modified file:
`CLAUDE.md`.

## Five states, and only three are written to

| State | Means | Do |
|---|---|---|
| `file-absent` | no `CLAUDE.md` at all | **create it**, carrying the section and the region, and say that it was created |
| `no-section` | no `## Issue board` at all | append the section — slice 01's path |
| `section-no-markers` | hand-written prose, no region | **insert**, then report drift |
| `region-present` | a region is already there | **stop.** Slice 05 owns re-run and staleness |
| `markers-malformed` | `begin` without `end`, `end` without `begin`, nested, or out of order | **refuse**, file untouched |

`### Issue board` is never the section. A heading deeper than h2 belongs to something else, and
inserting board constants under an unrelated parent is a silent misplacement.

## The drift report, and the bucket that keeps it honest

Three buckets over the prose **outside** the markers:

- **confirms** — a probed value appears verbatim on the line.
- **contradicts** — a token of a *known shape* (`PVT_…`, `PVTSSF_…`, a docs-root URL) appears and
  matches no probed value. Contradiction wins the line outright; a line carrying one right id and
  one wrong one is a wrong line.
- **cannot evaluate** — everything else, and it is the honest bucket. A line the probe says nothing
  about is **never** `contradicts`. Most of a real board section lands here, and that is the correct
  result rather than a weak one: the hazards are prose recorded after contact, and no forge records
  them.

Two rules the first dogfood run bought, both of which had made the report *look* better than it was:

- **A probed scalar shorter than six characters is not evidence.**
- **Fact values are walked to full depth**, so ids nested inside a fact still count.

Line numbers are counted over the file with the region excised, so the report is identical before
and after placement. **The generated region agreeing with the probe is a tautology, not a
confirmation**, and must never appear in `confirms`.

The incidents behind all three rules are in
`${CLAUDE_PLUGIN_ROOT}/skills/board-setup/references/drift-and-retire.md`. **Read it before changing
the evidence floor, the flattening depth, or any retire-offer rule** — each number there was bought
by a false result on a real board.

## The retire offer

For a **contradicting** line stating a fact the region now owns, offer to remove it. Rules:

- **Applied only on an explicit answer.** Silence writes nothing and records nothing — no "no
  objection raised" path exists.
- **One whole line, deleted.** Never rewritten, reflowed, or partially edited. Deleting a line is
  reviewable in a diff; rewriting one is an edit nobody asked for.
- **Never offered for `cannot evaluate`.** There is no evidence the line is wrong, so there is
  nothing to retire it in favour of.
- **Never offered for a line inside the markers.** The region is regenerated, not retired.

### The facts with no template field still get written

Five facts carry no `template_field`: `default-branch`, `fork`, `project-discovery`, `board-view`,
`other-single-select-fields`. **They are not surplus and must not be dropped.** Write them as
bullets in the same region, after the template-shaped ones, each carrying its provenance and
Q-number like any other. `fork` and `other-single-select-fields` appear only when the forge returned
them. Why *how the board was found* is itself a constant: `${CLAUDE_PLUGIN_ROOT}/skills/board-setup/references/provenance-model.md`.

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
3. **CLASSIFY.** `--classify` the target. Branch on the state per the five-state table above, and
   keep the `sha256` it returns — every writing call needs it back. On `file-absent` the `sha256`
   is `null`, and that is the only case where a writing call may be given no `--expect-sha`.
4. **PLACE.** On `file-absent`, the file is created carrying the section and the region. On
   `no-section`, append the section containing only the region. On `section-no-markers`, insert
   after the heading. Say which of the three happened. On the other two states, stop.
5. **DRIFT.** `--drift` against the probe JSON. Report all three bucket counts, and list the
   contradictions in full — a count alone hides which line is wrong.
6. **OFFER**, only for contradictions, one line at a time, per the retire rules above. No
   contradictions means no question: a run with nothing to ask must ask nothing.
7. **WRITE**, then **REPORT** — naming what was left out and who owns it. The declared and assumed
   totals are still **necessarily zero**, because slices 03 and 04 are not built; say so rather
   than printing a bare `0` that invites filling.

**Scope is the working tree's `CLAUDE.md`** — one `CLAUDE.md`, the one in the working tree, never a sibling
checkout. Confirming the forge target is required; the file target is not negotiable.

## What the probe reaches, and what it cannot

The probe reaches every field of `phil:issue-board`'s *Per-project setup* template except
**`label-families`** and **`local-task-system`** — both slice 03's, both correctly *declared* rather
than guessed. `phil:issue-board` owns the template and the forge mechanics;
`phil:nwave-issue-board` owns the artifact→issue mapping. Coverage detail and the GitHub tier
reasoning: `${CLAUDE_PLUGIN_ROOT}/skills/board-setup/references/provenance-model.md`.

**`/phil:claude-md` does not know this region exists.** It revises `CLAUDE.md` against a checklist
including line budgets and "no long explanations", so running it over a configured repo can compress
or delete probed ids — silently. Until that skill learns to treat a marked region as off-limits,
re-run this command after any `/phil:claude-md` pass and check the region survived.

## Decision outcomes

Report **exactly one terminal outcome** by name, every run:

`WROTE` · `WROTE-BESIDE-PROSE` · `AMBIGUOUS-TARGET` · `REFUSED` · `REGION-PRESENT` ·
`MALFORMED-MARKERS`

**Two report lines are not outcomes, and both accompany a terminal one.** `DRIFT` names the three
bucket counts on any run reaching step 5. `REPORTED-NOT-WRITTEN` names the half-probed values on any
run where the probe returned some. Neither can stand alone, and a run emitting one as its verdict
has not reported an outcome.

**`SECTION-EXISTS` is retired.** It was slice 01's boundary marker, and slice 02 is the thing it
pointed at; a run that still reports it is running the old skill.

The discriminator is **who stopped the run**, because the script has one failure state and the model
has another. `${CLAUDE_PLUGIN_ROOT}/skills/board-setup/references/outcomes.md` gives each outcome's
meaning, what it must name, and the fixture contradiction that split the report lines out. Read it
before adding an outcome or changing what one reports.

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
- **Touch anything outside the markers**, on any path including failure — with exactly one
  exception, the retire offer, which deletes one whole line on an explicit answer and nothing else.
- **Guess a region's extent.** A `begin` marker with no `end` is refused, file unchanged (S2 AC4).
- **Rewrite, reflow or reformat a hand-written line.** Reporting it is the whole job. The only
  permitted change is deleting one whole line, on an answer.
- **Call a line `contradicts` without a probed value to point at.** Absence of evidence is
  `cannot evaluate`. Upgrading it makes the board's habits audit themselves.
- **Offer to retire a `cannot evaluate` line**, or treat silence as consent.
- **Rewrite an existing region.** That is slice 05's, and doing it here is undefined behaviour that
  reports success.
- **Leave `PROBE.json`, `REGION.md` or any other intermediate in the target repo.** They belong in
  the session's scratch directory. One file changes, and it is `CLAUDE.md`.
- **Place, insert or retire a line by hand.** `region-place.py` owns every write to the target,
  including creating an absent file. The `Write`/`Edit` grant exists for the script's output path,
  not as a fallback when a call refuses.
- **Relay a fix the product cannot honour**, or print a null `fix`.
- **Restate `phil:issue-board`'s template or its tier probe.** That skill owns both.
- **Claim a re-run is safe.** Slice 05 owns re-run behaviour; running twice is undefined until it
  ships.

## Slice boundary — what is not built yet

Slices 01 and 02 ship CONFIRM → PROBE → CLASSIFY → PLACE → DRIFT → OFFER → WRITE, against a
`CLAUDE.md` with no section **or** with a hand-written one. Deliberately absent, and not an
oversight to improvise:

| Not built | Owner | Consequence today |
|---|---|---|
| Eliciting label families | slice 03 | Grooming keeps reporting rule 4 **unevaluated**, and the report says so |
| The `assumed` label and confirm offer | slice 04 | Half-probed values are reported, never written |
| Safe re-run, staleness, vanished option ids | slice 05 | A file that already has a region stops with `REGION-PRESENT` |
| GitLab (`glab`) | slice 06 | GitHub only; a GitLab repo is refused, not half-served |

**Only two questions are permitted**: confirming the forge target, and the retire offer on a
contradicting line. Anything else asked is a defect — the measurement is what comes out without it.

## Acceptance

Two halves: the scripts are unit-tested, and the prose is model-driven against the seven fixtures in
`self-test/`. **Drive the fixtures whenever this file or the command loader changes.**

`self-test/README.md` explains how to drive them, what each manifest key means, why
`expected_decision` and `expected_report_lines` are separate keys, and how AC3 splits across the two
halves.

Every failure mode here is silent. A block with a remembered id looks exactly like a probed one, a
partial block looks more complete than a refusal, and a drift report that judged nothing looks like
one that found nothing wrong.
