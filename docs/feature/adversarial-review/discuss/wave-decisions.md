# DISCUSS Decisions — adversarial-review

## Key Decisions
- [D1] New sibling job + persona + journey (not an edd extension): edd *produces evidence for a
  human to judge*; adversarial-review *does the judging*. (see: docs/product/jobs.yaml)
- [D2] Feature type: cross-cutting — standalone command + reviewer agent, composable into
  phil:work / phil:edd / phil:refactor-tests + ad-hoc workflows.
- [D3] Walking skeleton: discipline-first — standalone honest SOFT review of a no-oracle target,
  with the honesty label; hard/oracle path deferred to slice 02.
- [D4] Research depth: lightweight.
- [D5] Intent source dual: host passes it (composed); inferred from conversation/context (standalone).
- [D6] Typed, advisory verdict a host can gate on programmatically; reviewer never self-adjudicates.
- [D7] First composition consumer: phil:work review-wave (also fills phil:work v1 gap UI-1).

## Load-bearing constraints (the design is built against soft-critic theatre)
- C1 INDEPENDENCE — fresh context, no builder reasoning trace.
- C2 HARD/SOFT SPLIT — run the check / inherit the host oracle vs adversarial soft, labeled.
- C3 ADVISORY, NEVER SELF-ADJUDICATING — host or human gates.
- C4 HONESTY LABEL — no oracle → `draft-signal`, never dressed as a sound gate (the defining guard).
- C5 SPAN-AND-EVIDENCE / ANTI-FLATTERY — no finding without a span; empty praise → CANNOT_ASSESS.

Provenance: informed by the tri-agent clarification framework (Zhao, KDD '25), read via the harebrain
summary docs/research-summaries/tri-agent-clarification (in the sibling `harebrain` repo) — three-role
split, reason-before-verdict, adversarial persona, author-then-ablate self-tests — + its LLM-Modulo/ABC
warnings (hardest-critic soundness, correlated errors, unvalidated judge).

## Requirements Summary
- Primary need: an independent adversary that attacks a completed task and returns ranked
  evidence-bearing findings, honest about hard-vs-soft, advisory not self-adjudicating.
- Walking skeleton scope: standalone no-oracle soft review with the honesty label (slice 01).
- Feature type: cross-cutting (tooling / plugin command + agent).

## Constraints Established
- Inherit oracles, never re-implement (ADR-005 lineage). Reuse refactor-critic-correctness schema
  + anti-flattery, refactor-loop GUARD (severity threshold/ranking), test-runner-detection,
  ADR-002 human port.

## Upstream Changes
- None. Greenfield feature; no DISCOVER/DIVERGE to reconcile. SSOT bootstrapped:
  personas/rowan-skeptical-delegator.yaml, journeys/adversarial-review.yaml, jobs.yaml (+1 job).

## Handoff
- To: nw-solution-architect (DESIGN). Deliverables: feature-delta.md (DISCUSS [REF] sections),
  slice briefs 01–03, SSOT updates. Open design questions listed in feature-delta DoR section.
