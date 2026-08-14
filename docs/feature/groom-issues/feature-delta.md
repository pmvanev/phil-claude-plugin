# Feature Delta — groom-issues

Forge: pmvanev/phil-claude-plugin#5 · Wave: DISCUSS ✓ (2026-08-12)
Density: lean + ask-intelligent (`~/.nwave/global-config.json`)

**Build path:** DISCUSS here, then authored with `plugin-dev` — not DESIGN/DISTILL/DELIVER. The
deliverable is a skill plus a thin command, and this repo settled twice that skills are authored
rather than waved (`todo.md` 2026-06-17; edd-loop DDD8). Same path `session-handoff` took.

---

## Wave: DISCUSS / [REF] Persona ID

**`robin-backlog-curator`** — Robin owns a board that other people, and a past self, also file into,
and pays when a card turns out to mean something other than what it said. Registered at
`docs/product/personas/robin-backlog-curator.yaml`.

Curator rather than steward: Quinn holds stewardship of the codebase; Robin holds the board that
decides what gets worked on it.

## Wave: DISCUSS / [REF] JTBD one-liner

When a board has accumulated half-finished cards, Robin wants it brought into shape with the
judgement calls put to a human rather than guessed — so the board can be trusted, and ranked over
understood work.

## Wave: DISCUSS / [REF] Locked decisions

- **[D1]** Feature type = **infrastructure/tooling**. One surface (a board) plus a mapping, not a
  concern spanning layers — narrower than `session-handoff`, matching `phil-work`. (User)
- **[D2]** Walking skeleton = **yes**, and it is **read-only**: scan and report, change nothing.
  #5 forbids applying any set-level operation unasked, so a read-only first slice delivers most of
  the value with none of the blast radius. (User)
- **[D3]** UX depth = **comprehensive**. The damaging failures here are irreversible and live in the
  error paths. (User)
- **[D4]** JTBD = **yes**, forced — a developer-invocable command has a user-visible surface.
- **[D5]** Loop pacing = **scan → report → user scopes → fix**. Chosen over report-only-backlog
  because a defect backlog file would be a second authority over issue state; chosen over
  issue-at-a-time because #5 is explicit that duplicate detection "cannot run inside a per-issue
  loop". (User)
- **[D6]** **No `groomed` marker** — no label, no timestamp block. Re-derive the defect table every
  run. Carried from #5 and confirmed: a stored marker lies the moment a human edits the issue.
- **[D7]** The **house-default body standard** ships with the skill and is overridable per project in
  `CLAUDE.md`. Without it, "appropriate description" is not checkable and grooming is taste. This is
  the gap #5 says must close first.

## Wave: DISCUSS / [REF] Resolved before design

Two positions #5 asked for, both answerable from work completed today:

- **Session state in an issue body is a groomable defect.** ADR-013 placed the session snapshot in a
  git-ignored root dotfile precisely because a board is world-readable. Scratch in a body is
  misplaced state, and grooming should say so.
- **A missing `Work this with:` line is *not* a body defect.** It is generated into the delimited
  `nwave:status` block by `phil:nwave-issue-board`. Grooming must never hand-write one — that is
  typing into a generated region, which the next refresh overwrites.

And #5's open risk is closed: **the cheap scan works on both forges.** The flag in the issue was
wrong (`-F` is `--output-format`); it is `-O/--output json`. Verified — one call returned 5 issues,
39 fields, **5/5 populated descriptions**, plus labels and milestone. `gh issue list --json body`
likewise. No N+1, so D6's scan-every-run design stands.

## Wave: DISCUSS / [REF] Scope Assessment

**OVERSIZED — 2 signals. Split confirmed by user.**

| Signal | Fired? | Evidence |
|---|---|---|
| >3 bounded contexts | **YES** | Four: the body standard · per-issue mechanical fixes · cross-issue set operations · consuming the milestone/nWave mapping |
| Multiple independently shippable outcomes | **YES** | Three: scan+report (read-only) · mechanical fixes · set-level operations |
| >10 user stories | not established | not claimed |
| WS needs >5 integration points | no | the skeleton is a read-only scan |
| Effort >2 weeks | not established | not claimed |

## Wave: DISCUSS / [REF] Slices and order

| # | Slice | Learning hypothesis — disproves… | Depends on |
|---|---|---|---|
| 01 | Scan and report (**WS**, read-only) | …that a defect oracle can be stated at all | — |
| 02 | Mechanical fixes within a scope | …that any fix is safe unasked | 01 |
| 03 | Set-level operations, all ask-first | …that set-level defects are detectable with actionable evidence | 01 |

Ordered by learning leverage. Slice 01 carries the feature's central bet: if the report reads as
taste rather than checkable findings, the house-default standard (D7) is insufficient and everything
downstream rests on nothing. It is also read-only, so a failed bet costs nothing but the reading.

## Wave: DISCUSS / [REF] Driving ports

| Port | Surface | Slice |
|---|---|---|
| `/phil:groom-issues` | Slash command — scan and report, holds no write tool | 01 |
| `/phil:groom-fix` | Slash command — applies the mechanical column inside a chosen scope | 02 |
| `/phil:groom-set` | Slash command — resolves merge, split, close and group, asking before each | 03 |

**Revised at slice 02, and again at 03.** DISCUSS planned one port, on the reasoning that scoping and
every judgement call happen inside the session through `AskUserQuestion` rather than as separate
commands. That held for the *decisions* and failed for the *tools*: a single command must carry every
write tool the feature will ever need, which destroys the scan's read-only guarantee (slice 02) and puts
a reversible label edit behind the same consent as an irreversible close (slice 03). The judgement calls
are still made in-session by `AskUserQuestion`; what the extra ports buy is that the tools a command
lacks are unreachable from it. Three ports, each holding the narrowest grant its job needs.

## Wave: DISCUSS / [REF] Journey

SSOT: `docs/product/journeys/groom-issues.yaml`. Comprehensive depth per D3.

**Happy path:** invoke → scan → scope → fix-mechanical → decide-set-level → report.
**Emotional arc:** wary → relief → control → momentum → confidence → trust (upward).

**The cost D6 buys, named plainly.** Because the defect table is re-derived every run and nothing is
stored, **a declined set-level candidate will be proposed again next run**. That is the price of
having no second authority. It is not a bug, and the report must say so — otherwise it reads as the
tool forgetting, and the user starts wanting the marker that D6 exists to refuse.

Six error paths are mapped in the SSOT journey. The two that shape the design: a partial scan must
never report "N clean", because a completeness claim over a partial read is the one output that
actively misleads; and a fix that would edit inside a generated region is refused outright.

## Wave: DISCUSS / [REF] Out-of-scope

- **Ranking.** `phil:rank-issues` owns it. Grooming settles what a card means; ranking settles order.
- **Deriving status.** `phil:nwave-slice-status` owns that, and `nwave-issue-board` already forbids a
  second derivation.
- **Writing inside generated blocks.** Ever.
- **Any set-level operation without asking** — merge, split, close, group.
- **A groomed marker**, in any form. D6.

## Wave: DISCUSS / [REF] Pre-requisites

- No DISCOVER or DIVERGE wave ran (`docs/feature/groom-issues/` did not exist before this wave).
- SSOT read: `jobs.yaml` (7 jobs), 5 personas, 6 journeys. `vision.md`, `project-brief.md`, and
  `stakeholders.yaml` do not exist in this repo.
- Depends on decisions already landed: **#7** (a milestone is a goal — grooming consumes this
  convention for the "ungrouped effort" defect rather than inventing a second one) and **#8**
  (ranking exists, and runs after grooming by advice rather than gate).

## Wave: DISCUSS / [REF] Wave decisions summary

### Requirements summary

- **Primary job:** make a board trustworthy — every card says what it means, defects between cards
  are surfaced with evidence, and every irreversible call is the human's.
- **Walking skeleton:** slice 01 — scan and report, read-only.
- **Feature type:** infrastructure/tooling; deliverable is prose (a skill + one command loader).

### Constraints established

- **C1 — No stored grooming state.** Re-derive every run; a marker is a second authority.
- **C2 — Nothing irreversible without asking.** Merge, split, close, group are all human calls.
- **C3 — Never write inside a generated region.**
- **C4 — A partial scan may not make a completeness claim.**
- **C5 — A clean board is reported clean.** No manufactured work.
- **C6 — The body standard is stated, not implied**, and is overridable per project.

### Upstream changes

None. No prior wave ran for this feature.

---

# DISCUSS — slice 04 (2026-08-13)

A second DISCUSS pass on the same feature, run against issue #25 after all three planned slices had
shipped. Density: lean + ask-intelligent. The 2026-08-12 wave's decisions D1–D7 are **consumed, not
re-derived**; only what slice 04 adds is recorded below.

## Wave: DISCUSS / [REF] Pre-requisites

SSOT read: `jobs.yaml` (7 jobs), `journeys/groom-issues.yaml`, `personas/robin-backlog-curator.yaml`.
`vision.md`, `project-brief.md` and `stakeholders.yaml` do not exist in this repo; no DISCOVER or
DIVERGE wave ran for this feature. No contradiction found with prior evidence — the slice is
consistent with D5 (loop pacing), D6 (no marker) and D7 (the body standard it helps a card satisfy).

## Wave: DISCUSS / [REF] Persona and JTBD

Unchanged: `robin-backlog-curator`, job `keep-a-backlog-trustworthy` (`status: validated`). The job
was **consumed rather than re-run** — a second job statement covering work an existing validated job
already owns would be the duplicate-authority defect this feature exists to detect. An *elicitation
facet* is recorded on the job in `jobs.yaml`, following the mobile-facet precedent on
`catch-ux-violations-while-building-ui`.

The facet's new force, which the original wave did not name: **a real finding with no route to
resolution is indistinguishable from one a human read and chose to leave**, because D6 stores no
marker. The board that most needs grooming produces the most durable report and the least change.

## Wave: DISCUSS / [REF] Locked decisions

- **[D8]** **Elicitation is a fourth command, not a mode of an existing one.** `/phil:groom-ask`.
  Consistent with the blast-radius split already established: this one writes bodies from dictated
  content, which is neither derivable (02) nor set-changing (03). (User, name confirmed 2026-08-13.)
- **[D9]** **The session supplies the questions; the human supplies every word of content.** No
  inference from the title, the labels, or a sibling card. The refusal in `/phil:groom-fix` is not
  relaxed — the gap was never permission to invent, it was the absence of a scribe.
- **[D10]** **One card at a time. No batch, no apply-to-all**, in any form. The content differs per
  card, so a population-scaled offer has nothing to scale over; slice 02 already measured that a
  scale-shaped offer over a small population is ceremony, and ceremony is what teaches people to
  click through a consent gate.
- **[D11]** **A partial answer is written partially.** One field given and one withheld writes the
  one given. Completing the body by inventing the missing half is the failure the whole slice is
  shaped against, and it is most tempting exactly here.
- **[D12]** **A decline leaves no trace and the finding returns**, per D6. Same accepted cost as a
  declined set-level candidate, and it is now the third place this cost is paid — worth stating once
  per surface rather than assuming the user carries it over.

## Wave: DISCUSS / [REF] Driving ports

| Port | Surface | Slice |
|---|---|---|
| `/phil:groom-ask` | Slash command — the per-card elicitation loop | 04 |

Fourth port. The DISCUSS wave planned one and the tool grants forced four; the reasoning is recorded
under *Driving ports* above. This port's grant is `mutates: true`, `Bash` scoped to issue **read and
edit** verbs only — no `create`, no `close`, no `gh api`.

## Wave: DISCUSS / [REF] Journey

SSOT: `docs/product/journeys/groom-issues.yaml`, extended rather than replaced. New step
`elicit-semantic` between `fix-mechanical` and `decide-set-level`; the journey already models each
command as a step, so a separate journey for one job and one persona would have restated the scan as
a precondition and created two authorities over one flow.

Emotional arc gains a beat: **wary → relief → control → momentum → relief(again) → confidence →
trust**. The second relief is a different feeling from the first — the first is learning the size of
the problem, this one is learning the findings have an exit.

Three error paths added, and the third is the sharp one: **the user answers one question and not the
other.** New shared artifact `elicited_body_content`, whose single source is recorded as *Robin, via
the questions asked* — never the session.

## Wave: DISCUSS / [REF] Scope assessment

**RIGHT-SIZED — 0 of 5 oversized signals fire.** One bounded context (elicitation), one shippable
outcome, one command plus three fixtures, no new abstraction, well under two weeks. `## Scope
Assessment: PASS`.

## Wave: DISCUSS / [REF] Out-of-scope

- **Inventing any content**, from any source. D9.
- **Batch or apply-to-all**, in any form. D10.
- The mechanical column (`/phil:groom-fix`) and the set-level column (`/phil:groom-set`).
- Rules 3, 4 and 5 — links, labels and chains are not what a title-only card is missing.
- **Deliberately deferred, from #25's own out-of-scope**: a bare-title card yields two findings and
  silence on rules 3–5, because those rules have no candidate to judge. The report is technically
  correct and reads as though the card were mostly fine. Whether that warrants a change to the
  reporting rules is its own question and its own card.

## Wave: DISCUSS / [REF] Wave decisions summary

### Requirements summary

- **Primary job:** unchanged — make a board trustworthy. This slice closes the semantic column's exit.
- **Feature type:** infrastructure/tooling (D1, inherited).
- **Walking skeleton:** not applicable — shipped as slice 01.

### Constraints established

- **C7 — Content is collected, never composed.** The session may structure and prompt; every word of
  the written body traces to an answer the human gave.
- **C8 — No batch.** One card per elicitation, always.
- **C9 — A partial answer is honoured partially.** Never completed by inference.

### Upstream changes

The 2026-08-12 wave's *Slices and order* table listed three slices and described the split as
complete. It is now four. Recorded here rather than by editing that table, so the original split
stays readable as what was decided at the time.

## Wave: DISCUSS / [REF] Slice 04 fold-back — the dogfood measurement (2026-08-14)

Two rules folded into `skills/groom-issues/SKILL.md` after the slice-04 dogfood, with the fixtures that
would have caught each. Route 1 per `CLAUDE.md`; plugin version 0.36.0 → 0.37.0.

**The measurement.** Scanned this repo's real board for rule 1 and rule 2 failures:

| | Cards failing |
|---|---|
| Rule 1 — no purpose stated | **0** |
| Rule 2 — no way to tell when it is done | **3** (#1, #2, #3) |

Every failing card already states a purpose and lacks only a done-condition. **The population is
partial, not empty.**

**Fold-back 1 — ask only what the scan reported missing.** The shipped text said to ask "what the card
is for, and how they will know it is done — the two things rules 1 and 2 require", which asks both
regardless of the findings. Against the only population ever observed that is ceremony on the answered
half, and it invites overwriting a purpose that passes. Fixture `30` pins it.

**Why the suite could not catch this.** Fixtures `25`-`28` each construct a card with an **empty body**
and two findings, so all four pass while the loop asks two questions. They share the assumption under
test, which is why four agreeing fixtures were not coverage. This is the third time on this feature that
the real board contradicted a constructed population — `16` and `23` are the other two — and the pattern
is now consistent enough to state as a habit: **a fixture built to a brief's expected shape tests the
brief, not the world.**

**Fold-back 2 — `REFUSE-GENERATED` belongs to `/phil:groom-ask`.** `/phil:groom-fix` refuses to write
inside a generated region; the elicitation loop was never given the equivalent, at any of the three
levels where the rule lives — the decision outcomes, the must-never-do list, or the journey's error
paths. A card can carry a full `nwave:status` block and still state no purpose, because the block is
published from the artifacts and says nothing about why the work is wanted. Fixture `31` pins it, and
distinguishes itself from `15`: there the correct content exists at the generator, here it exists
nowhere, so the remedy is a refusal that hands the answers back rather than a redirection.

This second fold-back was surfaced by the DISCUSS wave for `single-issue-per-feature`, which makes a
generated block the shape of **every** feature card rather than an occasional one. The gap was reachable
before that change and is not created by it.

### Still outstanding on slice 04

**The write path has never executed.** A by-hand exercise of the working-tree prose at 0.37.0 reached
`ASK-CONTENT` and then `DECLINE-NO-TRACE`, so AC1 and AC2 — write from the answers, attribute each field —
remain unverified. `/phil:groom-ask` cannot be run as a command until the plugin updates past 0.27.0.
**Issue 25 stays open**: the slice is authored and its read path exercised, not proven.

Two findings from that exercise, both about the skill rather than about any card:

1. ~~**`AskUserQuestion` is the wrong tool for elicitation, and the skill only implies it.**~~ Its options
   are authored by the session, so a human picking one is selecting from inventions rather than dictating
   content — exactly what *the human supplies every word* forbids.

   **REVERSED the same day.** This was correct under the design as shipped and is wrong under the
   scribe→editor amendment below: offering suggestions is now required, and `AskUserQuestion` is the apt
   tool for it, with free text as the escape hatch. Struck rather than deleted, because the claim is
   already in commit `4192385` and a reader arriving from that commit needs to find the reversal, not a
   silent absence.
2. **Nothing covers an ambiguous non-answer.** Fixtures 25-28 cover both-answered, declined, body-moved and
   partial. A reply that is neither an answer nor a decline — "ok" — has no rule and no fixture. The
   correct rule is to treat ambiguity as unanswered, ask once more, and never resolve it by composing;
   without it, the tempting move is to read assent as licence to draft. Candidate fixture 32.

Neither is folded in yet.

## Wave: DISCUSS / [REF] Slice 04 amendment — scribe to editor (2026-08-14)

Owner reversal, taken through `nw-discuss` as an amendment pass. **Design only** — the `SKILL.md` and
fixture edits are a separate authoring step with `plugin-dev` consulted, per `CLAUDE.md`'s build path.

Telemetry not emitted: `scripts/shared/telemetry.py` does not exist in this install and the wave forbids
writing JSONL directly. No Tier-2 expansion was triggered by this pass, so none is rendered.

### The instruction

1. *(additive)* The prompt must not assume familiarity with the card — present what it is, what it says,
   and which rule failed.
2. *(reversal)* Offer a suggestion or two on how to fill the gap.
3. *(reversal)* Do not take the user's words verbatim — write a clean card following the card-writing
   principles, based on their answers.

### The invariant is swapped, not dropped

**What matters is that the human can SEE what the session contributed — not that the session contributed
nothing.** Verbatim was one mechanism for that visibility. Two replace it, and together they cover more:

- **Per-field provenance**, from a fixed set: `you wrote` · `you accepted my suggestion` ·
  `you edited my suggestion` · `I rephrased your answer`. **A field written without a label is the
  defect.**
- **Answer beside written form** wherever the two differ, so a rewrite is inspectable rather than
  asserted.

This is stronger than verbatim, not weaker, because verbatim never contemplated the suggestion path at
all — a session that offered a draft and got a nod would have satisfied the old rule while producing a
body the human never composed.

### Anxiety (E) is narrowed, not abandoned

`jobs.yaml`, elicitation facet, quoted verbatim:

> (E) A tool that writes a purpose it inferred. The refusal in `phil:groom-fix` is correct and must
> survive — the gap is not permission to invent, it is a scribe. Elicitation asks the human and writes
> THEIR answer.

Its **subject changes** from *what the session may write* to *what the session may write unseen*. The
`groom-fix` refusal is untouched: that command still may not draft a purpose, because it never asks.

### Eight rules that survive unchanged

Stated explicitly, because a reversal read as general licence is how the rest of the boundary erodes:

1. Nothing is written before an answer or a decline.
2. A decline writes nothing and records nothing (D6); the finding returns next run.
3. One card per invocation. No batch, no apply-to-all.
4. Re-read immediately before writing; refuse a moved body — now handing back **both** the answers and
   any draft.
5. `REFUSE-GENERATED` — elicited prose never lands inside a generated region.
6. Ask only what the scan reported missing.
7. **A rule that passed is never rewritten.** The session may rephrase what it elicited; a purpose that
   already satisfies rule 1 is out of reach. This is the new boundary, and fixture 30's *"neither
   re-asked nor rewritten"* is where it is already pinned.
8. A partial answer stays partial. Suggesting the missing half is now permitted; **silently supplying it
   is not** — the difference is a visible, refusable offer.

### The ambiguous non-answer is now load-bearing

Recorded earlier today as candidate fixture 32, after a real dogfood reply of "ok". Under the old design
that reply was merely unanswerable. **Under this one it plausibly reads as *accept your suggestion*** — so
the tempting misreading now has a concrete thing to adopt, and adopting it would produce a body the human
never sanctioned while every visible rule appeared satisfied. The rule is required rather than tidy: treat
ambiguity as unanswered, ask once more, never resolve it by composing.

### Consequences for the authoring step

- **`commands/groom-ask.md`** — the entry point, which loads *before* the skill. **This line was missing
  from the first version of this list, and its absence is exactly why the file was missed.**
- **C7 is rewritten** from *collected, never composed* to the visibility constraint above. C8 (no batch)
  survives; C9 (partial stays partial) survives with rule 8's clarification.
- **Fixture 25 is rewritten.** Its entire subject is verbatim plus no polishing.
- **Fixture 28 amended** — partial plus a refused suggestion for the withheld half.
- **New fixtures**: a suggestion declined in favour of the human's own words; a rewrite whose
  transformation is shown; and 32, the ambiguous non-answer.
- **Fixtures 26, 27, 29, 30, 31 survive**, 27 with the widened hand-back and 30 as the pin for rule 7.
- **`WRITE-ELICITED` gains the provenance report**; an unlabelled field fails.
- The journey's `elicited_body_content` artifact stops being sourced from Robin alone.

The slice brief is now 130 lines against the ≤100 guideline, ~22 of which are the `Changed Assumptions`
section the back-propagation contract requires on top of a standard brief. Stated rather than trimmed into
inaccuracy, as with `single-issue-per-feature` slices 05 and 06.

### What the reviewer pass caught

`plugin-dev:skill-reviewer` ran over the authored result and returned **Needs Improvement**. The design was
sound and the design docs were correctly back-propagated; **the propagation into normative text was
incomplete in one file entirely and two fixtures partially.** All of the following are fixed.

**The one that would have shipped a contradiction:** `commands/groom-ask.md` still read *"It composes
nothing: every word is yours"* in its frontmatter and *"This command is a scribe, and the distinction is
the whole design"* in its body. It is the **entry point and loads before the skill**, so a session would
have read the retired rule first. A conservative resolution silently reverts the change and fails fixtures
25, 32 and 33; a liberal one ignores an explicit written prohibition in the command it was invoked as.

**The old guarantee survived 420 lines from the edit.** `SKILL.md`'s rationale for the command existing at
all still said *"the guarantee it needs is not did you consent but did you compose this"* — both halves
false under the amendment, since a suggestion exists before the human says anything. The axis (*where the
content comes from*) survives; the guarantee is now consent **plus provenance**.

**The section contradicted itself on the unit of sanction.** *"The human sanctions every word"* is not what
the `I rephrased your answer` path delivers: the session picks the words and discloses afterwards. Stated
precisely now — **the human sanctions the claim; the session may choose the words** — plus the fidelity
constraint that only fixture 25 carried: rephrasing is a tidying licence, not a modelling one. A rewrite
that changes what the card asserts is composition wearing a truthful label, and it is the one failure the
provenance rule cannot catch alone.

**`ASK-CONTENT` had no legal standalone form**, so fixtures 29 and 32 both required an outcome the grammar
forbade — and the only terminal outcome reachable was `DECLINE-NO-TRACE`, which records a refusal that did
not happen. Now stated as a terminal state, with the two-ask limit and its fall-through promoted out of
fixture 32 into the skill.

**Fixtures 28 and 30 still printed `← your answer, verbatim`** — the retired shape, which the skill now
calls the defect. Converted to `[you wrote]`, and fixture 30 gained the unlabelled-field gate failure it
lacked.

**Under-specification, all satisfiable in letter while violating intent:** the action→label mapping was
never stated (`replace` → `you wrote`) though fixture 33 penalises getting it wrong; no rule covered
accept-then-polish; the accept criterion was a closed list of three tokens, and a naming criterion would
have collapsed where only one suggestion is offered — so the criterion is now positive (*name it or restate
its text*, never a bare affirmation, even with one suggestion on the table).

**Also fixed, predating this change:** a drifted forge claim at `SKILL.md:354` asserted a comment is dropped
after a close "once the project's close workflow has run". Neither `phil:issue-board` nor `CLAUDE.md`
establishes that direction — both observed Status-first. The advice was right and the mechanism was
invented. Corrected with the observation cited to its owner.

**Left as follow-ups, not fixed here:** three unattributed restatements of `phil:issue-board` mechanics in
the `/phil:groom-set` section (two-pass seeding, `item-add` before Status, close-sets-Status), and one
genuine forge mechanic living in the wrong skill — `glab`'s `-O`/`--output` versus `-F`, which silently
returns a human-readable table. That belongs in `issue-board` and is not there.

**The structural finding worth keeping.** The reviewer's diagnosis of *why* the command file was missed: this
file states every rule three or four times — narrative, decision outcomes, must-never-do — so **every
amendment is a five-site edit with no checklist of the sites**, and this one hit three. The provenance rule
alone landed in four places with three different scopings. That is a stronger argument than the word count,
and it is not fixed by a `references/` split, which would add a fifth location. The proposal on the table is
to declare **one normative site per rule** and demote the others to an index. Not taken here — it is a
restructure, and bundling one into an amendment is the defect this repo has already recorded twice.

### Also corrected

Slice 04's **AC1 still described asking for both the purpose and the done-condition**, which this
morning's *ask only what the scan reported missing* fold-back had already superseded — the fold-back
amended the skill and the journey but not the slice brief. Fixed in the same pass. A fold-back that
updates the normative text and leaves the brief behind is how a brief becomes the stale authority.
