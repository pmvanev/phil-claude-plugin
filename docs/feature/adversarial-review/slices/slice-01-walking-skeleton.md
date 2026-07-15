# Slice 01 — Walking skeleton: honest soft review

**Goal.** Standalone `/phil:adversarial-review` on a **no-oracle** target (a doc / skill / design just
written) dispatches an independent reviewer that returns a **typed, advisory, span-and-evidence
verdict labeled DRAFT SIGNAL**; the human decides what to do with it.

## IN scope
- `commands/adversarial-review.md` (thin loader) + `skills/adversarial-review/SKILL.md` (spine).
- A reviewer agent (`agents/adversarial-reviewer.md`) — independent (C1): fresh context, curated
  input (artifact + stated-or-inferred intent + standards), **never** the builder's reasoning trace.
- The typed verdict schema (reason-before-verdict; ranked worst-first; each finding has span +
  evidence; `CANNOT_ASSESS` for unsupportable praise — C5).
- The **honesty label**: no oracle → `draft-signal` (C4). Reviewer is **advisory** — never declares
  done (C3).
- Intent source: inferred from conversation/context when standalone (D5).

## OUT of scope
- Oracle detection / hard-check path / `sound-gate` label → slice 02.
- Any host composition → slice 03.
- Applying or fixing findings (reviews only).

## Learning hypothesis
- **Confirms** (if it succeeds): an independent, honestly-soft-labeled adversarial pass produces
  findings a developer acts on that the builder's self-assessment missed.
- **Disproves** (if it fails): the findings are noise, **or** the tool cannot resist presenting a
  soft review as a sound gate — either kills the concept (it would be the theatre it exists to
  prevent, anxiety A).

## Acceptance criteria
- AC1: running the command on a no-oracle target returns a verdict whose overall label is
  `draft-signal` and whose findings are each ranked with a span + evidence.
- AC2: a finding that is generic praise with no span is emitted as `CANNOT_ASSESS`, not `accept`.
- AC3: the verdict never contains a done/not-done adjudication — only advisory findings.
- AC4: the reviewer is dispatched with curated input that excludes any builder reasoning trace
  (independence observable in the dispatch contract).

## Production data (not synthetic)
Review a real just-written artifact in this repo (e.g. a skill or ADR draft) — real prose, real
findings.

## Dogfood moment
Run it on one of this feature's own DISCUSS artifacts within the same day.

## Dependencies
Reuse: `refactor-critic-correctness` (schema, reason-before-verdict, anti-flattery), ADR-002 (human
port). No new infrastructure.

## Effort / reference class
Small — one prose skill + one agent, patterned on existing `agents/refactor-critic-correctness.md`
and the edd skill spine. Reference class: edd slice 01 (walking-skeleton off-ramp).
