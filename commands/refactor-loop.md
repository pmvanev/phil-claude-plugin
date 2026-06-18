---
description: "Gated closed-loop refactoring — a separate proposer and correctness critic, hard test gates, and a DAG ledger drive structure-only change until convergence. Orchestrated by the Workflow tool (the deterministic cage)."
argument-hint: "[--max-iterations N] [--scope file-or-dir] [--interactive]"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, Agent, Workflow, TaskCreate, TaskUpdate
---

# phil:refactor-loop

The production substrate is the **Workflow tool** — the JS owns the loop, gates, and stop
decision (the cage); the model cannot decide it is done (ADR-008).

**Default (Workflow):** confirm with the user (the Workflow tool needs opt-in and runs in the
background), then invoke it with the shipped orchestrator script and the parsed arguments:

- script: `workflows/refactor-loop.js`
- args: `{ max_iterations: <N or 10>, theta: 0.6, scope: "<path or '.'>" }`

Before invoking, ensure the **G2 test-file write-block hook is wired** (`hooks/refactor-loop/`
+ `hooks/hooks.json`) — it is the one safety boundary that must hold under the Workflow
substrate (proposer-can't-edit-tests). If it is not wired, warn the user that the test-file
lockbox is not yet platform-enforced.

The Workflow runs the INIT→PROPOSE→REVIEW→GUARD→APPLY→TEST→{LEDGER|REVERT}→{DONE|HALT} loop,
writes a DAG ledger to `.refactor-loop-ledger.md`, and returns a status object. Relay the
result (status, iterations, applied/reverted node ids).

**Optional fallback (`--interactive`):** for interactive, step-by-step debugging, load and
follow `skills/refactor-loop/SKILL.md` instead — the same loop expressed as prose the model
executes (the original substrate, retained for inspection; less deterministic — see ADR-008).
