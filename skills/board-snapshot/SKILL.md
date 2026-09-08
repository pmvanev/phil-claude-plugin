---
name: board-snapshot
description: >-
  Use when asked where an issue board stands right now rather than what is wrong with it —
  "summarise my board", "what's on the board", "where does the board stand", "what's blocked",
  "what's in flight", "what should I pick up next on the board" — on a GitHub Projects v2 board.
  Produces a bounded standing check inside a 200-word ceiling: what is blocked and what each waits
  on, what is in flight, and the next few in the board's own order. Consumes board position, never computes it.
  Reports drift and never fixes it. For what is WRONG with the cards, use phil:groom-issues
  instead; for the order itself, phil:rank-issues; for the inside of one card,
  phil:nwave-slice-status.
---

# Board snapshot — where the board stands, not what is wrong with it

A board that is in perfect shape still costs a full read. Every other command over a board answers a
different question and answers it at length. This one answers *where does it stand*, and stops.

**GitHub Projects v2 only.** GitLab is not implemented and is not stubbed: its boards express a column
as a scoped label rather than a project field, so the items query below has no counterpart there. Say so
and stop rather than approximating — a snapshot that quietly reported a label as a column would be
confidently wrong in the one place this skill exists to be trusted.

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

## The read

**One call for the board.** Status is a project field, so this is a project-items query and never
`gh issue list`, which returns no Status at all.

**Send the document with GraphQL variables, never interpolated into the query string.** An inline
`-f query='… fieldValueByName(name: "Status") …'` fails to parse on nested quotes, and a command cannot
write a temp file inside its grant. This is a shipped hazard, measured 2026-09-08, not a style preference.

**Branch on the owner's type first.** `user(login:)` errors with `Could not resolve to a User` against
an organization-owned board, and `organization(login:)` errors the same way against a personal one. There
is no form that serves both, so resolve the owner and pick — `scripts/probe-board.py` already branches
this way and is the reference.

```sh
gh api graphql -f query='{ repositoryOwner(login:"<owner>"){ __typename } }'   # User | Organization
```

Then substitute `user` or `organization` for the root field below. Everything after it is identical.

```sh
gh api graphql -f query='query($o:String!,$n:Int!,$f:String!){ user(login:$o){ projectV2(number:$n){
  items(first:100){ nodes { id content { ... on Issue { number title state url } }
    fieldValueByName(name:$f){ ... on ProjectV2ItemFieldSingleSelectValue { name } } } } } } }' \
  -f o=<owner> -F n=<project-number> -f f=Status
```

**Items arrive in board-position order and that order is authoritative.** Consume it. Never sort, never
re-rank, never infer an order from labels or dates — `phil:rank-issues` is the one surface that produces
an order, and a second producer makes neither answer trustworthy.

**Paginate rather than truncate.** A `first:100` that returns a cursor is a partial read until the next
page is fetched. See *Partial reads*.

### Blocked cards need a second, small read

The forge records that a card is blocked; the reason lives in prose. Read the `## Chain` section of each
blocked card's body and quote what it waits on.

```sh
gh issue view <n> -R <owner/repo> --json body
```

**One call per blocked card, and blocked cards are few.** Fetching every body in the main call to serve a
section that is usually empty is the cost this split avoids. **Where a blocked card carries no `## Chain`
line, say the blocker is unrecorded.** Never infer one from a title, a label or an adjacent card.

## The three sections

In this order, always: **blocked**, **in flight**, **queued**.

- **Blocked** — every card, each naming what it waits on or saying the blocker is unrecorded.
- **In flight** — every card. No cap; a board with many is telling the reader something.
- **Queued** — the first *N* in board order. **N defaults to 5** and is set by `--next N`. The board is
  `[<owner/repo>]`, defaulting to the current repo.

**Say where the order came from.** One clause is enough: the queued cards are the forge's own order, not
this command's.

## The ceiling

**200 words, counted over the whole rendered output, including the drift line and every report line.**

**Where the ceiling would break, print fewer queued cards and state how many were withheld.** Never
breach it, and never truncate in silence. **Count the withheld against the whole queued population, not
against N** — a reader who asked for five and got three needs to know whether thirty-seven are waiting or
two are. Never truncate in silence. An honest short count leaves the reader able to ask for more; a
silent one does not, and a breach makes the ceiling decorative.

Blocked and in-flight cards are never dropped to fit. Only the queued section gives ground.

## Empty sections

**Name an empty section in one leading sentence. Never print a heading with nothing under it.**

The reader needs to know the section was *checked*, and on a healthy board this is the common rendering
rather than an edge case.

## What is reported and never fixed

Three things are free to detect from the call already made. Each is **one line, printed only when it
fires**, counting against the ceiling, naming the command that resolves it.

- **Drift** — an open card sitting in Done, or a closed one outside it. Always a defect. Hand it to
  `phil:groom-issues`.
- **Uncolumned** — a card on the project with no Status. Invisible in a kanban grouped by Status, so it
  is invisible in the three sections above too. Naming it is the only thing that stops it vanishing.
- **Inflation** — a board still carrying slice cards where one card should be one feature, which inflates
  every count. Report it. **Never consolidate and never refuse to render**: consolidating is irreversible
  and belongs to `phil:groom-set`, and refusing withholds the read exactly when the board is worst.

**None of these is fixed here.** This skill holds no write, and a read that repaired what it found would
be a second grooming standard arriving by the back door.

## Partial reads

**A partial read may never make a completeness claim.** If pagination failed, the forge was unreachable,
or a page was dropped, say the read was partial and report only what was found.

This binds harder here than on a scan, because **a bounded read looks complete by construction**. Nothing
in a 200-word output tells a reader that forty cards were never fetched.

## Decision outcomes

Report exactly one terminal outcome, every run:

`SNAPSHOT-RENDERED` · `SNAPSHOT-CLIPPED` · `SNAPSHOT-PARTIAL`

**`READ-ONLY` is reported on every run**, and counts against the ceiling like everything else. It is a
claim about the calls this run made, not about the tool list.

These are reported **alongside** the terminal outcome, each only when it fires: `DRIFT` · `UNCOLUMNED` ·
`INFLATION`.

- **`SNAPSHOT-CLIPPED`** — the ceiling would have been breached, so fewer queued cards were printed. It
  must state how many were withheld. Clipping without the count is `SNAPSHOT-RENDERED` lying.
- **`SNAPSHOT-PARTIAL`** — the board was not fully read. It supersedes the other two: a clipped render
  over a partial read is partial.
- **`READ-ONLY`** asserts that every forge call this run made was a read. The `gh api graphql` grant
  accepts a mutation document and only the never-do list below forbids one, so this is a claim the run
  makes about itself — which is why it is unconditional rather than printed on a condition.

## The clauses this skill composes

Most of the output is quoted: card titles are the filer's words and pass through verbatim, and a blocked
card's reason is lifted from its `## Chain` line. **Four things are this skill's own sentences** — the
leading sentence naming empty sections, the withheld-count clause, the clause saying where the order came
from, and the line for each of drift, uncolumned and inflation.

**Those are composed, so `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` governs them.** The discriminator is
`CLAUDE.md`'s: *who composed the words, never where they sit*. Terminal-only output does not exempt a
sentence this skill wrote.

**Read it as compose well, never as compose short.** The ceiling already bounds length and is a separate
constraint; the standard bears here on active voice, positive form and putting the emphatic word last —
in clauses a reader meets on every single run, which is what makes four short sentences worth a standard
at all.

**Never apply it to a card's title.** Judging prose a human wrote is the taste-policing the board family
refuses, and quoting is what keeps this surface out of it.

## What this skill must never do

- **Write anything.** No issue edits, no labels, no comments, no Status writes. It holds no `Write` and
  no `Edit`.
- **Send a `mutation` document through `gh api graphql`.** No tool boundary backs this. The grant exists
  to read a project's items and permits a mutation as a side effect; issue `query` documents only.
- **Compute an order.** Board position is consumed. Sorting by number, age, label or title invents a
  second answer to a question another command owns.
- **Drop a card to fit the ceiling** other than from the queued section, and never without the count.
- **Claim completeness over a partial read.**
- **Fix, consolidate, or refuse to render** on account of anything it reports.
- **Infer a blocker.** No `## Chain` line means the blocker is unrecorded, and saying so is the answer.
- **Print an empty heading.**
- **Probe for the board constants.** Project id, project number and Status field are read from the target
  repo's `CLAUDE.md`, which `phil:board-setup` owns and writes. Re-deriving them here creates a second
  authority over a fact the repo already records — and this skill is triggerable with no command in play,
  so the rule belongs here rather than only in the command.
- **Judge a card's prose.** Titles are quoted verbatim; this skill reports where the board stands and
  never whether a card is well formed.

## Acceptance

`self-test/` holds the fixtures, driven by `tests/test_board_snapshot_fixtures.py`. Run them whenever
this file, the command loader, or `phil:issue-board`'s items-query sections change.

Rationale, measurements and the decisions behind these rules: `references/why-these-rules.md`.
