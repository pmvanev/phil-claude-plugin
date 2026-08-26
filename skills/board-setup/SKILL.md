---
name: board-setup
description: Use when recording a repo's issue-board constants in its `CLAUDE.md` — the forge and repo, the project and Status field ids, every option id, the enabled workflows, the tier, the docs root and whether the repo is nWave — on GitHub or GitLab. Triggers on "record the board constants", "write the issue board section", "probe the board", "add the board block to a repo that already documents its board", "check whether the board notes still match the forge", "re-run the board setup", or "why can't grooming evaluate rule 4". Probes what a forge answers, asks only what none records, labels every generated line `probed` or `assumed`, coexists with prose it cannot regenerate, and writes zero bytes when nothing moved. Never infers a declaration from the labels in use, and never writes to the forge.
---

# Board setup — probe, label, write

Discover a repo's board constants and write them down **before** they are learned by contact.

Probe everything discoverable, ask for what is not, and **label every line with where it came
from**. A line whose origin cannot be told is the defect here — not a line that is missing.

Why that is the thesis, and why this plugin's own `CLAUDE.md` is the evidence for it:
`${CLAUDE_PLUGIN_ROOT}/skills/board-setup/references/provenance-model.md`.

## Three categories, and every fact line carries one

| Category | Means | Where it is written |
|---|---|---|
| **probed** | the forge returned it | **inside** the markers |
| **assumed** | the forge returned *half* of it, or it is derived from a proxy | inside the markers, labelled, saying what is not knowable |
| **declared** | only a human can say it | a **separate** region, attributed, never regenerated |

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

## Two regions, and the second is a human's

A declaration must live **outside** the probed markers, which collides with AC1's byte-identity. It is
resolved with a **second delimited region**, not loose prose:

```
<!-- phil:board-setup:declared:v1:begin -->
generated … · declarations, not probed facts — a human's answers
- Label family **wave** (`wave: discuss`): **single-valued** *(you declared · 2026-08-17)*
<!-- phil:board-setup:declared:v1:end -->
```

- The **probed** region is regenerated freely, every run.
- The **declared** region is written once on an answer and **never regenerated**. A second
  `--declare` refuses.

**Every ask that fills the declared region follows `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`.**
Load it before the first `AskUserQuestion` call.

Two things that standard cannot know: what makes a question *un-probeable* is this skill's own finding,
so the context block carries the probe that failed and why no forge answers it; and the counted ask must
describe the convention in plain terms — a question about label families that names the families as
identifiers is asking the reader to hold the vocabulary the answer is supposed to establish.

- Bytes outside **both** regions are byte-identical, save the one newline the declared region
  contributes as its own terminator, and the sanctioned retire deletion.

Loose prose would have satisfied "outside the markers" and left slice 05 no way to know what it must
not touch. **Both regions are checked for malformation**: a dangling declared `begin` is
`MALFORMED-MARKERS` like any other, because the command whose rule is *an extent is never guessed*
must not write one itself.

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
| `--file F --refresh REGION.md --expect-sha S` | regenerates the region; **zero bytes if nothing moved** | only on a change |
| `--file F --declare DECL.md --expect-sha S` | inserts the declared region, once | yes |
| `--file F --retire N --expect-sha S` | deletes exactly one whole line | yes |

**`render-block.py` renders both regions, and nothing else may.**

| Call | Does |
|---|---|
| `--probe P.json --stamp T` | the probed-and-assumed region |
| `--probe P.json --stamp T --declarations A.json --declared-only` | the declared region |

Hand-writing a region breaks determinism, and determinism is the whole of KPI-3: a model's ordering
and wording drift run to run, so every refresh would write bytes and the diffs would stop being read.
The renderer refuses a probe whose `status` is not `ok`, so a refusal cannot render as an
empty-but-well-formed block.

**GitLab is `probe-board.py --repo GROUP/PROJ --host gitlab.com`.** A `--forge` contradicting the host
is refused rather than half-served.

The `sha256` from `--classify` is passed back to every writing call, so a file that moved between
read and write is refused rather than overwritten.

**`PROBE.json` and `REGION.md` are intermediates, and they never touch the target repo.** Write both
to the session's scratch directory and pass absolute paths. Left unqualified they default into the
repo root, which contradicts this command's whole contract — *one local file changes* — and leaves
untracked litter in someone else's tree. The target repo gains exactly one modified file:
`CLAUDE.md`.

## Five states, and four are written to

| State | Means | Do |
|---|---|---|
| `file-absent` | no `CLAUDE.md` at all | **create it**, carrying the section and the region, and say that it was created |
| `no-section` | no `## Issue board` at all | append the section — slice 01's path |
| `section-no-markers` | hand-written prose, no region | **insert**, then report drift |
| `region-present` | a region is already there | **`--refresh` it** — zero bytes if nothing moved |
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

## Eliciting what no forge records

Two template fields are answerable only by a human: **`label-families`** and
**`local-task-system`**. The probe returns *evidence* for the first and never an answer.

`probe-board.py` emits `elicitation_evidence`: every family, its members, per-label counts,
co-occurring pairs, and **the issue numbers carrying more than one**. Two groupings, and the
difference is load-bearing:

| Grouping | Means |
|---|---|
| `syntactic prefix` | `wave: discuss` and `status::doing` group under `wave` / `status` because the label's **name** says so — a fact about the string |
| `candidate grouping, unconfirmed` | unprefixed labels cannot be grouped syntactically, so **the grouping is part of the question** |

Ask per family, with the evidence beneath the question. Five rules:

- **Never pre-select, default, or write on silence.** Not "likely", not a confidence, not a
  recommended option. This is the one thing the slice exists to make impossible.
- **A decline writes nothing at all** — not even a line saying it was declined. Report that rule 4
  stays `unevaluated` for that family. A "declined" line is still a line, and rule 4 would read a
  declaration no human made.
- **An ambiguous reply is asked once more**, naming what is still needed. "ok" / "sure" / "sounds
  right" is unanswered, never resolved by composing.
- **A declaration contradicting observed use is written as given**, with the disagreement recorded
  beside it. Never resolved: the human is the authority, and the observation is what a later reader
  needs to understand why it looked odd.
- **Every declared line is attributed** — `you declared`, with the date. An unattributed line is the
  defect (C3).

**A family whose labels never co-occur is still offered.** Absence of co-occurrence is evidence *for*
single-valued and it is the human's to weigh; dropping the family would answer by omission.

**If the evidence could not be read, say so and ask nothing.** `elicitation_evidence.families` is
`null` — not `[]` — when the label read failed, and that happens on **GitHub too**, not only GitLab.
Iterating an empty list, asking nothing and reporting nothing is answering by omission, which is the
one thing this section exists to forbid. Report the families as unread and name rule 4 as still
unevaluated.

**An `unread` value is reported outside the region, never written inside it.** It is neither a fact
nor a guess but the absence of both, so no provenance label for it would be honest. Saying nothing
about it produces the silent partial block this skill calls worse than none.

## Re-running it

`--refresh` regenerates the probed region and **writes zero bytes when nothing moved** (KPI-3).

**The timestamp question, decided: the stamp is not refreshed on a no-change run.** KPI-3 demands zero
bytes and re-stamping writes bytes, so excluding the stamp from the comparison while still writing it
would fail KPI-3 while looking correct. A run that rewrites the file to move a clock diffs every time,
the diffs stop being read, and the block decays into issue #31's unnoticed-stale state wearing the
look of maintenance.

The change report is **line by line, never a count**: constants are not interchangeable. An option id
that changed means `updateProjectV2Field` was run against the field; a docs root that changed means
every absolute link in every issue body is now wrong.

**`unchanged` and `unread` are never spelled the same way.** A refresh with no rendered region in hand
refuses rather than reporting `unchanged` — a probe that could not be read is not a board that did not
move.

## GitLab

Same region shape, different calls — verified mechanically: the `template_field` set is identical
across forges. Two things are never defaults:

- **Projects-v2 facts render as *not applicable on this forge***, never `none enabled`. GitLab has no
  Projects-v2 workflow system to be empty.
- **An unread label set is not an empty one.** On GitLab the `status::` label set *is* the board, so
  `count: 0` on a failed read states the project has no columns — the most misleading thing that fact
  can say. Such a value carries provenance `unread` and **never enters the markers**.

**The JSON flag differs per `glab` subcommand**: `glab api` takes none, `glab repo view` uses `-F`,
`glab issue list` uses `-O`. `phil:issue-board`'s blanket rule — *"the JSON flag is `-O`; `-F` fails
silently"* — holds for one of the three, and the correction is folded back there too.

**A connectivity failure is retried; an auth failure is not.** A single timeout against a self-hosted
instance is usually the network; a 401 is not flaky, so retrying it only delays the real answer.

The call table, the fold-back, and what remains unverified: `${CLAUDE_PLUGIN_ROOT}/skills/board-setup/references/gitlab.md`. **Read it before changing a
`glab` call** — one of these constants was already wrong in a shipped skill.

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
   `upstream` are two repos with two boards, and the one that matters is usually not the push
   target. This is the first of the three permitted questions, and the only one that runs before the
   probe.
2. **PROBE.** One pass of the script. Report each value beside the call that found it.
3. **CLASSIFY.** `--classify` the target. Branch on the state per the five-state table above, and
   keep the `sha256` it returns — every writing call needs it back. On `file-absent` the `sha256`
   is `null`, and that is the only case where a writing call may be given no `--expect-sha`.
4. **RENDER.** `render-block.py --probe … --stamp …`. Never hand-write the region: determinism is
   what lets step 5 write nothing, and a model cannot hold it.
5. **PLACE or REFRESH.** On `file-absent`, the file is created carrying the section and the region.
   On `no-section`, append the section. On `section-no-markers`, insert after the heading
   (`--place`). On `region-present`, `--refresh` — which writes **zero bytes** if nothing moved.
   Say which of the four happened. On `markers-malformed`, stop.
6. **DRIFT.** `--drift` against the probe JSON. Report all three bucket counts, and list the
   contradictions in full — a count alone hides which line is wrong. Runs on a refresh as well as a
   placement: the prose can drift while the region is current, and that is the common case.
7. **ELICIT.** Ask the label-family question per family, with the evidence beneath it, per the rules
   under *Eliciting what no forge records*. Write the answers with `--declare`. A decline writes
   nothing and is reported as `UNEVALUATED`.
8. **OFFER**, only for contradictions, one line at a time, per the retire rules. No contradictions
   means no question: a run with nothing to ask must ask nothing. **Never offer a declared line.**
9. **REPORT** — the outcome, the three drift counts, the three provenance totals, and what was left
   out with who owns it. A total of zero is stated as such rather than printed bare.

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

`WROTE` · `WROTE-BESIDE-PROSE` · `REFRESHED` · `UNCHANGED` · `DECLARED` · `AMBIGUOUS-TARGET` ·
`REFUSED` · `MALFORMED-MARKERS`

`REGION-PRESENT` is **retired**: slice 05 shipped the re-run it deferred to, so a file already
carrying a region is now `REFRESHED` or `UNCHANGED`. A run still reporting it is running an old
skill — the same retirement `SECTION-EXISTS` went through.

**Three report lines are not outcomes, and each accompanies a terminal one.** `DRIFT` names the three
bucket counts on any run reaching the drift step. `UNEVALUATED` names each label family left
undeclared, so a decline is visible rather than silent. `REPORTED-NOT-WRITTEN` survives only for a
value that is neither probed nor assumable — half-probed values are now *written*, as `assumed`. None
can stand alone, and a run emitting one as its verdict has not reported an outcome.

**`SECTION-EXISTS` is retired.** It was slice 01's boundary marker, and slice 02 is the thing it
pointed at; a run that still reports it is running the old skill.

The discriminator is **who stopped the run**, because the script has one failure state and the model
has another. `${CLAUDE_PLUGIN_ROOT}/skills/board-setup/references/outcomes.md` gives each outcome's
meaning, what it must name, and the fixture contradiction that split the report lines out. Read it
before adding an outcome or changing what one reports.

## What this skill must never do

- **Type a value the script could have returned**, or fill a gap it left.
- **Write a half-probed value as a fact.** It is written as `assumed`, stating what is not knowable
  and why. Spelling it like a probed value is the defect; omitting it is not.
- **Infer a label family from the labels in use.** Nothing on a forge records whether a family is
  single- or multi-valued. The labels in use may be shown as *evidence beside a question*; they may
  never be adopted as the answer. Inferring one makes the board's habits audit themselves and mints
  precisely the declaration `phil:groom-issues` rule 4 exists to read.
- **Write to the forge.** This command reads the forge and writes one local file. It creates no
  project, no field, no option, no label. `updateProjectV2Field`'s full-replacement hazard is a
  reason to *record* a field's shape, never to modify it.
- **Touch anything outside both regions**, on any path including failure — with exactly two
  sanctioned exceptions and no others: the retire offer deleting one whole line on an explicit
  answer, and the declared region's one-time insertion carrying its own terminating newline.
- **Guess a region's extent.** A `begin` marker with no `end` is refused, file unchanged (S2 AC4).
- **Rewrite, reflow or reformat a hand-written line.** Reporting it is the whole job. The only
  permitted change is deleting one whole line, on an answer.
- **Call a line `contradicts` without a probed value to point at.** Absence of evidence is
  `cannot evaluate`. Upgrading it makes the board's habits audit themselves.
- **Offer to retire a `cannot evaluate` line**, or treat silence as consent.
- **Rewrite a *declared* region.** A human's answer is never regenerated; a second `--declare`
  refuses. The probed region, by contrast, is regenerated on every refresh — that is its contract.
- **Leave `PROBE.json`, `REGION.md` or any other intermediate in the target repo.** They belong in
  the session's scratch directory. One file changes, and it is `CLAUDE.md`.
- **Place, insert or retire a line by hand.** `region-place.py` owns every write to the target,
  including creating an absent file. The `Write`/`Edit` grant exists for the script's output path,
  not as a fallback when a call refuses.
- **Relay a fix the product cannot honour**, or print a null `fix`.
- **Restate `phil:issue-board`'s template or its tier probe.** That skill owns both.
- **Rewrite, reflow or delete anything in the declared region**, including through the retire
  offer. It is the one thing here that cannot be regenerated if lost.

## Slice boundary — what is built, and what is merely unverified

**All six slices are built.** CONFIRM → PROBE → CLASSIFY → PLACE/REFRESH → DRIFT → ELICIT → OFFER →
WRITE, on GitHub and GitLab, against a `CLAUDE.md` that is absent, sectionless, hand-written, or
already configured.

What remains open is **verification, not construction**, and it is recorded rather than implied:

| Open | Why | Recorded in |
|---|---|---|
| AC3's `ambiguous`-path asking (slice 01) | skipped by explicit decision; needs a session rooted in a two-remote checkout | slice 01 brief |
| A real GitLab region diffed against a real GitHub one (slice 06 AC1–AC2) | `projects/X` reads unauthenticated but `projects/X/labels` returns 401, and on GitLab the label set *is* the board | slice 06 brief |
| A real self-hosted connection failure (slice 06 AC5) | the retry is unit-tested; no unreachable instance was available | slice 06 brief |

**Three questions are permitted and no more**: confirming the forge target, the label-family question
per family, and the retire offer on a contradicting line. Anything else asked is a defect — the
measurement is what comes out without it.

## Acceptance

Two halves: the scripts are unit-tested, and the prose is model-driven against the twelve fixtures in
`self-test/`. **Drive the fixtures whenever this file or the command loader changes.**

`self-test/README.md` explains how to drive them, what each manifest key means, why
`expected_decision` and `expected_report_lines` are separate keys, and how AC3 splits across the two
halves.

Every failure mode here is silent. A block with a remembered id looks exactly like a probed one, a
partial block looks more complete than a refusal, and a drift report that judged nothing looks like
one that found nothing wrong.
