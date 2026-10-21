# CI Review Backlog — items expected

Scope: .
Standard: rules/ci-pipelines.md; rules/ci-runners.md, where runner configuration was read; rules/security.md (Supply chain and build, the privilege row, the credential-literal row)

## Backlog

### [C001] PIPE-10 — `test` retries any failure twice

- **File**: `.gitlab-ci.yml`
- **Lines**: 25
- **Severity**: must-fix
- **Row**: PIPE-10
- **Preferred form**: Retry only infrastructure failures (GitLab `when: [runner_system_failure, stuck_or_timeout_failure]`); fix or delete the flaky test
- **Cite**: ci-pipelines.md — PIPE-10 · Zampetti Q11, BP17 · Luo et al. 2014; CD-Linter; GitLab `retry` docs
- **Status**: pending

### [C002] RUN-1 — the open pool mounts the host's Docker socket on machines that run ten jobs each

- **File**: `aws/config.toml.tftpl`
- **Lines**: 14-18
- **Severity**: must-fix
- **Row**: RUN-1
- **Preferred form**: Build without a host daemon — rootless BuildKit, Buildah, Kaniko — with the layer cache in the registry; or keep one job per machine — here: for the open pool, set `max_use_count = 1`, or drop the socket mount and build daemonless
- **Cite**: ci-runners.md — RUN-1 · CWE-653 · CICD-SEC-7; SLSA v1.0 Build L3; CIS Docker Benchmark socket control; GitLab Docker-build docs
- **Status**: pending

### [C003] RUN-12 — the open pool's `scale_factor = 1.0` never changes the instance count

- **File**: `aws/config.toml.tftpl`
- **Lines**: 27-28
- **Severity**: must-fix
- **Row**: RUN-12
- **Preferred form**: Leave `scale_factor` at 0 and size `idle_count`; or set `scale_factor` above 1, with no limit or a limit above `idle_count` — here: remove `scale_factor` and `scale_factor_limit`, keeping `idle_count = 2`
- **Cite**: ci-runners.md — RUN-12 · taskscaler source, `internal/capacity/capacity.go` at `1f87885729aa`; GitLab autoscaler docs
- **Status**: pending

### [C004] RUN-4 — the deploy pool holds the deploy role and takes untagged jobs from unprotected refs

- **File**: `aws/runners.tf`
- **Lines**: 11-18
- **Severity**: must-fix
- **Row**: RUN-4
- **Preferred form**: A protected runner (`access_level = "ref_protected"`) that refuses untagged jobs, and one pool per credential set; tags route, protection authorizes — here: in the deploy runner's registration, `access_level = "ref_protected"` and `untagged = false`
- **Cite**: ci-runners.md — RUN-4 · CWE-266 · CICD-SEC-5; GitLab protected-runner docs; GitHub runner-group docs
- **Status**: pending

### [C005] CWE-1357 — `test` installs Python packages from an export that drops the lockfile's hashes

- **File**: `scripts/ci.sh`
- **Lines**: 7-8
- **Severity**: must-fix
- **Row**: CWE-1357
- **Preferred form**: Commit the lockfile and install from it, its hashes checked — here: drop `--no-hashes`, so the exported requirements carry hashes and `pip` checks every one
- **Cite**: security.md — CWE-1357 · CWE-1357 · v5.0.0 V15
- **Status**: pending

### [C006] CWE-494 — `test` fetches a CA bundle with no checksum and writes it where TLS will trust it

- **File**: `scripts/ci.sh`
- **Lines**: 9
- **Severity**: must-fix
- **Row**: CWE-494
- **Preferred form**: Pin by digest or commit SHA; verify a checksum or signature before running or trusting it — here: check the bundle against a pinned SHA-256 before writing it to `aws/`
- **Cite**: security.md — CWE-494 · CWE-494 (fetched code, and a CA bundle, which decides what code is trusted), CWE-829 (a CI action or image) · v5.0.0 V15
- **Status**: pending
