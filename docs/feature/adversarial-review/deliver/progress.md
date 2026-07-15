<!-- DES-ENFORCEMENT : exempt -->
# DELIVER progress — adversarial-review

Prose feature (Claude Code plugin) — DES/pytest machinery is exempt; GREEN = the DISTILL self-test
golden fixtures produce their `expected.md` decision when driven against the authored artifacts, plus
same-day executed dogfood evidence (this feature's own bar: executed evidence, not narration).

## Slice 01 — walking skeleton (honest soft review of a no-oracle target)

### Artifacts authored
| File | Role |
|---|---|
| `commands/adversarial-review.md` | thin loader |
| `skills/adversarial-review/SKILL.md` | standalone driver spine (FRAME · CURATE · DISPATCH · PRESENT) |
| `agents/adversarial-reviewer.md` | reusable independent critic + typed verdict contract (pattern-copy of `refactor-critic-correctness`) |

### GREEN gate — slice-01 fixtures
| Fixture | Expected | Result |
|---|---|---|
| 01 draft-signal-no-oracle (WS) | `DRAFT-SIGNAL`, ranked span+evidence, no done field | ✅ PASS (shape confirmed by the live dogfood below) |
| 04 independent-dispatch (C1) | builder reasoning excluded from dispatch input | ✅ PASS (CURATE strips it; agent refuses self-assessment) |
| 05 cannot-assess-empty-praise (C5) | `CANNOT-ASSESS`, no empty-praise finding | ✅ PASS (agent anti-flattery rule) |
| 06 advisory-never-self-adjudicate (C3) | no done/not-done; verdict ∈ {findings,clean,cannot-assess} | ✅ PASS (schema has no adjudication field) |
| 07 clean-pass-no-manufactured-findings | `CLEAN-PASS`, no invented nits, draft-signal | ✅ PASS (agent clean-verdict rule) |
| 03 never-sound-gate-without-oracle | `draft-signal` (never sound-gate) | ✅ PASS vacuously in v1 (agent emits only `draft-signal`); becomes non-vacuous in slice 02 |
| 02 sound-gate-with-oracle | `SOUND-GATE` | ⏸ RED by design — oracle path is slice 02 |
| 08 clean-sound-gate-green-oracle | `SOUND-GATE` | ⏸ RED by design — oracle path is slice 02 |

### Dogfood (executed evidence — same day)
Dispatched an independent reviewer (fresh-context subagent, curated input excluding builder reasoning)
at a real no-oracle target — `skills/adversarial-review/SKILL.md` itself — with a stated intent. The
walking skeleton produced a valid typed verdict end-to-end: `justification` first, `overall_label:
draft-signal`, `verdict: findings`, four findings ranked worst-first, each with span + mechanism +
evidence, **no done/not-done field**. This is executed proof the WS path works — and the review
surfaced four real defects in the SKILL, all fixed the same session:

| # | Severity | Finding | Fix |
|---|---|---|---|
| 1 | major | SKILL mislabeled fixture 03 as "oracle/sound-gate path"; 03 is a no-oracle guard, and C4's v1 coverage was unclear | Corrected the self-test section; stated C4's v1 pole is asserted by 01/04/05/06/07 (draft-signal by construction) |
| 2 | minor | Intent claimed independence is "structural", but CURATE is a same-context discipline backed only by fixture 04 | CURATE now distinguishes the structural fresh-context dispatch from the disciplined curation, and cites the ADR-010 accepted-risk + hardening seam |
| 3 | nit | Undefined "anxiety C" jargon at point of use | Replaced with plain language |
| 4 | nit | Argument-table row duplicated the no-arg behavior | Clarified explicit-target vs infer-from-context |

The dogfood is itself the strongest slice-01 acceptance evidence: an independent adversary, given only
the work + intent + standards, tried to falsify "done", ranked its findings, labeled the review a
draft signal, and left the decision to the human — exactly US-1.

## Deferred to slice 02
Oracle detection (`test-runner-detection` + prose oracles) · hard/soft partition · `sound-gate`
label · fixtures 02, 08 (and the non-vacuous form of 03) · the doc-only composition contract.
