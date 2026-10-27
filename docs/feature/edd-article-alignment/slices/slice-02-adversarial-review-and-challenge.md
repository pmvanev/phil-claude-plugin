# Slice 02 — Adversarial review and challenge before any verdict

**Goal (one sentence):** an independent adversary attacks the built work before the developer judges
it, and the developer can challenge evidence instead of only accepting or rejecting it.

Story 3 · Decisions D2 (adversarial-review row), D7.

## IN scope
- REVIEW: `phil:adversarial-review` runs over the built work against the expectations after evidence
  and before any verdict.
- The ask per expectation shows the evidence, the confirmed findings and the article's four challenge
  questions, under `skills/shared/decision-request.md`.
- Three answers: accept, reject (rebuild, then re-gather evidence), challenge (commission evidence for
  the named scenario or expectation, rebuild nothing).
- A confirmed `major` finding blocks done until fixed or waived by name.
- Fixtures: challenge commissions without a rebuild; unwaived `major` blocks done; stop over a
  standing challenge reports not done. Fixture 06 extended to the three-answer set.
- `tests/test_edd_skill.py` assertions for the review dispatch, the three answers and the block.

## OUT of scope
- An automated verdict: `phil:adversarial-review` advises, the developer decides.

## Learning hypothesis
- **Disproves** "an adversary before the verdict earns its time" if, on a real run, it confirms no
  finding and the developer asks for no challenge.
- **Confirms** it if a confirmed finding or a challenge changes at least one verdict.

## Acceptance criteria
AC3.1–AC3.4 in `feature-delta.md`.

## Dependencies
Slice 01.

## Effort estimate
≤1 day. Reference class: edd-loop slice 02's gate.

## Production data
The slice 01 dogfood intent, re-run through review.

## Dogfood moment
Challenge at least one piece of evidence on a real run the same day.
