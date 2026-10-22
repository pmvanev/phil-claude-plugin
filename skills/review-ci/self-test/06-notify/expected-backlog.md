# CI Review Backlog — items expected

Scope: .
Standard: rules/ci-pipelines.md; rules/security.md (Supply chain and build, the privilege row, the credential-literal row)
Policy: Pipelines: open MR only; Docs-only paths: `docs/**`, `**/*.md`; MR: everything; Main: everything; Merge: a passing MR pipeline is required; Secret scan: every pipeline, docs-only included; Notify: a failure or a warning names whoever started the pipeline

## Trigger matrix

| Job | MR | docs-only MR | main push | docs-only main | schedule | tag | web or API |
|---|---|---|---|---|---|---|---|
| (pipeline) | created | created | created | created | created | — | created |
| gitleaks | runs | runs | runs | runs | runs | — | runs |
| lint | runs | exits early | runs | exits early | runs | — | runs |
| unit-tests | runs | exits early | runs | exits early | runs | — | runs |
| coverage-trend | runs | exits early | runs | exits early | runs | — | runs |
| tell-author | on failure | on failure | on failure | on failure | — | — | on failure |

- `tell-author` starts when `gitleaks`, `lint` or `unit-tests` fails; `coverage-trend`'s failure, allowed, never starts it.
- Schedule and web or API read a pipeline started on the default branch, which `workflow:rules` admit; whether a schedule exists is a forge setting. `tell-author` skips the schedule, which has no author.

Read from the rules, not run; GitLab's CI lint API with `dry_run` confirms a cell.

## Backlog

### [C001] PIPE-26 — coverage-trend's failure is allowed, so its warning names nobody

- **File**: `.gitlab-ci.yml`
- **Lines**: 48-52
- **Severity**: must-fix
- **Row**: PIPE-26
- **Preferred form**: Name whoever started the pipeline: a last job that runs `./scripts/ci/run.sh tell-author` when an earlier job fails — GitLab `when: on_failure` in the `.post` stage, GitHub `if: failure() && github.event_name != 'schedule'` with `needs:` on every job but the andon — and each job meant only to inform running its check as `./scripts/ci/run.sh inform <task>`, with no `allow_failure` or `continue-on-error` — here: drop `allow_failure: true` and run `./scripts/ci/run.sh inform coverage`
- **Cite**: ci-pipelines.md — PIPE-26 · Fowler 2024 · GitLab `allow_failure` and notification-email docs; GitHub workflow-run notification docs
- **Status**: pending
