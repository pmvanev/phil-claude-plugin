---
name: refactor-loop
description: Skill bundle for phil:refactor-loop command — gated closed-loop refactoring with a separate proposer and correctness critic, hard test gates, and a DAG ledger
---

# Refactor Loop

> **Substrate note.** The production orchestrator is the **Workflow tool**
> (`${CLAUDE_PLUGIN_ROOT}/workflows/refactor-loop.js`): deterministic JS owns the loop, the gate and the
> stop, so the G7 and G10 hooks are unneeded there and only the G2 test-file lockbox remains. This prose
> skill is the **optional `--interactive` fallback** for step-by-step debugging — the same loop as prose
> the model executes, and less deterministic, because prose can drift. Prefer the Workflow path unless
> inspecting the loop by hand.

Act as the **orchestrator** of a gated refactoring loop — the cage — and own its control flow: the
test gate, the routing decisions, the stop predicate. Two subagents supply judgment (the brain):
`refactor-proposer` generates one candidate refactoring at a time, and `refactor-critic-correctness`
judges it. Keep the gate decision from every subagent, and let no subagent declare the loop done.

This is structure-only work. Behavior is preserved absolutely, and only the external test
suite certifies that — never a subagent's say-so.

The standards are `${CLAUDE_PLUGIN_ROOT}/rules/refactoring.md`, `${CLAUDE_PLUGIN_ROOT}/rules/coding.md`,
and the named refactorings in `${CLAUDE_PLUGIN_ROOT}/rules/refactoring-catalog.md`. The frozen rubric the
critic applies is `${CLAUDE_PLUGIN_ROOT}/refactor/rubric.md`.

## Relationship to /phil:refactor

`/phil:refactor` works a flat `.refactoring-backlog.md` interactively, committing per item.
This loop is different: it runs a closed proposer/critic/gate cycle against a **separate**
DAG ledger, `.refactor-loop-ledger.md` in the project root. The two never share a file and
never collide. Both detect the test runner the same way — see
`${CLAUDE_PLUGIN_ROOT}/skills/shared/test-runner-detection.md`.

## The argument

`$ARGUMENTS` may contain `--max-iterations N` to override the default of **10**. It may also
name a `target_scope` (a file, directory, or `--changes`). With no argument, the scope is
the code files in `git diff HEAD~1 --name-only` and `max_iterations` is 10. Resolve the scope once,
at INIT; it stays fixed for the run, because each green refactor moves HEAD.

---

## The state machine

Run these states in order. Each transition is a deterministic decision you make — not a
subagent's. Track `iter`, starting at 0.

```
INIT ─►PROPOSE ─►REVIEW ─►[GUARD]─►APPLY ─►TEST ──green──►LEDGER ─┐
          ▲         │ reject/≥major │              │              │
          │         └──────────────┘              red             │
          │            back-prompt                 ▼              │
          │            the proposer             REVERT ─► LEDGER ──┤
          │                                  (invalidate deps)     │
          └──────────────── strong-left, iter<max ─────────────────┤
                                                                    │
                              no-actionable / none pending ► DONE ◄──┘
                              iter≥max ────────────────────► HALT (report, don't fake)
```

### INIT  (cage)

1. Work with the session's working directory at the project root, where the hooks look for the
   ledger. If an existing ledger was left `active-run: true` from an interrupted run, say so and clear
   the flag first.
2. Run `git status --porcelain -- . ':!.refactor-loop-ledger.md'` — the ledger is the loop's own
   uncommitted file. If it prints anything, stop and ask the user to commit or stash
   (`git stash push -u -- . ':!.refactor-loop-ledger.md'`) first: REVERT discards uncommitted edits in
   the files it restores. A diff an interrupted run left applied was never gated, so suggest stashing
   it rather than committing it.
3. Detect the test runner using `${CLAUDE_PLUGIN_ROOT}/skills/shared/test-runner-detection.md`.
4. Run the **baseline suite** as a discrete Bash call and read `$?` directly. Guard **G1**:
   if the exit code is non-zero, the suite is red — go straight to **HALT**. Never refactor
   on a red suite (`${CLAUDE_PLUGIN_ROOT}/rules/refactoring.md` §Safety). This is a `stop`.
5. Create or load `.refactor-loop-ledger.md` in the project root (format below). Write its
   header: `runner`, `baseline: green @ <git-sha>`, `iter: 0 / max <N>`, and the `pinned:`
   list. Write the active-run marker, which arms the G2 hook for this run.
6. Snapshot the pinned constraints into the ledger header — the durable, compaction-immune
   source (G7). Default pinned set: `preserve-public-api`, `no-test-file-writes`.
7. If the ledger has no nodes yet, gather candidate smells for the `target_scope`. You may
   run `/phil:review-code <scope>` to seed nodes, then convert its backlog into ledger nodes.
8. Set `iter = 0`. Proceed to PROPOSE. Increment `iter` on every return to PROPOSE, whatever the path
   back — G5, a G6 skip, the green or the red LEDGER — so G8 bounds them all.

### PROPOSE  (brain → cage)

1. **Guard G8 (every step):** if `iter ≥ max_iterations`, go to HALT-INCOMPLETE.
2. Re-assert the pinned constraints from the ledger header (**G7**) before invoking.
3. Invoke `refactor-proposer` via the Task/Agent tool. Pass it the curated state — and only
   that: `pinned_constraints[]`, `ledger_open_nodes[]` (status `pending` only — never pass
   reverted nodes or their invalidated dependents), `last_failure_evidence?`, `target_scope`.
   Do **not** pass prior proposer reasoning traces.
4. If the proposer returns `"no actionable proposal"`, go to **DONE** (T2).
5. **Guard G6 (schema):** if the manifest is not schema-valid JSON (§ proposer output),
   re-ask once. A second malformed return → log it, mark the node `skipped`, return to PROPOSE.
6. Otherwise proceed to REVIEW with the manifest.

### REVIEW  (brain → cage)

1. Invoke `refactor-critic-correctness` via the Task/Agent tool. Pass `{ diff, original_code,
   stated_intent (one line, NOT the proposer's trace), rubric_slice (Slice 1 of
   `${CLAUDE_PLUGIN_ROOT}/refactor/rubric.md`), pinned_constraints }`. Do **not** pass the proposer's
   reasoning — the critic must judge independently.
2. **Guard G6 (schema):** malformed verdict → re-ask once, then skip as above.
3. Proceed to GUARD with the verdict JSON.

### GUARD  (cage — pure boolean, no LLM)

Route on `verdict + severity + confidence`, threshold **θ = 0.6**:

- **G5:** if `verdict = reject`, OR any failing `per_criterion` item (`met: false`) has
  `severity ≥ major` and `confidence ≥ 0.6` → back-prompt the proposer (`llm_self_examine`): return to PROPOSE with
  the failing `per_criterion` items as `last_failure_evidence`.
- If `verdict ∈ {accept, revise}` with no blocking item → proceed to APPLY (T4).
- A `CANNOT_ASSESS` verdict is **not** an accept — back-prompt the proposer, as G5 does. An
  `accept` citing no `file:line` span is coerced to `CANNOT_ASSESS` first (rubric anti-flattery clause).
  A criterion whose `met` is `CANNOT_ASSESS` abstains and is not a failure.

### APPLY  (cage)

1. Confirm the tree is clean — `git status --porcelain -- . ':!.refactor-loop-ledger.md'` prints
   nothing — so HEAD is the pre-APPLY state a revert restores. If it is not, HALT and report.
2. **Guard G2:** refuse any diff that touches a test path — under `tests/`, `test/`, `spec/` or
   `__tests__/`, or named `test_*.py`, `*_test.*`, `*.test.*`, `*.spec.*` or `conftest.py`. Apply
   nothing: record the reason, mark the node `reverted`, and continue at REVERT step 3. The PreToolUse
   hook guards `Edit` and `Write` only, so a diff applied through Bash passes it; this scan is the
   guard, and never attempt a test-file write yourself.
3. Apply the proposer's single diff to disk.

### TEST  (cage)

Run the hard gate as **discrete Bash calls**, reading `$?` after each. A non-zero exit cannot
be narrated past — branch on the actual code.

1. `lint` → read `$?`.
2. `types` (if the project has a type checker) → read `$?`.
3. `tests` → read `$?`.
4. Compute the **actual** test delta and a **public-API diff**:
   - Public-API diff is language-specific. **Python:** `__all__` + top-level `def`/`class`.
     **TypeScript:** exported declarations. For other languages, degrade to the manifest's
     own `public_api_touched` claim (no independent API diff) — note the degradation.
5. **Guard G3 (hard-gate-red):** any non-zero exit → REVERT (chained G3a).
6. **Guard G4 (manifest-mismatch):** the actual test delta contradicts
   `predicted_regressions_risk`, OR the public-API diff contradicts `public_api_touched`
   (e.g. the manifest claims `false` but the API changed) → REVERT. The proposer never
   self-certifies; the measured contract wins.
7. All gates green AND manifest matches → LEDGER (green path, T7).

### REVERT  (cage)

1. **G3a:** `git checkout -- <changed files>` for the files the diff modified, and remove any file the
   diff created, to restore the pre-APPLY state.
2. Record the failing evidence (test output or the mismatch) on the node.
3. Mark the node `reverted`. **Auto-invalidate dependents:** walk the DAG transitive closure
   of the reverted node and set every node that depends on it to `invalid`. Invalidated nodes
   are never passed to a future PROPOSE.
4. Proceed to LEDGER.

### LEDGER  (cage)

1. Mark the current node `resolved` (green) or `reverted`/`invalid` (red path, already done
   in REVERT). On green, commit the changed files, naming the node and its refactoring, so a later
   REVERT cannot reach this work. If the commit fails, HALT and report: the next red gate would
   otherwise wipe this work.
2. **G7:** re-assert the pinned constraints in the ledger header. Update `iter` in the
   header.
3. Prune: scan `pending` nodes for smells the just-applied refactoring incidentally resolved;
   mark them `resolved-incidental`.
4. Evaluate the stop predicate (next).

### DONE  (cage — computed predicate, never a vibe)

Reach DONE on a green suite when the proposer returns `"no actionable proposal"` or no `pending` node
remains, as the Workflow path does. The predicate is computable; the proposer never gets to assert
it.

If the suite was already green with no actionable proposals, report **"nothing to do"** — not
"converged after improvements." A no-op is not a success story.

### HALT  (cage)

Reach HALT when `iter ≥ max_iterations` (**G8**) or the baseline was red (**G1**). Report the
**incomplete** state honestly — what was resolved, what remains, why it stopped. Never narrate
a partial run as success; grade the final state, not the effort.

> **HALT limitation (accepted).** Abort is interrupt-only (Ctrl-C / Esc), plus the G8
> max-iterations HALT. No sentinel-file user-abort (G9) exists — a top-priority abort that would win
> over an in-progress APPLY from every state — so the loop has no abort that is always reachable.

---

## The ledger — `.refactor-loop-ledger.md` (project root)

A dependency **DAG**, not a flat list. A reverted prerequisite voids its dependents.

```markdown
# Refactor-Loop Ledger
runner: pytest
baseline: green @ <git-sha>
iter: 7 / max 10
pinned: [preserve-public-api, no-test-file-writes]
active-run: true

## Nodes
| id   | smell            | span               | depends_on | status     | note |
|------|------------------|--------------------|------------|------------|------|
| R031 | Long Function    | order.py:42-87     | -          | resolved   | Extract Function, green @sha |
| R042 | Feature Envy     | order.py:90-110    | R031       | reverted   | red: test_discount; deps invalidated |
| R043 | Primitive Obsess | order.py:90-110    | R042       | invalid    | auto: prerequisite R042 reverted |
| R051 | Magic Number     | tax.py:12          | -          | pending    | |
```

Status lifecycle:

```
pending ─►(applied+green)─► resolved
pending ─►(applied+red, or touches a test path)──► reverted ──► [each n with this node in depends_on → invalid]
pending ─►(manifest or verdict malformed twice)──► skipped
pending ─►(smell gone)───► resolved-incidental
```

The header (`runner`, `baseline`, `iter`, `pinned`, `active-run`) is the durable,
compaction-immune source. Re-read it each iteration; do not trust the rolling context for the
pinned constraints. `active-run: true` plus the ledger's existence is the sentinel that arms the G2
hook. Clear `active-run` at DONE/HALT. An interrupt (Ctrl-C / Esc) reaches neither, so the flag stays
set and blocks test-file edits in that directory until cleared — say so whenever a run is
interrupted, and INIT clears it on the next run.

---

## The guard set (G1–G10)

| Guard | Fires at | Predicate | Outcome class | Where enforced |
|---|---|---|---|---|
| **G1** baseline-green | INIT suite finishes | suite exit ≠ 0 | `stop` → HALT | this skill (Bash `$?`) |
| **G2** test-file-write-block | before APPLY, and any Edit/Write | path matches test glob | `stop` | this skill's diff scan + **PreToolUse hook** (Edit/Write only) |
| **G3** hard-gate-red | TEST suite finishes | exit ≠ 0 | `stop` + G3a | this skill (Bash `$?`) |
| **G3a** auto-revert | chained from G3 | — | `invoke_action` | `git checkout`, and removing created files |
| **G4** manifest-mismatch | TEST finishes | actual delta ≠ manifest, or API diff ≠ claim | `stop` + G3a | this skill |
| **G5** verdict-route | post-REVIEW | reject ∨ (severity≥major ∧ conf≥0.6) | `llm_self_examine` | this skill (back-prompt) |
| **G6** schema-valid | proposer/critic finishes | output not schema-valid | `llm_self_examine` | this skill (re-ask once) |
| **G7** pinned-reinject | every LEDGER / iteration boundary | always | `invoke_action` | this skill (hook not wired) |
| **G8** max-iterations | every step | `iter ≥ max` | `stop` → HALT-INCOMPLETE | this skill |
| **G10** anti-premature-exit | session Stop | DONE predicate not satisfied | `invoke_action` | this skill (hook not wired) |

Guards are essentially free to evaluate — gate liberally on the recurring invariants
(red suite, test-file touched, public-API changed, max-iterations). Do not hand-author a
guard per code smell; that is the rubric's job.

> **G9 (user-abort sentinel) does not exist.** See the HALT limitation note above.

---

## Hooks — what ships, and what is prose here

Three hooks back this loop: **G2** (PreToolUse test-file write-block), **G10** (Stop
anti-premature-exit, gated on the `active-run` sentinel), and **G7** (UserPromptSubmit pinned
re-inject). **G2 ships wired** in the plugin's own hooks. **G7 and G10 are not wired**: in this
fallback, G7 is re-reading the ledger header every iteration, and G10 is stopping only on the DONE
predicate or a HALT. The scripts live in `${CLAUDE_PLUGIN_ROOT}/hooks/refactor-loop/` and the exact `hooks.json`
merge snippet is in `${CLAUDE_PLUGIN_ROOT}/hooks/refactor-loop/README.md`.

Merge new entries into existing hook config; never overwrite it. If wiring risks clobbering existing
config, leave it to the user: tell them to run the `update-config` skill with the snippet from the
README rather than editing config blindly. Surface this as the one item needing human follow-up.

Until G7 and G10 are wired, their checks are the prose above; wiring them adds defence in depth.

---

## Self-test

`${CLAUDE_PLUGIN_ROOT}/refactor/self-test/` holds deliberately-bad refactorings that the loop **must**
reject — a diff that breaks a test (must REVERT at G3), a diff that broadens the public API while
claiming `public_api_touched: false` (must REVERT at G4), and a "perfect refactor!" verdict with no span
(must be coerced to `CANNOT_ASSESS`). These are the regression gate for the frozen rubric: run them whenever
`${CLAUDE_PLUGIN_ROOT}/refactor/rubric.md` changes. See that directory's README.

---

## Safety rules

- Never refactor on a red suite. G1 halts at baseline; G3 reverts mid-loop.
- One refactoring per gate pass — each breakage is attributable to one change, and revert restores
  that one change.
- The proposer never edits tests and never runs the suite; the critic never edits or runs
  anything. Behavior preservation is certified only by the external suite plus the
  manifest-vs-actual check.
- More iterations is not better. The `max_iterations` cap is a feature; a loop that keeps
  going is not a loop that is improving.
- Report the final state honestly at DONE and HALT. Never fake success.
