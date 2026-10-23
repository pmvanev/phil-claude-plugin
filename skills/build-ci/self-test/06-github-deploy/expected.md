# Expected outcome — fixture 06 (a project that deploys, on GitHub)

Fixture 05's project on GitHub: a `Dockerfile`, and `scripts/deploy.sh <environment> [image]`, which
falls back to `:latest` when handed none. `AGENTS.md` records that every green main commit goes to
staging and production is deployed by hand, from `ghcr.io/phil-fixture-invalid-org/tally`; each
environment sets its own `KUBE_CONTEXT` and `TALLY_LEDGER_DIR`. No CI. Its remote names a repository
that does not exist.

**Pins:** a GitHub build deploys only what passed. The gated run pushes one image after every gate that
runs on a push, and hands it on as a job output and an artifact. Staging deploys in that run. Production
deploys from a dispatch that names a commit, and ships the image that commit's green main run built,
read back from that run; no one types a digest.

**How to drive it:** per `../README.md`, with `git remote add origin
https://github.com/phil-fixture-invalid-org/tally.git`, answering as fixture 04 does: "adopt the
default policy", "open an issue labelled andon" for the andon, and "no" to any forge question.

**Expected:** the run writes a gated workflow, a production workflow, an entry-point script and the
`AGENTS.md` lines fixture 04 expects, and reports a trigger matrix matching `expected-matrix.md` job kind
by job kind:

| Kind | Jobs in `expected-matrix.md` | What its cells must say |
|---|---|---|
| fixture 04's kinds | `gitleaks` to `build`, `mutation-diff`, `mutation-full`, `andon`, `tell-author` | as fixture 04's |
| image | `build-image` | runs on every push to main; exits early on a docs-only one; absent from pull requests and the schedule |
| staging deploy | `deploy-staging` | the same cells as `image` |
| production deploy | `deploy-production` | started by a person, by dispatch, alone |

**Hard assertions (any failure blocks the change), beside every one of fixture 04's:**

- **One image, after every gate.** The `build-image` job's `if:` admits a push alone and holds no status
  function, and its `needs:` name every gate that runs on a push to main: the secret scan, the checks,
  the tests and the build, never `mutation-diff`. It grants itself `packages: write`, logs in with the
  job token through stdin, and hands the digest on as the job output `image` and as the artifact
  `image`, with `retention-days`.
- **Staging takes that digest.** `deploy-staging` needs `build-image`, admits a push alone, runs under
  `environment: staging`, and passes `IMAGE: ${{ needs.build-image.outputs.image }}` through `env:` to
  `./scripts/ci/run.sh deploy staging`.
- **Production names a commit.** A second workflow, on `workflow_dispatch` alone, takes a commit input,
  passes it through `env:`, grants `actions: read`, and runs `./scripts/ci/run.sh promote production
  <commit>` under `environment: production`. It builds nothing. The entry-point script's `promote` task
  finds that commit's green default-branch run of the gated workflow and deploys the image recorded in
  its `image` artifact, refusing a commit whose run built none. No input takes a digest.
- **No deploy falls back to `:latest`** (PIPE-30). On a docs-only commit the image job builds nothing
  and the staging deploy exits early (PIPE-24).
- **Settings at deploy time.** `KUBE_CONTEXT` and `TALLY_LEDGER_DIR` come from each environment's
  `vars` or `secrets`, never the workflow file or the image. The report lists them by environment, and
  says that on a private repository on GitHub Free they become repository secrets named for their
  environment.
- **A rollback the report names:** the production dispatch, given an earlier commit, within the
  artifact's retention.
- **`andon` and `tell-author` need the image and staging jobs too.**
- **No `/phil:review-ci` must-fix item** fires, and none of PIPE-27 to PIPE-31.

**Not a failure:** fixture 04's allowances; another daemonless image builder; a job `concurrency:` per
environment, or none; the Dockerfile rebuilding `dist/`, reported as rework the project owns; a
`.gitignore` entry for `image.env` and `image.ref`; required reviewers on the production environment
offered as a forge question and answered "no"; a `staging` choice on the dispatch, and an `if:` that
runs it from the default branch alone.

**Driven 2026-10-22** blind, against this working tree: every assertion above held but one. It built and
deployed on a docs-only commit, as the skill then said to, which PIPE-24 forbids; the skill is fixed
since. It pinned every action by a commit it read, and the production dispatch named a commit and read
the image from that commit's green run. A second drive, after the fix, held every hard assertion:
`build-image` needing every push gate and never `mutation-diff`, the docs-only commit building nothing
and uploading no record, `promote` refusing a commit whose run built none, settings by environment with
the GitHub Free caveat. Its actions stayed at their tags under "To pin".
