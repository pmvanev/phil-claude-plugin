# CI Review Backlog — items expected

Scope: .
Standard: rules/ci-pipelines.md; rules/security.md (Supply chain and build, the privilege row, the credential-literal row)
Policy: Pipelines: open MR only; Docs-only paths: `docs/**`, `**/*.md`; MR: tests and mutation for changed and affected code; Main: everything except mutation; Schedule: full mutation, weekly, off-hours, sharded; Merge: a passing MR pipeline is required; Secret scan: every pipeline, docs-only included

## Trigger matrix

| Job | MR | docs-only MR | main push | docs-only main | schedule | tag | web or API |
|---|---|---|---|---|---|---|---|
| (pipeline) | refused if paths ✗ C002 | refused if paths ✗ C002 | created | created | created | — | created |
| gitleaks | runs | runs | runs | runs | runs | — | runs |
| lint | if paths ✗ C001 | — | runs | exits early | — | — | runs |
| unit-tests | runs | exits early | runs | exits early | — | — | runs |
| build | runs | exits early | runs | exits early | — | — | runs |
| e2e | if paths | if paths | runs | exits early | — | — | runs |
| e2e-report | runs | exits early | runs | exits early | — | — | runs |
| accessibility | runs ✗ C002 | exits early ✗ C002 | runs | exits early | — | — | runs |
| mutation-diff | runs | exits early | runs ✗ C003 | exits early | — | — | exits early |
| mutation-full | — | — | — | — | runs | — | — |
| deploy-dev | — | — | runs | exits early | — | — | runs |
| deploy-staging | — | — | runs | exits early | runs ✗ C004 | — | runs |
| deploy-prod | — | — | manual | manual | — | — | manual |
| rollback-prod | — | — | manual ✗ C005 | manual ✗ C005 | manual ✗ C005 | — | manual ✗ C005 |

- An MR pipeline that leaves `e2e` out is refused (C002); job cells read as if it were created.
- Web or API reads a pipeline started on the default branch; `workflow:rules` create none elsewhere.
- With `ROLLBACK_TAG` set, a pipeline runs gitleaks and rollback-prod, and every other job is `—`.

Read from the rules, not run; GitLab's CI lint API with `dry_run` confirms a cell.

## Backlog

### [C001] PIPE-21 — lint is skipped for any MR that touches a doc, code changes included

- **File**: `.gitlab-ci.yml`
- **Lines**: 82-84
- **Severity**: must-fix
- **Row**: PIPE-21
- **Preferred form**: Skip only when every changed path is in the docs allow-list: GitHub `paths-ignore` with the allow-list, on a workflow that is not a required check; GitLab a step that compares the changed paths with the allow-list and exits early — here: drop the `changes:` rule; `scripts/ci/run.sh` already exits early for a docs-only change
- **Cite**: ci-pipelines.md — PIPE-21 · Zampetti BP11 · GitLab `rules:changes` docs; GitHub workflow-syntax docs
- **Status**: pending

### [C002] PIPE-18 — accessibility needs e2e, which an MR outside web/ leaves out

- **File**: `.gitlab-ci.yml`
- **Lines**: 142
- **Severity**: must-fix
- **Row**: PIPE-18
- **Preferred form**: Mark the edge `needs: [{job: …, optional: true}]`, or give both jobs the same rules so they skip together — here: give accessibility e2e's rules, since it tests e2e's server
- **Cite**: ci-pipelines.md — PIPE-18 · GitLab `needs` docs
- **Status**: pending

### [C003] PIPE-24 — mutation-diff runs on main, which the policy excludes

- **File**: `.gitlab-ci.yml`
- **Lines**: 153-156
- **Severity**: must-fix
- **Row**: PIPE-24
- **Preferred form**: Change the job's rules so the cell matches the field, or change the declared field — here: `if: $CI_PIPELINE_SOURCE == "merge_request_event"` as its only run rule, per `Main: everything except mutation`
- **Cite**: ci-pipelines.md — PIPE-24 · Zampetti BP11, BP26 · the project's `## CI policy` block
- **Status**: pending

### [C004] PIPE-17 — the weekly schedule promotes dev to staging

- **File**: `.gitlab-ci.yml`
- **Lines**: 189-191
- **Severity**: must-fix
- **Row**: PIPE-17
- **Preferred form**: Keep schedules out of deploy jobs: GitLab `if: $CI_PIPELINE_SOURCE == "schedule"` with `when: never` as the first rule; GitHub `if: github.event_name != 'schedule'` — here: make `!reference [.not-on-schedule, rules]` deploy-staging's first rule
- **Cite**: ci-pipelines.md — PIPE-17 · Zampetti BP11 · GitLab `rules` docs; GitHub `schedule` docs
- **Status**: pending

### [C005] PIPE-19 — rollback-prod's rule matches its empty tag, so every main and scheduled pipeline offers it

- **File**: `.gitlab-ci.yml`
- **Lines**: 213
- **Severity**: must-fix
- **Row**: PIPE-19
- **Preferred form**: Compare the value: `$VAR != null && $VAR != ""`; a bare `$VAR` is safe only as the whole expression — here: `if: $ROLLBACK_TAG != null && $ROLLBACK_TAG != "" && $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH`
- **Cite**: ci-pipelines.md — PIPE-19 · GitLab expression evaluator, `lexeme/and.rb` and `statement.rb`, read 2026-10-21; its `rules:if` docs say otherwise
- **Status**: pending
