---
name: build-ci
description: This skill should be used when the user asks to "set up CI", "set up GitLab CI", "set up GitHub Actions CI", "write our .gitlab-ci.yml", "only run pipelines for MRs", "make the pipeline match our CI policy", "add mutation testing to CI", or runs /phil:build-ci. It declares the CI policy, writes or edits the pipeline so every trigger-matrix cell keeps it, with each job calling one entry-point script, lints the result, and asks before changing a forge setting.
---

# Build CI

Build a project's pipeline to a declared policy, then prove it with the trigger matrix. Read
`${CLAUDE_PLUGIN_ROOT}/rules/ci-pipelines.md` whole on every run: its Principles say how to shape the
pipeline, its declared-policy section gives the default block, and its Always-flag rows say what a built
pipeline must never be. Read from `${CLAUDE_PLUGIN_ROOT}/rules/security.md` the **Supply chain and
build** table, the privilege row and the credential-literal row: a built pipeline pins what it runs,
installs from the lockfile, grants the narrowest token and holds no credential.

**This skill writes repository files and reads the forge.** It writes the CI files, `scripts/ci/run.sh`,
the project's instruction file, a hash-pinned lockfile for the tools CI installs where the project has
none, and `.gitignore` entries for what the jobs leave behind, and nothing else.
**Write no forge setting without an answer** — the merge gate, branch protection, auto-cancel, a pipeline
schedule. `glab api` and `gh api` can write as well as read: send a `POST`, `PUT` or `PATCH` only after a
yes, and never one that starts a pipeline. **Never push**, and never start a pipeline: a lint's dry run
creates none, and a push to find out is a guess sent to a runner. **Write no digest or SHA you did not
read** from a registry or the forge. Every ask follows `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`;
load it before the first `AskUserQuestion` call.

## Parse the Argument

A directory: the project rooted there. No argument: the repository root.

## Step 1: Survey the Project

Read before proposing anything; the project may already have decided.

- **The forge and its default branch.** GitLab or GitHub, from `git remote get-url origin` and any CI
  file present. The default branch from `git symbolic-ref --short refs/remotes/origin/HEAD`; failing
  that, the one local branch named `main` or `master`; failing both, ask.
- **The pipeline already there.** With a CI file present this run edits; gather the whole pipeline as
  `${CLAUDE_PLUGIN_ROOT}/skills/review-ci/SKILL.md` Step 1 does, and keep every job a recorded decision
  explains.
- **Recorded decisions.** ADRs, and dated decisions in `CLAUDE.md` or `AGENTS.md` about CI, mutation,
  schedules, deploys, releases and runners. A recorded decision outranks the default block.
- **What each job would run.** The project's own commands: the test runner, linter, type checker, build,
  mutation tool and deploy, from its task runner (`package.json` scripts, a `Makefile`, a `justfile`, a
  repository CLI) and its manifests. Name what is missing; never invent a command. Call each check so its
  failure fails the job: a wrapper that reports and exits 0 gates nothing, however useful it is
  elsewhere. Where the tools CI installs have no lockfile, write one with hashes — `uv pip compile
  --generate-hashes`, `npm install --package-lock-only` — and install from it, `pip` with
  `--require-hashes`. A project with no
  secret scanner gets gitleaks, in its own job and image: the policy's secret scan needs one.
- **Change classes.** The areas a change can touch — packages, apps, services — and the selector's own
  inputs: the lockfile and manifest, the CI configuration, `scripts/ci/`, shared test files, the build,
  lint and mutation configuration.
- **Documentation paths.** Where the docs live — and a path the suite or a check reads is never docs,
  whatever its folder is called: grep the tests and check scripts for each candidate path. In a
  repository whose product is prose — skills, rules, specifications in markdown — ask which markdown is
  product before calling any of it docs.

## Step 2: Declare the Policy

- **A `## CI policy` block exists:** use it. Raise a question only where the survey contradicts a field.
- **None exists:** propose the default block `ci-pipelines.md` gives, with its Docs-only paths taken from
  the survey and every field a recorded decision changes rewritten to that decision, naming it. Ask once
  whether to adopt it as shown or change a field.
- A field the project cannot yet keep — mutation where no mutation tool is installed — is the user's
  call: ask, and write what they decide. The policy has no field for releases; where the project tags
  releases, ask what a tag pipeline runs.

Write the block under `## CI policy` in the project's instruction file, in the rule's shape: its
`CLAUDE.md`, or its `AGENTS.md` where that is the file it keeps; with neither, create `CLAUDE.md`.

## Step 3: Map Each Change to Its Jobs

Write a table for the report: each change class against the jobs it starts and their scope. Choose the
selection the project's tools already offer, in this order:

1. **The build tool's dependency graph** — Nx `affected`, Bazel reverse dependencies, Turborepo filters.
2. **The test runner's own** — Vitest `--changed`, Jest `--changedSince`.
3. **Path lists per area**, with a guard that fails closed: a changed path no list names, outside the
   docs allow-list, runs the full suite (PIPE-22).

A change-scoped task scopes where its tool can and runs whole where it cannot; a type check and a build
run whole. A changed selector input widens the tests only (PIPE-20): mutation stays on the MR's changed
source files, and the schedule mutates the whole codebase (PIPE-23). Pass the changed files to the
mutation tool's own filter — StrykerJS `--mutate`, Stryker.NET `--since`, cargo-mutants `--in-diff` —
and exit 0 when no source file changed. Shard the scheduled run with GitLab `parallel:` or a GitHub
matrix, into no more shards than there are source files; a tool with no shard flag, such as StrykerJS,
gets its file list split by shard index in the script, which `./scripts/ci/run.sh shard` prints.

## Step 4: Write the Entry-Point Script

**Every job calls the entry-point script, one task per job; the CI file holds triggers, stages and
wiring.** Write `scripts/ci/run.sh` in POSIX `sh` from `${CLAUDE_PLUGIN_ROOT}/skills/build-ci/examples/run.sh`,
whose decision `tests/test_build_ci.py` pins. Keep its decision and its broad patterns
(`vitest.config.*`, not `vitest.config.ts`); add this project's own paths, drop only another forge's CI
paths, and point each task at the project's own task runner. Mark it executable with
`chmod +x scripts/ci/run.sh`.

The decision, which `./scripts/ci/run.sh scope` prints as `docs-only`, `scoped` or `full`:

- **The source and its base.** GitLab: `$CI_PIPELINE_SOURCE`, an MR measured against
  `$CI_MERGE_REQUEST_DIFF_BASE_SHA`, a push against `$CI_COMMIT_BEFORE_SHA`. GitHub: `$GITHUB_EVENT_NAME`,
  with the base passed through the workflow's `env:` as
  `BASE_SHA: ${{ github.event.pull_request.base.sha || github.event.before }}`. Locally: the merge base
  with `origin/<default branch>`. Any other source, an all-zeros base, or a base the clone lacks runs
  full.
- **The changed paths**, from `git diff --name-only --no-renames`, so code moved into `docs/` still
  counts as code. A failed diff leaves the list empty.
- **Docs-only only on a non-empty list** whose every path matches the Docs-only paths, written as `case`
  patterns: `*` matches `/` there, so `*.md` covers `**/*.md`. An empty list is never docs-only — that is
  the run that would skip every task and report green.
- **Full when a selector input changed**, or on the default branch; scoped otherwise.

The secret scan never consults the decision. **The script stops when git cannot read the checkout**: a
scanner that cannot read the history scans nothing and can still exit 0, as gitleaks does. The job's
image must hold `git`, and the checkout must reach the base: GitLab `GIT_DEPTH: "0"`, GitHub
`fetch-depth: 0`.

## Step 5: Write the Pipeline

On GitLab, write `workflow:` in this order:

```yaml
workflow:
  auto_cancel:
    on_new_commit: interruptible
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_PIPELINE_SOURCE == "schedule"
      auto_cancel:
        on_new_commit: none
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      auto_cancel:
        on_new_commit: none
    - when: never
```

It creates a pipeline for each MR commit, each default-branch commit — a hand-run one included — and the
schedule, and none for a bare branch push; superseded MR runs cancel and main's never do. Under
`Pipelines: every branch`, replace the `when: never` with PIPE-1's form: skip the branch pipeline when
`$CI_OPEN_MERGE_REQUESTS` is set. `workflow:rules:auto_cancel` needs GitLab 16.10; on an older instance
put `interruptible: true` only on MR-pipeline jobs. Each line below answers the row named.

| Need | GitLab | GitHub | Row |
|---|---|---|---|
| A pipeline per MR, none for a bare branch push, none twice | the `workflow:` block above | `on: pull_request`, `push` to the default branch, `schedule` | PIPE-1, PIPE-24 |
| Cancel a superseded MR run, never a main run | the block above, with `default: interruptible: true` | `concurrency` group `${{ github.workflow }}-${{ github.head_ref \|\| github.run_id }}`, `cancel-in-progress: true` | PIPE-6 |
| The full suite on every main commit | the script runs full on the default branch | the same | PIPE-2 |
| The secret scan in every pipeline | no rules, first stage, `needs: []` | its own job with no path filter | PIPE-8, PIPE-15 |
| Fail-fast checks first | first stage, `needs: []` | no `needs:` on the tests | PIPE-15 |
| A path rule that means something | only in MR pipelines, with `compare_to: refs/heads/<default branch>` | inside the job, never on a required workflow | PIPE-3, PIPE-4 |
| A schedule that runs only its own work | `if: $CI_PIPELINE_SOURCE == "schedule"` with `when: never` first in every job except the schedule's own work and the secret scan; the schedule's job admits that source alone | `if: github.event_name != 'schedule'` on the same jobs | PIPE-17 |
| An edge to a job that can skip | `needs:` with `optional: true`, or the same rules on both | an `if:` that tolerates the skip | PIPE-18 |
| A rule on a variable | `$VAR != null && $VAR != ""` | — | PIPE-19 |
| No manual step before the merge or the tests | `when: manual` only on a production deploy or rollback | `workflow_dispatch` only for the same | PIPE-7 |
| A gate that fails | no `allow_failure` on a test, lint or scan; `retry` only `when: [runner_system_failure, stuck_or_timeout_failure]` | no `continue-on-error` | PIPE-9, PIPE-10 |
| Build once | `artifacts:` with `expire_in`; deploy takes the artifact or the image digest; `cache:key:files` on the lockfile | `upload-artifact` and `download-artifact`; `hashFiles` on the lockfile | PIPE-11–13 |
| An image built in the pipeline | copy the manifest and lockfile, install, then copy the source | the same | PIPE-14 |
| Portable paths | `$CI_PROJECT_DIR`, or a path relative to the checkout | `$GITHUB_WORKSPACE` | PIPE-16 |
| A merge queue | — | `merge_group` in the required workflow's triggers | PIPE-5 |
| A job in a container whose user does not own the checkout | — | job `env:` `GIT_CONFIG_COUNT: 1`, `GIT_CONFIG_KEY_0: safe.directory`, `GIT_CONFIG_VALUE_0: "*"`; `actions/checkout` trusts the directory only for its own commands | — |
| Pinned, narrow and secret-free | images by digest; tools from their own image, never fetched by `curl`; installs from the lockfile; credentials from CI variables | actions by commit SHA; `permissions: contents: read` at the top; secrets from `secrets.*` | CWE-829, CWE-494, CWE-1357, CWE-250, CWE-798 |

Give each job a `timeout`. Keep production deploys and rollbacks manual. Read an action's commit with
`gh api repos/<owner>/<action>/git/ref/tags/<tag>`, and write the tag beside it as a comment. Where the
environment cannot read an image digest or an action's commit, write the tag and list each one under
"To pin". Editing an
existing pipeline, change the least that brings it to the policy, and name in the report the row each
change answers.

## Step 6: Check the Pipeline

1. **Build the trigger matrix** exactly as `${CLAUDE_PLUGIN_ROOT}/skills/review-ci/SKILL.md` Step 2
   says, with its seven columns — MR, docs-only MR, main push, docs-only main, schedule, tag, web or API
   — and its `(pipeline)` row. Compare every cell with the policy, and change the pipeline until no cell
   departs.
2. **Review it.** Apply that skill's Step 3 to the written files, and fix every must-fix item except a
   pin this run cannot read, which goes under "To pin". Write no `.ci-review.md`.
3. **Lint it.** GitLab: `glab ci lint --dry-run --ref <default branch> --include-jobs`, then compare the
   jobs it lists with the matrix's main push column. GitHub: `actionlint`. Check the entry-point script
   with `sh -n` and, where it is installed, `shellcheck -s sh`. The tasks themselves are the user's to run:
   the report gives each one's local command, to run once before the first push. Where a tool is missing or the forge refuses access, say so; never push instead.

## Step 7: Read the Forge's Settings, and Ask Before Changing One

Read each setting the policy depends on:

- **The merge gate.** GitLab: `glab api projects/:id` for `only_allow_merge_if_pipeline_succeeds` and
  `allow_merge_on_skipped_pipeline`. GitHub: `gh api repos/{owner}/{repo}/rules/branches/<default branch>`
  and `gh api repos/{owner}/{repo}/branches/<default branch>/protection` for the required status checks.
- **Auto-cancel.** GitLab: `auto_cancel_pending_pipelines` on the same project read.
- **The schedule.** GitLab: `glab api projects/:id/pipeline_schedules`. A GitHub schedule lives in the
  workflow file.

For each setting that departs from the policy, ask one question — "Require a passing MR pipeline to
merge?" — and write it only on a yes, then read it back. Where the forge cannot be read, ask nothing and
list each setting unread with the command that reads it.

## Step 8: Record the Workflow

In the instruction file that holds the policy, under `## CI workflow` after the block, add each line it
lacks, with this project's commands written in:

- Land every change on the default branch through an MR: push a feature branch, open an MR, and merge
  once its pipeline passes.
- Under `Pipelines: open MR only`: a branch runs a pipeline only while its MR is open, so test locally
  until then.
- Reproduce a failing job with `./scripts/ci/run.sh <task>` and fix it locally before the next push; the
  change that broke the pipeline owns the fix.
- Lint a pipeline change before pushing it: `glab ci lint --dry-run --ref <default branch>`, or
  `actionlint`.

## Step 9: Report

1. The policy block, and where it was written.
2. Each file written or edited, with the rows its changes answer.
3. The change-class table and the trigger matrix.
4. The lint result, or why none ran.
5. Each forge setting read, changed, declined or left unread.
6. "To pin": each image or action written by tag.
7. The local command for each job.
8. Not verified: no pipeline ran. The first MR pipeline is the test.

## Self-test (regression gate)

`skills/build-ci/self-test/01-empty-project/` holds a project with no CI and the matrix a build must
reach. `tests/test_build_ci.py` holds that matrix to the default policy cell by cell, and pins
`examples/run.sh`'s decision against a real git history. Whenever this skill, `examples/run.sh`,
`commands/build-ci.md` or `rules/ci-pipelines.md` changes, drive the fixture per `self-test/README.md`,
from this working tree's `SKILL.md`, since `/phil:build-ci` runs the released copy.
