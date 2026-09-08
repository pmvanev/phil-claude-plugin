# Feature Delta — board-snapshot

Forge: issue #34 · Wave: DISCUSS ✓ (2026-09-08)
Density: lean + ask-intelligent (`~/.nwave/global-config.json`; the resolver script is absent from this
install, so the documented cascade default was applied rather than computed — stated rather than implied)

**Build path:** DISCUSS here, then `plugin-dev:command-development` before the command file is written
and `plugin-dev:plugin-validator` after. Not DESIGN/DISTILL/DELIVER — one command over an existing
skill, and this repo settled twice that skills are authored rather than waved.

**Provoked by falling into the gap, not by planning to fill it.** On 2026-09-08 a session was asked what
summarises this board, answered `/phil:groom-issues`, and was interrupted mid-scan. The table actually
wanted was then hand-composed from two `gh` calls. Every measurement below comes from that run, and it is
recorded on the card at issue #34's comment thread.

---

## Wave: DISCUSS / [REF] Persona ID

**`robin-backlog-curator`, EXTENDED with a fourth facet — no new persona.**

Robin already holds the goal *"trust that every card says what it means, without reading all of them
again."* This feature acts on the second half of that sentence, which no shipped surface has ever
addressed.

**A new "returning reader" persona was considered and rejected**, on the precedent this file already set
twice. The board-prose feature rejected a "reader of machine-written prose" because Robin reads prose that
**is** the job's output rather than an ask that interrupts — and that is exactly this case. The contrast
is `ari-interrupted-decider`, which earned a new persona because its position (holding a question, without
the asker's context) is orthogonal to every domain. Here the role is identical and only the question moved,
from *does this card mean what it says* to *where does the whole board stand*.

## Wave: DISCUSS / [REF] JTBD one-liner

**New job: `orient-on-a-board-without-reading-it`.**

> When I come back to a board I own and need to know where it stands before deciding anything, I want a
> read short enough to finish in one pass and plain enough to act on, so I can pick up work without
> either reading forty cards or guessing.

**Not a facet of `keep-a-backlog-trustworthy`.** That job is about the board *meaning what it says*; a
perfectly groomed board still costs twenty minutes to read. The precedent for same-persona-new-job is
`know-a-boards-hazards-before-contact`, registered against Robin for the same reason: the persona is
unchanged and the outcome is different.

## Wave: DISCUSS / [REF] Locked decisions

| # | Decision | Verdict |
|---|---|---|
| D1 | **Both reads ship behind one command.** The standing check is the default; the per-card table is a flag | **Locked** — user, 2026-09-08. The card specified only the standing check; the session wanted only the table. Neither alone is the job |
| D2 | Robin is extended; no new persona | **Locked** — precedent above |
| D3 | New job, not a facet of the grooming job | **Locked** — different outcome, same persona |
| D4 | **The ceiling is per-mode, not global.** The standing check is bounded in total; the per-card table is bounded per card and unbounded in total | **Locked**. A total bound on the table would silently drop cards, which is the one failure a board read may not have |
| D5 | **Empty sections are named in one leading sentence, never printed as empty headings** | **Locked** — answered empirically 2026-09-08. The reader needs to know the section was checked, not to look at it |
| D6 | **N defaults to 5 and is an argument.** Where the ceiling would break, print fewer and say how many were withheld | **Locked**. Breaching the ceiling and truncating silently are both worse than an honest count |
| D7 | **The drift check ships as one line, only when it fires, and it counts against the ceiling** | **Locked**. An open card in Done is always a defect and the same call already returns both halves. A line exempt from the budget would be the budget leaking |
| D8 | **Slice-card inflation is reported, never consolidated and never refused** | **Locked**. Consolidating is irreversible and belongs to `/phil:groom-set`; refusing makes the read unavailable exactly when the board is worst |
| D9 | `mutates: true`, with read-only intent in prose | **Locked** by the card, and by the `phil:resume` precedent of 2026-08-17 |
| D10 | **The plain-language rule is extracted into a shared checker**, and the word ceiling is separated from the vocabulary list first | **Locked** — user, 2026-09-08. Three surfaces now want it and one already enforces it |
| D11 | **Card numbers are permitted on this surface and stay forbidden in an ask** | **Locked**, and it is the reason D10 needs the split. A board read that cannot print `#34` is useless; an interrupting question that prints it is the measured defect |
| D12 | **The extraction lands as a precursor commit inside a value-bearing slice, not as a slice of its own** | **Locked**. A slice carrying only infrastructure is a structural failure under this wave's own composition gate, and by slice 02 there are two live call sites to design against rather than one |
| D13 | **`rules/writing.md` applies to this command's composed output, from slice 01** | **Locked, and it contradicts a sibling.** `CLAUDE.md`'s discriminator is *who composed the words, never where they sit*; `groom-issues` excludes itself because its output is terminal-only. Both cannot be the rule. Recorded below as a finding rather than resolved here. **Scoped 2026-09-08 after `plugin-dev:skill-reviewer` found the shipped command reversing it:** the standard reaches the four clause types the skill composes — the empty-section sentence, the withheld count, the order-provenance clause, and the drift/uncolumned/inflation lines — and never a card title, which is quoted. It was tempting to defer the whole decision to slice 02's descriptions; that would have been true of the bulk and false of slice 01 |
| D14 | Command name `/phil:board-snapshot` | **Locked**, weakly. `board-status` collides with the project's Status field; `board` is too vague to win the routing contest that opened this feature |
| D15 | **A new skill, not a fold into `phil:issue-board`** | **Locked** — 2026-09-08, and the card asked DISCUSS to settle it rather than authoring. Measured: `issue-board` is **7,173 words with no `references/`**, already 1.4x the authoring maximum that issue #41 is an open card about in its sibling. Folding a second subject in worsens a defect this board has already filed. It is also the wrong home by subject — that skill covers how to MANIPULATE a forge, and this is how to COMPOSE a bounded read. The family pattern is a skill per subject with commands over it, which `groom-issues` and `session-handoff` both follow |

## Wave: DISCUSS / [REF] What the provoking session measured

Every number here is from 2026-09-08 against this board, at plugin 0.86.0.

- **The routing failure precedes the output.** Asked what summarises the board, the honest answer was the
  grooming audit — and it was wrong, and it was interrupted. Nothing in either description separates
  *what is broken* from *what is here*.
- **Twelve open cards, all in Todo. Zero blocked, zero in flight.** So two of the card's three sections
  were empty, and the 200-word budget was never exercised. Enforced against twelve Todo cards it would
  have bought sixteen words each, which is a restated title.
- **Descriptions were composed from bodies of 400 to 6,500 words.** Compression is the deliverable, not
  a side effect of one.
- **Status needs a second query against the project items.** `gh issue list` returns none. Board-position
  order arrives free and unsorted from that same call.
- **`gh api graphql -f query='…'` failed to parse nested quotes** in a `fieldValueByName(name: "Status")`
  selection; `-F query=@file` worked. A shipped command cannot write a temp file inside its grant, so the
  document must use GraphQL variables. Not previously recorded anywhere.

## Wave: DISCUSS / [REF] Scope assessment

**PASS — 0 of 5 oversized signals.** Four stories, one bounded context, one driving port, under two weeks.
The near-miss is D10: the shared checker touches a shipped hook with its own tests, which is the only part
of this feature that can break something already working. It is contained by D12 — the extraction lands
beside a live second consumer, and the hook's own suite is the guard.

## Wave: DISCUSS / [REF] Slices and order

| # | Slice | Answers |
|---|---|---|
| 01 | The standing check — blocked, in flight, next N, inside the ceiling | Is the bounded read useful at all on a real board? |
| 02 | The per-card table, with the shared checker extracted as its precursor | Can one command carry both reads, and is anything genuinely shared? |
| 03 | The vocabulary half — internal codes stripped, card numbers kept | Does enforcing plain language change the output, or was it already there? |

**Ordered by learning leverage, and slice 01 exists to be able to fail.** This board has nothing blocked
and nothing in flight, so the standing check renders almost empty here. If that reads as useless rather
than as reassuring, the card's own specification is wrong and slice 02 becomes the whole feature. Finding
that out costs one slice.

**The abstraction is deliberately not first.** The carpaccio taste test says ship an abstraction first
when every slice depends on it — and slices 01 and 03 do not. Extracting the checker in slice 02, against
two live call sites plus the hook, is empirical design; extracting it in slice 01 against one would be
speculation about what the second consumer needs.

## Wave: DISCUSS / [REF] WS strategy

**Strategy B — the first slice is the walking skeleton.** Slice 01 runs end to end: real forge call, real
composition, real ceiling, rendered to a terminal. Nothing is stubbed, because the only integration
point is a `gh` call this session has already made by hand.

## Wave: DISCUSS / [REF] Driving ports

- **`/phil:board-snapshot`** — the standing check. The only port slice 01 needs.
- **`/phil:board-snapshot --all`** — the per-card table. Slice 02.
- **`/phil:board-snapshot [owner/repo]`** — the argument the sibling board commands already take.

No HTTP surface. The knowledge lands in a **new skill**, per [D15].

## Wave: DISCUSS / [REF] Journey

`docs/product/journeys/board-snapshot.yaml`. Arc: **avoidant → oriented → decided**.

Opening on `avoidant` rather than `uncertain` is deliberate and is what the provoking session showed.
Robin does not arrive doubting the board; Robin arrives having stopped asking it, because every existing
answer costs a full read. The failure mode this feature acts on is **a board that is fine and goes
unread**.

## Wave: DISCUSS / [REF] User stories

### S1 — See where the board stands before deciding anything

**As** Robin, **I want** one command that says what is blocked, what is in flight and what is next,
**so that** I can pick up work without reading the board.

`job_id: orient-on-a-board-without-reading-it`

### Elevator Pitch
Before: no way to ask the board where it stands; the only short answer is one a person writes by hand.
After: run `/phil:board-snapshot` → sees three sections, at or under 200 words, ending with the next five queued in board order.
Decision enabled: which card to open, without opening any.

**AC**
1. Output is at or under 200 words, counted on the rendered text, on a board carrying at least one
   blocked card, one in flight and five queued.
2. The queued section is the first N in the order the forge returned, and the output says that is where
   the order came from.
3. Every blocked card names what it waits on, or says plainly that the blocker is unrecorded.
4. Where a section is empty, one leading sentence names it as empty and no heading is printed for it.
5. Where the ceiling would be breached, fewer queued cards are printed and the count withheld is stated.

### S2 — Read the whole board in language I can scan

**As** Robin, **I want** every open card as a number, a title and a short plain-English description,
**so that** I can re-orient after time away without opening forty cards.

`job_id: orient-on-a-board-without-reading-it`

### Elevator Pitch
Before: the titles are unreadable as a list, and the bodies run from 400 to 6,500 words.
After: run `/phil:board-snapshot --all` → sees one row per open card: number, title, and a description of 100 words or fewer.
Decision enabled: which of forty cards is worth opening.

**AC**
1. Every open card appears. Nothing is dropped to fit a budget.
2. No description exceeds 100 words, measured per row.
3. Descriptions are composed from the card body, not copied from the title.
4. Rows appear in board order, and cards outside any column are named as such rather than omitted.

### S3 — Get a read with the internal codes taken out

**As** Robin, **I want** the descriptions written without the plugin's internal vocabulary,
**so that** I can read them without first resolving what each handle refers to.

`job_id: orient-on-a-board-without-reading-it`

### Elevator Pitch
Before: a card's own title reads `nwave-issue-board is 8,744 words with no references/`, which tells a reader nothing.
After: run `/phil:board-snapshot --all` → sees descriptions with wave labels, slice ids, decision numbers and artifact paths absent, and card numbers present.
Decision enabled: whether a card is yours to act on, from the description alone.

**AC**
1. No description contains a decision handle, a wave label, a slice id or an artifact path.
2. Card numbers **are** present — this surface requires them, and the check must permit them.
3. A fixture proves the check fires: a description containing a forbidden handle fails it.

### S4 — Reach the shared checker from both surfaces `@infrastructure`

**As** a maintainer, **I want** the word ceiling separated from the forbidden-vocabulary list,
**so that** a surface can take the ceiling without inheriting a rule that forbids what it must print.

`job_id: orient-on-a-board-without-reading-it`

**Paired into slice 02 as a precursor commit, per D12.** It ships no user-visible output of its own and
therefore may not be a slice.

**AC**
1. The existing decision-request hook's behaviour is byte-unchanged, proven by its own suite.
2. The word counter has at least two call sites after slice 02.
3. The vocabulary list is parameterised, and the board surface's permitted-identifier set is declared
   rather than inherited.

## Wave: DISCUSS / [REF] Outcome KPIs

| # | KPI | Target | Method |
|---|---|---|---|
| KPI-1 | Standing-check output, on a board with ≥1 blocked, ≥1 in flight, ≥5 queued | **≤ 200 words** | `wc -w` on the rendered fixture output. A board large enough to breach it, per the card |
| KPI-2 | Longest description in the per-card table | **≤ 100 words** | `wc -w` per row, on this repo's live board |
| KPI-3 | Internal handles in the per-card output | **0**, card numbers excluded | The extracted checker, run over the rendered output |
| KPI-4 | Call sites of the shared word counter after slice 02 | **≥ 2** | `grep` |
| KPI-5 | Decision-request hook behaviour after the extraction | **byte-unchanged** | `tests/` for that hook, re-run |
| KPI-6 | Asked *what summarises my board*, the command chosen is this one | **1 of 1 trials, recorded either way** | One dogfood run, n=1, stated as n=1 |

**KPI-6 is honest rather than useful, and is kept for that reason.** A single trial proves nothing. It is
recorded because the routing failure is what opened this feature, and a feature that fixes the output
while leaving the routing untouched would report success against KPI-1 through KPI-5 and change nothing.

**KPI-1 can fail the feature.** If the standing check cannot fit a real board inside 200 words, D1's
default mode is wrong and the flag should be inverted.

## Wave: DISCUSS / [REF] Definition of Ready

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | Persona identified | ✓ | `robin-backlog-curator`, extended; the rejected new-persona alternative and its precedent are stated |
| 2 | Job traceability | ✓ | New job `orient-on-a-board-without-reading-it`; every story carries it |
| 3 | Journey mapped | ✓ | `journeys/board-snapshot.yaml`, arc upward, error paths carrying the empty-board and ceiling-breach costs |
| 4 | Stories with elevator pitches | ✓ | S1–S3 name a real invocable entry point; S4 marked `@infrastructure` and paired into slice 02 |
| 5 | ACs testable | ✓ | Every AC is a count, a presence check or a rendered-output comparison |
| 6 | Scope assessed | ✓ | PASS on 0 of 5 signals; the near-miss and its containment recorded |
| 7 | Slice briefs exist | ✓ | Three briefs under `slices/`, each with a learning hypothesis, IN/OUT scope and a dogfood moment |
| 8 | Outcome KPIs numeric | ✓ | KPI-1..6, each with a target and a method; KPI-1 able to fail the feature |
| 9 | Out-of-scope explicit | ✓ | Below |
| 10 | Domain examples with real data | ✓ | This board's twelve live cards, the two `gh` calls that read them, and the quoting failure — all from 2026-09-08. No invented fixture |

**Self-graded.** Stated so a ticked table is not mistaken for an external gate.

## Wave: DISCUSS / [REF] Out-of-scope

- **Ranking.** The order comes from the forge and is consumed, never computed. `phil:rank-issues` owns it.
- **Fixing anything the read reveals.** Drift is reported in one line and handed to the audit. D7, D8.
- **Consolidating slice cards.** D8. Irreversible, and another command's.
- **Reading inside a card.** Step-level state belongs to `phil:nwave-slice-status`.
- **Writing to the forge.** D9 declares the grant honestly and the intent lives in prose.
- **Changing what the decision-request hook enforces.** The extraction preserves behaviour; KPI-5 is the guard.
- **A second grooming standard.** This command reports where the board stands, never whether it is well formed.

## Wave: DISCUSS / [REF] Two findings outside this feature

Recorded here because both were produced by this wave and neither belongs to it.

1. **The sibling audit's description does not push readers away.** Asked what summarises the board, a
   session correctly chose `/phil:groom-issues` and was correctly interrupted. That command may owe one
   sentence naming what it is not. A route-1 fold into its own file, not this feature's work.
2. **D13's contradiction is real and is unresolved.** `CLAUDE.md` says the discriminator for the prose
   standard is *who composed the words, never where they sit*. `groom-issues` excludes its own output
   because it is terminal-only. Both are written down, they disagree, and this feature had to pick one.
   That is a route-2 finding — it changes what the repo does — and it needs a mechanism, not a paragraph.

## Wave: DISCUSS / [REF] Pre-requisites

- `hooks/decision-request/check-ask.py` exists with its own tests — verified 2026-09-08.
- `gh auth` carries the `project` scope, and the board constants in `CLAUDE.md` are current.
- **No blocking dependency on issues #39 or #42.** #39 wants the same bounded plain-English read one
  level down and will consume whatever slice 02 extracts; #42 covers the missing suite drivers that this
  feature's fixtures will need if they are to be a gate rather than a claim. Both are adjacent. Neither
  blocks, and neither is blocked.

## Wave: DISCUSS / [REF] Wave decisions summary

### Requirements summary
Robin owns a board and has stopped asking it where it stands, because every answer costs a full read. One
command gives two bounded reads: a 200-word standing check by default, and a per-card table on request.
Both are composed, not copied, and both are enforced by a checker shared with the surface that already
has one.

### Constraints established
- Status is a project field, so the read is a project-items query and never `gh issue list`.
- The GraphQL document must use variables; interpolated quotes fail to parse and no temp file is available.
- Board-position order is authoritative and arrives unsorted from the same call.
- The grant permits a mutation, so the declaration is `mutates: true` and the intent is prose.
- Card numbers must be printable on this surface and must stay forbidden in an interrupting ask.

### Upstream changes
None. No DISCOVER or DIVERGE wave ran for this feature, and no prior wave asserted anything this
contradicts.
