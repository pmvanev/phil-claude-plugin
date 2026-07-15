# Slice 02 — The hard half: oracle detection + hard/soft partition

**Goal.** On a target that HAS an oracle (a code target with a test suite), detect it, **partition**
findings into hard-checkable vs soft (C2), **run the hard checks**, and label the verdict a
**SOUND GATE** — while the soft findings still flow through the slice-01 spine.

## IN scope
- Oracle detection for code targets — reuse `skills/shared/test-runner-detection.md`.
- The hard/soft **partition** (C2): each finding tagged `hard` or `soft`.
- Run the hard checks (or, when an oracle result is already available, **inherit** it — ADR-005
  lineage, never re-implement).
- Honesty label upgrade: oracle-backed hard findings → `sound-gate`; soft-only remainder stays
  `draft-signal`.

## OUT of scope
- Editing any existing host skill to consume the verdict (DESIGN D-scope: standalone only, zero
  host edits — deferred to each host's own future work per ADR-010).
- Oracle types beyond a test suite + the WS prose checks (broader prose-oracle catalog) — note as future.

## Composition contract (DOC-ONLY — no host edits)
Publish the reusable contract so a future host / workflow can adopt it mechanically:
- The agent's typed input/output contract (`{target, intent, standards}` → typed verdict) is
  documented in `agents/adversarial-reviewer.md`.
- The SKILL documents the ad-hoc Workflow-weaving pattern: call the agent via `agent()` / Task,
  read the typed verdict, route on `severity` + `overall_label` (never treat `draft-signal` as a
  passed gate). No existing skill is modified.

## Learning hypothesis
- **Confirms**: a hard/soft partition backed by a real oracle yields a sound-gate verdict that
  carries signal beyond running the suite alone (it localizes + explains, and pairs hard failures
  with adversarial soft findings).
- **Disproves**: the hard findings merely duplicate what the suite already reports — the partition
  adds nothing over `npm test`, so the hard half is not worth its complexity.

## Acceptance criteria
- AC1: on a code target with a detectable runner, the verdict is labeled `sound-gate` and every
  finding is tagged `hard` or `soft`.
- AC2: a hard finding cites the actual check result (exit code / failing test), not a prediction.
- AC3: on a target with no detectable oracle, behavior degrades to slice-01 (`draft-signal`) — the
  label is never `sound-gate` without an oracle (C4 regression guard).

## Production data (not synthetic)
Review a real code change in a repo with a real suite.

## Dogfood moment
Run against a real code target the same day.

## Dependencies
Slice 01. Reuse `skills/shared/test-runner-detection.md`, ADR-005 lineage.

## Effort / reference class
Small–medium. Reference class: refactor-loop's INIT/TEST oracle handling.
