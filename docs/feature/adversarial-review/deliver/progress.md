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

## Slice 02 — the hard half (oracle detection + hard/soft split + sound-gate)

### Changes
- `agents/adversarial-reviewer.md`: added the `oracle_result` input + inherit-the-oracle step;
  `kind: hard` findings cite the actual result; `overall_label` is now the mechanical rule
  (`sound-gate` iff an oracle backed the review, else `draft-signal`) with explicit over- AND
  under-claim prohibitions; examples for the failing-oracle, green-oracle, and confident-soft cases.
- `skills/adversarial-review/SKILL.md`: added the **ORACLE** step (driver detects + runs/inherits a
  code suite via `test-runner-detection` or a prose oracle — self-test/dead-link/frontmatter/length/
  citation — and passes the captured `oracle_result`; never a builder's *claim*). Scope note, C4
  line, PRESENT, safety rules, and the composition contract updated. Reviewer stays read-only
  (inherit, never re-implement — ADR-005).
- `commands/adversarial-review.md`: added `Bash` to allowed-tools (the driver runs oracles).

### GREEN gate — all 8 fixtures
| Fixture | Expected | Result |
|---|---|---|
| 02 sound-gate-with-oracle | hard finding cites real result; `sound-gate` | ✅ (agent inherit-oracle step + example; mechanism exercised by the live label logic below) |
| 03 never-sound-gate-without-oracle | `draft-signal` despite confident findings | ✅ (agent rule: no oracle → never sound-gate; confidence never flips) |
| 08 clean-sound-gate-green-oracle | clean + `sound-gate` | ✅ **live dogfood** below |
| 01/04/05/06/07 (regression) | unchanged no-oracle behavior | ✅ (no `oracle_result` → soft-only, `draft-signal`) |

### Dogfood (executed evidence — oracle path)
Ran a real deterministic prose oracle — a broken-skill-reference scan on
`skills/adversarial-review/SKILL.md` (`broken_refs=0`, GREEN) — then dispatched an independent
reviewer with that captured `oracle_result`. It returned `overall_label: "sound-gate"` (the
mechanical upgrade from a green oracle — it did **not** under-claim `draft-signal`), `verdict:
"clean"`, empty findings, and refused to manufacture nits. It independently confirmed the slice-01
fix held (it credited the SKILL for honestly conceding CURATE is a discipline, not a hard boundary).
Executed proof the hard half labels correctly. Fixture 02's hard-finding-cites-failure path is
verified by the agent's inherit-the-oracle rule + worked example (not live-dogfooded — no real
failing oracle was manufactured).

## Post-finalize dogfood — review the reviewer (the agent itself)
Drove the skill against `agents/adversarial-reviewer.md` (the reusable unit — untouched by the two
earlier SKILL dogfoods). Ran deterministic oracles (frontmatter valid · broken_refs=0 · tools
read-only) → GREEN, then dispatched an independent reviewer with that `oracle_result`. Verdict:
`overall_label: sound-gate` (correct mechanical upgrade), `verdict: findings`, no done field, 2 soft
findings ranked worst-first — both real and fixed:
- (minor) `cannot-assess` had no mechanical-label guidance and its example anchored `draft-signal`,
  admitting an accidental under-claim after a green oracle → added the both-directions label note to
  the `cannot-assess` rule.
- (nit) top-level `confidence` field was in the schema but undocumented in field rules (sibling
  `refactor-critic-correctness` documents it) → added a field rule for it.
Third dogfood, third real catch — including one it found by comparing against its own pattern-lineage
sibling. No fixture regressions (additive clarifications).

## Slice 03 — the third role (adversary → judge separation)

Prompted by a maintainer question: the tri-agent concept has three roles, but v1 merged the adversary
(RA) and judge (EA) into one reviewer. Slice 03 splits them → a true **builder → adversary → judge**
triple (ADR-012).

### Changes
- `agents/adversarial-verifier.md` (CREATE NEW) — the **judge**: receives ONE finding + target +
  intent + standards + oracle_result, but **not** the reviewer's reasoning/confidence/other findings.
  Tries to refute; defaults to `refuted` when it cannot independently confirm; may correct severity.
  Read-only.
- `skills/adversarial-review/SKILL.md` — added the **VERIFY** step (dispatch the judge per finding,
  keep confirmed, drop+count refuted, present confirmed-only). Updated scope note (the triple), the
  safety rules, PRESENT (report the refuted count), and the composition contract (the judge is a
  separate reusable unit; a host may run reviewer-alone with unverified findings, or reviewer+judge).
- Fixtures 09 (judge refutes a false positive) + 10 (judge confirms a real finding, independently).
- `acceptance.feature` +2 scenarios; ADR-012; brief.md (files + C4 container + ADR list); feature-delta.

### GREEN gate
Fixtures 09 + 10 green; 01–08 unaffected (verification is an added stage, the reviewer's behavior is
unchanged). Honesty label unchanged by verification (still oracle-mechanical).

### Dogfood (executed evidence — the judge)
Handed the judge the very finding the slice-01/agent dogfood raised ("cannot-assess has no
mechanical-label guidance") against `agents/adversarial-reviewer.md` **as it now stands (fixed)**.
Reading the real file independently (no reviewer reasoning), it returned `judgment: "refuted"`,
confidence 0.97, `basis` quoting the both-directions label sentence now present — correctly dropping a
finding that no longer holds. The full triple demonstrated end-to-end: adversary raised → builder
fixed → judge independently refuted the stale claim.

## Status: three slices delivered
All 10 self-test fixtures green (no-oracle path, oracle path, and the judge each dogfooded live with
executed evidence; the rest fixture-verified). A true builder → adversary → judge triple. Composition
contract + judge documented as separate reusable units; no existing skill edited.
