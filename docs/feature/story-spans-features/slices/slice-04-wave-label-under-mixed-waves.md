# Slice 04 — The wave label under mixed waves

**Goal:** Settle what one single-valued wave label says about a card holding features in three waves,
and what `Work this with:` says then — including the case where the answer is that the card is wrong.

**Stories:** S2 (know which command to run when the features are in different waves)
**Answers:** issue #36's question 3

## Learning hypothesis

**Disproves the one-label design** if a single-valued label cannot serve a multi-wave card honestly: if
the current-feature reading misleads in a state grooming does not already flag, the label has to go
multi-valued — which breaks the declaration `groom-issues` rule 4 reads — or disappear from story cards,
which takes the board's biggest cards out of wave filtering.
**Confirms**, if it passes, that the approximation degrades only where the card is already a defect.

## IN scope

- **The label rule** ([D10]): single-valued, equal to the current feature's wave, swapped never added.
  The shipped failure this preserves — four accumulated wave labels and an unreadable record while every
  command reported success — is cited, not restated from memory.
- **Non-monotonicity, stated in the skill and in the block.** The label steps backwards when the next
  feature begins. This reads as an error to anyone who has only seen feature cards, and an unexplained
  backwards step invites someone to "correct" it forwards.
- **The routing line** ([D11]): `Work this with: <command> · feature <id>`. The three shipped rules
  survive verbatim — the wave label is the source, no label means no line, no row means no line **with
  the reason stated**. A fourth is added: **no line ever names a command for the story.**
- **The two-in-flight case, as far as this slice owns it:** where the fold reports two features
  `in progress`, the label takes the first in roster order and the roster's Notes column carries
  `⚠ also in flight` on the other. **The block does not hide it and does not resolve it.** Grooming's
  finding is slice 05's.
- Fixtures: three waves, one label; a backwards step rendered with its explanation; this repo's own
  no-row case on a story card; two in flight, both visible.

## OUT scope

- The grooming finding for two-in-flight — slice 05. This slice makes the state *visible*; that one makes
  it *reported*.
- Wave columns. Settled and unchanged: the wave is never a column
  (`nwave-issue-board/SKILL.md:136-147`), and nothing here reopens it.
- A `wave: mixed` value. Rejected in the delta and not revisited.

## Acceptance criteria

1. A four-feature story spanning three waves carries exactly **one** wave label, and it is the current
   feature's. Pinned by a fixture.
2. The routing line names a command **and** the feature it applies to; a fixture pins a bare
   story-scoped command as a failure.
3. A fixture pins the backwards step as **correct output**, with the explanatory clause present. Without
   that fixture the next reader fixes the non-monotonicity and reintroduces accumulation.
4. This repo's own case still holds: a story whose current feature's wave has no routing row emits no
   line **and says the table does not cover the build path**. The shipped rule is exercised at the new
   tier, not re-derived.
5. Two features in flight render two `▶` rows and a `⚠` note; the label is not silently ambiguous.
6. `groom-issues` rule 4's single-valued declaration for `wave: *` is **untouched**. If this slice needs
   to change it, the design is wrong.

## Dogfood moment

Slice 01's card exhibits the case, but **as a reconstruction, not a live observation** — and the brief
must not claim otherwise. `single-issue-per-feature` finished past DISCUSS on a build path with **no
routing row**; `story-spans-features` sits at DISCUSS, which has one. So the current feature moving from
the first to the second takes the label from *no line* to `/nw-discuss`, which is backwards in wave
order. Position 01 was already done when the card was built, so nobody watched it happen.

**The honest dogfood is therefore the forward half:** advance `story-spans-features` out of DISCUSS and
watch the label and the routing line both change on a real card. The backwards case needs a fixture, and
saying so is the point — the predecessor's rule that a dogfood claim must name what it actually exercised.

## Why this is a slice and not a paragraph in 03

The question has a real open decision behind it and four candidates, three of which fail on shipped,
measured evidence rather than on taste. It also carries the only rule in this feature whose *correct*
behaviour looks like a bug — and a rule like that needs its own fixture and its own explanation, or it
gets helpfully undone.

## Dependencies

- Slice 03's block layout, which the label and routing lines sit above.
- Slice 02's fold, which identifies the current feature.

## Effort

~0.5-1 day. Reference class: the `Work this with:` routing line added on 2026-08-12, which was one table,
three rules and one fixture.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — two header lines and their rules, in one skill. |
| Depends on a new abstraction? | On 02's fold naming a current feature. Shipped. |
| Disproves a pre-commitment? | Yes — that one single-valued label can serve a multi-wave card. |
| Synthetic data only? | No — the backwards step is exercised on #36 for real; the three-wave case is a fixture, since no three-wave story exists here. |
| Duplicate of another slice at scale? | No. 03 owns the tables; this owns the header lines above them, which derive from a different source and fail differently. |
