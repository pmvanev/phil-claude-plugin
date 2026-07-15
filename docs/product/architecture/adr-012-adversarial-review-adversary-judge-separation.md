# ADR-012 — adversarial-review: separate the adversary from the judge (the triple)

Status: accepted (DELIVER slice 03, 2026-07-15) · Feature: adversarial-review · Extends ADR-010

## Context

DISCUSS/DESIGN shipped adversarial-review with **one** new agent (`adversarial-reviewer`) that both
*attacked* the work and *rendered* the verdict. The tri-agent research this feature is built on keeps
those apart: **QCA** (candidate), **RA** (adversary), **EA** (judge). Mapped to this feature the
builder is the QCA (whoever did the work — not built here), and we had merged RA + EA into the single
reviewer. ADR-010 recorded the separation ("different-model / multi-lens reviewer") as an accepted-risk
hardening **seam**, deferred. A review of the shipped feature surfaced the merge as an unstated
decision; the maintainer chose to build the separation.

The merge's risk: a single agent that both attacks and judges can **over-report** — it is motivated
to find something, and it certifies its own findings. Nothing filters a plausible-but-wrong finding
before it reaches the human.

## Decision

**Add a third role — an independent judge (`agents/adversarial-verifier`) that confirms-or-refutes
each finding the adversary raises — making the tool a true builder → adversary → judge triple.**

- The **adversary** (`adversarial-reviewer`) raises findings (unchanged).
- The **judge** (`adversarial-verifier`) receives **one finding** + `{ target, intent, standards,
  oracle_result? }` and **not** the adversary's `justification`, `confidence`, or other findings. It
  reads the span itself, tries to **refute**, and **defaults to `refuted`** when it cannot
  independently confirm. Output: `{ judgment: confirmed|refuted, confidence, corrected_severity,
  basis }`.
- The skill's **VERIFY** step dispatches the judge per finding (fresh subagent each), keeps
  `confirmed` findings, drops+counts `refuted` ones, and presents only confirmed findings.
- The **honesty label is unchanged** by verification — it still tracks only whether an oracle backed
  the review (C4). Verification changes *which findings survive*, never the label.

The judge shares C1's independence discipline: it never sees the adversary's reasoning, so the two
cannot agree their way past a shared blind spot. Refute-by-default is the diversity lever available
without a different model.

## Alternatives considered

- **Keep the single reviewer (merge RA+EA)** — rejected by the maintainer: defensible (the hard
  oracle in C2 is the stronger soundness lever, and reason-before-verdict separates attack from
  conclusion within one agent), but it leaves false-positive filtering to the same motivated agent
  and under-delivers on the tri-agent structure the feature advertises.
- **Multi-lens panel (N judges, majority)** — deferred: strongest soundness, highest cost; better
  suited to composed/workflow use than the standalone default. Recorded as the next seam.
- **Different-model judge** — deferred: the honest same-model residual risk remains (ADR-010); a
  model split is a later hardening when data warrants it.

## Consequences

- (+) Precision: a motivated adversary's misreads are filtered before a human sees them; the refuted
  count is itself a signal about reviewer noise.
- (+) Faithful to the tri-agent RA/EA separation and to the "adversarial verify" pattern.
- (+) The judge is a **separate reusable unit** — composable independently (a host may run reviewer
  alone with unverified findings, or reviewer+judge for confirmed-only).
- (−) Cost: one judge pass per finding (skipped when there are no findings).
- (−) Same-model adversary+judge is not full independence (accepted; refute-by-default mitigates;
  different-model/panel is the recorded seam).
- (−) A judge that is too eager to refute could suppress true findings — pinned against by fixture 10
  (must confirm a real finding), the mirror of fixture 09 (must refute a false one).
