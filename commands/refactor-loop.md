---
description: "Gated closed-loop refactoring — a separate proposer and correctness critic, hard test gates, a bounded fix sub-loop, and a DAG ledger drive structure-only change until convergence. Orchestrated by the Workflow tool (the deterministic cage)."
argument-hint: "[--changes | function | class | file | directory] [--max-iterations N] [--max-fix-attempts N]"
mutates: true
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, Agent, Workflow, TaskCreate, TaskUpdate
---

# phil:refactor-loop

The **Workflow tool** is the production substrate: its script owns the gates and the stop decision, so the
model cannot decide it is done. Red gates enter a bounded fix sub-loop before a scoped revert; each landed
refactor is committed on its own.

## Step 1 — resolve the target (parity with `/phil:refactor`)

Parse `$ARGUMENTS` into a `scope` (and optional `focus`) the proposer will work on:

| Input | scope | focus |
|---|---|---|
| `--changes` | the files in `git diff HEAD~1 --name-only` (code files only) | — |
| A function name / `file::symbol` | the enclosing file | the function name |
| A class name / `file::Class` | the enclosing file | the class name |
| A file path | that file | — |
| A directory (or no arg → `.`) | that directory (proposer recurses) | — |

`focus`, when set, narrows the proposer to that symbol within the file; otherwise it refactors across
the whole scope.

## Step 2 — gather the required run config

The workflow **requires** `repo` and `test_cmd` and halts with `HALT-CONFIG` without them; it never
guesses its target. Determine:

- **repo** — the absolute path of the target repo's working directory, where git and the tests run.
  Default to the current project root when the user is refactoring the repo they are in.
- **test_cmd** — the **full** gate command. Prefer the whole suite to a narrow slice: the suite is the
  oracle (e.g. `uv run pytest`, which recurses unit, integration, property and acceptance tests; `npm
  test`), and a narrow command is a weak one. Read the project's `CLAUDE.md` for a declared command first.

Confirm both with the user before launching, and confirm the test-file lockbox hook (G2) is wired:
`hooks.json` `PreToolUse` → `block-test-file-write.py`. If it is not, warn that the lockbox falls back
to the workflow's own diff scan only.

## Step 3 — invoke the Workflow

The Workflow tool needs opt-in and runs in the background — confirm, then invoke with
`scriptPath: workflows/refactor-loop.js` and **`args` as a JSON object**:

```
args: {
  repo: "<abs path>",            // required
  test_cmd: "<full suite cmd>",  // required
  scope: "<path>",               // from Step 1
  focus: "<symbol>",             // optional, from Step 1
  max_iterations: <N or 10>,
  max_fix_attempts: <N or 2>,
  theta: 0.6
}
```

The loop runs INIT→PROPOSE→REVIEW→GUARD→APPLY→TEST→(FIX sub-loop)→{commit | undoable+revert}→
{DONE | HALT}, commits each landed refactor, writes a DAG ledger to `<repo>/.refactor-loop-ledger.md`,
and returns `{ status, iterations, applied, undoable[], invalid[] }`. Relay it, and surface every
`undoable` finding — a refactoring proven infeasible — with its reason.

## Optional fallback (`--interactive`)

For step-by-step debugging, load and follow `${CLAUDE_PLUGIN_ROOT}/skills/refactor-loop/SKILL.md`
instead: the same loop as prose the model executes, and less deterministic.
