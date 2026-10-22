# The Andon and the Author Tier — Wiring

Two alerts carry out two policy fields. The **andon** tells the whole team when a default-branch pipeline
fails (PIPE-25). **Tell-author** names whoever started a failed pipeline, and `inform` names them when a
check meant only to inform fails (PIPE-26). Copy these forms, then fit job names, `needs:` lists and
images to the pipeline being built.

## GitLab

The andon is a forge setting, written in Step 7 only on a yes:

```
glab api -X PUT projects/:id/integrations/pipelines-email -f recipients=<the field's addresses, comma-separated> -f notify_only_broken_pipelines=true -f branches_to_be_notified=default
```

Tell-author is the pipeline's last job. Keep its two rules in this order: GitLab rejects a job-level
`when:` beside `rules:`.

```yaml
tell-author:
  extends: .node            # any image holding git and curl
  stage: .post
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
      when: never
    - when: on_failure
  script:
    - ./scripts/ci/run.sh tell-author

# Gates nothing: a coverage trend for the reviewer. Its check informs, and the job passes.
coverage-trend:
  extends: .node            # its check's tools, and curl
  script:
    - ./scripts/ci/run.sh inform coverage
```

Both jobs read `NOTIFY_TOKEN`, a project access token with the `api` scope and the Reporter role, which
the user creates and stores as a CI/CD variable that is masked, not protected: a protected variable
never reaches a feature branch's MR pipeline. On GitLab.com, project access tokens require Premium or
Ultimate; on Free, use a personal access token of a dedicated bot account. A token lasts at most 365
days by default, so record its expiry date in the report. An MR from a fork runs with no project
variables, so its comment cannot post.

## GitHub

Both alerts are jobs. Each needs every job but the other, since two jobs that each need every other job
form a cycle, which GitHub rejects.

```yaml
  andon:
    needs: [secret-scan, lint, unit-tests]  # every job but tell-author
    if: failure() && github.ref == 'refs/heads/main'
    runs-on: ubuntu-24.04
    timeout-minutes: 5
    permissions:                             # a job's permissions replace the top's
      contents: read
      issues: write
    steps:
      - uses: actions/checkout@<commit SHA> # <tag>
      - run: ./scripts/ci/run.sh andon
        env:
          GH_TOKEN: ${{ github.token }}

  tell-author:
    needs: [secret-scan, lint, unit-tests]  # every job but the andon
    if: failure() && github.event_name != 'schedule'
    runs-on: ubuntu-24.04
    timeout-minutes: 5
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@<commit SHA> # <tag>
      - run: ./scripts/ci/run.sh tell-author
        env:
          GH_TOKEN: ${{ github.token }}
          PR_NUMBER: ${{ github.event.pull_request.number }}

  # Gates nothing: a coverage trend for the reviewer. Its check informs, and the job passes.
  coverage-trend:
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@<commit SHA> # <tag>
      - run: ./scripts/ci/run.sh inform coverage
        env:
          GH_TOKEN: ${{ github.token }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
```

With several workflows on main, give each workflow its own `tell-author` job, and either an `andon` job
of its own or one `workflow_run` andon for them all:

```yaml
on:
  workflow_run:
    workflows: [<each workflow that runs on main>]
    types: [completed]
    branches: [main]

jobs:
  andon:
    if: github.event.workflow_run.conclusion == 'failure' && github.event.workflow_run.event == 'push'
    # … as above, with the failed run's URL and commit in the step's env:
    #   ANDON_RUN_URL: ${{ github.event.workflow_run.html_url }}
    #   ANDON_SHA: ${{ github.event.workflow_run.head_sha }}
```

The `if:` tests the event because a pull request's runs fire `workflow_run` too. A `workflow_run`
notifier cannot use `tell-author`: its `GITHUB_RUN_ID`, `GITHUB_SHA` and `GITHUB_TRIGGERING_ACTOR` name
itself, not the failed run.

A fork's pull request, and Dependabot's, run with a read-only `GITHUB_TOKEN` whatever `permissions:`
says, so their comment cannot post. Never reach for `pull_request_target` to get a write token.

## On Both Forges

- **A schedule has no author**, so tell-author skips it; the andon covers a red schedule on main.
- **A comment that cannot post** fails `tell-author`, whose pipeline is already red, and leaves `inform`
  passing with a line on stderr, since a warning gates nothing.
- **On main**, tell-author names the starter on the merged PR on GitHub and on the commit on GitLab. A
  direct push to main on GitHub has no PR, so nobody is named and the job fails.
- **Editing an existing pipeline** under a Notify field, turn each job meant only to inform, under
  `allow_failure` or `continue-on-error`, into `./scripts/ci/run.sh inform <task>`.
