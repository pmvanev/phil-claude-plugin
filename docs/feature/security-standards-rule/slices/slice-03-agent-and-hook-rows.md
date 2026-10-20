# Slice 03 — Agent and hook rows

**Goal.** A review of a hook or agent names prompt injection and its sinks by CWE-1427 and OWASP LLM
ids, and never demands a filter.

**Story:** US-03 · **Job:** catch-security-defects-in-review

## IN scope
- Agent rows F31–F36 from the research; the six design patterns as preferred forms.
- Do not flag: a missing prompt-injection detector.
- Fixture: two or more agent defects, one or more agent decoys.

## OUT scope
- Markdown frontmatter grants (a `harden-instructions` card).

## Learning hypothesis
Disproves "agent defects can be flagged as data-flow patterns in code" **if** the fixture's agent
defects are missed or the decoy is filed.

## Acceptance criteria
See US-03 in `feature-delta.md`.

## Dependencies
Slice 01.

## Effort / reference class
≤ 1 day.

## Production data
`hooks/decision-request/check-ask.py` reads model-composed text.
