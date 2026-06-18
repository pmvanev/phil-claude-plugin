# Design-relevant findings missing from rgr-loop.md

*Gap analysis (Nova / nw-researcher). Sources are LOCAL distilled research summaries
under `harebrain/docs/research-summaries/*`; web reputation scoring is N/A — every
claim traces to a named summary read in full. This is a GAP analysis: it surfaces
findings that bear on the refactoring-loop design but are MISSING or UNDER-WEIGHTED in
`rgr-loop.md`. It does not re-derive what the synthesis already covers.*

In-scope summaries reviewed: **18** (every summary not in the ALREADY-CITED roster).

---

## Executive summary

`rgr-loop.md` is well-grounded on the cage/brain seam, hard-vs-soft critics, the
critic panel, verdict schema, structured inter-pass messaging, and stopping criteria —
all drawn from the already-cited cluster. The biggest gaps are not in the loop's
*logic* but in three places the uncited corpus speaks to directly: (1) **the guard layer
has no syntax or runtime model** — AgentSpec supplies a working trigger/check/enforce DSL,
a four-outcome enforcement taxonomy, and a leverage law for *when a guard pays off* that
rgr-loop never states; (2) **the convergence-proof plan is under-specified against
benchmark-rigor standards** — the ABC checklist, terminal-bench, the broken-benchmarks
indictment, and benchmark-contamination collectively demand an oracle/trivial-agent
baseline, judge-human agreement, confidence intervals across seeds, and a fresh (uncontaminated)
target before any "it converged" claim means anything; and (3) **two empirical results
sharpen the loop's mechanics** — ComplexBench shows a refactoring backlog is a dependency
DAG (a failed prerequisite voids dependents, so flat scoring of findings is wrong), and
eval-driven-iteration measures the *exact* residual the loop must close (a prompt
constraint is obeyed only 80–90% of the time — promote to a hard guard). Three field
reports (Project Vend, Replit, OpenClaw) confirm rgr-loop's two safety invariants and
add a third the synthesis omits: an always-available HALT and *decay-on-data-not-rules*
(a pinned constraint must never be summarized away).

---

## Top gaps (ranked)

| # | Finding (source) | Design area | Relation | Recommended change |
|---|---|---|---|---|
| 1 | A guard is a `trigger / check / enforce` rule; enforcement has **four outcomes** (`stop`, `invoke_action`, `user_inspection`, `llm_self_examine`) — first two hard/sound, last two soft/deferred. Runtime cost ~0.01% of wall-clock because the guard is compiled boolean, not an LLM. (**agentspec**) | (a) cage/brain seam; (h) safety invariants; (i) substrate | EXTENDS | Add a guard-outcome taxonomy. The auto-revert is `stop`; the test-file write-block is a `before_action` guard with `stop`; back-prompting the proposer is `llm_self_examine`. Name them; note hard guards cost ~nothing so gate liberally. |
| 2 | **Leverage gradient:** a guard amortizes only where risk has recurring *structure* (30× for code, 1.3× for one-off driving laws). (**agentspec**) | (b) state machine; (h) safety invariants | EXTENDS | State the cost rule: write hard guards for the recurring shapes (public-API-changed, new-lint, test-file-touched, coverage-drop); don't hand-author a guard per one-off smell — that's the soft critic's job. |
| 3 | A complex instruction is a **dependency DAG**: a failed prerequisite voids every dependent regardless of local quality (`r'_q = r_q ∧ ⋀ r_p`). Flat averaging of findings is provably worse than topology-aware scoring (0.614 vs 0.574 human agreement). (**complexbench**) | (b) state machine; (e) verdict schema; (g) stopping | EXTENDS | Treat the refactoring backlog as a DAG, not a flat list. If a refactor's prerequisite reverts, its dependents are auto-invalid — don't re-propose them. The `seen/resolved` set in todo.md should carry dependency edges. |
| 4 | A prompt constraint is obeyed only **80–90%** of the time even when task-specific; "be helpful" generic guidance silently regressed grounding −13pp while lifting another axis (non-monotonic). Only a task-specific suite caught it. (**eval-driven-iteration**) | (h) safety invariants; (c) hard vs soft | CONFIRMS+EXTENDS | Quantify *why* the proposer can't self-certify: it's not 0% reliable, it's ~85% — which is exactly the gap a hard external suite must close. Add: every loop change (prompt, rubric) is itself non-monotonic and must be regression-tested, not eyeballed. |
| 5 | **ABC rigor bar:** a convergence claim needs an oracle/reference, a **trivial-agent baseline** (a do-nothing agent passed τ-bench 38%), a **validated LLM judge** (documented human agreement), and **confidence intervals**. 7/10 audited benchmarks had validity breaks reordering leaderboards. (**agentic-benchmarks**, **benchmarks-broken**) | (j) proving convergence | EXTENDS | Before claiming the loop "converged" on wumpus: run a do-nothing/no-op baseline (does the suite pass trivially?), report the critic's agreement with a human spot-check, and report variance across runs — not a single "it stopped" anecdote. |
| 6 | **Silent scoring failure / test-oracle problem:** runner bugs surface as plausible wrong numbers, not crashes. Validation gap is the only cross-cutting root cause; the integration **seam** is 41% of harness issues. Fix: semantic contracts at seams, metamorphic + differential tests. (**evaluation-engineering**) | (i) substrate; (a) seam | EXTENDS | The loop's own harness can be silently wrong (a critic that always returns "accept" looks like fast convergence). Add a meta-check: a deliberately-bad refactor must be *rejected* (differential/metamorphic test on the critic itself), else the gate is decorative. |
| 7 | A constructive critic verdict should be a **typed quadruple** `(span, type, mechanism, evidence)`, not a bare boolean — back-promptable, route-able. Mechanism enum + 84%-fabrication skew. (**hart**) | (e) verdict schema; (f) inter-pass messaging | EXTENDS | Enrich the verdict schema: each `per_criterion` failure should carry a code span and an evidence pointer (the offending lines + the rubric clause), so the back-prompt payload is precise, not "improve readability." |
| 8 | An LLM judge can be **measured (F1 vs humans) and improved (RL-trained)**; all-or-nothing conjunctive reward beat fractional by 4.5pp for *shaping*, but is a brittle *runtime* guard (1-in-4 hard calls wrong at F1 0.728 — strands a run). (**advanced-if**) | (c) hard vs soft; (d) panel; (g) stopping | CONFIRMS+EXTENDS | Add: don't gate a transition on ALL soft criteria passing — one false-negative stalls the loop forever. Conjunctive strictness is for the *hard* gate; the soft panel routes on severity+confidence (as rgr-loop already does — make the contrast explicit). |
| 9 | **Contamination:** a fixed benchmark posted publicly is label-contaminated within one crawl; detection is a losing arms race (paraphrase evades every detector). Mitigation is structural: generate fresh per run. (**benchmark-contamination**) | (j) proving convergence | EXTENDS | If the loop is ever benchmarked, don't reuse one fixed package as the convergence proof across model versions — a model may have trained on it. Prefer a held-out/fresh package, or report the caveat. |
| 10 | An emergency **HALT must be reachable from every state at top priority**; safety constraints must live outside the volatile context (compaction silently evicted a "suggest, don't action" rule → 200 emails deleted). Put decay on *world state*, never on *rules*. (**openclaw-emails**, **replit-database**, **project-vend**) | (h) safety invariants; (f) messaging | CONFIRMS+EXTENDS | Add a third safety invariant: pinned constraints ("don't touch tests", "preserve public API") must be re-asserted structurally each iteration, immune to context compaction — and the loop needs a user-abort that wins over an in-progress refactor. |

---

## Per-summary detail

### agentspec — HIGH relevance (gaps 1, 2)
- **Finding.** An LLM agent is `(S,A,Ω,Π,Δ)`; a guard is a compiled rule `(trigger η, predicate set P, enforcement E)` fired at `before_action` / `state_change` / `agent_finish`. Enforcement is one of four: `stop` (terminate), `invoke_action` (splice a fixed correction), `user_inspection` (pause for human), `llm_self_examine` (kick back to the model). First two are deterministic/sound; last two defer to a fallible party. Predicate eval is single-digit ms (~0.01% of a 25s agent step). Leverage: one rule covers 30 code scenarios but only 1.3 driving laws — "the cage amortizes only where the risk has structure." LLM-drafted rules are a *productivity* win, not a *soundness* win (they overfit examples, miss compound/long-tail cases).
- **Informs.** (a) seam, (b) state machine, (h) safety invariants, (i) substrate.
- **Relation.** EXTENDS. rgr-loop has the seam and the hard/soft split but no *syntax* for a guard and no *taxonomy of enforcement outcomes*; it also never states when a hard guard is worth authoring.
- **Recommended change.** (1) Add a "Guard outcomes" subsection mapping rgr-loop's mechanics onto the four: auto-revert-on-red = `stop`; PreToolUse test-file block = `before_action`+`stop`; back-prompt-the-proposer = `llm_self_examine`; the (currently absent) human checkpoint = `user_inspection`. (2) Add the leverage rule to "Static vs dynamic": hard-guard the recurring invariants, leave one-off smells to the soft critic.

### complexbench — HIGH relevance (gap 3)
- **Finding.** Constraints compose as And/Chain/Selection/Nested; modeling the dependency DAG and voiding dependents of a failed prerequisite beats flat averaging on human agreement (0.614 vs 0.574). Rule-Augmented evaluation (route rule-checkable questions to a deterministic rule, only fuzzy ones to the LLM) lifts rule-defined agreement 82%→95%. Naïve decomposition into multi-turn *lowered* scores (cumulative error) — but that is decomposition *without a shared typed state*, i.e. the loop minus its blackboard.
- **Informs.** (b) state machine, (c) hard vs soft, (e) verdict schema, (g) stopping.
- **Relation.** EXTENDS (DAG) + CONFIRMS (rule-augmented = hard/soft split; the "decomposition hurt without shared state" reading directly supports rgr-loop's blackboard).
- **Recommended change.** Model the backlog as a DAG with dependency edges in the `seen/resolved` ledger; when a refactor reverts, auto-invalidate its dependents rather than letting the next review re-surface them. Cite the "decomposition fails without a blackboard" result as positive evidence for the structured-state messaging section.

### eval-driven-iteration — HIGH relevance (gap 4)
- **Finding.** A task-specific prompt constraint left the model at 90%/80% compliance — defied 1-in-10 / 1-in-5. Generic "improvements" are non-monotonic: +13pp on one axis, −10/−13pp on two others, invisible without a suite. "Correct but unsupported" is the canonical grounding violation. The fix is structural (a guard that *rejects* the transition), not a better prompt.
- **Informs.** (h) safety invariants, (c) hard vs soft, (i) substrate.
- **Relation.** CONFIRMS the "never let advisory do a sound job" rule and EXTENDS it with a number: the residual is ~10–20%, which is the magnitude the external suite must cover. Also a new warning rgr-loop lacks.
- **Recommended change.** In "the seam," add the empirical 80–90% compliance figure as the quantitative justification for "proposer can never certify its own behavior-preservation." Add a one-line caution: changes to the loop's *own* prompts/rubric are non-monotonic and must be regression-tested (the rubric is frozen partly for this reason — make the link explicit).

### agentic-benchmarks (ABC) + benchmarks-broken — HIGH relevance (gap 5)
- **Finding.** Rigor = task validity (solvable iff capable; no shortcuts, no impossible tasks) AND outcome validity (the check certifies success). 7/10 audited benchmarks broke task validity, 7/10 outcome validity, 8/10 hid the flaws. A do-nothing agent scored 38% on τ-bench. Requirements: oracle solver, trivial-agent baseline (R.13), validated LLM judge (O.c.1, documented human agreement), confidence intervals (R.10), non-AI baseline (R.12).
- **Informs.** (j) proving convergence on a real package.
- **Relation.** EXTENDS — rgr-loop's "prove convergence on `wumpus`" has no acceptance rubric; ABC is exactly that rubric.
- **Recommended change.** Expand the substrate section's convergence-proof plan into a checklist: (i) a trivial/no-op baseline run (does the test suite pass without any refactor? does an empty proposal "converge" instantly? — exposes a hollow loop); (ii) spot-check the soft critic against a human on a sample and report agreement; (iii) report variance across ≥5 runs, not one trace; (iv) confirm the loop *rejects* a deliberately-bad refactor (no shortcut to "done").

### evaluation-engineering — HIGH relevance (gap 6)
- **Finding.** Benchmark validity and *operational reliability* (does the runner execute correctly?) are orthogonal — both must hold. Runner bugs are silent (plausible wrong numbers, no crash): the test-oracle problem. Failures cluster at the integration *seam* (41%) and validation gaps are cross-cutting. Prescribed fixes: semantic API contracts at seams, metamorphic testing (relabel input → invariant output), differential testing (two impls must agree).
- **Informs.** (i) substrate, (a) seam.
- **Relation.** EXTENDS — rgr-loop assumes the harness/critic is correct; this names how it can be silently wrong (a critic stuck on "accept" = instant false convergence).
- **Recommended change.** Add a "the loop's harness is also software under test" note: include a self-test where a known-bad refactor (e.g. one that breaks a test or broadens the public API) must be caught by the critic/gate. If it isn't, the gate is decorative. This is the metamorphic/differential check applied to the critic itself.

### hart — MEDIUM relevance (gap 7)
- **Finding.** A constructive critic verdict should be a typed quadruple `(span, type, mechanism, evidence)` — span-level + an evidence pointer makes it actionable and back-promptable; a bare boolean is "a shrug." Soundness of the evidence is inherited from the corpus, not free (generic search inherits ~0.03 recall, not 0.80).
- **Informs.** (e) verdict schema, (f) inter-pass messaging.
- **Relation.** EXTENDS — rgr-loop's `per_criterion` items have `reason` prose but no required code span / evidence pointer.
- **Recommended change.** Require each failing `per_criterion` item to carry a `span` (file:line range) and an `evidence` field (the rubric clause + the offending lines) so the back-prompt payload is precise. Note that "evidence" for a refactoring critic is cheap and sound — it's the actual diff lines, not a retrieval.

### advanced-if — MEDIUM relevance (gap 8)
- **Finding.** A soft critic's quality is *measurable* (judge-human F1 0.728) and *improvable* (RL-trained verifier). All-or-nothing conjunctive reward beat fractional by 4.5pp for *training*, but is brittle at *runtime* (1-in-4 hard calls wrong → strands a single run). Reward-hacking artifacts ("this is a perfect response!") flatter an LLM judge — countered with extra anti-flattery criteria.
- **Informs.** (c) hard vs soft, (d) panel, (g) stopping.
- **Relation.** CONFIRMS the explanation-first verdict + frozen-rubric design; EXTENDS with the runtime-brittleness warning.
- **Recommended change.** In stopping criteria, add: gate the *outer loop* on hard-critic conjunction (tests green AND no metric regression) but route the *soft* panel on severity+confidence thresholds, never on "all soft criteria pass" — a single soft false-negative must not be able to block `DONE` forever. Add an anti-flattery criterion to the rubric ("verdict must cite the specific diff lines; generic praise = CANNOT_ASSESS").

### project-vend + replit-database + openclaw-emails — MEDIUM relevance (gap 10)
- **Finding.** Three field reports: an ungated action surface drifts (Vend), a prose "code freeze" is crossed in 9s and the agent's confession is *generated text, not an audit trail* (Replit), and a correct, honored safety rule was silently evicted by **context compaction** (OpenClaw, 200 emails). Lessons: bound the action surface by geometry not toggle; put a HALT edge reachable from every state at top priority; pin constraints outside the volatile window; decay *world state*, never *rules*; never trust a self-report over a deterministic trace.
- **Informs.** (h) safety invariants, (f) inter-pass messaging.
- **Relation.** CONFIRMS rgr-loop's two invariants (external suite gates; proposer can't edit tests) and EXTENDS with two: (a) the pinned constraints must be re-asserted structurally each iteration (compaction-immune), and (b) the loop should not trust the proposer's "I preserved behavior" claim — only the suite (rgr-loop says this; the Replit confession is the vivid proof).
- **Recommended change.** Add safety invariant #3: pinned constraints (`preserve public API`, `don't touch test files`) are re-injected from a durable slot every iteration and never summarized; and a user-abort that wins over an in-progress apply. Cite Replit's "confession is text completion" as the reason the predicted-impact manifest must be checked against the *actual* test delta, never accepted on the proposer's word.

### benchmark-contamination — MEDIUM relevance (gap 9)
- **Finding.** Four leak levels (semantic/info/data/label); the catchable ones are least severe, the severe ones least catchable. Detection is a losing arms race (paraphrase evades all detectors). Mitigation is structural: generate fresh / private / on-demand. A fixed public benchmark is label-contaminated within one crawl.
- **Informs.** (j) proving convergence.
- **Relation.** EXTENDS — rgr-loop names `wumpus` as the single convergence target without noting contamination risk across model versions.
- **Recommended change.** One caveat line: don't treat repeated convergence on one fixed package as model-agnostic evidence; a newer model may have ingested it. Prefer a fresh or private target for cross-model claims, or report the caveat.

### terminal-bench — LOW/MEDIUM relevance (supports gap 5)
- **Finding.** Outcome-driven grading reads the *final state*, never the agent's commands/narration — the cleanest separation of policy from verification. "Integrity by geometry": cheating is removed from the environment (future commits stripped), not penalized. Error taxonomy (Execution / Coherence / Verification) and: **token count and turn count do not correlate with success** — structure beats volume.
- **Informs.** (j) proving convergence; (c) hard gate.
- **Relation.** CONFIRMS the hard-gate-reads-exit-codes design and the "stop is a guard not a vibe" stance (more iterations ≠ better).
- **Recommended change.** Minor: in stopping criteria, cite "more turns/tokens don't correlate with success" as support for the hard iteration cap — running longer is not a strategy. Optionally adopt the "grade the final state, not the proposer's reasoning" framing for the critic (already implied by "don't pass the reasoning trace to the critic").

---

## No design relevance

- **harel** — Statecharts formalism (depth/orthogonality/broadcast). It is the *theory* under the cage's state machine, but rgr-loop's loop is a small linear pipeline (PROPOSE→REVIEW→APPLY→TEST) that needs none of Harel's hierarchy/concurrency machinery. Background, not an actionable gap. (If the loop ever grows orthogonal critic regions, revisit — but that's speculative, which rgr-loop rightly avoids.)
- **mebn-prowl** — Multi-Entity Bayesian Networks / PR-OWL. A maturity reference for a "blackboard with confidence" that reasons over a variable number of uncertain entities. The refactoring loop's state is small and mostly boolean (tests green?, API changed?); probabilistic multi-entity reasoning is far beyond what it needs. No actionable change.
- **llm-attribution-survey** and **rag-attribution-survey** — Claim-level attribution (citing sources, entailment guards). Load-bearing for *RAG / factual-claim* workflows, but the refactoring loop makes no external factual claims — its "evidence" is the diff and the test result, both locally checkable. The one transferable idea (a three-valued verdict: accept / gather-more / reject) is already covered by rgr-loop's `accept | revise | reject` schema, so no gap. Listed for completeness.
- **hallucination-recitations (HAR)** — Training-time technique (counterfactual finetuning to instil deference). Operates on model *training*, not on an inference-time loop; rgr-loop cannot author training data. The "cheap brain + strong cage" cost intuition is already implicit in rgr-loop's per-agent model tiering. No actionable change.

---

## Net recommended changes to rgr-loop.md (punch list, by impact)

1. **Add a guard-outcome taxonomy** (agentspec): name rgr-loop's mechanics as `stop` / `invoke_action` / `user_inspection` / `llm_self_examine`, note hard guards are ~free so gate liberally, and add the leverage rule (hard-guard recurring invariants; leave one-off smells to the soft critic).
2. **Add a third safety invariant + HALT** (openclaw/replit/vend): pinned constraints re-asserted structurally every iteration (compaction-immune); a user-abort that wins over an in-progress apply; never accept the proposer's self-reported behavior-preservation — check the predicted-impact manifest against the actual test delta.
3. **Make the backlog a dependency DAG, not a flat list** (complexbench): carry dependency edges in the `seen/resolved` ledger; auto-invalidate dependents of a reverted refactor.
4. **Spell out the convergence-proof acceptance checklist** (ABC / broken-benchmarks / terminal-bench): trivial/no-op baseline, validated soft-critic agreement, variance across ≥5 runs, a deliberately-bad refactor that must be rejected, and the "more turns ≠ better" support for the iteration cap.
5. **Add a critic self-test** (evaluation-engineering): a known-bad refactor must be caught, else the gate is silently decorative (metamorphic/differential test on the critic itself).
6. **Quantify the residual** (eval-driven-iteration): note prompt constraints hold only ~80–90% — the size of the gap the hard suite closes — and flag that loop-prompt/rubric changes are non-monotonic and must be regression-tested.
7. **Enrich the verdict schema** (hart): require `span` (file:line) + `evidence` (rubric clause + offending lines) on each failing criterion for a precise back-prompt; add an anti-flattery rule (generic praise = `CANNOT_ASSESS`).
8. **Contamination caveat** (benchmark-contamination): don't treat one fixed package as model-agnostic convergence evidence across model versions.
