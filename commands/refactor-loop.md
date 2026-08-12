---
description: "Gated closed-loop refactoring — a separate proposer and correctness critic, hard test gates, a bounded fix sub-loop, and a DAG ledger drive structure-only change until convergence. Orchestrated by the Workflow tool (the deterministic cage)."
argument-hint: "[--changes | function | class | file | directory] [--max-iterations N] [--max-fix-attempts N]"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, Agent, Workflow, TaskCreate, TaskUpdate
---

# phil:refactor-loop

The production substrate is the **Workflow tool** — JS owns the loop, gates, and stop decision
(the cage); the model cannot decide it is done (ADR-008). Red gates enter a bounded fix
sub-loop before a scoped revert; landed refactors are committed per item (ADR-009).

## Step 1 — resolve the target (parity with `/phil:refactor`)

Parse `$ARGUMENTS` into a `scope` (and optional `focus`) the proposer will work on:

| Input | scope | focus |
|---|---|---|
| `--changes` | the files in `git diff HEAD~1 --name-only` (code files only) | — |
| A function name / `file::symbol` | the enclosing file | the function name |
| A class name / `file::Class` | the enclosing file | the class name |
| A file path | that file | — |
| A directory (or no arg → `.`) | that directory (proposer recurses) | — |

`focus` (when set) tells the proposer to narrow to that symbol within the file; otherwise it
refactors across the whole scope.

## Step 2 — gather the required run config

The orchestrator **requires** `repo` and `test_cmd` and will HALT-CONFIG without them
(ADR-009 — it must never guess its target). Determine:

- **repo** — absolute path to the target repo working dir (where git + tests run). Default to
  the current project root if the user is refactoring the repo they're in.
- **test_cmd** — the **full** gate command. Prefer the whole suite, not a narrow slice — the
  suite is the oracle (e.g. `uv run pytest`, which recurses unit/integration/property/acceptance;
  `npm test`; etc.). Read the project CLAUDE.md for a declared command first. A narrow command
  is a weak oracle.

Confirm both with the user before launching, plus that the **G2 hook is wired** (`hooks.json`
PreToolUse → `block-test-file-write.py`); if not, warn that the test-file lockbox falls back to
the cage's in-JS diff scan only.

## Step 3 — invoke the Workflow

The Workflow tool needs opt-in and runs in the background — confirm, then invoke with
`scriptPath: workflows/refactor-loop.js` and **`args` as a real JSON OBJECT** (never a
JSON-encoded string, or every field silently defaults — the first-run misfire):

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
and returns `{ status, iterations, applied, undoable[], invalid[] }`. Relay it — and surface any
`undoable` findings (refactorings proven infeasible, with the reason).

## Optional fallback (`--interactive`)

For step-by-step debugging, load and follow `${CLAUDE_PLUGIN_ROOT}/skills/refactor-loop/SKILL.md` instead — the same
loop as prose the model executes (original substrate, less deterministic; see ADR-008).
