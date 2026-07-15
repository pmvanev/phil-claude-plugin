# Evolution — adversarial-review (2026-07-15)

## What shipped

`/phil:adversarial-review` — a general-purpose **independent adversarial critic**. Point it at a
just-completed task and a fresh reviewer (that never sees the builder's reasoning) tries to falsify
"done" and returns a typed, advisory, ranked span-and-evidence verdict — honestly labeled, never
deciding "done" for you.

- `commands/adversarial-review.md` — thin loader.
- `skills/adversarial-review/SKILL.md` — the standalone driver: FRAME · ORACLE · CURATE · DISPATCH ·
  PRESENT.
- `agents/adversarial-reviewer.md` — the **adversary**: the reusable independent critic that raises
  findings + the typed-verdict **composition contract** (pattern-copied from
  `refactor-critic-correctness`).
- `agents/adversarial-verifier.md` — the **judge**: independently confirms-or-refutes each finding
  (fresh context, never sees the adversary's reasoning). Together with the builder this makes a
  **builder → adversary → judge** triple (ADR-012), realizing the tri-agent RA/EA separation.
- `skills/adversarial-review/acceptance.feature` + `self-test/` (8 golden fixtures) — the acceptance
  + regression gate.

Registered SSOT: persona `rowan-skeptical-delegator`, job
`get-independent-adversarial-critique-of-completed-work`, journey `adversarial-review`,
ADR-010 + ADR-011, and the Application Architecture entry (C4 diagrams) in `brief.md`.

## Why

The plugin already had the adversarial critic in narrow forms — `refactor-critic-correctness` (bound
to a test-suite oracle), edd's deferred evidence-critic — but no *general* adversary you could point
at any completed task. Rowan (the skeptical delegator) wants an independent second opinion before
trusting AI-produced or hand-built work, without either rubber-stamping the builder's self-assessment
or reading every line. Sibling to edd: edd *produces evidence for a human to judge*;
adversarial-review *does the judging*.

## The design, in one idea

Generalize `refactor-critic-correctness` out from behind its test-suite oracle — and confront the
soundness problem that move creates. Informed by the tri-agent clarification framework (Zhao,
KDD '25), read via the harebrain summary `docs/research-summaries/tri-agent-clarification` (in the
sibling `harebrain` repo), and its LLM-Modulo/ABC lineage: an all-soft-critic
loop dressed as a sound gate is "a graded essay presented as a verified plan." So the feature is built
against that (anxiety A) via five locked constraints:

- **C1 independence** — fresh-context reviewer; builder reasoning withheld (correlated-error avoidance).
- **C2 hard/soft split** — deterministic checks run/inherited as `hard` findings; judgment as `soft`.
- **C3 advisory** — the reviewer never self-adjudicates; the host or human gates.
- **C4 mechanical honesty label** — `sound-gate` iff an oracle backed the review, else `draft-signal`;
  over- and under-claiming both fail. Generalized to **prose oracles** (self-test, dead-link,
  frontmatter, length, citation), because the plugin's targets are usually prose.
- **C5 span-and-evidence / anti-flattery** — no finding without a span; empty praise → `cannot-assess`.

Architecture (ADR-010/011/012): a prose spine drives Task-dispatched subagents; the **agents are the
reusable units**, the **typed verdict is the composition contract**. The driver runs/inherits the
oracle; the reviewer stays read-only (inherit, never re-implement — ADR-005). Slice 03 (ADR-012)
separated the **adversary** (raises findings) from an independent **judge** (`adversarial-verifier`,
confirms/refutes each finding without the adversary's reasoning) — a builder → adversary → judge
triple that filters a motivated attacker's false positives before a human sees them. Standalone only
— **edits no existing skill**; hosts adopt the contract later (ADR-008 second-consumer rule).

## Outcome (before → after)

- **Goal:** ship a standalone, composable, honest adversarial reviewer as a builder → adversary →
  judge triple. **Met.** **10/10 self-test fixtures green**; three slices delivered (no-oracle soft
  review → oracle + `sound-gate` → the judge), plus a wave-gate catch-up.
- **Preservation:** no existing skill touched (verified — Reuse Analysis all pattern-copy/invoke).
- **Dogfood (executed evidence — five passes, each a real catch).** The tool was pointed at its own
  construction repeatedly, and every time an independent adversary caught what the builder (the
  session) had rationalized past:
  1. **Walking skeleton** on its own SKILL → 4 real defects (1 major), all fixed.
  2. **Oracle path** → correctly applied the mechanical `sound-gate` label; refused to manufacture nits.
  3. **The reviewer agent** → 2 real defects (undocumented field; a `cannot-assess` label gap), fixed.
  4. **The verifier agent** → a **major** flaw: no guard against *over-refuting* (it could suppress a
     true-but-subtle finding); fixed with a symmetric confirm step.
  5. **The whole feature** → 5 cross-file doc-drift findings; the judge confirmed the major one but
     corrected its severity major→minor (runtime self-consistent, only the ADR wording had drifted).
  This is the feature's own thesis, demonstrated on itself: separation of powers surfaces defects a
  self-assessment misses — and the adversary→judge split measurably added precision (the severity
  correction in pass 5).

## Scope / accepted limitations

- The adversary and judge are now separate agents (ADR-012), but both share a base model —
  refute-by-default is the diversity lever without a different model, so this is not *full*
  independence (tri-agent correlated-error caveat). Accepted; a **different-model judge** and a
  **multi-lens panel** (N judges, majority) are the recorded remaining seams (trivial when composed
  into a Workflow via `parallel()`).
- Composition is a documented contract, not wired into any host. First host adoption is future work.
- Prose-oracle catalog is a bounded v1 subset; breadth can grow.

## Follow-ups

- Adopt the contract in a first real host (candidate: `phil:work` review-wave — also fills its v1
  prose-gap UI-1), once it's a genuine second consumer.
- Different-model / multi-lens reviewer hardening when single-reviewer data warrants it.
