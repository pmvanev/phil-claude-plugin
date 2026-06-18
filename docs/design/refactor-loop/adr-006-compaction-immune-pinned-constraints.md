# ADR-006: Pinned constraints in a durable slot, re-asserted each iteration; HALT reachable everywhere

**Status:** Accepted
**Date:** 2026-06-17
**Scope:** safety invariant #3 / messaging + hooks

## Context

gap-memo §openclaw-emails: context compaction **silently evicted** a correct, honored safety
rule → 200 emails deleted. The lesson: decay belongs on **world state, never on rules**.
gap-memo §project-vend / §replit-database add: an ungated action surface drifts, and an
emergency HALT must outrank an in-progress action.

## Decision

Two mechanisms:
1. **Compaction-immune pinned constraints.** `preserve public API`, `don't touch test
   files`, the active `max_iterations`, and user-abort reachability live in a **durable
   source** (the ledger header / `refactor/pinned-constraints.md`), NOT only in the rolling
   context. Guard **G7 re-asserts them structurally at the top of every iteration**
   (`UserPromptSubmit` / iteration-boundary hook). Never left to summarization.
2. **Always-reachable HALT.** A `user-abort` guard (G9) fires `before_action` on **every**
   step at **top priority** — it wins over an in-progress apply. `max_iterations` (G8) also
   forces HALT-INCOMPLETE; the loop reports honestly and never fakes success.

## Consequences

- (+) The two safety invariants survive context compaction — the failure mode that deleted
  200 emails cannot recur.
- (+) The user can always stop the loop, even mid-apply.
- (−) Requires a durable slot and a re-injection hook; G7 runs every iteration (cost is
  negligible — guard eval ~0.01% of a step, gap-memo §agentspec).

## Trace
rgr-loop.md §messaging, §safety-invariants; gap-memo §openclaw-emails, §replit-database,
§project-vend.
