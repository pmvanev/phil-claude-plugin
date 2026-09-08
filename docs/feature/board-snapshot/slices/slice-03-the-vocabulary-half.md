# Slice 03 — The vocabulary half, where card numbers survive

**Goal:** Enforce plain English on the composed descriptions — internal handles absent, card numbers
present — using the checker slice 02 extracted.

**Stories:** S3
**Answers:** issue #34's open question on where the plain-language constraint is enforced

## Learning hypothesis

**Disproves [D11] — that the two surfaces genuinely need different vocabularies — if the board read turns
out never to want a card number inside a description after all.** The numbers already sit in their own
column. If no description needs one, the split done in slice 02 bought nothing and the surfaces could
have shared one list.

**Disproves [D10]'s premise more broadly if enforcement changes no output.** The descriptions written by
hand on 2026-09-08 contained no internal handles, because a person wrote them carefully. If the check
fires zero times on real input, it is a mention rather than a mechanism — which is precisely the failure
this repo has recorded twice, committed inside the feature that cites it.

**Confirms**, if it fires, that the constraint drifts back toward the source vocabulary whenever nothing
holds it — which is the argument the adjacent card makes and cannot currently evidence.

## IN scope

- The forbidden set, declared for this surface: decision handles, wave labels, slice ids, artifact paths.
- **The permitted set, declared rather than inherited: card numbers.** [D11]. A read that cannot print
  `#34` is useless, and the same token is a measured defect in an interrupting ask.
- Enforcement over composed descriptions **only** — never over a card's title, which is a human's words
  and is quoted verbatim. This is the repo's standing discriminator: judging prose a human wrote is taste.
- **A fixture that fails without the check.** A description carrying a forbidden handle must break the
  suite. A citation shipped without one is what this repo means by a mention.
- KPI-3 measured on the live board and reported whichever way it goes.
- Version bump.

## OUT scope

- Rewriting card titles, or any prose a human wrote. Out on principle, not on cost.
- Widening the forbidden set beyond the four classes above. Anything else arrives without evidence.
- Applying this to the adjacent card's wave summaries. They will consume the checker; they are not this
  feature.
- Changing the standing check's output. Its sections are structural, not composed.

## Acceptance criteria

S3's three. The third — a fixture that fails without the check — is the one that separates this slice
from a paragraph.

## Dependencies

Slice 02, for the extracted checker and the parameterised vocabulary list.

## Effort

Half a day.

## Reference class

`decision-request-standard` — the same rule, enforced in code, measured against a real corpus before it
was trusted.

## Dogfood moment

Same day: run `--all` and count how many descriptions the check rejects on first composition. **Report
zero if it is zero.** A check that never fires is the finding.

## Taste tests

- **Ships 4+ new components?** No — one declared list and one fixture.
- **Depends on a new abstraction?** It consumes slice 02's, which is the ordering the taste test asks for.
- **Disproves a pre-commitment?** Yes, two, and one of them is this feature's own reuse decision.
- **Synthetic data only?** No — the live board, plus one deliberately bad description in the fixture.
- **Identical to another slice but for scale?** No. Slice 02 bounds length; this bounds vocabulary.

## Pre-slice SPIKE

None.
