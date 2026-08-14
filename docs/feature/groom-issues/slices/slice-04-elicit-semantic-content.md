# Slice 04 — Elicit the semantic content

Feature: groom-issues · Job: `keep-a-backlog-trustworthy` · Persona: `robin-backlog-curator`
Driving card: #25 · DISCUSS: 2026-08-13, consuming the feature's 2026-08-12 wave (D1–D7)

> **Unplanned.** The 2026-08-12 wave split this feature into three slices and all three shipped. This
> one comes from a question asked afterwards — *what does the family do with an underspecified
> issue?* — and the answer was **nothing**. It is a fourth slice, not a revision of the split.

## Goal

Give the semantic half of the standard an exit: ask the human what a card is for and how they will
know it is done, and write **their** answers into the body.

## Learning hypothesis

**Disproves that the mechanical/semantic split is a complete design.** The split says an automated
pass must never invent intent, and that is right. But if the semantic column has no route to
resolution, then a board of title-only cards produces the same report run after run, forever, and
the tool that reports it teaches people to stop running it — the failure the skill already names,
reached from the other direction. If elicitation turns out to be unusable in-session, the honest
conclusion is that grooming ends at the report and the semantic column belongs to a browser.

**Confirms** that the missing piece is a scribe rather than permission — that a session can collect
content it is forbidden to author, and that the boundary survives contact with a real card.

## IN scope

- **Elicit and write.** Ask for the purpose and the done-condition of one card; write the answers
  into the body. Every word of content comes from the human.
- **One card at a time.** No batch, no apply-to-all. The content differs every time, so a
  population-scaled offer has nothing to scale over — and slice 02 already measured that a
  scale-shaped offer over a small population is ceremony.
- **Re-read immediately before writing**, and refuse to overwrite a body that moved since the read.
  Slice 02's rule, and it binds harder here: the text at risk is prose a human wrote.
- **A partial answer is written partially.** One field given and one withheld writes the one given.
- **A decline writes nothing and records nothing** (D6). The finding returns next run.

## OUT scope

- **Inventing any content.** Not from the title, not from the labels, not from a sibling card. The
  refusal in `/phil:groom-fix` is correct and survives intact; this slice does not relax it.
- **The mechanical column** — `/phil:groom-fix` owns it.
- **Changing which cards exist** — `/phil:groom-set` owns that, and this command holds no `create`,
  no `close`, no `gh api`.
- **A batch or apply-to-all mode**, in any form.
- Rules 3, 4 and 5. Links, labels and chains are not what a title-only card is missing.

## Acceptance criteria

1. Given a card failing rules 1 and 2, when the command runs, then the user is asked what the card is
   for and how they will know it is done, and **nothing is written before both answers or a decline**.
2. Given answers, then the body is written from those answers alone, and the report states which
   field came from which answer so an invented sentence would be visible.
3. Given a decline, then no body is written, no label is set, no comment is posted, and no record of
   the offer exists anywhere — and the report says the finding will return next run.
4. Given the body moved between the scan and the write, then the write is refused, what moved is
   reported, and the elicited answers are shown so the user does not lose them.
5. Given one field answered and one withheld, then only the answered field is written.
6. Given more than one card with semantic findings, then they are offered **one at a time**, and
   there is no path to apply an answer to several.

**Production data:** this repo's real board.

## Dogfood moment

Same day, and the board supplies a target only if one exists — every current card was authored to the
standard. **If no card on the real board fails rules 1 or 2, say so and dogfood against a card
created for the purpose, labelled as synthetic.** Slice 02 measured a population of one and slice 03
a population of two declines; a slice that assumes a queue here would repeat the mistake those two
already corrected.

## Dependencies

**Slice 01** — consumes its semantic findings. Independent of 02 and 03.

## Effort and reference class

≤1 day. Reference class: `/phil:groom-fix` (slice 02) — a per-card, human-approved write loop with a
re-read gate, which is this slice minus the elicitation.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — one command, one loop, three fixtures. |
| Depends on a new abstraction? | No. Consumes slice 01's findings and slice 02's re-read rule. |
| Disproves a pre-commitment? | Yes — that the mechanical/semantic split is a complete design. |
| Synthetic data only? | Real board first; synthetic only if it holds no failing card, and labelled. |
| Duplicate of another slice at scale? | No. 02 writes derivable content; this writes dictated content. |
