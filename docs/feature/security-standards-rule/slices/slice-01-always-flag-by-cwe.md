# Slice 01 — Always-flag by CWE

**Goal.** `/phil:review-code` names each classic security defect by its CWE id and fix, and leaves
the known false alarms alone. *(Walking-skeleton slice.)*

**Story:** US-01 · **Job:** catch-security-defects-in-review

## IN scope
- `rules/security.md`: frontmatter, sources line, ownership paragraph, Always-flag rows F1–F30 from
  the research, Do not flag list, dated editions line.
- `skills/review-code/SKILL.md` Priority 1 names the rule and requires the CWE id.
- Self-test fixture `02-security-findings-cite-a-cwe/`: six or more seeded defects, four or more decoys.
- README Rules list; version bump.

## OUT scope
- Principles and Advisory (slice 02); agent rows (slice 03).
- Item-level ASVS ids (D4).

## Learning hypothesis
Disproves "30 rows keyed by CWE stay readable and precise enough that a reviewer flags the seeded
defects without flagging the decoys" **if** the fixture run misses a seeded defect, cites the wrong
CWE, or files any decoy.

## Acceptance criteria
See US-01 in `feature-delta.md`.

## Dependencies
- Research precursor (committed with this slice).
- D5: every CWE id opened on cwe.mitre.org first.

## Effort / reference class
≤ 1 day. Reference class: `ux-standards-rule` US-01 (a new two-tier rule from a research document).

## Production data
A dogfood run over `hooks/` and `scripts/` — six files there shell out or call a forge.
