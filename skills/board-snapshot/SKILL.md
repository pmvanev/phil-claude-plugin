---
name: board-snapshot
description: >-
  Use when asked where an issue board stands right now rather than what is wrong with it —
  "summarise my board", "what's on the board", "where does the board stand", "what's blocked",
  "what's in flight", "what should I pick up next on the board" — on a GitHub Projects v2 board.
  Two modes: a standing check inside a 200-word ceiling, and an orientation read giving every open
  card a number, a title and a composed description of 100 words or fewer. Consumes board position,
  never computes it. Reports drift and never fixes it. For what is WRONG with the cards, use
  phil:groom-issues instead; for the order itself, phil:rank-issues; for the inside of one card,
  phil:nwave-slice-status.
---

# Board snapshot — where the board stands, not what is wrong with it

A board in perfect shape still costs a full read. Every other command over a board answers a different
question and answers it at length. This one answers *where does it stand*, and stops.

**GitHub Projects v2 only.** GitLab is not implemented and is not stubbed: its boards express a column as
a scoped label rather than a project field, so the items query below has no counterpart there. Say so and
stop rather than approximating.

**REQUIRED BACKGROUND: `phil:issue-board`.** Every forge mechanic — `-R` targeting, Status as a project
field, GraphQL over `item-list`, the board constants in a project's `CLAUDE.md` — lives there. Do not
guess any of it here.

## The routing this skill exists to win

**Keep these apart, out loud, whenever more than one could be intended.** The measured failure that
produced this skill is in `references/why-these-rules.md`.

| Question | Command |
|---|---|
| Where does the board stand? | **this one** |
| What is wrong with the cards? | `phil:groom-issues` |
| What order should these be in? | `phil:rank-issues` |
| What is happening inside one card? | `phil:nwave-slice-status` |
| What was *I* doing? | `phil:resume` |
| What did the finished thinking decide? | `phil:nwave-wave-summary` |

## The read — shared by both modes

**One call for the board.** Status is a project field, so this is a project-items query and never
`gh issue list`, which returns no Status at all.

**Branch on the owner's type first.** `user(login:)` errors with `Could not resolve to a User` against an
organization-owned board, and `organization(login:)` errors the same way against a personal one. There is
no form that serves both, so resolve the owner and pick — `${CLAUDE_PLUGIN_ROOT}/scripts/probe-board.py`
already branches this way and is the reference.

```sh
gh api graphql -f query='{ repositoryOwner(login:"<owner>"){ __typename } }'   # User | Organization
```

**Send the document with GraphQL variables, never interpolated into the query string.** An inline
`-f query='… fieldValueByName(name: "Status") …'` fails to parse on nested quotes, and a command cannot
write a temp file inside its grant. Substitute `user` or `organization` for the root field; everything
after it is identical.

```sh
gh api graphql -f query='query($o:String!,$n:Int!,$f:String!){ user(login:$o){ projectV2(number:$n){
  items(first:100){ nodes { id content { ... on Issue { number title state url } }
    fieldValueByName(name:$f){ ... on ProjectV2ItemFieldSingleSelectValue { name } } } } } } }' \
  -f o=<owner> -F n=<project-number> -f f=Status
```

**Items arrive in board-position order and that order is authoritative.** Consume it. Never sort, never
re-rank, never infer an order from labels or dates — `phil:rank-issues` is the one surface that produces
an order, and a second producer makes neither answer trustworthy.

**Read the board constants from the target repo's `CLAUDE.md`.** Never probe for them; `phil:board-setup`
owns writing them.

**Paginate rather than truncate.** A `first:100` that returns a cursor is a partial read until the next
page is fetched. See *Partial reads*.

### The project holds only what was added to it

**A `projectV2` items query returns cards, and an issue reaches the board only by an explicit
`gh project item-add`.** An open issue nobody added is invisible to the query — so a read whose whole
purpose is saying what is there would omit it in silence, which is the completeness failure *Partial
reads* forbids, arriving structurally rather than through a dropped page.

**So reconcile, in one more call**, and report the difference rather than absorbing it:

```sh
gh issue list -R <owner/repo> --state open --json number --limit 200
```

Any open issue not among the project's items is **off the board**. Report the count in one line, name
`phil:issue-board` for adding them, and add nothing.

## Mode 1 — the standing check

The default. Three sections, in this order, always: **blocked**, **in flight**, **queued**.

- **Blocked** — every card, each naming what it waits on or saying the blocker is unrecorded.
- **In flight** — every card. No cap; a board with many is telling the reader something.
- **Queued** — the first *N* in board order. **N defaults to 5** and is set by `--next N`.

**Say where the order came from.** One clause: the queued cards are the forge's own order, not this
command's.

### Blocked cards need a second, small read

The forge records that a card is blocked; the reason lives in prose. Read the `## Chain` section of each
blocked card's body and quote what it waits on.

```sh
gh issue view <n> -R <owner/repo> --json body
```

**One call per blocked card, and blocked cards are few.** **Where a blocked card carries no `## Chain`
line, say the blocker is unrecorded.** Never infer one from a title, a label or an adjacent card.

### The ceiling

**200 words, counted over the whole rendered output, including every report line.**

**Where the ceiling would break, print fewer queued cards and state how many were withheld.** Count the
withheld against the whole queued population, not against N — a reader who asked for five and got three
needs to know whether thirty-seven are waiting or two are. Never truncate in silence.

**Blocked and in-flight cards are never dropped to fit.** Only the queued section gives ground.

**When the two rules collide, the ceiling yields and the run says so.** Blocked and in-flight cards alone
can exceed 200 words on a badly stuck board. Then zero queued cards still breaches, and there is no
satisfying both — so print every blocked and in-flight card, breach the ceiling, and state that the
mandatory sections exceeded it. **Dropping a blocked card is the worse failure**, because the blocked
section is the one a reader trusts most, and a silent overrun would be worse than both.

### Empty sections

**Name an empty section in one leading sentence. Never print a heading with nothing under it.**

The reader needs to know the section was *checked*, and on a healthy board this is the common rendering
rather than an edge case.

## Mode 2 — the orientation read (`--all`)

Mode 1 answers *where does it stand*. After time away, or before ranking, the question is *what is on
this board at all* — and the answer cannot be 200 words, because the honest form of it is one row per
card.

**One row per open card: the number, the title, and a description of 100 words or fewer.**

**The bound is per row and there is no total.** Nothing is dropped to fit. A read whose purpose is saying
what is there may not omit a card, so the two modes bound themselves differently on purpose.

**`SNAPSHOT-CLIPPED` is unreachable here.** Reaching it means something was dropped, which is a defect
rather than a mode.

**Every card on the project appears, including cards in no column.** A card with no Status has no place
in mode 1's three sections and it does have a row here, marked as uncolumned. Issues that were never
added to the project are **not** rows — they are the off-board line above, because inventing a row for a
card the board does not hold would misreport the board.

**Rows follow board order.** `--next N` does nothing here; the mode has no queued section to bound.

**On a board with no open cards, say so in one sentence** — the same rule mode 1 applies to an empty
section, for the same reason.

### The description is composed, never copied

**The title is not a description.** Titles on a real board are long, internal and unreadable as a list. A
row that rewords its own title has done no work.

**Compose from the body.** The first sentence of a body is not a description either; it is the opening of
an argument, and cards routinely open with context before saying what they want.

**Say what the card is for and what would change if it were done.** Where the body leaves a real question
open, say so — an open question is often the most useful thing in a hundred words.

**Where a card body is empty or says nothing, say that.** A confident hundred words about a card that
states nothing is the worst output this mode can produce, because it is indistinguishable from a summary
of a card that said something.

### The vocabulary a description may not use

**Forbidden: a file path, a bracketed identifier, and a bare handle such as `D11`, `ADR-013` or `DDD-7`.**
Each names a record the reader has to resolve before the sentence containing it means anything.

**Permitted: card numbers — and the reason is not the obvious one.** `#34` survives not because a
description needs it (the number has its own column) but because **forbidding it only launders it.** A
composer told not to write `#34` writes *card 34*, which escapes any pattern and carries exactly the same
meaning. A rule that changes the spelling and not the content is theatre.

**Not forbidden, and unenforced rather than overlooked: wave labels, slice ids and other project-local
vocabulary.** Jargon here, ordinary domain words elsewhere, so machine-forbidding them would refuse a
stranger's board for a local reason. Avoid them; nothing checks that you did.

**Applies to descriptions only. Never to a title**, which is quoted verbatim because it is the filer's
words, and judging those is the taste-policing this family refuses.

**This rule is enforced at build time only, and has never caught anything.** Fixtures check it; no hook
sees a command's rendered output, so at run time it is prose — half enforced and half promised, and which
is which matters. Measured against twelve hand-composed descriptions, it found nothing while ten of the
twelve source bodies carried a forbidden class. It is a regression guard on a failure not yet observed,
and it is not claimed as more. The numbers are in `references/why-these-rules.md`.

## What both modes compose, and what they quote

**Quoted, never touched:** card titles, and a blocked card's reason as written in its `## Chain` line.

**Composed, and therefore governed by `${CLAUDE_PLUGIN_ROOT}/rules/writing.md`:** the sentence naming
empty sections, the withheld-count clause, the clause saying where the order came from, the drift,
uncolumned, off-board and inflation lines, and every description in mode 2.

The discriminator is `CLAUDE.md`'s: *who composed the words, never where they sit*. Terminal-only output
does not exempt a sentence this skill wrote. Read the standard as **compose well, never compose short** —
the ceilings already bound length, and the standard bears on active voice, positive form and putting the
emphatic word last.

## What is reported and never fixed

Each is **one line, printed only when it fires**, counting against mode 1's ceiling, naming the command
that resolves it.

- **Drift** — an open card sitting in Done, or a closed one outside it. Always a defect. Hand it to
  `phil:groom-issues`.
- **Uncolumned** — a card on the project with no Status.
- **Off board** — an open issue that is not on the project at all. `phil:issue-board` adds it.
- **Inflation** — a board still carrying slice cards where one card should be one feature, which inflates
  every count. **Never consolidate and never refuse to render**: consolidating is irreversible and
  belongs to `phil:groom-set`, and refusing withholds the read exactly when the board is worst.

**None of these is fixed here.** This skill holds no write, and a read that repaired what it found would
be a second grooming standard arriving by the back door.

## Partial reads

**A partial read may never make a completeness claim.** If pagination failed, the forge was unreachable,
or a page was dropped, say the read was partial and report only what was found.

This binds harder here than on a scan, because **a bounded read looks complete by construction.** Nothing
in a 200-word output tells a reader that forty cards were never fetched.

## Decision outcomes

Report exactly one terminal outcome, every run:

`SNAPSHOT-RENDERED` · `SNAPSHOT-CLIPPED` · `SNAPSHOT-PARTIAL`

**`READ-ONLY` is reported on every run** and counts against the ceiling. It asserts that every forge call
this run made was a read — the `gh api graphql` grant accepts a mutation document and only the never-do
list forbids one, so this is a claim the run makes about itself.

These are reported **alongside** the terminal outcome, each only when it fires: `DRIFT` · `UNCOLUMNED` ·
`OFF-BOARD` · `INFLATION`.

- **`SNAPSHOT-CLIPPED`** — the ceiling forced fewer queued cards. It must state how many were withheld;
  clipping without the count is `SNAPSHOT-RENDERED` lying. **Mode 1 only** — mode 2 drops nothing, so a
  clipped `--all` is a defect wearing an outcome name.
- **`SNAPSHOT-PARTIAL`** — the board was not fully read. It supersedes the other two: a clipped render
  over a partial read is partial.

## What this skill must never do

- **Write anything.** No issue edits, no labels, no comments, no Status writes. It holds no `Write` and
  no `Edit`.
- **Send a `mutation` document through `gh api graphql`.** No tool boundary backs this. Issue `query`
  documents only.
- **Compute an order.** Board position is consumed.
- **Probe for the board constants.** They are read from `CLAUDE.md`, which `phil:board-setup` owns.
  This skill is triggerable with no command in play, so the rule belongs here.
- **Claim completeness over a partial read**, or over the project's items alone while open issues sit
  off the board.
- **Fix, consolidate, or refuse to render** on account of anything it reports.
- **Infer a blocker.** No `## Chain` line means unrecorded, and saying so is the answer.
- **Print an empty heading.**
- **Breach the ceiling in silence**, or drop a blocked or in-flight card to avoid breaching it.
- **Drop a card from `--all` for any reason**, including length.
- **Reword a title into a description**, or lift the body's first sentence and call it one.
- **Write a confident description of a card that says nothing.**
- **Put a file path, a bracketed identifier or a bare handle in a description**, or spell a card number
  in longhand to dodge that rule.
- **Judge a card's prose.** Titles are quoted.

## Acceptance

`self-test/` holds the fixtures, driven by `tests/test_board_snapshot_fixtures.py`. Run them whenever this
file, the command loader, or `phil:issue-board`'s items-query sections change.

Rationale, measurements and the decisions behind these rules: `references/why-these-rules.md`.
