# Slice 03 — Wave columns and the blocked question

**Goal:** Put both column families on one board, and settle what happens to a card that is blocked
while sitting in a wave column.

**Stories:** S1 (the column half of "understand in seconds")

## Learning hypothesis

**Disproves** the one-board design if two column families cannot share one Status enum without the
board becoming illegible — in which case the answer is two boards, or wave-as-label after all, and
[D3] was the wrong reversal.
**Confirms**, if it holds, that a mixed board serves both nWave features and ordinary stories.

## The question this slice exists to answer

A blocked card must leave its wave column, because blocked is a column and a card holds one position.
The moment it does, the board stops showing which wave the feature is in. Three candidate resolutions,
to be decided against the rendered board rather than in prose:

1. **The wave label carries it** ([D4]) — the card sits in `blocked`, and its `wave: deliver` label
   says where it will return to. Cheapest; relies on a label being read, which is exactly what the
   wave-as-column reversal was meant to stop relying on.
2. **Blocked is not a column** — it is a label or a forge dependency link, and the card stays in its
   wave. Keeps the wave visible; loses the at-a-glance "what is stuck" read that a column gives.
3. **Blocked is a column and the wave is restated in the block** — the generated projection already
   carries a `Wave:` line, so the information is never actually lost, only moved off the board surface.

Option 3 is the current lean, because the block exists either way and is generated rather than typed.
Record the decision with the reasoning; do not let it be settled by whichever was implemented first.

## IN scope

- Wave columns on user project 3: `discover · diverge · discuss · design · devops · distill · deliver`,
  plus the generic family `to do · in progress · blocked · done`, in one Status field.
- The **feature-level fold** in `phil:nwave-slice-status` ([D10]): no slice started → to do; any
  started, not all done → in progress; all done → done; current slice blocked → blocked. This is a new
  derivation and it lands with its owner, not here.
- Resolution of the blocked question, written into `nwave-issue-board` with the reasoning.
- A fixture pinning the fold — including the case that motivated it: **five of six slices done and the
  sixth not started must not render as `to do`**, because that reports near-finished work as untouched.

## OUT scope

- Non-nWave column semantics beyond the generic four.
- Automating the column write on a wave change. Refresh happens at boundaries, as it already does.
- Any per-step column movement.

## Acceptance criteria

1. Both families exist in one Status field and the board is legible with cards in both.
2. The fold is implemented in `nwave-slice-status` and **not** duplicated in `nwave-issue-board`.
3. The five-of-six fixture passes: the card renders `in progress`, not `to do`.
4. The blocked decision is recorded with its alternatives, in the skill, not only in this brief.
5. `unknown` still publishes as `unknown` — the fold must not launder a missing artifact into a
   confident column.

## Dependencies

Slice 02 landed (the mapping asserts feature-as-card, so a column per feature means something).

## Effort

~4-6 hours: board configuration is minutes, the fold plus its fixture is the work, and the blocked
decision needs the rendered board in front of it.

Reference class: the wave-columns-vs-label decision of 2026-08-10, which was reversed mid-session once
someone looked at what the board would actually hold. This slice is that same decision re-opened on a
corrected premise, so it deserves the same "look at it before deciding" treatment.

## Result — 2026-08-14

**Hypothesis resolved by dropping its subject.** The slice asked whether two column families could share
one Status enum. The owner's answer: **there is only one family.** Wave columns are dropped — not deferred —
because a board carries non-nWave work and seven wave columns are noise to everyone filing it. So the enum
question never arises, and [D3] is reversed before implementation.

**The reversal's lesson is bigger than the slice.** It upholds the 2026-08-10 decision *after* [D2] refuted
that decision's stated reason. The decision was right for a reason nobody wrote down. **Refuting a recorded
rationale does not refute the ruling it was offered for.** Recorded in `feature-delta.md` under [D3].

### What landed

1. **The feature-level fold, with its owner** — `phil:nwave-slice-status`, plus fixture 13. AC2 met, and it
   became load-bearing rather than incidental: with the wave off the columns, **the fold is what the columns
   hold.**
2. **`Blocked` added to the real board**, option `39094273`, RED. Status went 3 → 4 options, not 3 → 11.
   Option 3 chosen for the blocked question: blocked is a column, the wave is restated in the block. Its
   *reason* changed with the wave-column drop — the card is not leaving a wave column, because there never
   was one; the block is simply the only place the wave appears.
3. **A near-miss worth recording.** `updateProjectV2Field`'s `singleSelectOptions` is a **full replacement**,
   and the option `id` is documented as *optional — include this to preserve the option*. Omitting the three
   existing ids would have dropped `Todo`, `In Progress` and `Done` **and every card's assignment to them**
   — 25 cards silently destatused by a call that reports success. Read back after: 26 items, 17 Done, 9
   Todo, **zero without a status.** This belongs in `phil:issue-board` as a forge mechanic; noted here and
   not yet folded there.
4. **Fixture 18 — `unknown` and `deferred` write no column.** The fold returns six states; the board has
   four. The two with no column must never be coerced, and `Todo` is the tempting coercion because a card
   with an unrecorded feature is usually *already* sitting in it. `Todo` asserts nobody has started;
   `unknown` asserts nobody has checked. Re-asserting the value the card already had is still asserting it.

### Not done

**AC4's three recorded candidates are moot rather than weighed.** The brief required the blocked decision be
made against a rendered board with its alternatives recorded. Two of the three assumed wave columns existed;
with those gone the decision collapsed to "add a Blocked column or don't", and the owner chose to add it.
The alternatives are recorded in `feature-delta.md` under *Alternatives considered*; nothing was decided by
implementation order this time.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — board configuration, one derivation in an existing skill, one fixture. |
| Depends on a new abstraction? | The feature-level fold is new, and it ships **here**, in the slice that first needs a column state — not assumed by an earlier one. |
| Disproves a pre-commitment? | Yes — the one-board design, and behind it [D3]'s reversal of the 2026-08-10 wave-as-label decision. |
| Synthetic data only? | No. The five-of-six fixture is constructed, but the column decision is made against the real board with real cards in it — including, deliberately, the mixed old/new shapes during the migration transient. |
| Duplicate of another slice at scale? | No. 02 settles what a card *is*; this settles where it *sits*. |
