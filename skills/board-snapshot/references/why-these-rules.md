# Why these rules

Rationale and measurement for `../SKILL.md`. Nothing here is normative — the skill states the rules and
this file says where each came from. Written from the start rather than extracted later, because issue
#41 is an open card about the sibling skill that grew to 8,744 words with no `references/`.

## The routing table exists because the routing failed in front of someone

On 2026-09-08 a session was asked what summarises this board. It answered `/phil:groom-issues` — which
was correct against every description then shipped — began the scan, and was interrupted. The table
wanted was hand-composed afterwards from two raw `gh` calls.

**The output was never the problem.** The audit's report is good. It answers *what is wrong with the
cards*, and the question was *what is here*. Nothing in either description separated those, so the
default choice was the wrong one and the cost was a wasted scan.

That is why the skill leads with a routing table rather than with its own procedure. A feature that fixed
the output and left the routing untouched would pass every other measure and change nothing.

## The ceiling is per-mode, and the queued section is the only one that gives ground

The card's specification is a total ceiling. Applied naively to a board where every card is queued, 200
words buys sixteen words per card — a restated title, which is worse than no read.

Blocked and in-flight cards are never dropped because **their populations are self-limiting**. A board
with twenty blocked cards has a problem the snapshot should show, not hide. The queued section is
unbounded by nature and is the only one with a defensible stopping point, so it is the only one that
clips.

**`SNAPSHOT-CLIPPED` must carry the count** because a clip without one is indistinguishable from a board
that simply had five queued cards. The outcome name and the number are the same claim.

## Empty sections were answered by the board, not by argument

On 2026-09-08 this repo's board carried twelve open cards, **all in Todo — zero blocked, zero in flight**.
Two of the three sections were empty, and the hand-written summary opened with one sentence naming both
rather than printing two empty headings. That read correctly, and it is the reason the rule is a rule.

Note what it implies: on a healthy board the empty rendering is the **common** case, not an edge case.
The 200-word ceiling was never exercised that day, and it will rarely be exercised in practice — which is
why the fixture that breaches it matters more than any fixture drawn from the live board.

## Board order is consumed because a second producer makes both answers untrustworthy

`CLAUDE.md` establishes that GraphQL returns items in board-position order and that the order is
authoritative — the top queued card is what to work on next. `phil:rank-issues` is the surface that
*produces* that order, by eliciting goals and writing dependencies as real forge links.

A snapshot that sorted by anything would be a second opinion about priority, delivered by a command
nobody asked for one from. The rule is not efficiency; it is single authorship.

## The quoting hazard is measured, and is why the query uses variables

`gh api graphql -f query='… fieldValueByName(name: "Status") …'` fails to parse: the nested double quotes
inside a single-quoted shell argument reach the GraphQL parser malformed. Observed 2026-09-08, error
`Expected NAME, actual: (none)`.

Sending the document as `-F query=@file` works and is what the hand-run used. **A shipped command cannot
do that** — writing a temp file is outside a read-only grant, and `CLAUDE.md` forbids a path inside a
`Bash(...)` grant besides. Variables are the remaining route, and they are also the correct one.

## Blocked reasons cost a second call, deliberately

The forge records the edge; the reason lives in a `## Chain` section, which is `phil:issue-board`'s
convention and requires the body. Fetching every body in the main items call would pay for a section that
is empty on most boards most of the time.

**"Unrecorded" is a real answer.** Inferring a blocker from a title or an adjacent card would be the
bare-option-list failure one level down: a confident sentence covering an absence, indistinguishable
afterwards from a recorded one.

## Drift, uncolumned and inflation are reported because detecting them is already paid for

The single items call returns issue state and Status together, so an open card in Done, a closed one
outside it, and a card with no Status at all are all free. `CLAUDE.md` states the first as always a
defect; `phil:issue-board` states that a card never added to the project is invisible in a kanban grouped
by Status.

**They are reported and never fixed** for two reasons. Fixing needs a write this command does not hold,
and a read that repaired what it found would be a second grooming standard reached by the back door —
with none of the consent machinery `phil:groom-fix` and `phil:groom-set` exist to provide.

**Inflation is the sharpest case.** Consolidating slice cards is irreversible. Refusing to render is the
other tempting answer and is worse: it withholds the read at exactly the moment the board is in the state
that most needs reading.

## `READ-ONLY` means more here than it used to elsewhere

`phil:groom-issues` records the same downgrade: once `gh api graphql` is granted, "read-only" stops being
a property of the tool list and becomes a claim about the run. The same applies here from the first
commit, so the outcome is defined as a claim about calls actually made rather than as a restatement of
the frontmatter.

The declaration is `mutates: true` for the same reason, on the precedent set by `commands/resume.md` on
2026-08-17: an honest declaration beside a grant that permits mutation, with the intent in prose.

## The word-count fixture does not contradict the board-prose rule

`CLAUDE.md` records that `tests/test_issue_board_fixtures.py` forbids a fixture from asserting a word
count. **That rule is about the prose standard**, where the point is *compose well, never compose short*,
and a word count would turn a composition test into a brevity test.

**This ceiling is a specified feature, not a proxy for quality.** The card asks for output verifiably at
or under 200 words and for a fixture that pins it on a board large enough to breach it. Asserting the
count here is the requirement; asserting it over a composed description would be the defect. Stated
because the two look identical from a distance, and the next reader will meet the CLAUDE.md rule first.


## The vocabulary rule fired zero times, and that is recorded rather than buried

Measured 2026-09-08, against the twelve descriptions a session composed by hand before any check existed
— the only real sample this feature has:

| | |
|---|---|
| Source bodies carrying a forbidden class | **10 of 12** |
| Composed descriptions carrying one | **0 of 12** |
| Longest description | 53 words, against a 100 bound |

**The hazard upstream is real and the compression removed it every time.** Ten opportunities, ten
strips, no leaks.

What that does *not* establish is that the check is needed — but the obvious hedge is wrong, and worth
correcting. **The composer did not know the vocabulary rule: it did not exist yet.** What they knew was
that the descriptions had to be short and readable. So the zero is *stronger* evidence than it first
looks — compression alone strips handles — which argues for demoting the check further rather than for
hedging the number. What remains genuinely unestablished is generality: n is twelve, in one session,
by one composer. So the honest status is a regression guard on a failure nobody has observed — which the
skill says in as many words, because a check presented as a mechanism while having never fired is the
defect `CLAUDE.md` records twice and the one this slice's own hypothesis named.

**The same measurement inverted the card-number decision's reasoning.** [D11] justified permitting `#N`
on the grounds that a board read must print card numbers. The sample says otherwise: not one description
used `#N`, because the number has its own column — and the two cross-references were written in longhand,
as *card 20* and *card 4*.

That is the real argument, and it is stronger than the original. **Forbidding `#34` does not remove the
identifier; it renames it to `card 34`,** which no pattern catches and which means exactly the same
thing. The permission stands, on evidence, for a reason nobody had written down.


## The handle pattern was blind to this repo's own spelling

The first `BARE_HANDLE` required two or more letters before the digits — `ADR-013`, `DDD-7`, `Mandate-12`.
**This repo writes its decision handles as bare `D11`,** which matched neither that pattern nor the
bracketed one, so a description reading *"as D11 settled"* passed every rule and every check. Fixture 12's
counterexample used `DDD-7`, a shape nobody here writes, so the guard's own evidence tested the case least
likely to occur.

Widened to letters-then-digits with the hyphen optional. That admits false positives — `Python-3`,
`COVID-19`, `Section-4` — and they are asserted in `tests/test_plain_language.py` rather than left to be
found. The class is named *decision handle* and the pattern says *letters then digits*; those are not the
same thing, and the gap is tolerable only because this check is build-time, where a false positive costs a
rephrase and never a denial. **A runtime consumer must not reuse this pattern unexamined.**

## The project holds only what was added to it

A `projectV2` items query returns cards. An issue reaches the board only through an explicit
`gh project item-add`, and `CLAUDE.md` records that this very board is **not linked to its repository** —
so an issue nobody added is invisible to the query.

Without a reconciliation call, a read whose stated purpose is saying what is there omits those issues in
silence. That is the completeness failure the *Partial reads* rule already forbids, arriving structurally
rather than through a dropped page — and it is worse than a dropped page, because nothing in the output
looks incomplete. One extra `gh issue list` turns a silent omission into a reported line.

## The ceiling and the never-drop rule collide, and the ceiling yields

Both were written as absolutes. On a badly stuck board the blocked and in-flight sections alone exceed 200
words, and then zero queued cards still breaches — so there is no satisfying both, and a skill stating two
absolutes with no tiebreak has no answer at the one point where the answer matters.

**The ceiling yields and the run says so.** Dropping a blocked card is the worse failure, because the
blocked section is the one a reader trusts most; a silent overrun is worse than either.

Fixture 01 asserted the unsatisfiable corner before this was settled: its `situation` said the mandatory
sections consumed *most* of the budget while its stated purpose said they *exceeded* it, and its guard
demanded both a 200-word output and every mandatory card. No run could have passed it. The two cases are
now fixtures 01 and 13, and the driver checks each is sized for its own.
