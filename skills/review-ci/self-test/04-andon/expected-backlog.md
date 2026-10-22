# CI Review Backlog — items expected

Scope: .
Standard: rules/ci-pipelines.md; rules/security.md (Supply chain and build, the privilege row, the credential-literal row)
Policy: Pipelines: open MR only; Docs-only paths: `docs/**`, `**/*.md`; MR: everything; Main: everything; Merge: a passing MR pipeline is required; Secret scan: every pipeline, docs-only included; Andon: a failed main pipeline notifies the whole team, through an issue the repository's watchers are emailed about

## Trigger matrix

| Job | MR | docs-only MR | main push | docs-only main | schedule | tag | web or API |
|---|---|---|---|---|---|---|---|
| (pipeline) | created | created | created | created | — | — | — |
| ci.yml: secret-scan | runs | runs | runs | runs | — | — | — |
| ci.yml: test | runs | exits early | runs | exits early | — | — | — |
| ci.yml: andon | — | — | on failure | on failure | — | — | — |
| build.yml: zipapp | runs | exits early | runs | exits early | — | — | — |

- Neither workflow triggers on `schedule`, a tag or `workflow_dispatch`, so those columns hold no pipeline.
- `ci.yml: andon` runs on main only when `secret-scan` or `test` fails; a failure of `build.yml: zipapp` never starts it.

Read from the rules, not run; GitLab's CI lint API with `dry_run` confirms a cell.

## Backlog

### [C001] PIPE-25 — a red build workflow on main tells only the person who pushed

- **File**: `.github/workflows/build.yml`
- **Lines**: 15-26
- **Severity**: must-fix
- **Row**: PIPE-25
- **Preferred form**: Pull the cord on every failed default-branch pipeline: GitHub a last job with `needs:` on every other job and `if: failure() && github.ref == 'refs/heads/<default branch>'`, or one `workflow_run` workflow on the default branch that tests `github.event.workflow_run.conclusion == 'failure'`, notifying the team where the Andon field says; GitLab the Pipeline status emails integration, with `notify_only_broken_pipelines: true` and `branches_to_be_notified: default` — here: give `build.yml` a last job like `ci.yml`'s `andon`, or replace both with one `workflow_run` workflow naming `ci` and `build`
- **Cite**: ci-pipelines.md — PIPE-25 · Fowler 2024 · GitHub workflow-run notification docs; GitLab notification-email and pipeline-status-email docs
- **Status**: pending
