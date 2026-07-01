# Continue — phil:refactor-loop

Resume point for the `/phil:refactor-loop` feature. Last updated 2026-07-01.
Latest commit: **f881b48** (`main`, local — the two smoke-run hardening fixes).

> **MILESTONE (2026-07-01): first successful end-to-end run.** The convergence
> run below is DONE — the machinery is validated. See "First successful run"
> before planning next steps.

---

## What this is

A new, gated **closed-loop refactoring autopilot** built *alongside* the existing
`/phil:refactor` (which is untouched). Loop: propose → critique → apply → test → (fix sub-loop)
→ commit-or-revert, repeated until convergence. Orchestrated by the **Workflow tool** (the
deterministic "cage"); a separate proposer and correctness critic are the only LLM "brain"
leaves. Grounded in research (the harebrain corpus) and a cited gap analysis.

## How it was built (the trail)

research → patch design (`rgr-loop.md`) → gap analysis → architecture/ADRs → forge agents →
substrate pivot to Workflow → first run (post-mortem) → ADR-009 redesign. All committed.

## Current state — DONE

- **Design** (all in `docs/design/refactor-loop/`): `architecture.md` + ADR-001..009 +
  `wave-decisions.md`. Gap memo: `docs/research/refactor-loop/rgr-loop-gap-analysis.md`.
  Grounded design notes: `rgr-loop.md` (root).
- **Orchestrator**: `workflows/refactor-loop.js` (Workflow tool; the cage). `node --check` clean.
- **Agents**: `agents/refactor-proposer.md` (returns a diff as text, no Edit/Bash),
  `agents/refactor-critic-correctness.md` (read-only, span+evidence verdicts).
- **Command**: `commands/refactor-loop.md` (parses target, gathers args, invokes the Workflow).
  Fallback prose substrate: `skills/refactor-loop/SKILL.md` (`--interactive`).
- **Rubric**: `refactor/rubric.md` (correctness slice active; idiom/architecture stubbed for v2).
- **Hooks** (Python): `hooks/refactor-loop/*.py`. Only **G2** (test-file write-block) is wired
  in `hooks/hooks.json` and **functionally verified**. G7/G10 are obviated under the Workflow
  (interactive-fallback only).
- **Self-test fixtures**: `refactor/self-test/` (3 must-be-rejected cases).

## Key decisions (ADRs)

- **ADR-008**: Workflow tool is the v1 orchestrator (not the prose skill). Keep G2 hook, drop
  G7/G10. mplv2 statecharts = the rigorous "v2+" option if this becomes a standalone tool.
- **ADR-009** (post first-run): revert is a last resort behind a bounded **FIX sub-loop**;
  reverted nodes are marked **`undoable`** with findings; **commit-on-green**; **scoped revert**
  (never `git checkout -- .`); **fail-fast** on missing `repo`/`test_cmd`; **no-test → HALT**.

## First-run post-mortem (run wf_3138f9d2-f13, 2026-06-18)

Misfired because `args` were passed as a JSON **string**, not an object → every field defaulted
→ it refactored THIS plugin repo with a decorative (no-test) gate, then `git checkout -- .`
wiped the tree. Recovered fully. It validated the machinery end-to-end (G3/G4 guards fired) and
confirmed the bugs ADR-009 now fixes. Lesson baked into the code: missing `repo`/`test_cmd` →
HALT-CONFIG; and `args` MUST be a real JSON object.

---

## First successful run (run wf_dfe9faa4-5a4, 2026-07-01) — machinery VALIDATED

Target: harebrain `python/packages/wumpus`, on throwaway branch `refactor-loop-smoke-test`
(since discarded). `args` passed as a real JSON object. Result: **`HALT-INCOMPLETE`, 3/3
refactors landed green & committed** (R001–R003, all duplication removal in `engine/game.py`,
net −115 lines), **zero reverts / undoable / invalid**. 20 agents, ~29 min, 766k tokens.

§6 checklist outcomes:
- **Non-decorative gate** ✅ — 202 real unit tests collected + run every iteration (baseline non-zero).
- **Real structure-only refactors** ✅ — spot-checked R001 (six 10-field `World(...)` copies →
  `dataclasses.replace`); independent post-run re-run green (202 passed).
- **Commit-on-green, one per refactor** ✅ (ADR-009).
- **Scoped revert never destructive** ✅ — only `game.py` touched.
- **FIX sub-loop (ADR-009 A) exercised & worked** ✅ — R003's first `git apply` failed →
  `fix#3.1` produced a corrected diff → green. This is the key ADR-009 mechanism, now proven.
- **NOT yet exercised** ⧗ — self-test fixture rejection (adversarial critic), cross-run variance.

**Oracle note:** the full suite (`uv run pytest`) is NOT usable as the gate — it hangs >17 min on
the subprocess/acceptance tier (a harebrain issue, not ours). Used `uv run pytest tests/unit`
(202 tests, ~2s). For future runs pick a fast, deterministic tier as `test_cmd`.

**Two bugs found & fixed** (committed f881b48):
1. **args string-vs-object footgun** — the run-1 misfire class, *still live* (ADR-009 only
   documented it). The cage now normalizes `args` as either an object or a JSON string.
2. **Gate timeout blindness** — gate agents used the 120s Bash default; a slow-but-green suite
   read as a red gate. Prompt now instructs max 600s and reports a kill as `exit_code:-1`.

## NEXT — optional follow-ups (nothing blocking)

- **Adversarial gate proof**: run the 3 `refactor/self-test/` fixtures through the critic and
  confirm all are **rejected** (the one §6 check the happy-path run didn't cover).
- **Variance run**: a second convergence run to confirm non-determinism across runs.
- **Decide on v2**: the disjoint-rubric critic panel (idiom + architecture critics), gated behind
  a *measured* trigger (ADR-002) — only if the single critic demonstrably misses a class of problem.
- Optional far future: mplv2 "rigorous edition" (ADR-008) for a standalone, auditable tool.
- Housekeeping: `continue.md` latest-commit line is local-only; push `main` when ready.

## Quick file map

```
workflows/refactor-loop.js              # the cage (orchestrator)
agents/refactor-{proposer,critic-correctness}.md
commands/refactor-loop.md               # entry point / arg parsing
skills/refactor-loop/SKILL.md           # interactive fallback substrate
refactor/rubric.md, refactor/self-test/ # frozen rubric + gate self-tests
hooks/refactor-loop/*.py, hooks/hooks.json   # G2 wired; G7/G10 fallback-only
docs/design/refactor-loop/              # architecture.md + ADR-001..009 + wave-decisions.md
docs/research/refactor-loop/rgr-loop-gap-analysis.md
rgr-loop.md, todo.md                    # grounded design notes / running todo
```
