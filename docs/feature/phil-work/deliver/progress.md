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

## Remaining (RED until their slice ships)

| Step | Slice | Fixtures | Status |
|---|---|---|---|
| 03-01 | SAFETY-NET (spike-gated) | (dogfood + `06`) | RED — pending |
| 04-01 | Initiative-goal gate | `07` (+ reinforces `01`) | RED — pending |
| 05-01 | Breadth + routing + evolution | `04`, `05` | RED — pending |
