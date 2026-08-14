---
name: rank-issues
description: Skill bundle for the phil:rank-issues command — guides a developer through ranking the issues on a board that nothing upstream already orders. Elicits goals, orders the goals by milestone due date, then orders the issues inside each goal by board position, records the reasoning in each milestone's description, and writes any dependency it discovers as a real forge link.
---

# Rank issues — turn an unsorted board into a queue

A column read top to bottom says what to pick up next. Nothing makes that true by itself: a board
that nobody ranked still renders in *some* order, and that order is indistinguishable from a chosen
one. This session makes it chosen.

**Scope.** Issues that nothing upstream already orders. Work inside an nWave slice gets its order
from `roadmap.json` — `phil:nwave-issue-board` owns that and this skill does not touch it. This is
for the residue.

**REQUIRED BACKGROUND: `phil:issue-board`.** Every forge mechanic — naming the target with `-R`,
position mutations per forge, dependency links, reading the end state — lives there. Do not guess any
of it from here.

## The two-level scheme

One flat order across a whole backlog has to be re-cut every time an issue arrives. Two levels do not.

| Level | Ordered by | Survives new arrivals? |
|---|---|---|
| Between goals | milestone **due date** | **yes** |
| Within a goal | board **position** | needs a re-rank, but only inside that one goal |

**In an nWave repo the ranked unit is the FEATURE card, not a slice.** One issue is one feature there
(`phil:nwave-issue-board`), so a feature holds one position and its slices hold none — they are rows in
its roster. **An order inherited from a board that carried slice cards must be re-derived, not adjusted**:
it ranked a unit that no longer exists, and nudging it forward preserves a sequence whose subject changed.

A new issue then costs a goal assignment and one position — not a re-cut. **A milestone is a goal**
on both forges; that mapping is settled in `phil:issue-board` and is not renegotiated here.

## The session

Five steps. Ask, then write — never write during elicitation, because a half-ranked board is worse
than an unranked one.

### 1. READ

List the unranked issues with their current column order, and say plainly that the order shown may
never have been chosen. Exclude anything already ordered upstream.

### 2. GOALS

Ask what goals these issues serve. Propose a grouping from their titles and let the user correct it —
proposing is faster than interrogating, and a wrong proposal is corrected in one word.

Keep goals few. Ten issues across eight goals is not a grouping; it is a rename. If nearly every
issue lands in its own goal, say so and offer to merge — that signal usually means the goals are
being drawn at the size of tasks rather than outcomes.

An issue may end up in no goal. Leave it unassigned rather than inventing a home; unassigned is a
visible state, and a wrong goal is not.

**Say what that costs.** An unassigned issue drops out of the between-goals level entirely: only its
position carries it, so when a new goal is added later its placement relative to that goal is
arbitrary rather than ranked. That is usually the right trade against a false grouping — but it is a
trade, and the user should hear it rather than discover it.

### 3. ORDER THE GOALS

Ask which goal comes first, and why. The *why* is the deliverable here, not a nicety — it is what
step 5 records.

Turn the order into **due dates**, spaced far enough apart to be re-ordered later without collisions
— a month is ample. Dates are a rank here, not a commitment; say that out loud, and put it in the
description too, because a due date reads as a promise to anyone who did not sit in this conversation.

**Send midday, not midnight.** GitHub stores a milestone `due_on` of `T00:00:00Z` as the *previous*
day — send `2026-09-15T00:00:00Z` and read back `2026-09-14`. `T12:00:00Z` stores the date you meant.
Observed on both milestones of a real run, and corrected by re-sending at midday. It does not break
the ranking, since every goal shifts equally, but a date read as a commitment is then a day wrong.

### 4. ORDER WITHIN EACH GOAL

For each goal, show its issues and ask for an order in one pass. Most people can simply state it.

**Fall back to pairwise only when they cannot.** Comparing two at a time surfaces preferences people
cannot articulate as a list — and if the comparisons come back intransitive (A over B, B over C, C
over A), do not average them. That pattern means the goal is mis-cut and holds work that is not
really comparable; go back to step 2.

**Watch for enablers.** "B is pointless until A lands" is not a preference, it is a dependency —
carry it to step 5 rather than silently encoding it as an order.

### 5. WRITE

In this order, so a failure part-way leaves the board honest rather than half-sorted:

1. **Milestones** — create or update one per goal, with its due date **and its description**.
2. **Assignment** — put each issue in its goal's milestone.
3. **Positions** — write the within-goal order, **top-down in one pass**. Each call anchors to a
   neighbour, so anchoring to a card not yet placed shifts everything after it, successfully and
   silently.
4. **Dependencies** — for every enabler found in step 4, write the forge link *and* a `## Chain`
   line on both issues carrying the reason.
5. **Read back** the ordered list and compare it against the intended sequence.

## Record the why, never the order

The goal's basis goes in **the milestone's description** — the page a reader of that goal already
lands on. `phil:issue-board` requires it: *"A stated guess gets corrected; an unstated one gets
followed."*

```
Milestone: Board tooling usable · due 2026-09-01
  Ranked first because it unblocks ranking for everything else, and the
  board is re-cut by hand until it lands.
```

**Never write the order itself into prose.** Position is authoritative for the order; a numbered list
in a description is a second copy of it, and the copy is the one that goes stale. Record *why this
goal ranks here*, not *which issue comes third*.

## Dependencies are not orderings

Position says A sits above B. A dependency says B **cannot start** until A lands. These are different
claims, and the board can hold both.

When step 4 surfaces one, write both halves — the forge's own link, and a `## Chain` line on each
issue carrying the reason. The mechanics are in `phil:issue-board`; the point here is that an order
which merely *encodes* a dependency has thrown the reason away. The next person sees A above B,
reads it as taste, and reorders freely.

## What will go wrong

Four failure modes, each of which reports success:

- **The order reverses on GitLab.** `move_after_id` is the inverse of GitHub's `afterId` — the
  subject moves *ahead of* the named issue on GitLab, *behind* it on GitHub. Both calls succeed.
- **A no-op reads as a success.** On GitLab, `relative_position` is never serialized; it reads `null`
  before and after a working reorder. Verify by reading the ordered list back, never that field.
- **Anchoring forward.** Placing a card relative to one you have not positioned yet moves everything
  after it. Write top-down, in one pass.
- **Re-cutting the whole board** when a single issue arrives. That is the flat order the two-level
  scheme exists to avoid; give the new issue a goal and one position.

## Known limit — deferred work has no outcome

A deliberately deferred issue — parked pending evidence, not abandoned — has no expression here. Rank
it and it sits in the queue saying "work me second"; leave it out and it falls off the board's order
entirely. Neither is right, and the column's top is an instruction, so a deferred card ranked normally
is a small lie about what is next.

Surface the choice rather than picking silently: ask whether to rank it in place or leave it out, and
say which failure each buys. A `DEFERRED` outcome that ranks an issue *within* its goal while marking
it not-next would resolve this properly; it does not exist yet.

## Boundaries

- **Grooming is a separate concern.** This ranks; it does not clarify what an issue means. A ranking
  conversation over issues whose purpose is unclear produces a confident order across misunderstood
  work. Say so if the board looks unclear, and rank anyway if the user wants to — the precondition is
  advice, not a gate.
- **Do not change issue status or close anything.** Ranking says what is next, not what is done.
- **Do not touch upstream-ordered work.**

## Extraction seam

`phil:issue-board` owns the forge mechanics; this skill owns only the session. Should a grooming
command arrive and genuinely share the elicit-then-write discipline, extract that discipline then —
with two consumers to shape it. Extracting now, on one, would be guessing at the shared part
(`ADR-008`'s rule, and the same call it made).

## Acceptance

`self-test/` holds the fixtures. Run them whenever this file, the command loader, or
`phil:issue-board`'s position or milestone sections change — this skill's correctness is partly
that skill's.
