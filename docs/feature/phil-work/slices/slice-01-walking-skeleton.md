# Slice 01 — Walking Skeleton: one initiative, one delegated skill, end-to-end

**Goal:** `/phil:work "<initiative>"` carries one real invisible initiative end-to-end — FRAME → delegate to one tactical skill → suite stays green → write a decision doc.

## IN scope
- New `commands/work.md` (thin loader) + `skills/work/SKILL.md` (the loop).
- FRAME: capture the initiative as a scoped goal + a preservation contract, plus IN/OUT scope. Interactive confirm. Preservation-oracle is artifact-aware (D9): for code = the test suite; for prose artifacts (skills/rules/agents) = the self-test harness where one exists, else the human-approval diff oracle (per `refactor-tests`, ADR-002).
- Delegate the actual change to **one** tactical skill (default `refactor-loop` for code; `refactor-tests`/`redesign-tests` carry the human-approval oracle for prose), chosen by the developer or defaulted.
- Preservation floor enforced: check the oracle before and after; if it fails after (suite red, self-test broken, or diff rejected), the delegated skill's own revert applies and the run reports failure.
- Write `decisions.md` for the initiative: goal, preservation result, commits made.
- FRAME off-ramp: if the initiative obviously suits a single tactical skill, recommend running it directly and exit.

## OUT scope
- Multi-wave roadmap (slice 02).
- Characterization-test authoring (slice 03).
- Declared per-initiative goal metric beyond behavior-preservation (slice 04).
- Routing across multiple tactical skills / initiative types (slice 05).

## Learning hypothesis
**Disproves** "the general-contractor model adds real value over just running a tactical skill" **if** a full `/phil:work` run feels like pure overhead on a real refactor with no clearer outcome or trail than running `refactor-loop` alone.
**Confirms** the contractor spine (frame → delegate → preserve → document) is worth building out **if** the framed goal + decision trail make the run more disciplined and reviewable than the bare skill.

## Acceptance criteria
- Running `/phil:work "<initiative>"` on a repo with a passing preservation oracle produces a confirmed goal + preservation contract, a delegated change, a still-passing oracle, and a written `decisions.md` — verified end-to-end on a REAL initiative in this plugin (production data, not a toy). At least one verification run targets a **prose artifact** (skill/rule/agent), exercising the human-approval oracle path.
- If the oracle fails after delegation, the run reports failure and leaves the tree in its last-good state (revert), not broken.
- On an initiative a single tactical skill clearly handles, FRAME recommends the direct skill and exits without ceremony.

## Dependencies
- Existing `refactor-loop` skill; command→skill split convention; test-runner detection (`skills/shared/`).

## Effort estimate
~1 day (≤6h dispatch). **Reference class:** `refactor-tests` walking skeleton (command + skill + one adapter), shipped in comparable time.

## Pre-slice SPIKE
None required — the delegation target (`refactor-loop`) and the command→skill pattern already exist and are proven in this repo.
