# CI Review Backlog — items expected

Scope: .
Standard: rules/ci-pipelines.md; rules/security.md (Supply chain and build, the privilege row, the credential-literal row)

## Backlog

### [C001] PIPE-6 — superseded-run cancellation reaches main runs

- **File**: `.github/workflows/ci.yml`
- **Lines**: 8-10
- **Severity**: must-fix
- **Row**: PIPE-6
- **Preferred form**: Cancel only superseded MR runs: a GitHub group keyed on `github.head_ref || github.run_id`; GitLab `interruptible` only on MR-pipeline jobs — here: key the group on `${{ github.workflow }}-${{ github.head_ref || github.run_id }}`
- **Cite**: ci-pipelines.md — PIPE-6 · Zampetti BP6, read inversely · Fowler 2024; GitHub `concurrency` docs; GitLab `interruptible` docs
- **Status**: pending

### [C002] PIPE-8 — secret scan skipped for docs-only changes

- **File**: `.github/workflows/secrets.yml`
- **Lines**: 4-5
- **Severity**: must-fix
- **Row**: PIPE-8
- **Preferred form**: Run the secret scan on every pipeline, docs-only changes included
- **Cite**: ci-pipelines.md — PIPE-8 · Zampetti BP29 · Meli et al. 2019; GitHub secret-scanning docs
- **Status**: pending

### [C003] PIPE-13 — dependency cache keyed on a constant

- **File**: `.gitlab-ci.yml`
- **Lines**: 7-9
- **Severity**: must-fix
- **Row**: PIPE-13
- **Preferred form**: Derive the key from the lockfile or manifest (`cache:key:files`; `hashFiles(...)`) — here: `cache:key:files: [package-lock.json]`
- **Cite**: ci-pipelines.md — PIPE-13 · GitLab caching docs; GitHub caching docs
- **Status**: pending

### [C004] PIPE-1 — branch and MR pipelines both run for a branch with an open MR

- **File**: `.gitlab-ci.yml`
- **Lines**: 11-14
- **Severity**: must-fix
- **Row**: PIPE-1
- **Preferred form**: One pipeline per commit: GitLab `workflow:rules` that skip the branch pipeline when `$CI_OPEN_MERGE_REQUESTS` is set; GitHub `push` limited to the default branch — here: add `workflow:rules` that skip the branch pipeline when `$CI_OPEN_MERGE_REQUESTS` is set
- **Cite**: ci-pipelines.md — PIPE-1 · Zampetti BP11 · GitLab `workflow` docs
- **Status**: pending

### [C005] PIPE-9 — unit tests tolerate their own failure

- **File**: `.gitlab-ci.yml`
- **Lines**: 22
- **Severity**: must-fix
- **Row**: PIPE-9
- **Preferred form**: Let the job fail the pipeline; move a job meant only to inform out of the gate and name it so
- **Cite**: ci-pipelines.md — PIPE-9 · Zampetti BP16, BP8 · CD-Linter
- **Status**: pending

### [C006] PIPE-10 — integration tests retried on any failure

- **File**: `.gitlab-ci.yml`
- **Lines**: 30
- **Severity**: must-fix
- **Row**: PIPE-10
- **Preferred form**: Retry only infrastructure failures (GitLab `when: [runner_system_failure, stuck_or_timeout_failure]`); fix or delete the flaky test
- **Cite**: ci-pipelines.md — PIPE-10 · Zampetti Q11, BP17 · Luo et al. 2014; CD-Linter; GitLab `retry` docs
- **Status**: pending

### [C007] CWE-829 — secret-scan image pinned by a mutable tag

- **File**: `.gitlab-ci.yml`
- **Lines**: 44
- **Severity**: must-fix
- **Row**: CWE-829
- **Preferred form**: Pin by digest or commit SHA; verify a checksum or signature before running
- **Cite**: security.md — CWE-829 · CWE-494 (fetched code), CWE-829 (a CI action or image) · v5.0.0 V15
- **Status**: pending

### [C008] PIPE-15 — lint waits for the test stage

- **File**: `.gitlab-ci.yml`
- **Lines**: 53-54
- **Severity**: must-fix
- **Row**: PIPE-15
- **Preferred form**: Run fail-fast checks first or beside the tests, never after them
- **Cite**: ci-pipelines.md — PIPE-15 · Zampetti BP7 · GitLab pipeline-efficiency docs
- **Status**: pending

### [C009] PIPE-16 — absolute runner path in the package script

- **File**: `.gitlab-ci.yml`
- **Lines**: 77
- **Severity**: must-fix
- **Row**: PIPE-16
- **Preferred form**: A path relative to the checkout (`$CI_PROJECT_DIR`, `$GITHUB_WORKSPACE`)
- **Cite**: ci-pipelines.md — PIPE-16 · Zampetti BM1
- **Status**: pending

### [C010] PIPE-3 — `changes` deploys dev from a scheduled pipeline

- **File**: `.gitlab-ci.yml`
- **Lines**: 99-101
- **Severity**: must-fix
- **Row**: PIPE-3
- **Preferred form**: Guard on `$CI_PIPELINE_SOURCE` before `changes`, or give `changes` a `compare_to` naming the branch to compare against — here: guard deploy-dev on `$CI_PIPELINE_SOURCE == "push"`
- **Cite**: ci-pipelines.md — PIPE-3 · Zampetti BP11 · GitLab `rules:changes` docs
- **Status**: pending

### [C011] PIPE-12 — deploy-dev takes build output from the cache

- **File**: `.gitlab-ci.yml`
- **Lines**: 102-106
- **Severity**: must-fix
- **Row**: PIPE-12
- **Preferred form**: Pass build output as an artifact (`artifacts:`; `upload-artifact` and `download-artifact`); keep the cache for dependencies
- **Cite**: ci-pipelines.md — PIPE-12 · Zampetti BP28 · GitLab caching docs
- **Status**: pending

### [C012] PIPE-11 — deploy-staging rebuilds instead of deploying the tested package

- **File**: `.gitlab-ci.yml`
- **Lines**: 110-117
- **Severity**: must-fix
- **Row**: PIPE-11
- **Preferred form**: Deploy what was tested: pass the build output as an artifact, or push the image once and deploy it by digest
- **Cite**: ci-pipelines.md — PIPE-11 · Zampetti BP28 · Humble and Farley; SLSA v1.2
- **Status**: pending

### [C013] PIPE-14 — source copied before dependencies install

- **File**: `Dockerfile`
- **Lines**: 3-4
- **Severity**: must-fix
- **Row**: PIPE-14
- **Preferred form**: Copy the manifest and lockfile, install, then copy the source
- **Cite**: ci-pipelines.md — PIPE-14 · Zampetti BP28 · Docker cache docs
- **Status**: pending
