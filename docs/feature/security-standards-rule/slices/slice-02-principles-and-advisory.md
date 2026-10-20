# Slice 02 — Principles and Advisory

**Goal.** The rule carries the half no diff can check — the design principles and the questions a
reviewer raises — labelled so neither borrows the other's authority.

**Story:** US-02 · **Job:** catch-security-defects-in-review

## IN scope
- Principles: Saltzer and Schroeder with Smith's triage; *Secure by Design*; Shostack's four
  questions and trust boundaries; Kohnfelder; *Building Secure and Reliable Systems*; Thompson.
- Advisory list, including the new-trust-boundary and new-dependency questions.
- Checklist, Anti-Patterns, Mantra, and the Sources section (D11).
- `review-code` raises Advisory items as author-decided findings.

## OUT scope
- Threat-modelling this repo; SDL, SAMM and BSIMM beyond one line.

## Learning hypothesis
Disproves "principles can sit beside an always-flag table without the reviewer flagging them as
defects" **if** a review files a principle as a Priority 1 item on the fixture.

## Acceptance criteria
See US-02 in `feature-delta.md`.

## Dependencies
Slice 01.

## Effort / reference class
≤ 1 day. Reference class: `clean-craftsmanship.md` (a rule split on checkability).
