# CI Review Backlog — items expected

Scope: .
Standard: rules/ci-pipelines.md; rules/security.md (Supply chain and build, the privilege row, the credential-literal row)

## Backlog

### [C001] PIPE-27 — the production deploy starts after a failed gate

- **File**: `.github/workflows/ci.yml`
- **Lines**: 74-76
- **Severity**: must-fix
- **Row**: PIPE-27
- **Preferred form**: Deploy only after the gates pass: drop the status function or `when: always`, or test each need's `result` beside it; give a production deploy `needs:` that reach every gate on what it ships, or on GitLab no `needs:` and a stage after the gates'; guard a `workflow_run` deploy with the run's `conclusion` and event — here: drop `!cancelled()` from `deploy-production`'s `if:`, leaving `github.ref == 'refs/heads/main'`
- **Cite**: ci-pipelines.md — PIPE-27 · MinimumCD single path to production and deployable definition · GitHub `needs`, status-check and `workflow_run` docs; GitLab `needs` and `stages` docs
- **Status**: pending

### [C002] PIPE-28 — a dispatch input turns the worker's tests off, and worker-deploy.yml still deploys

- **File**: `.github/workflows/worker.yml`
- **Lines**: 9-13, 20
- **Severity**: must-fix
- **Row**: PIPE-28
- **Preferred form**: Remove the switch: a hotfix passes the same gates as any change — here: delete the `skip_tests` input and `test-worker`'s `if:`
- **Cite**: ci-pipelines.md — PIPE-28 · MinimumCD deployable definition · GitHub `needs` docs; GitLab `rules:if` docs
- **Status**: pending

### [C003] PIPE-29 — the worker image is built once per environment

- **File**: `.github/workflows/worker.yml`
- **Lines**: 38-43
- **Severity**: must-fix
- **Row**: PIPE-29
- **Preferred form**: Build once, inject environment configuration at deploy time, and promote that one artifact through every environment — here: build one worker image, and pass `config/<env>.toml`'s values to `deploy-worker` at deploy time
- **Cite**: ci-pipelines.md — PIPE-29 · MinimumCD immutable artifacts and application configuration · Humble and Farley; GitLab `parallel:matrix` docs
- **Status**: pending

### [C004] PIPE-30 — the worker deploys by a tag the next push moves

- **File**: `scripts/ci/run.sh`
- **Lines**: 20-21, 29
- **Severity**: must-fix
- **Row**: PIPE-30
- **Preferred form**: Deploy the artifact by the digest, or the immutable version, its build job pushed — here: have `build-worker` upload the digest it pushed as an artifact, and have `worker-deploy.yml` download it by `github.event.workflow_run.id` and deploy `$WORKER@<digest>`
- **Cite**: ci-pipelines.md — PIPE-30 · MinimumCD immutable-artifacts docs · SLSA v1.2
- **Status**: pending

### [C005] PIPE-31 — the hotfix workflow ships any ref with no gate

- **File**: `.github/workflows/hotfix.yml`
- **Lines**: 4-9, 32-42
- **Severity**: must-fix
- **Row**: PIPE-31
- **Preferred form**: Put the deploy behind the gates: in the gating run, with `needs:` that reach them, or in a `workflow_run` workflow guarded as PIPE-27 says. A hotfix takes the same path as any change — here: delete `hotfix.yml`: a hotfix merges to main and ships through `ci.yml`
- **Cite**: ci-pipelines.md — PIPE-31 · MinimumCD single path to production · GitHub `workflow_run` docs; GitLab `rules` docs
- **Status**: pending

### [C006] Advisory — the worker has no rollback the files show

- **File**: `.github/workflows/worker-deploy.yml`
- **Lines**: 1-34
- **Severity**: advisory
- **Row**: Advisory
- **Preferred form**: none — the author decides
- **Cite**: ci-pipelines.md — Advisory: A deployable with no rollback the files show
- **Status**: pending
