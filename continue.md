# Continue — phil:refactor-loop

Resume point for the `/phil:refactor-loop` feature. Last updated 2026-06-18.
Latest commit: **9e6c8a9** (`main`, pushed).

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

## NEXT — a corrected convergence run (held for explicit go)

This is the immediate next action. Nothing has been run successfully end-to-end yet.

1. **Branch for isolation** in the target repo:
   `git -C <target-repo> checkout -b refactor-loop-smoke-test`
   (the harebrain `wumpus` package is the intended target: `python/packages/wumpus`, baseline
   green = 202 unit tests in ~3s; full suite via `uv run pytest`.)
2. **Confirm G2 hook is wired** (`hooks/hooks.json` PreToolUse → `block-test-file-write.py`) —
   already wired + verified.
3. **Invoke the Workflow** with `scriptPath: workflows/refactor-loop.js` and **`args` as a real
   JSON OBJECT** (not a string!):
   ```
   { repo: "C:/Users/PhilVanEvery/Git/github/pmvanev/harebrain/python/packages/wumpus",
     test_cmd: "uv run pytest",        // full suite — the suite is the oracle
     scope: "src/wumpus",
     max_iterations: 3, max_fix_attempts: 2, theta: 0.6 }
   ```
   Start small (`max_iterations: 3`) — it's a machinery-validation run, not exhaustive.
4. **Validate against the §6 convergence checklist** (`architecture.md` §6): no-op baseline,
   the 3 self-test fixtures must all be **rejected** (gate not decorative), variance across runs.
5. **Watch with `/workflows`.** Expect to find and fix real bugs — it's the script's first true
   end-to-end execution. The one unverified assumption: whether `agent({agentType})` resolves
   plugin-defined agents (the script currently inlines prompts, so it doesn't depend on it).

## After the run converges

- Reconcile any bugs the run surfaces; re-commit.
- Decide on **v2**: the disjoint-rubric critic panel (idiom + architecture critics), gated
  behind a *measured* trigger (ADR-002) — only if the single critic demonstrably misses a class
  of problem.
- Optional far future: mplv2 "rigorous edition" (ADR-008) for a standalone, auditable tool.

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
