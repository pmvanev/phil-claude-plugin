# DELIVER progress — phil-work

Roadmap: `docs/feature/phil-work/deliver/roadmap.json`. Delivered slice by slice; each step drives
its self-test fixtures to their `expected.md` decision (no CI collector — driven by human/model,
per `skills/work/self-test/README.md`).

## Step 01-01 — Walking skeleton (slice 01) — ✅ GREEN

Built: `commands/work.md` (thin loader) + `skills/work/SKILL.md` (FRAME → single delegate →
preserve → document spine).

Drive trace (SKILL.md logic vs each fixture's manifest → expected decision):

| Fixture | Manifest situation | SKILL.md path exercised | Decision | Expected | Result |
|---|---|---|---|---|---|
| `01-frame-refuses-vague-goal` | goal = "make it better" (uncheckable) | FRAME §2 — goal not checkable → decline; ask for a metric or explicit preservation-only; change nothing | REFUSE | REFUSE | ✅ |
| `02-frame-offramp-trivial` | single Rename, single-skill-sized | FRAME §1 — off-ramp → recommend `/phil:refactor`, exit, no trail opened | OFF-RAMP | OFF-RAMP | ✅ |
| `03-walking-skeleton-end-to-end` | extract tax (code), delegate refactor-loop, oracle green, human confirms | FRAME §2–4 (checkable goal, code→refactor-loop→suite oracle, confirm) → EXECUTE delegates, inherits oracle (no own gate) → VERIFY writes decisions.md + summary | DELEGATE+RECORD | DELEGATE+RECORD | ✅ |

All three slice-01 fixtures reach their expected decision. Key invariants confirmed in the prose:
delegate owns the oracle (ADR-005 — SKILL never runs its own preservation check); a delegate
failure leaves last-good and is not reported done; trivial work is off-ramped; an uncheckable goal
is refused.

## Step 02-01 — MAP roadmap + sequencing gate (slice 02) — ✅ GREEN

Extended `SKILL.md`: added MAP (survey via review-code/spirit-walk/hotspot → ordered editable
roadmap written to `roadmap.md`); upgraded EXECUTE to iterate the roadmap one gated wave at a
time; made resume substantive (continue from first non-`done` wave); sequencing gate now stops the
*rest of the roadmap* and names the failed wave.

Drive trace:

| Fixture | Manifest situation | SKILL.md path | Decision | Expected | Result |
|---|---|---|---|---|---|
| `06-delegate-failure-leaves-last-good` | 3-wave roadmap; wave 1 green, wave 2 delegate red, wave 3 not reached | MAP builds roadmap → EXECUTE: wave 1 `done`+commit; wave 2 delegate reverts → sequencing gate STOPS, wave 3 not run, tree at wave-1 last-good, failure recorded, reported stopped/not-done | STOP-LAST-GOOD | STOP-LAST-GOOD | ✅ |

## Step 03-01 — SAFETY-NET before change (slice 03) — ✅ DONE

Spike resolved inline (coverage-thinness detection): **code** — grep the suite for the wave's
target symbols/files, use coverage if available; unhit target = thin. **Prose** — is the touched
behavior pinned by a self-test fixture / acceptance scenario? No harness or no covering fixture =
thin (no code coverage; the pin is a self-test scenario or a recorded human-approval baseline).

Added the SAFETY-NET step to `SKILL.md` (between MAP and EXECUTE): detect a thin pin → pin current
behavior (characterization tests for code; captured self-test scenarios / human-approval baseline
for prose, delegating authoring where a skill fits) → establish a good baseline → for an
unpinnable seam, fall back to the human-approval gate and flag high-risk (never proceed silently).

Verification: no dedicated fixture in the v1 harness (documented in DISTILL). The behavior
reinforces the sequencing gate already pinned by fixture `06` (a pin that catches a regression
reverts that wave and leaves last-good) and is dogfood-validated per the slice-03 brief. Consistency
re-checked against fixtures `01`, `02`, `03`, `06` — all still reach their expected decisions.

## Step 04-01 — initiative-goal gate (slice 04) — ✅ GREEN

Extended `SKILL.md`: FRAME now records the goal metric's **before** reading; VERIFY is a two-gate
check — preservation gate (every wave's oracle green) AND goal gate (read the after value, compare
to target). A behavior-preserving run that misses the goal is reported **not achieved** with the
`before → after (target)` reading, never done.

Drive trace:

| Fixture | Manifest situation | SKILL.md path | Decision | Expected | Result |
|---|---|---|---|---|---|
| `07-verify-reports-goal-not-met` | preservation green; deps 8→6, target <5 (missed) | VERIFY: preservation gate passes; goal gate reads 6 vs <5 → not met → report "goal not achieved" w/ reading, not done | REPORT-NOT-DONE | REPORT-NOT-DONE | ✅ |
| `01-frame-refuses-vague-goal` (reinforced) | uncheckable goal | FRAME still refuses; now also records the before-reading when checkable | REFUSE | REFUSE | ✅ |

## Remaining (RED until their slice ships)

| Step | Slice | Fixtures | Status |
|---|---|---|---|
| 05-01 | Breadth + routing + evolution | `04`, `05` | RED — pending |
