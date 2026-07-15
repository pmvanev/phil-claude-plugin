---
name: adversarial-review
description: Skill bundle for phil:adversarial-review command — a general-purpose independent adversarial critic. Points a fresh, independent reviewer at a completed task, curating its input so it never sees the builder's reasoning, and presents a typed, advisory, span-and-evidence verdict — honestly labeled, never self-adjudicating. Standalone driver; the agent (agents/adversarial-reviewer.md) is the reusable unit and its typed verdict is the composition contract.
---

# Adversarial Review

You are the **standalone driver** for an independent adversarial critic. A developer (Rowan) has just
completed a task — or delegated it to an AI agent — and wants someone who **isn't the builder** to
try to break it before they trust it. Your job is to frame the target, dispatch an **independent
reviewer** at it, and put the reviewer's findings in front of the human. You do **not** judge the
work yourself, and you do **not** decide whether it is done.

The real judgment is the reviewer's; the real decision is the human's. You are the connective tissue:
you set up the review so it is honest and independent, and you present the result.

The standards a review is held to are whatever applies to the target —
`~/.claude/rules/coding.md`, `~/.claude/rules/testing.md`, `~/.claude/rules/architecture.md`,
`~/.claude/rules/eos.md`, and the target's own stated intent.

> **The through-line (ADR-010/011).** The reusable unit is the **agent**
> (`agents/adversarial-reviewer.md`); this skill is only the standalone human driver. The agent's
> **typed verdict is the composition contract** — the same agent, unchanged, is what a host or a
> workflow invokes later (composition is documented, not wired — see the seam at the end).

> **Scope (slices 01–02).** Both paths ship. **No oracle** (a doc/skill/design with no deterministic
> check): soft findings only, labeled `draft-signal`. **Oracle available** (code with a test suite,
> or prose with a runnable check): the driver runs/inherits it (ORACLE step), the reviewer emits
> `hard` findings citing the actual result plus `soft` findings, and the verdict is labeled
> `sound-gate`. The label is mechanical — `sound-gate` iff an oracle backed the review, else
> `draft-signal` — never a matter of the reviewer's confidence.

---

## The three lines you never cross

1. **Independence (C1).** The reviewer is dispatched in **fresh context** and is given the target +
   intent + standards **only**. You never pass it the **builder's reasoning or self-assessment** —
   that is the correlated-error trap (the reviewer would be agreeing with the builder, not judging
   the work). This is the structural analog of edd's producer ≠ builder separation of powers.
2. **Advisory, never self-adjudicating (C3).** Neither you nor the reviewer declares the task done or
   not done. The reviewer emits findings; **the human decides**. You present, you do not rule.
3. **Honesty label (C4).** The label is **mechanical**: `sound-gate` iff a deterministic oracle
   actually backed the review, else `draft-signal`. You never present a soft review as a verified
   pass (over-claiming), and never bury a real oracle result as a mere draft signal (under-claiming).
   The label answers one question — "did an oracle back this?" — not "how sure is the reviewer?"

---

## Parse the argument

| Pattern | Action |
|---|---|
| `"<target>"` — an explicit path or artifact name | Review that named target. |
| `--intent "<...>"` | Use this as the stated intent/claim-of-done (otherwise infer it). |
| No argument (or a bare "the task I just completed") | Review the task just completed in this session; infer the target + intent from the conversation context leading up to the invocation (D5). |

Intent source is dual (D5): a composing host passes it explicitly; standalone, you infer it from the
context leading up to the invocation. Inferring **intent** from context is fine — inferring or
importing the **builder's reasoning** is not (line 1).

---

## FRAME — establish the review contract

Assemble three things, and only these, as the review contract:

1. **Target** — the completed artifact(s) under review. If invoked with no argument, identify what
   was just completed from the conversation; if it is ambiguous, ask the developer what to review
   (one short question) rather than guessing.
2. **Intent** — the claim-of-done: what the task was meant to achieve. Stated by the host, given via
   `--intent`, or inferred from context. Show the inferred intent to the developer so they can
   correct it.
3. **Standards** — the rules that apply to this target type (code → coding/testing; prose → eos +
   the relevant rule; a skill/agent → the plugin's own conventions).

Do not begin the review until the target and intent are settled.

---

## ORACLE — detect and run/inherit a deterministic check (sets the label)

Determine whether a **deterministic oracle** exists for this target, then run or inherit it. You run
the oracle here (the driver), not the reviewer — the reviewer stays read-only and only *cites* the
result (ADR-005 lineage: inherit, never re-implement).

- **Code target:** detect a test runner via `skills/shared/test-runner-detection.md`; if one exists,
  run the suite (and lint/types if present) and capture the result. If a host already ran it, inherit
  that result rather than re-running.
- **Prose target** (skill / agent / rule / doc): run the deterministic prose checks that apply —
  self-test fixture pass, dead-link / broken skill-ref scan, frontmatter validity, file-length limit,
  required-citation presence. Capture each result.
- **No deterministic oracle** (a design doc's "soundness", a subjective artifact): none available —
  proceed with no `oracle_result`.

Record the outcome as `oracle_result` (the captured output + what was run), or note that none was
available. This single fact sets the honesty label downstream: **an oracle ran → `sound-gate`; none
→ `draft-signal`.** Never invent or approximate an oracle to earn a `sound-gate` label — if the only
"check" is your own judgment, there is no oracle.

---

## CURATE — assemble independent input (C1, the load-bearing step)

Build the reviewer's input as **exactly**: `{ target, intent, standards, oracle_result? }` — the
`oracle_result` from ORACLE if one ran, omitted otherwise. Then **strip everything else** — in
particular, any builder reasoning, self-assessment, prior "looks good to me", or your own opinion of
the work. If the conversation contains the builder's rationale, it does **not** go into the dispatch.
(An `oracle_result` is a machine-produced fact, not builder reasoning — it is safe and required to
pass; a builder's *claim* that "the tests pass" is not — pass the actual captured result, never the
claim.)

Independence has two parts, and they are not equally strong. The **fresh-context dispatch** is
structural: the subagent cannot see this session's history. The **curation** here is a *discipline*
you apply inside your own (builder-adjacent) context — nothing mechanically stops you from copying
the builder's rationale into the contract, so this step is backed by fixture 04 as a regression
guard, not by a hard boundary. Treat it with the seriousness that gap demands: when in doubt, pass
less. (The residual "same actor curates" risk is the honestly-accepted v1 limitation recorded in
ADR-010; a different-model / multi-lens reviewer is the recorded hardening seam.)

---

## DISPATCH — invoke the independent reviewer

Invoke `agents/adversarial-reviewer` via the Task/Agent tool, passing the curated contract. It runs
in **fresh context** (a subagent) — this is where independence comes from. You do not review the work
yourself and you do not pre-judge it for the reviewer; pass the neutral contract and let it attack.

The reviewer returns the **typed verdict JSON** (schema in
`docs/feature/adversarial-review/feature-delta.md` § DISTILL and in the agent file). Do not rewrite
it, do not add an adjudication to it, do not upgrade its label.

---

## PRESENT — put the findings to the human (advisory)

Present the verdict to the developer via the human port (ADR-002 — a clear summary, and offer to open
the target/spans in their editor):

- Lead with the **honesty label** so it is never mistaken for more or less than it is:
  *"Draft signal (no oracle) — an independent read, not a verified gate."* or
  *"Sound gate — backed by the test suite; hard findings cite the actual run."*
- List findings **worst-first**, each with its span, mechanism, and evidence.
- If `verdict: "clean"`, say so plainly, carrying the label: "independent review found nothing —
  still a draft signal, not a verified pass" (no oracle) or "nothing found, and the suite ran green —
  sound gate" (oracle). If `verdict: "cannot-assess"`, report that honestly rather than dressing it
  as approval.
- **Do not** tell the developer whether the task is done. State that the decision is theirs; the
  review is input.

By default **write no trail** — report to the developer and stop; a review should add no ceremony.
If the developer asks for a persisted record, write it where they ask; a composing host owns its own
trail.

---

## Safety rules

- **Independence is non-negotiable (C1).** Fresh-context reviewer; builder reasoning withheld. A
  correlated review is not a review.
- **Advisory only (C3).** Neither you nor the reviewer declares done/not-done. Present; the human
  decides.
- **Honest label (C4).** Mechanical: oracle ran → `sound-gate`; none → `draft-signal`. Never dress a
  soft review as a sound gate (over-claim), never bury a real oracle result as a draft signal
  (under-claim). Never invent an oracle to earn the label.
- **No manufactured findings; no empty praise (C5).** A clean pass is honest; praise with no span is
  coerced to `cannot-assess` (the reviewer owns this, but never override it toward approval).
- **You do not edit or fix anything.** This skill reviews; it does not change the work.
- **Report honestly.** Present the verdict as it is; never soften a major finding or invent one.

---

## Composition contract (documented, not wired — ADR-010 DDD7)

The reusable unit is `agents/adversarial-reviewer.md`; its **typed verdict is the contract**. A host
command or an ad-hoc Workflow script composes adversarial review by invoking that agent directly
(Task / `agent()`):

- **Input:** `{ target, intent, standards, oracle_result? }`. The caller is responsible for the same
  two disciplines this skill applies — **curate out builder reasoning** (C1), and **run/inherit the
  oracle itself** and pass the captured `oracle_result` (never a builder's *claim* that tests pass).
- **Output:** the typed verdict. Route on the typed fields only — `overall_label` and per-finding
  `kind` + `severity` (+ a threshold θ) — with **no re-judging**.
- **The boundary rule:** a `draft-signal` verdict must **never** be consumed as a passed sound gate,
  and the reviewer's advisory verdict is never treated as an adjudication of "done" (C3) — the host
  owns its gate.

This feature **edits no existing skill.** Hosts (`phil:work`, `phil:edd`, `phil:refactor-tests`)
adopt this contract later, each as their own work, once a real second consumer exists (ADR-008
second-consumer rule). Ad-hoc Workflow weaving needs nothing more than the agent + this contract:
call `agent()` with the input, read the verdict, route on it.

---

## Self-test (regression gate)

`skills/adversarial-review/self-test/` holds author-then-ablate golden fixtures that pin these
behaviors: honest soft review labeled `draft-signal` (01, walking skeleton), independent dispatch
with builder reasoning withheld (04), anti-flattery `cannot-assess` (05), advisory / never
self-adjudicate (06), and an honest clean pass with no manufactured findings (07). Fixtures 02
(oracle + failure → `sound-gate` with a hard finding) and 08 (clean + green oracle → `sound-gate`)
exercise the hard half; fixture 03 is the honesty-label guard — findings alone, however confident,
never earn `sound-gate` without an oracle. Fixtures 02/03/07/08 pin the label in both directions —
over- and under-claiming both fail. Whenever this skill, `commands/adversarial-review.md`,
or `agents/adversarial-reviewer.md` changes, drive the fixtures per `self-test/README.md` and confirm
each produces its `expected.md` decision — every edit here is non-monotonic, so these are changed and
regression-tested, never changed and eyeballed.
