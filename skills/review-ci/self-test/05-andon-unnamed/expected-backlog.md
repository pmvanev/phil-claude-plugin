# CI Review Backlog — items expected

Scope: .
Standard: rules/ci-pipelines.md; rules/security.md (Supply chain and build, the privilege row, the credential-literal row)
Policy: Pipelines: open MR only; Docs-only paths: `docs/**`, `**/*.md`; MR: everything; Main: everything; Merge: a passing MR pipeline is required; Secret scan: every pipeline, docs-only included; Andon: a failed main pipeline notifies the whole team

## Trigger matrix

| Job | MR | docs-only MR | main push | docs-only main | schedule | tag | web or API |
|---|---|---|---|---|---|---|---|
| (pipeline) | created | created | created | created | — | — | — |
| ci.yml: secret-scan | runs | runs | runs | runs | — | — | — |
| ci.yml: test | runs | exits early | runs | exits early | — | — | — |

- The workflow triggers on no `schedule`, tag or `workflow_dispatch`, so those columns hold no pipeline.

Read from the rules, not run; GitLab's CI lint API with `dry_run` confirms a cell.

## Backlog

### [C001] PIPE-25 — the Andon field names no channel, and no job tells the team when main fails

- **File**: `CLAUDE.md`
- **Lines**: 14
- **Severity**: question
- **Row**: PIPE-25
- **Preferred form**: Pull the cord on every failed default-branch pipeline: GitHub a last job with `needs:` on every other job and `if: failure() && github.ref == 'refs/heads/<default branch>'`, or one `workflow_run` workflow, with `branches: [<default branch>]`, that tests `github.event.workflow_run.conclusion == 'failure' && github.event.workflow_run.event == 'push'`, notifying the team where the Andon field says; GitLab the Pipeline status emails integration, with `notify_only_broken_pipelines: true` and `branches_to_be_notified: default` — here: if a chat app subscribed to this repository's workflow runs pulls the cord, name it in the Andon field; if nothing does, name the channel there and give `ci.yml` a last `andon` job
- **Cite**: ci-pipelines.md — PIPE-25 · Fowler 2024 · GitHub workflow-run notification docs; GitLab notification-email and pipeline-status-email docs
- **Status**: pending
