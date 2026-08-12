> **Historical record — not a live resume point.**
>
> This file was `continue.md` at the repository root, hand-maintained as a resume point for the
> `phil:refactor-loop` build. It is preserved here because it is the **only** narrative record of
> that feature — `docs/evolution/` had no `refactor-loop` entry — and it is moved because a
> hand-maintained resume point at the root is exactly the second-authority drift that
> `/phil:handoff` and `/phil:resume` exist to prevent. The plugin validator flagged it as
> *"precisely the second-authority drift the new skill exists to prevent, left standing in the
> skill's own repo."*
>
> Everything below is as of **2026-07-01**, pinned to commit `f881b48`, and has not been updated
> since. Read it as history. For where work actually stands now, run `/phil:resume`, which will tell
> you whether what it holds is current before it tells you anything else — the property this file
> never had.

---

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

---

## Appendix — retired `todo.md` (2026-08-12)

The repo root also carried `todo.md`, a 20-line hand-maintained list. Both of its top-level items were
marked `DONE`; nothing in it was live. It is preserved verbatim here rather than scattered, because
its subject is this feature — the second item (language idioms in rules/) is the lone exception and is
one line.

Retired for the same reason as `continue.md`, of which it was the sibling: a hand-maintained backlog
at the repo root is a second authority beside the issue board, and it is the drift `/phil:handoff` and
`/phil:resume` exist to prevent. The board now holds the backlog (issues #1–#12).

```markdown
- refactor,green,review agent loop
  - DECISION (2026-06-17): keep /phil:refactor AS-IS. Build a SEPARATE new /phil:refactor-loop skill alongside it. The two coexist (phil:refactor = controlled walk through a reviewed backlog; phil:refactor-loop = gated autopilot). Deliverables are skills+agents, so construct via nw:forge (5-phase agent-builder), NOT traditional acceptance-test/Outside-In TDD.
  - Full grounded design: rgr-loop.md (now patched with the 8-item gap analysis). Gap memo: docs/research/refactor-loop/rgr-loop-gap-analysis.md. Corpus lives in sibling repo: ../harebrain/docs/research-summaries.
  - SUBSTRATE DECISION (2026-06-18, ADR-008): orchestrator = Workflow tool (workflows/refactor-loop.js), NOT the prose skill-loop. Deterministic JS owns loop/gate/stop. Prose skills/refactor-loop/SKILL.md kept as --interactive fallback. Hooks are PYTHON now (.ps1 removed; notify-stop.ps1 left as-is). Only G2 stays a hook (defense-in-depth); under Workflow the real test-file lockbox is the cage's in-JS diff scan; G7/G10 obviated (interactive-fallback only). mplv2 = rigorous v2+ option (its ledger = the audit trail the gap memo wants).
  - DONE: research->design->forge->workflow-pivot committed; G2 hook wired+verified; **first successful end-to-end run 2026-07-01** (harebrain wumpus, HALT-INCOMPLETE, 3/3 refactors landed green, FIX sub-loop proven, net -115 LOC; run wf_dfe9faa4-5a4). Machinery VALIDATED. Fixed 2 bugs during the run (args string-vs-object footgun + gate timeout blindness), committed f881b48. See docs/evolution/2026-07-01-refactor-loop.md (was continue.md) "First successful run".
  - PENDING (optional, non-blocking): adversarial gate proof (run refactor/self-test fixtures through critic -> must all be rejected); cross-run variance run; v2 critic panel deferred behind measured trigger (ADR-002). NOTE: harebrain full suite hangs >17min (subprocess/acceptance tier) -> use a fast test tier as test_cmd, not `uv run pytest`.
  - Idea: closed-loop review -> refactor+test -> re-review until quality crosses a threshold.
  - A FRESH review subagent each pass = independent perspective (avoids rubber-stamping its own work; adversarial-verify pattern).
  - Review is read-only and returns a structured artifact (.refactoring-backlog.md) -> ideal subagent task. The backlog file is the natural convergence ledger.
  - Termination is the hard part. Don't loop on "review finds nothing" (subjective naming never converges). Instead:
    - Objective threshold: loop until ZERO Priority 1-2 findings (correctness + structure). Treat P3-P7 as advisory.
    - Loop-until-dry: stop after a pass yields no NEW actionable items (1-2 consecutive near-clean passes).
    - Hard iteration cap (e.g. 5) so a thin test suite can't fund infinite churn.
    - Carry a seen/resolved set across passes so reverted/won't-fix items don't reappear and block convergence.
  - Keep refactoring in the MAIN loop, sequential, one commit per item (preserves test-green-before/after, undo-on-failure, per-item commit hygiene, user visibility). Only use worktree-isolated subagents if refactoring items in parallel -- which conflicts with the one-atomic-change discipline. Don't.
  - Add a coverage/mutation gate at the start: tests passing != behavior preserved when coverage is thin; the loop's safety rests entirely on the suite.
  - Build options: (a) new phil:refactor-loop skill that calls the Agent tool per review pass (finally uses the dead `Agent` entry already in refactor.md's allowed-tools), or (b) a Workflow (needs explicit opt-in). For a shipped plugin skill, prefer (a) -- self-contained, no opt-in.
  - Possible shape: gate -> loop(max N){ backlog = fresh-review-subagent(code); new = backlog.P1P2 - seen; if empty break; refactor each in main loop (test, commit); seen += resolved } -> report P3-P7 advisory.
- language idioms in rules/standards/review-skill
  - DONE: added rules/cpp.md, python.md, typescript.md, react.md (path-scoped frontmatter) and wired into review-code SKILL.md as Priority 7 - Language Idioms.
```

