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

## Step 1 — resolve the target

Take `--interactive`, `--max-iterations N` and `--max-fix-attempts N` out of `$ARGUMENTS` first. With
`--interactive`, skip to *Optional fallback*. Parse the rest into a `scope` (and optional `focus`) the
proposer will work on:

| Input | scope | focus |
|---|---|---|
| `--changes` | the code files in `git diff HEAD~1 --name-only`, joined with spaces | — |
| A function name / `file::symbol` | the enclosing file | the function name |
| A class name / `file::Class` | the enclosing file | the class name |
| A file path | that file | — |
| A directory (or no arg → `.`) | that directory (proposer recurses) | — |

`focus`, when set, narrows the proposer to that symbol within the file; otherwise it refactors across
the whole scope.

## Step 2 — gather the required run config

The workflow **requires** `repo`, `test_cmd` and `plugin_root` and halts with `HALT-CONFIG` without them;
it never guesses its target. `plugin_root` is fixed in Step 3. Determine:

- **repo** — the absolute path of the target repo's working directory, where git and the tests run.
  Default to the current project root when the user is refactoring the repo they are in.
- **test_cmd** — the **full** gate command. Prefer the whole suite to a narrow slice: the suite is the
  oracle (e.g. `uv run pytest`, which recurses unit, integration, property and acceptance tests; `npm
  test`), and a narrow command is a weak one. Read the project's `CLAUDE.md` for a declared command first.

Confirm both with the user before launching.

Run `git -C <repo> status --porcelain -- . ':!.refactor-loop-ledger.md' ':!.refactor-loop-patch.diff' ':!.refactor-loop-commit-msg'`
— the ledger, the patch file and the commit message file are the loop's own uncommitted files. If it prints anything, stop and
ask the user to commit or stash (`git stash -u`) first: a red gate reverses the diff with `git apply -R`,
which halts the run when uncommitted edits overlap it, and a landed refactor commits whole files.

The workflow's own diff scan refuses any proposal that touches a test file. The plugin's
`block-test-file-write.py` hook guards `Edit` and `Write` only, and the workflow applies diffs with `git
apply`, so the hook does not fire on this path.

## Step 3 — invoke the Workflow

The Workflow tool needs opt-in and runs in the background — confirm, then invoke with
`scriptPath: ${CLAUDE_PLUGIN_ROOT}/workflows/refactor-loop.js` and **`args` as a JSON object**, numbers
as numbers:

```
args: {
  repo: "<abs path>",            // required
  test_cmd: "<full suite cmd>",  // required
  plugin_root: "${CLAUDE_PLUGIN_ROOT}", // required: the workflow names the rules from it
  scope: "<path>",               // from Step 1
  focus: "<symbol>",             // optional, from Step 1
  max_iterations: <N or 10>,
  max_fix_attempts: <N or 2>,
  theta: 0.6
}
```

The loop runs INIT→PROPOSE→REVIEW→GUARD→APPLY→TEST→(FIX sub-loop)→{commit | undoable+revert}, commits each
landed refactor, and writes a DAG ledger to `<repo>/.refactor-loop-ledger.md`. It ends in `DONE` (nothing
left worth refactoring), `HALT-INCOMPLETE` (out of iterations), `HALT-CONFIG` (a required argument
missing) or `HALT` (a red or empty baseline suite, a failed proposer, or a revert or commit that failed —
the working tree then still holds that diff). Relay the status; on any halt,
relay its `reason`, and on a red baseline its `baseline` output. A finished run also returns
`{ iterations, applied, undoable[], invalid[] }`: surface every `undoable` finding with its reason — a
refactoring judged infeasible, a diff that touched a test file or would not apply, one that stayed red or
changed the public API unpredicted after its fix attempts, or one whose fix agent failed.

## Optional fallback (`--interactive`)

For step-by-step debugging, load and follow `${CLAUDE_PLUGIN_ROOT}/skills/refactor-loop/SKILL.md`
instead: the same loop as prose the model executes, and less deterministic. Say what differs before
starting: with no target the skill takes the latest git changes, not `.`, and it reads no `focus` and no
`--max-fix-attempts`.
