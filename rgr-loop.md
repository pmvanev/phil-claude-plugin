# Refactoring loop — design notes & research findings

*Loose suggestions for a Claude Code refactoring skill/agent system. Not a spec — a
pile of grounded ideas to pick from. Goal: review code → propose refactors → review
the proposals → apply → run tests → repeat until reviews turn up only weak/few
suggestions. Everything below is anchored in this repo's research summaries
(`docs/research-summaries/*`) + `docs/harebrain/harebrain.md`.*

> Builds on the existing `phil:review-code` (produces a prioritized refactoring
> backlog) + `phil:refactor` (works through it — test, fix, prune, repeat). This is
> the closed-loop, gated evolution of that pair.
>
> **Decision (2026-06-17):** keep `phil:refactor` exactly as it is (incremental,
> one-commit-per-item, main-loop). This design ships as a SEPARATE new
> `phil:refactor-loop` skill alongside it — not a rewrite. The two coexist: reach for
> `phil:refactor` for a controlled walk through a reviewed backlog, `phil:refactor-loop`
> for the gated autopilot. Because the deliverables are skills + agents (not application
> code), construction goes through **`nw:forge`** (the 5-phase agent-builder workflow),
> not the traditional acceptance-test / Outside-In TDD path.
>
> **Gap analysis folded in** (`docs/research/refactor-loop/rgr-loop-gap-analysis.md`,
> 2026-06-17): passages tagged **[GAP]** below incorporate findings from the previously
> uncited corpus — agentspec, complexbench, eval-driven-iteration, agentic-benchmarks,
> evaluation-engineering, hart, advanced-if, terminal-bench, benchmark-contamination, and
> the Vend/Replit/OpenClaw field reports.

---

## The one idea everything hangs on: the seam (cage vs brain)

Every harness paper makes the same cut — `Agent = Model + Harness`; harebrain's
*"cage owns where/when, brain owns what."* The whole design is deciding which
refactoring decisions are deterministic vs model judgment.

**Cage (deterministic):**
- the loop, iteration counter, max-iteration bound
- *when* to run each agent / the test suite
- applying the diff; reverting on red
- running tests/lint/types and **reading exit codes**
- the **stop decision** (a guard reading state)

**Brain (LLM):**
- *what* to refactor and *how* (the proposal)
- *whether* a refactor improves quality (the critique)
- *whether* a surviving critique is "weak" — emitted as a typed verdict, not a halt

Load-bearing rule (Böckeler, *harness-engineering*): **computational checks are
*sound* (green type-checker has *proven* something); inferential checks are
*advisory* (LLM "looks good" has *estimated* something).** Tests = sound; critics =
advisory. Never let advisory do a sound job. Never let the model decide it's done.

**[GAP] Quantify the residual the sound check must close (eval-driven-iteration).** "Advisory
is unreliable" isn't 0% — a *task-specific* prompt constraint is still obeyed only ~80–90% of
the time (defied 1-in-5 to 1-in-10). That ~10–20% is precisely the gap the external suite
exists to cover, and it's why the proposer can never self-certify behavior preservation.
Corollary: changes to the loop's *own* prompts/rubric are themselves non-monotonic (a generic
"be more helpful" tweak silently cost −13pp grounding while lifting another axis). Every edit
to a loop prompt or the rubric must be regression-tested against a fixed suite, never eyeballed —
this is a second reason the rubric is frozen.

---

## Component map → Claude Code primitives

| Research role | What it does | CC artifact | Model |
|---|---|---|---|
| Orchestrator (cage) | loop, hard gates, routing, stop | skill `/refactor-loop` **or** Workflow tool | — |
| Generator | proposes refactors as structured backlog | subagent `refactor-proposer` | strong |
| Soft critics | review proposals vs frozen rubric | subagent(s) `refactor-critic-*` (separate from proposer) | mixed |
| Hard critics | tests, type-check, lint, mutation/coverage | Bash commands the orchestrator runs | — (sound) |
| Frozen rubric | the standard critics apply | committed `rubric.md` | — |
| Anti-premature-exit | force loop to continue until guard satisfied | Stop hook (Ralph loop) | — |

Structural facts that aren't optional:

- **Separate proposer from critics.** LLM-Modulo: self-verification *decreases*
  accuracy (model "corrects" right answers into wrong ones). Tri-agent paper is the
  cautionary tale — asker/adversary/judge all the same model → *correlated errors,
  not independent verification*. Decorrelate via role diversity + distinct rubrics +
  different model tiers. (Caveat: CC can't do cross-vendor decorrelation like
  CollabEval's Mistral/Claude/Llama panel; role + rubric diversity matter more anyway.)
- **Proposer may never touch the tests.** AHE regression-blindness: a self-editing
  agent predicts what it'll *fix* at ~5× chance but what it'll *break* at ~2× (11%
  recall) — *"cannot reliably name what it is about to break."* So behavior
  preservation is certified by the **pre-existing** suite only, run externally every
  iteration. Lockbox: scope tools so proposer can't edit test files.

---

## The loop (state machine the cage owns)

```
PROPOSE ─► REVIEW ─►[guard: any actionable proposal?]─► APPLY one ─► TEST (hard gate)
                                                                        │
   ┌────────────────────────────────────────────────────────────────────┤
   │  red                      → REVERT (git) ─► feed failure evidence ─► PROPOSE
   │  green + strong critiques → next proposal / PROPOSE (new iteration)
   │  green + only weak left   → DONE
   └─ bounded by max_iterations → HALT-INCOMPLETE (report, don't fake success)
```

- **Hard critics gate first, cheaply** (LLM-Modulo: soundness inherited only from
  hard critics). Apply → lint/type/tests → red = auto-revert, no LLM in loop. Only
  survivors get a soft panel's tokens.
- **Stop is a guard, not a vibe.** Harebrain names premature conclusion *the* biggest
  long-horizon failure mode. Orchestrator decides done, not the proposer. Stop hook
  re-injects "continue until guard satisfied" (Ralph Loop, agent-harness-anatomy).
- **One refactor at a time through the gate** → each breakage attributable to one
  change (AHE commit-per-edit → free file-granular rollback).
- **[GAP] The backlog is a dependency DAG, not a flat list (complexbench).** A complex
  instruction composes as And/Chain/Selection/Nested; a failed prerequisite voids every
  dependent regardless of local quality (`r'_q = r_q ∧ ⋀ r_p`), and topology-aware scoring
  beat flat averaging on human agreement (0.614 vs 0.574). So when an applied refactor
  reverts on red, its *dependents* are auto-invalid — do **not** let the next REVIEW
  re-surface them. The `seen/resolved` ledger must carry dependency edges, not just a set of
  resolved IDs. (Same paper confirms the blackboard: naive decomposition *lowered* scores —
  but only when run *without* shared typed state.)

---

## Critic panel — lean default, earned escalation

Two forces to honor. CollabEval/Sage/judge-debate: heterogeneous independent critics
beat a single judge. dynamic-workflows + AHE non-additivity (+11pp single-component
gains collapsed to +7pp combined — *"a cage has a coordination budget; past it, more
controls subtract"*): most coding tasks don't need a 5-reviewer panel.

**Default (lean):** proposer → one *separate* `refactor-critic` → hard gate. Promote
only when single-review demonstrably misses a class of problem.

**Escalation (earned): disjoint-rubric panel, wired as CollabEval's three phases —
collaborative, NEVER adversarial.** Sage: *adversarial* debate makes things worse
(persuasive hallucination, anchoring, echo chamber). judge-debate: *collaborative*
refinement helps. Same act, opposite protocols.

```
PHASE 1  Independent: 3 critics, DISJOINT rubrics (correctness/behavior,
         idiom/readability, architecture/coupling). Each emits verdict+confidence+
         justification, none seeing the others.  → consensus? EXIT EARLY.
PHASE 2  On disagreement: critics see each other's structured verdicts and re-judge,
         order shuffled each round. Gated by consensus / unchanged-results / max 3 rounds.
PHASE 3  Deadlock → tiebreaker. HAREBRAIN IMPROVEMENT: route to the HARD critic, not
         a bigger LLM ("tests green + no metric regression → accept safer/smaller
         refactor, else reject"). A bigger model inherits the bias the panel escaped.
```

- Disjoint rubrics (not n copies) are what make a panel earn its tokens; redundant
  critics that mostly agree are mostly wasted (AHE).
- **Seed every soft round with hard-critic output** (test results, type-check,
  complexity deltas) in-context. judge-debate: debate is *Bayesian amplification, not
  generation* — locks onto whatever seed is present. No seed → can converge stably
  onto a shared error with high confidence. Tests = guaranteed correct seed.
- Panel size 3, odd, for majority fallback (CollabEval uses 3; judge-debate n=7).

---

## Verdict schema + frozen rubric

Critics emit structured output, **justification before verdict** (Sage: dropping
explanation-first ordering degrades consistency):

```json
{ "justification": "<reasoning, written first>",
  "verdict": "accept | revise | reject",
  "confidence": 0.0,
  "per_criterion": [ {"criterion": "...", "met": true,
                      "severity": "major|minor|nit", "reason": "...",
                      "span": "path/to/file.py:42-58",
                      "evidence": "<rubric clause + the offending diff lines>"} ] }
```

- Orchestrator routes on `verdict` + `severity` + `confidence` — computable, which is
  what makes the stop a guard not a judgment.
- Failing `per_criterion` items = the **back-prompt payload** to the proposer
  (Autorubric: 0.47→0.85 in one revision doing exactly this).
- **[GAP] Make each verdict a typed quadruple, not a bare boolean (hart).** A finding
  carries `(span, type, mechanism, evidence)` — a `met:false` with no code span is "a shrug."
  The `span` (file:line range) and `evidence` (the rubric clause + the actual offending diff
  lines) make the back-prompt precise — "extract lines 42-58, they violate single-responsibility"
  beats "improve readability." For a refactoring critic this evidence is *cheap and sound*: it's
  the real diff, not a retrieval (generic search inherits ~0.03 recall — irrelevant here because
  we hand the critic the diff directly).

**Rubric: authored once, frozen, committed, applied to every proposal** (Sage
situational-preference fix — don't let critics re-improvise their standard per call;
that's what makes them order-invariant). Analytic, not holistic:
- **Binary** criteria where possible — highest reliability ("public API unchanged",
  "no new lint warnings", "extracted unit has single responsibility").
- **Behavioral anchors, not adjectives** — "reduces nesting below N" > "good style."
- **Narrow ordinal (3–5 level) with anchors** for graded ones; no continuous scales
  (LLMs poorly calibrated).
- **Negative-weight criteria** for anti-patterns — dock lateral churn, speculative
  generality, hallucinated abstractions, broadened public surface (counters leniency).
- Mandatory per-criterion explanation + a `CANNOT_ASSESS` abstention.
- **[GAP] Anti-flattery criterion (advanced-if).** Reward-hacking artifacts ("this is a
  perfect refactor!") flatter an LLM judge. Require every verdict to cite specific diff lines;
  generic praise with no `span` = `CANNOT_ASSESS`, not `accept`.

Two clocks (harebrain): rubric + topology authored slowly, reviewed; a **human owns
construct validity** (Autorubric: a well-formed rubric on the *wrong* construct is
confidently wrong). Execution runs fast.

---

## Messaging between passes — structured state, NOT transcripts

Counterintuitive but measured. OS-Symphony: naive Last-K reflection over a rolling
transcript *hurt* (56.10 vs 60.20 for no reflection); only reflection over curated
milestone memory helped. Harebrain: *"reads named slots, not its rolling transcript."*

- **Proposer → Critic:** diff + original code + *stated intent* — **NOT** the
  proposer's reasoning trace (primes the critic toward agreement = self-preferential
  bias). CC subagents give clean scoped context for free.
- **Critic → orchestrator:** the typed verdict JSON. Prose stays inside; route on fields.
- **Across iterations:** summary blackboard — current diff, **verbatim** test output,
  unresolved critique items, **pinned constraints** ("preserve public API", "don't
  touch test files") immune to context rot (harebrain pinned slot, `∞`).
- Borrow AHE **predicted-impact manifest**: proposer attaches per-refactor *what it
  expects to fix + what it might regress*; harness checks prediction vs actual test
  delta next iteration. Self-justification → measurable contract.
- Handoffs leak (NLAH via harebrain: parent/child recall collapses to 0.32) — prefer
  a shared blackboard snapshot over private task-packets.
- **[GAP] Pinned constraints decay-on-data-not-rules, and the manifest is checked, never
  trusted (Replit / OpenClaw field reports).** Context compaction silently evicted a correct,
  honored safety rule → 200 emails deleted (OpenClaw); a prose "code freeze" was crossed in 9s
  and the agent's *confession was generated text, not an audit trail* (Replit). Therefore: the
  pinned slot ("preserve public API", "don't touch test files") must be **re-asserted
  structurally every iteration** from a durable source, immune to summarization — never just
  left in the rolling window. And the predicted-impact manifest is verified against the *actual*
  test delta; the proposer's "I preserved behavior" is never accepted on its word (this is the
  vivid proof of the existing safety invariant, not a new mechanism).

---

## Stopping criteria — "repeat until weak/satisfied," operationalized

Nest cheapest-first:
1. **Consensus early-exit** (CollabEval) — critics agree → stop this review now. Most
   cases stop here (avg ~1.5–2.3 rounds).
2. **Unchanged-results** (CollabEval) — round reproduces prior verdicts → saturated.
   Discussion cap = **3 rounds**.
3. **Outer-loop stop** = `tests green AND no critique item ≥ major above confidence
   threshold AND iterations < max`. "Only weak suggestions remain" = no
   high-severity/high-confidence verdicts left — a computable predicate.
4. *(rigorous)* **Stability detection** — judge-debate KS-needle: panel agreement
   distribution stops moving (`D_t < 0.05` over two rounds) → stop. Their table: 0.05
   stops ~6 rounds, <0.6% accuracy loss vs full 10-round run.

Red flag to LOG: panel convergence-locks **without** a hard anchor present = false
convergence (stably wrong), not a green light.

- **[GAP] Conjunctive strictness belongs to the HARD gate only (advanced-if).** All-or-nothing
  "every criterion must pass" is right for the sound check (tests green AND types AND no metric
  regression). It is *brittle* as a soft-panel rule: a judge wrong on ~1-in-4 hard calls (F1
  0.728) means one soft false-negative would strand the run forever. So gate the outer loop on
  hard conjunction; route the *soft* panel on severity+confidence thresholds (as above) — never
  on "all soft criteria pass."
- **[GAP] More iterations ≠ better (terminal-bench).** Token count and turn count do **not**
  correlate with success — structure beats volume. This is positive support for the hard
  `max_iterations` cap: running longer is not a strategy, and a loop that keeps going is not a
  loop that's improving. Grade the final state, not the proposer's narration.

---

## Static vs dynamic control flow

Hard-code control flow; let the model decide only content (harebrain two-clocks; AHE:
*structure transfers, prose does not* — system-prompt-only variant regressed below
baseline).

| Decision | Cage or brain | Why |
|---|---|---|
| propose→review→apply→test sequence | **static** | fixed pipeline; never reorder |
| whether to loop again | **static guard** | premature-conclusion is *the* failure mode |
| when to run tests | **static** (always after apply) | ground truth must be unconditional |
| revert on red | **static** | safety invariant, not judgment |
| *what* to refactor / *how* | **dynamic** | the "what" the brain owns |
| *whether* a critique is valid/weak | **dynamic verdict, static threshold** | model judges, harness counts |
| how many reviewers / which model | **static config** | don't let the model spend the budget |

### [GAP] Guard outcomes + the leverage law (agentspec)

A guard is a compiled rule `(trigger, predicate, enforcement)` fired at `before_action` /
`state_change` / `agent_finish`; predicate eval is single-digit ms (~0.01% of a 25s agent
step), so **hard guards are essentially free — gate liberally.** Enforcement is one of four
outcomes, and naming them disambiguates this design's mechanics:

| Outcome | Sound/soft | This loop's instance |
|---|---|---|
| `stop` | sound | auto-revert on red; HALT on max-iterations |
| `invoke_action` | sound | splice a fixed correction (e.g. `git checkout` the reverted file) |
| `user_inspection` | soft (defers to human) | the user-abort / HALT checkpoint |
| `llm_self_examine` | soft (defers to model) | back-prompt the proposer with failing criteria |

**Leverage law:** a guard amortizes only where the risk has *recurring structure* (one rule
covered 30 code scenarios but only 1.3 one-off driving laws). So **hard-guard the recurring
invariants** — public-API-changed, new-lint-warning, test-file-touched, coverage-drop — and
leave *one-off* smells to the soft critic. Don't hand-author a guard per smell; that's the
critic's job. (Caveat: LLM-drafted guards are a *productivity* win, not a *soundness* win —
they overfit the examples and miss compound/long-tail cases, so a human reviews the guard set.)

---

## Substrate — the determinism dial

The more reliability wanted, the more control flow moves from prose into executable code.

- **Start: skill-driven loop.** `/refactor-loop` skill = orchestrator; runs hard gates
  as **real Bash commands** (reads exit codes itself — don't delegate the gate), spawns
  proposer/critic subagents, Stop hook prevents premature exit. Native, debuggable.
  Risk: loop control lives in prose the model executes → can drift.
- **Turn it up: the Workflow tool.** The dynamic-workflows paper realized — JS
  orchestrator with real loops, barriers, `schema`-validated agent outputs, per-agent
  model selection, `pipeline()`/`parallel()`. Loop/gating/stop become deterministic JS;
  agents are the only LLM leaves. Closest CC gets to "cage owns control flow." Needs
  opt-in, runs background. Right home for the panel + bounded rounds + tiebreaker.

Suggested path: build lean skill first (proposer + 1 critic + Bash hard gates + Stop
hook), prove convergence on a real package (e.g. `python/packages/wumpus`), then lift
orchestration into a Workflow for the disjoint-rubric panel + formal stopping guards.

### [GAP] "Proved convergence" needs an acceptance bar (agentic-benchmarks, evaluation-engineering, benchmark-contamination, terminal-bench)

"It stopped on wumpus" is an anecdote, not evidence — 7/10 audited benchmarks had validity
breaks, and a *do-nothing* agent scored 38% on τ-bench. Before claiming the loop works, clear
this checklist:

1. **Trivial/no-op baseline** — does the suite already pass with zero refactors? Does an empty
   proposal "converge" instantly? A loop that declares success on a no-op is hollow.
2. **Critic self-test (the gate is also software under test).** Runner/critic bugs are *silent* —
   they surface as plausible wrong numbers, not crashes (the test-oracle problem; integration
   seams are 41% of harness faults). A critic stuck on "accept" looks exactly like fast
   convergence. So feed the loop a **deliberately-bad refactor** (breaks a test, or broadens the
   public API) and assert it is *rejected*. If it isn't, the gate is decorative. This is a
   metamorphic/differential test applied to the critic itself.
3. **Validated soft critic** — spot-check the critic against a human on a sample; report the
   agreement (don't assume an unmeasured judge is right).
4. **Confidence intervals** — report variance across ≥5 runs, not one trace.
5. **Contamination caveat** — don't treat repeated convergence on one fixed package as
   *model-agnostic* evidence; a newer model may have ingested it (detection is a losing arms
   race — paraphrase evades all detectors). Use a fresh/private target for cross-model claims,
   or state the caveat.

---

## Suggested file layout

New skill alongside the untouched `phil:refactor` (built via `nw:forge`, not TDD):

```
skills/refactor-loop/SKILL.md        # NEW phil:refactor-loop — orchestrator: state machine + gating + stop guard
commands/refactor-loop.md            # thin stub → loads the skill (matches plugin convention)
agents/
  refactor-proposer.md               # generator; tools Read,Grep,Glob (NO test write)
  refactor-critic-correctness.md     # behavior-preservation rubric
  refactor-critic-idiom.md           # readability/idiom rubric   (panel mode)
  refactor-critic-architecture.md    # coupling/structure rubric  (panel mode)
refactor/rubric.md                   # frozen analytic rubric, committed
                                     # backlog ledger carries DAG edges (seen/resolved + deps), not a flat set
settings.json                        # Stop hook + read-only test-file guard + compaction-immune pinned-constraint re-inject
```

**Three hard safety invariants:**
1. proposer can never certify its own behavior-preservation — only the external suite gates
   (AHE regression-blindness; the manifest is checked against the *actual* test delta, never
   accepted on the proposer's word — Replit "confession is text completion");
2. proposer can never edit tests (tool-scoping + PreToolUse hook blocking writes to
   test paths). An agent that can edit the oracle has disabled the oracle (AHE);
3. **[GAP] pinned constraints are compaction-immune and HALT is always reachable**
   (OpenClaw/Replit/Vend): re-assert "preserve public API" / "don't touch test files" from a
   durable slot every iteration (never leave them only in the rolling context — compaction
   silently evicted one and deleted 200 emails), and provide a user-abort that wins over an
   in-progress apply, reachable from every state at top priority.

---

## Source map

- `harness-engineering` — computational(sound)/inferential(advisory) split; checks-far-left.
- `agentic-harness-engineering` (AHE) — regression-blindness (load-bearing safety);
  read-only verifier lockbox; predicted-impact manifest; non-additive coordination
  budget; commit-per-edit + file-granular rollback.
- `agent-harness-anatomy` — Agent=Model+Harness; Ralph Loop; handoff-leak recall 0.32.
- `meta-harness` — proposer/produced two-clock split; no-compression diagnostic.
- `dynamic-workflows` — fan-out+barrier, adversarial verification, loop-until-done,
  tournament; "most coding tasks don't need a 5-reviewer panel"; per-agent model choice.
- `os-symphony` — Last-K-hurts ablation (curated state beats raw transcript); typed verdicts.
- `llm-modulo` — hard vs soft critics; self-verification fails; soundness from sound checker.
- `collabeval` — three-phase state machine; verdict+confidence+justification; 3 critics, cap 3.
- `assessing-judges` (Sage) — independent panel helps / debate hurts; situational-preference fix.
- `judge-debate` — collaborative > adversarial; Bayesian amplification; KS-needle stability.
- `tri-agent-clarification` — correlated-errors cautionary tale (all agents same model).
- `autorubric` — analytic rubric design; per-criterion feedback as optimization signal.
- `harebrain` — cage/brain seam; two clocks; pinned constraints; bounded loops.

Added by the 2026-06-17 gap analysis (`docs/research/refactor-loop/rgr-loop-gap-analysis.md`):
- `agentspec` — guard DSL (trigger/check/enforce); four enforcement outcomes; ~free runtime; leverage law (hard-guard recurring structure only).
- `complexbench` — instruction is a dependency DAG; failed prerequisite voids dependents; topology-aware > flat; decomposition fails *without* shared state.
- `eval-driven-iteration` — task-specific prompt constraints hold only ~80–90%; loop-prompt/rubric edits are non-monotonic (must be regression-tested).
- `agentic-benchmarks` (ABC) + `benchmarks-broken` — trivial-agent baseline, validated judge, confidence intervals; 7/10 audited benchmarks had validity breaks.
- `evaluation-engineering` — silent runner/critic bugs (test-oracle problem); seams = 41% of faults; metamorphic/differential self-test for the gate.
- `hart` — verdict as typed quadruple `(span, type, mechanism, evidence)`; evidence cheap+sound when it's the diff itself.
- `advanced-if` — soft judge is measurable (F1 0.728) and brittle as a runtime conjunction; anti-flattery criteria.
- `terminal-bench` — grade final state not narration; token/turn count uncorrelated with success (supports the iteration cap).
- `benchmark-contamination` — fixed public target is label-contaminated within one crawl; mitigation is structural (fresh/private), not detection.
- `project-vend` / `replit-database` / `openclaw-emails` — field reports: ungated surface drifts; self-reports aren't audit trails; compaction evicts honored rules → HALT + compaction-immune pinned constraints.

No design relevance (reviewed, ruled out): `harel` (statechart theory — loop is a linear pipeline), `mebn-prowl` (probabilistic multi-entity reasoning — loop state is small/boolean), `llm-attribution-survey` + `rag-attribution-survey` (claim attribution — loop makes no external factual claims; three-valued verdict already covered), `hallucination-recitations` (training-time technique — not inference-loop authorable).
```