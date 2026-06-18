# ADR-004: Test-file lockbox = tool-scoping + PreToolUse hard guard (defence in depth)

**Status:** Accepted
**Date:** 2026-06-17
**Scope:** safety invariant #2 / hooks

## Context

AHE regression-blindness: a self-editing agent predicts what it'll *fix* at ~5× chance but
what it'll *break* at only ~2× (11% recall) — *"cannot reliably name what it is about to
break."* So behavior preservation must be certified by the **pre-existing** suite. An agent
that can edit the test files has disabled the oracle.

## Decision

The proposer can **never** edit test files, enforced two ways:
1. **Tool-scoping** — `refactor-proposer.allowed-tools` excludes `Bash` and is constrained
   so it cannot author test files (it gets `Edit` only for the production diff).
2. **PreToolUse hook (G2)** — a `before_action` guard that **blocks** any Edit/Write whose
   path matches the test-path glob set, regardless of which agent attempts it. Outcome
   `stop` (block the write).

Defence in depth: scoping is the policy, the hook is the enforcement. Either alone is
weaker (scoping can be misconfigured; a hook can be the only line if scoping drifts).

## Consequences

- (+) The oracle is structurally protected; the proposer cannot weaken the gate.
- (−) Requires a correct test-path glob set per project (open decision §10.7); a too-narrow
  glob is the failure mode — reviewed by a human before ship (leverage law: human reviews
  the guard set).

## Trace
rgr-loop.md §component-map (lockbox); gap-memo §agentspec (before_action + stop outcome).
