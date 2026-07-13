# Slice 02 — MAP: a wave-by-wave roadmap from the framed initiative

**Goal:** After FRAME, `/phil:work` surveys the current state and produces an ordered, editable roadmap that names which tactical skill each wave calls — then executes the waves in sequence.

## IN scope
- MAP step: delegate a survey of the change surface to `spirit-walk` / `review-code` / `nw-hotspot` (whichever fits), then propose an ordered roadmap of waves.
- Each roadmap wave names: the change, the delegated tactical skill, and the preservation gate.
- Developer approves or edits the roadmap before execution.
- EXECUTE iterates the roadmap sequentially, delegating per wave, gating each on the preservation floor, committing structural changes separately.
- Roadmap + per-wave progress recorded in the decision trail.

## OUT scope
- Characterization-test authoring before change (slice 03).
- Declared goal metric beyond preservation (slice 04).
- Skill routing heuristics across initiative types (slice 05) — MAP may still let the developer pick the skill per wave.

## Learning hypothesis
**Disproves** "cross-wave planning beats one-shot delegation" **if** the roadmap for real initiatives is always trivially one or two steps, making MAP redundant over slice 01.
**Confirms** planning earns its place **if** real initiatives decompose into several gated waves that are clearer and safer executed in sequence than as one blob.

## Acceptance criteria
- On a real multi-step initiative, `/phil:work` produces an ordered roadmap (≥2 waves) each naming a delegated skill + gate; the developer can edit it; EXECUTE runs the waves in order, each ending green with a separate structural commit.
- The decision trail records the roadmap and a progress entry per completed wave.
- A wave that fails its preservation gate stops the sequence and reports which wave failed — the tree stays green.

## Dependencies
- Slice 01 (FRAME + delegation + decision trail). `spirit-walk`, `review-code`, `nw-hotspot`.

## Effort estimate
~1 day. **Reference class:** `phil:refactor` backlog loop (survey → ordered items → iterate), already in repo.

## Pre-slice SPIKE
None — survey skills and the sequential loop pattern already exist.
