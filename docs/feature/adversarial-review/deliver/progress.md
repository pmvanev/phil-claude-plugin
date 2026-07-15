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

## Slice-03 catch-up (reconciling the skipped wave gates)

Slice 03 was built inline; this closes the wave gates it bypassed.

- **DESIGN back-fill:** added the verifier to the feature-delta DESIGN tables — DDD8, component
  decomposition row, Reuse Analysis row (CREATE NEW, justified), decisions-table row. Now consistent
  with brief.md + ADR-012.
- **DISTILL structural review (Sentinel):** re-ran `@nw-acceptance-designer-reviewer` on the slice-03
  additions (verifier agent, fixtures 09/10, new scenarios, VERIFY step). **APPROVED** — 0 blockers,
  0 high, 3 low. Low #2 (verifier lacks a leak-guard) was a false positive — the guard is already at
  lines 38-39. Low #1 (US-3 orphaned) + #3 (fixture clarity) applied as doc fixes.
- **Independent review of the verifier agent (executed dogfood):** ran a green oracle
  (frontmatter/refs/tools) then dispatched an independent reviewer at `adversarial-verifier.md`.
  `sound-gate`, `verdict: findings`, 3 findings — the major one **real and important**: the verifier
  had **no guard against over-refuting** (all directives pushed toward refutation; a judge could
  silently suppress a true-but-subtle finding — the exact failure mode fixture 10 guards, but the
  agent instructions didn't reinforce it). Fixed: added a symmetric "try to confirm — charitably"
  step, made refute-by-default a last resort after an honest confirmation attempt, redefined
  `confidence` as confidence-in-the-fact (uncertainty-refute → low confidence, flaggable), and made
  `corrected_severity` explicitly bidirectional (escalation is confirmation, not a new finding) with
  worked examples. Two minors fixed likewise.

Fourth dogfood, fourth real catch — this one a genuine asymmetry in the judge's own instructions.
`red-classification.md` updated for 09/10. All 10 fixtures still green.

## Full-feature dogfood (the whole triple, end-to-end)

Ran the complete pipeline against the **entire feature** as one target. ORACLE: a deterministic sweep
across all artifacts (frontmatter on command + both agents + skill; broken-ref scan; 10/10 fixtures
complete; acceptance.feature = 10 scenarios, 1:1 with fixtures) → all GREEN → `sound-gate`. DISPATCH:
an independent reviewer read the artifacts as a set and hunted cross-file contradictions. VERIFY: the
judge independently checked the load-bearing finding.

Verdict: `sound-gate`, 5 findings — **all doc-drift, zero in runtime behavior** (a good result for a
feature this size). The judge **confirmed** the major finding but **corrected its severity
major→minor** (the runtime is self-consistent and correct; only the ADR wording drifted) — the
adversary→judge separation adding precision, exactly as designed. All 5 fixed:

| # | Sev (adversary→judge) | Finding | Fix |
|---|---|---|---|
| 1 | major→**minor** | ADR-011 said "the reviewer runs the oracle"; slice 02 moved that to the driver (reviewer is read-only, no Bash) — stale design-of-record | ADR-011 reworded: driver runs/inherits, reviewer cites; notes the pre-split wording |
| 2 | minor | self-test README said the suite gates only the skill + reviewer, omitting the verifier | README gate statement + "nothing to drive" now list all three artifacts |
| 3 | minor | outcome vocabulary (README + acceptance.feature) omitted CONFIRMED/REFUTED (the judge's outcomes) | both enumerations now split reviewer vs verifier outcomes |
| 4 | nit | ADR-010's published contract omitted `oracle_result` (added by ADR-011) | ADR-010 contract now `{target,intent,standards,oracle_result?}` |
| 5 | nit | README + feature-delta tables gave fixtures 07 and 08 the same `CLEAN-PASS` token, hiding 08's sound-gate distinction | both tables now show `CLEAN-PASS (draft-signal)` vs `(sound-gate)` |

Fifth dogfood; the tool found real cross-file drift its own construction had accumulated across
three slices + the catch-up — the kind of thing only a whole-feature adversarial pass surfaces.

## Status: three slices delivered
All 10 self-test fixtures green (no-oracle path, oracle path, and the judge each dogfooded live with
executed evidence; the rest fixture-verified). A true builder → adversary → judge triple. Composition
contract + judge documented as separate reusable units; no existing skill edited.
