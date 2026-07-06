# ADR-004 — redesign-tests: coverage-equivalence claim at the human gate

Status: accepted (DESIGN wave, 2026-07-06) · Feature: redesign-tests

## Context

`refactor-tests` ADR-002 established the human-approval oracle: apply the move to the working tree,
run the suite as a sanity check, pause for the developer to review the *uncommitted diff in their
IDE*, then approve/reject/skip/quit. That works because `refactor-tests` moves are assertion-
preserving — the human is confirming "structure changed, meaning didn't."

`redesign-tests` is different: the human is the **sole** oracle for a change that *deliberately
alters what the test verifies* (DISCUSS D2, D7). A green suite proves nothing about whether the
rewritten assertion still catches the bugs the old one did. So the reviewer needs more than a raw
diff — they need to know **what coverage the rewrite claims to preserve**, or they cannot judge it.

## Decision

**Inherit ADR-002's apply-then-review mechanism verbatim** (apply → suite sanity → IDE diff review →
approve/reject/skip/quit; no chat diffs; auto-revert on post-apply red; one commit per approved
item). **Add one required element:** every proposal must carry a **coverage-equivalence claim** —
a short, explicit before/after statement the human validates:

> *"The old test caught {regression class} by asserting {implementation detail X}. The rewrite
> catches {the same regression class} by asserting {observable behavior Y}."*

The human gate is then a judgment on that claim, not just on the diff aesthetics. The claim is
surfaced with the proposal (in chat/rationale), while the diff itself is reviewed in the editor.

Flakiness-family rewrites (S4) additionally run an **N-run stability sanity check** before the gate
(the determinism analog of the coverage claim).

**No automated oracle in v1.** The propose step leaves a clean pre-screen seam where a future
automated coverage oracle (mutation testing or deliberate-break-and-confirm) would validate the
coverage-equivalence claim before it reaches the human — exactly the seam pattern `refactor-tests`
used to defer its test-diff critic (ADR-002 slice 04).

## Alternatives considered

- **Raw diff only (pure ADR-002 reuse)** — rejected: for assertion-preserving moves the diff is
  self-evidently safe; for behavior-changing moves it is not. Without the equivalence claim the
  human is guessing, which defeats the human-as-oracle premise.
- **Build the automated coverage oracle now** — rejected: its value (reducing review burden and
  catching silent coverage loss) is only measurable once a working loop produces real burden and
  loss data. Empirical over speculative — same reasoning ADR-002 used to defer the critic.
- **Block until an oracle exists** — rejected: the human-only loop is shippable and useful now; the
  accepted-risk (DISCUSS D7) is explicit and recorded.

## Consequences

- (+) The human gets exactly what they need to judge a behavioral rewrite: the claimed coverage
  equivalence, plus the real diff.
- (+) v1 matches the DISCUSS oracle (human-only) exactly; the automated oracle slots into the
  pre-screen seam later without rework.
- (−) A behavioral rewrite can still silently narrow coverage if the human accepts a wrong
  equivalence claim (DISCUSS D7 accepted risk). The claim reduces but does not eliminate this.
- (−) Proposals cost more to generate (the claim must be articulated), by design.
