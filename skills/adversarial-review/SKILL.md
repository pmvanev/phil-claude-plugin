---
name: adversarial-review
description: Skill bundle for phil:adversarial-review command — a general-purpose independent adversarial critic. Points a fresh, independent reviewer at a completed task, curating its input so it never sees the builder's reasoning, and presents a typed, advisory, span-and-evidence verdict — honestly labeled, never self-adjudicating. Standalone driver; the agent (agents/adversarial-reviewer.md) is the reusable unit and its typed verdict is the composition contract.
---

# Adversarial Review

Drive an independent adversarial critic at a completed task. Frame the target, dispatch a reviewer that
never sees the builder's reasoning, put each finding to an independent judge, and present what survives
to the human. Judge nothing yourself and decide nothing about "done": the judgment belongs to the
reviewer and the judge, the decision to the human.

The standards a review is held to are whatever applies to the target —
`${CLAUDE_PLUGIN_ROOT}/rules/coding.md`, `${CLAUDE_PLUGIN_ROOT}/rules/testing.md`,
`${CLAUDE_PLUGIN_ROOT}/rules/architecture.md`, `${CLAUDE_PLUGIN_ROOT}/rules/writing.md`, and the target's
own stated intent. **Where the target adds or changes tests, add
`${CLAUDE_PLUGIN_ROOT}/rules/test-patterns.md`** — a suite that is green because its tests assert on
mocks of in-process collaborators, or compute their expected values, proves less than its colour, and
that gap is evidence against "done".

Three roles keep the concerns apart. The **builder** is whoever did the work — the main session or a
delegated AI. The **adversary**, `agents/adversarial-reviewer`, attacks and raises findings. The
**judge**, `agents/adversarial-verifier`, confirms or refutes each finding without seeing the adversary's
reasoning, so a motivated attacker cannot rubber-stamp its own findings. The reviewer agent is the
reusable unit and its typed verdict is the composition contract (see *Composition contract*); this skill
is only the standalone human driver.

---

## Invariants

1. **Independence (C1).** Dispatch the reviewer in **fresh context** with the target, intent and
   standards **only**. Withhold the **builder's reasoning and self-assessment**: a reviewer that sees
   them agrees with the builder instead of judging the work. The judge is independent of the reviewer
   in the same way.
2. **Advisory, never self-adjudicating (C3).** The reviewer emits findings and the judge confirms or
   refutes them; neither declares the task done or not done. **The human decides.** Present; never
   rule.
3. **Honesty label (C4).** The label is **mechanical**: `sound-gate` iff a deterministic oracle backed
   the review, else `draft-signal`. It answers "did an oracle back this?", never "how sure is the
   reviewer?", and verification never changes it. Present a soft review as a draft signal and a real
   oracle result as a sound gate — over-claiming and under-claiming both fail. Never invent or approximate
   an oracle to earn the label.
4. **Adversary and judge stay separate.** The reviewer raises findings and a separate judge confirms or
   refutes each. Present only judge-confirmed findings as confirmed.
5. **No manufactured findings, no empty praise (C5).** A clean pass is honest; praise with no span is
   coerced to `cannot-assess` — the reviewer owns this; never override it toward approval.
6. **Edit or fix nothing.** This skill reviews; it does not change the work.
7. **Report the verdict as it is.** Soften no major finding and invent none.

---

## Parse the argument

| Pattern | Action |
|---|---|
| `"<target>"` — an explicit path or artifact name | Review that named target. |
| `--intent "<...>"` | Use this as the stated intent, the claim-of-done; otherwise infer it. |
| No argument, or a bare "the task I just completed" | Review the task just completed in this session; infer the target and intent from the conversation leading up to the invocation. |

A composing host passes the intent explicitly; standalone, infer it from context. Inferring the
**intent** is fine; inferring or importing the **builder's reasoning** breaks invariant 1.

---

## FRAME — establish the review contract

Assemble three things, and only these:

1. **Target** — the completed artifact or artifacts under review. With no argument, identify what was
   just completed from the conversation. If that is ambiguous, ask the developer what to review — one
   short question — rather than guessing.

   **That ask follows `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`.** Load it before the call.
   The candidate scopes go in the context block — this skill is the only thing that knows what they
   are — and the counted ask says what turns on the choice: a wrong scope reviews work nobody asked
   about and misses the work that was done.
2. **Intent** — the claim-of-done: what the task was meant to achieve, stated by the host, given via
   `--intent`, or inferred from context. Show an inferred intent to the developer so they can correct
   it.
3. **Standards** — the rules that apply to this target type: code → coding and testing; prose → eos and
   the relevant rule; a skill or agent → the plugin's own conventions.

Begin the review only once the target and intent are settled.

---

## ORACLE — run or inherit a deterministic check (sets the label)

Run the oracle here, in the driver: the reviewer stays read-only and only *cites* the result. Inherit a
result a host already captured; never re-implement it.

- **Code target:** detect a test runner via `${CLAUDE_PLUGIN_ROOT}/skills/shared/test-runner-detection.md`;
  if one exists, run the suite, and lint and types if present, and capture the result.
- **Prose target** (skill, agent, rule, doc): run the deterministic prose checks that apply —
  self-test fixture pass, dead-link and broken skill-ref scan, frontmatter validity, file-length limit,
  required-citation presence. Capture each result.
- **No deterministic oracle** (a design doc's "soundness", a subjective artifact): proceed with no
  `oracle_result`.

Record the outcome as `oracle_result` — the captured output and what was run — or note that none was
available. **An oracle ran → `sound-gate`; none → `draft-signal`.** If the only "check" is your own
judgment, there is no oracle.

---

## CURATE — assemble independent input (invariant 1, the load-bearing step)

Build the reviewer's input as **exactly** `{ target, intent, standards, oracle_result? }`, with
`oracle_result` omitted when none ran. Strip everything else: builder reasoning, self-assessment, a
prior "looks good to me", your own opinion of the work. An `oracle_result` is a machine-produced fact
and must pass; a builder's *claim* that "the tests pass" is not one — pass the captured result, never
the claim.

Independence has two parts, and they are not equally strong. The **fresh-context dispatch** is
structural: the subagent cannot see this session. The **curation** is a discipline you apply inside a
builder-adjacent context, and nothing mechanical stops the builder's rationale reaching the contract —
fixture 04 guards it as a regression check, not a boundary. When in doubt, pass less. The same actor
curating is an accepted limitation; a different-model or multi-lens reviewer is the seam left for
hardening it.

---

## DISPATCH — invoke the independent reviewer

Invoke `agents/adversarial-reviewer` via the Task or Agent tool with the curated contract. It runs in
**fresh context**, which is where independence comes from. Pass the neutral contract and let it attack:
review nothing yourself and pre-judge nothing for it.

It returns the **typed verdict JSON**, whose schema is in the agent file. Rewrite nothing in it, add no
adjudication, and never upgrade its label.

---

## VERIFY — an independent judge tests each finding

The reviewer is motivated to find something, so it can over-report. Put each finding to the judge,
`agents/adversarial-verifier`, before it reaches the human.

For **each** finding, dispatch `adversarial-verifier` — a fresh subagent per finding — with
`{ finding, target, intent, standards, oracle_result? }`, and **withhold the reviewer's
`justification`, `confidence` and other findings**: the judge must reach its own view from the work, or
the two would simply agree. The judge is prompted to **refute**, and **defaults to `refuted` when it
cannot independently confirm**.

Then filter:

- Keep the findings the judge **`confirmed`**, applying any `corrected_severity`; re-rank worst-first.
- **Drop** the findings the judge **`refuted`**, and count them.
- If the judge refuted every finding, report that: the reviewer raised N and the judge refuted all N.
  That is not a `clean` verdict — the reviewer did see problems — but nothing survived independent
  scrutiny.

Verification changes *which findings* survive, never the label. A hard finding that faithfully cites the
oracle should pass; one the judge refutes misread the oracle.

> **Cost and skip.** Verification costs one judge pass per finding. A review with no findings (`clean`,
> `cannot-assess`) has nothing to verify — skip it. A composing host may run the reviewer alone when it
> owns its own downstream gate, provided it labels the findings unverified — see the composition
> contract.

---

## PRESENT — put the findings to the human

Give the developer a clear summary, and offer to open the target and the spans in their editor:

- Lead with the **honesty label**, so it is never mistaken for more or less than it is:
  *"Draft signal (no oracle) — an independent read, not a verified gate."* or
  *"Sound gate — backed by the test suite; hard findings cite the actual run."*
- Present the **judge-confirmed** findings **worst-first**, each with its span, mechanism and evidence.
  Say how many the judge **refuted and dropped** — "the reviewer raised 5; an independent judge
  confirmed 3 and refuted 2". The refuted count is a signal about reviewer noise.
- On `verdict: "clean"`, say so plainly with the label: "independent review found nothing — still a
  draft signal, not a verified pass" (no oracle), or "nothing found, and the suite ran green — sound
  gate" (oracle). On `verdict: "cannot-assess"`, report exactly that, never as approval.
- Leave "done" to the developer: say the decision is theirs and the review is input.

Write no trail by default — report to the developer and stop. When the developer asks for a persisted
record, write it where they ask; a composing host owns its own trail.

---

## Composition contract (documented, not wired)

A host command or an ad-hoc Workflow script composes adversarial review by invoking
`agents/adversarial-reviewer.md` directly (Task or `agent()`):

- **Input:** `{ target, intent, standards, oracle_result? }`. The caller owns the same disciplines this
  skill applies: **curate out builder reasoning** (invariant 1), and **run or inherit the oracle
  itself** and pass the captured `oracle_result`, never a builder's *claim* that tests pass.
- **Output:** the reviewer's typed verdict. Route on the typed fields only — `overall_label` and each
  finding's `kind` and `severity`, against a threshold θ — with **no re-judging**.
- **Verification composes too.** The judge, `agents/adversarial-verifier`, is a separate reusable unit.
  A host that wants confirmed-only findings runs the reviewer, then the judge per finding, as VERIFY
  does; a host that owns its own downstream gate may consume the raw findings if it treats them as
  *unverified* and says so.
- **The boundary rule:** a `draft-signal` verdict is never consumed as a passed sound gate, and neither
  agent's advisory output is ever treated as an adjudication of "done" (invariant 2) — the host owns its
  gate.

`phil:work`, `phil:edd` and `phil:refactor-tests` adopt this contract later, each as its own work, once a
real second consumer exists; this skill edits none of them.

---

## Self-test (regression gate)

`skills/adversarial-review/self-test/` holds golden fixtures for these behaviours: an honest soft review
labeled `draft-signal` (01, the walking skeleton); oracle plus failure → `sound-gate` with a hard
finding (02); findings alone, however confident, never earn `sound-gate` (03); builder reasoning
withheld from the dispatch (04); anti-flattery `cannot-assess` (05); advisory, never self-adjudicating
(06); an honest clean pass with no manufactured findings (07); clean plus a green oracle → `sound-gate`
(08); the judge refuting a false positive (09) and independently confirming a real finding (10).
Fixtures 02, 03, 07 and 08 pin the label in both directions.

Whenever this skill, `commands/adversarial-review.md`, `agents/adversarial-reviewer.md` or
`agents/adversarial-verifier.md` changes, drive the fixtures per `self-test/README.md` and confirm each
produces its `expected.md` decision.
