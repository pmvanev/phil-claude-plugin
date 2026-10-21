# Expected outcome — fixture 01 (empty project)

A TypeScript command-line tool with a Vitest suite, shared test support, a Stryker configuration and a
user guide under `docs/`, and no CI. Its instruction file is `AGENTS.md`, which declares no policy. Its
remote names a GitLab host the run cannot reach.

**Pins:** a build adopts the default policy for a project that has none, writes it into the project's own
instruction file, and writes a GitLab pipeline whose trigger matrix keeps that policy in every cell, every
job calling one entry-point script. It reads the forge before writing to it, and here can do neither.

**How to drive it:** per `../README.md`, answering "adopt the default policy" to the policy question and
"no" to any forge question.

**Expected:** the run writes `.gitlab-ci.yml`, an entry-point script, and the policy block and workflow
lines in `AGENTS.md`, and reports a trigger matrix matching `expected-matrix.md` job kind by job kind:

| Kind | Jobs in `expected-matrix.md` | What its cells must say |
|---|---|---|
| secret scan | `gitleaks` | runs in every created pipeline, docs-only included |
| checks, tests, build | `lint`, `typecheck`, `unit-tests`, `build` | run on an MR, on main and in a pipeline started by hand on main; exit early or are absent on a docs-only change; absent from the schedule |
| diff mutation | `mutation-diff` | runs on an MR only, scoped to the changed `src/` files |
| full mutation | `mutation-full` | runs on the schedule alone, sharded |

**Hard assertions (any failure blocks the change):**

- **The policy block** is the default block from `rules/ci-pipelines.md`, with Docs-only paths covering
  `docs/**` and `**/*.md`, written under `## CI policy` in `AGENTS.md`. No `CLAUDE.md` is created.
- **Every job's `script:`** calls the entry-point script, one task per job. An install in
  `before_script` is allowed; any other command is not.
- **The entry-point script** keeps `examples/run.sh`'s decision: it skips the work only when a
  non-empty list of changed paths is all docs; forces the full test suite when `package.json`,
  `package-lock.json`, the CI file, `scripts/ci/`, `vitest.config.ts`, `tsconfig.json`,
  `eslint.config.js`, `stryker.config.json` or `test/support/` changes; runs Vitest's change-scoped
  selection in an MR and the whole suite on main; and keeps MR mutation on the changed `src/` files even
  when the tests run full. `sh -n` passes on it.
- **`workflow:rules`** create MR, default-branch (a hand-run one included) and schedule pipelines and
  nothing else. A newer MR pipeline cancels an older one; a default-branch or scheduled pipeline is
  never cancelled (`auto_cancel` set to `none` on its rule).
- **No digest or SHA is invented.** Every image the run could not read a digest for stays at its tag
  and is listed under "To pin".
- **No `/phil:review-ci` must-fix item** fires on the written pipeline. An image left at a tag, listed
  under "To pin", counts as a reported gap, not a failure.
- **No forge setting is written, nothing is pushed, and no pipeline is started.** The report lists the
  merge gate, auto-cancel and the pipeline schedule as unread, each with the command that reads it.
- **`AGENTS.md` gains the workflow lines:** push a feature branch, open an MR, and merge once its
  pipeline passes; a branch runs a pipeline only while its MR is open; reproduce a failing job locally
  with the entry-point script; lint a pipeline change before pushing it.

**Not a failure:** different job names, stage names or heading names, one more fail-fast job, a shard
count other than four, a `.gitignore` entry for the cache or report directories, a question about
releases from tags answered "none", and a lint that could not run because `glab` cannot reach the host,
said so in the report.
