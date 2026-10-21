---
paths:
  - "**/gitlab-runner/**"
  - "**/runners/**"
  - "**/config.toml.t*pl"
---

# CI Runner Guide

Guidelines drawn from the SLSA v1.0 Build track; NIST SP 800-204D, *Strategies for the Integration of Software Supply Chain Security in DevSecOps CI/CD Pipelines* (2024), and SP 800-190, *Application Container Security Guide* (2017); the OWASP Top 10 CI/CD Security Risks; Docker's "Docker Engine security" and the CIS Docker Benchmark's socket control; the GitLab Runner documentation on security, autoscaling and Docker builds, with the taskscaler source that implements its autoscaler; GitHub's hardening guidance for self-hosted runners; Anshul Gandhi, Mor Harchol-Balter and Ivo Adan's work on server farms with setup costs (2010) and John Little's law; AWS's EC2 Auto Scaling warm-pool and instance-metadata documentation; and the Terraform and CloudFormation drift documentation, with Martin Fowler's "PhoenixServer". The reviewer table is keyed to MITRE's CWE where a row is a security defect. Research: `docs/research/ci/ci-runner-infrastructure-canonical-sources.md`.

This rule owns **how the machines that run jobs are configured — isolation, credentials, autoscaling and lifecycle — and what an answer about a fleet must rest on**. Neighbouring rules keep what they already own: `ci-pipelines.md` everything a pipeline file decides, a bare `retry` included (PIPE-10); `security.md` mutable-tag actions and images, fetched code, a pipeline file's privileges and token scope, and every credential literal in a committed file, a runner's config included. A runner's own settings — `privileged`, the socket, its executor, its registration — are this rule's. Complement those — do not restate them.

**The two halves divide on checkability.** The reviewer half — Always-flag, Advisory, Do not flag — names defects runner configuration and the infrastructure code behind it show, each by its `RUN-n` id. The Principles half is design, and a review that files a principle as a defect lends it unearned authority.

---

## Principles — design, not review criteria

### Core Philosophy

> **"An ephemeral build environment MUST be provisioned for each build."** — SLSA v1.0, Build L3

A runner's isolation is decided by the machine, not the container. Give each job a machine that no earlier job touched, or run on one machine only jobs that could safely share it.

### One trust class per machine

OWASP's CICD-SEC-5: "Shared nodes should be used only for pipelines with identical levels of confidentiality", and "Revert the execution node to its pristine state". NIST SP 800-190 says the same of containers: "Only group containers with the same purpose, sensitivity, and threat posture on a single host OS kernel." **Reuse is a choice the trust boundary makes**: who can push CI configuration that runs on the pool, and what the pool's machines can reach. A pool that holds a cloud role or a deploy credential runs one job per machine.

### A fresh container is not a fresh machine

Docker: "only trusted users should be allowed to control your Docker daemon", and control of the daemon is root on the host. GitLab: binding the socket means "you effectively disable the container's security mechanisms and expose your host to privilege escalation". On a reused machine with the socket mounted, a new container per job is a new workspace on an old machine: images and tags, build cache, volumes, networks, leftover containers and any host file a job changed all carry over.

### Credentials follow the job, not the machine

An instance role is held by every job on the instance. A federated token — GitLab `id_tokens`, GitHub OIDC — is minted for one job and scoped by its subject claim. Protected runners and protected variables decide which refs reach a credential; tags only route.

### Warm capacity is setup time

Gandhi, Harchol-Balter and Adan model a machine's boot as setup time: a job that misses warm capacity pays the setup on top of its run. Little's law ties the queue to arrivals and wait, and queue wait is lead time. Measure queue wait and boot time before sizing a warm floor — `/phil:build-ci --speed` reports both — and name what each always-on machine costs a month. AWS: a warm pool where it is not needed "can lead to unnecessary costs".

### A setting means what the code does

The autoscaler's documentation and its source can disagree, and the source decides. Read a capacity setting against the code at the revision the fleet runs.

### Answer from what is live

Declared state, recorded state and live state drift apart. An answer about a fleet names which it read, prefers the live system, and never takes a retired platform's documentation for the current fleet.

---

## Always-flag — objective defects

Name each finding by its `RUN-n` id and take the fix from the row, writing ` — here: ` and this fleet's change where the row offers a choice.

**A row fires only on what the review read.** Runner configuration often reaches the review as infrastructure code: a `config.toml` template, a launch template, an IAM policy. Read a templated value from the variable that sets it. Where the value is set somewhere the review did not read, `ci-pipelines.md`'s premise rule decides: a value that would be a row's guard makes a question naming it; one that is only its premise goes under Not read, and nothing is filed. **Where a recorded decision accepts the risk a row names** — an ADR, a dated decision in a runbook — file a question naming the decision and what it accepted, not a must-fix item. **Where a setting's effect turns on the live system** — what the manager actually runs, which instances exist — list the live system under Not read, and say the items rest on the code at its commit (RUN-T1).

### Isolation

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| RUN-1 | The host's Docker socket mounted into jobs — `volumes = ["/var/run/docker.sock:/var/run/docker.sock"]` — on a runner whose machines run more than one job: `max_use_count` other than 1, `capacity_per_instance` above 1, Docker Machine's `MaxBuilds` above 1, or a persistent machine | Build without a host daemon — rootless BuildKit, Buildah, Kaniko — with the layer cache in the registry; or keep one job per machine | CWE-653 · CICD-SEC-7; SLSA v1.0 Build L3; CIS Docker Benchmark socket control; GitLab Docker-build docs |
| RUN-2 | `privileged = true` on a runner whose machines run more than one job | Privileged only on one-job machines; otherwise a daemonless builder | CWE-250 · GitLab runner security docs; CICD-SEC-7 |
| RUN-3 | A persistent or reused self-hosted runner that public-repository or fork pipelines can reach | Hosted runners for public code, or ephemeral runners on fresh machines that hold no credentials | CWE-653 · GitHub self-hosted runner hardening docs; CICD-SEC-5 |
| RUN-8 | `executor = "shell"` on a runner that serves more than one project or any unprotected ref | The Docker or instance executor, on one-job machines | CWE-653 · GitLab runner security docs |
| RUN-9 | `pull_policy` of `if-not-present` or `never` on a reused runner that projects of different visibility or trust share | `pull_policy = ["always"]` | CWE-653 · GitLab runner security docs |
| RUN-10 | A layer or dependency cache that lower-trust pipelines can write and higher-trust pipelines read — a registry cache ref MR jobs push, a host daemon's cache shared across trust classes, or GitLab's separate caches for protected branches turned off | Protected refs write the cache; others read it, or write a key of their own | CWE-653 · SLSA v1.0 Build L3; GitLab caching docs; NIST SP 800-190 |

### Credentials and authority

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| RUN-4 | A pool whose machines hold a cloud role, a deploy credential, or a security-group or route rule that reaches production, and that unprotected refs or MR pipelines can run on — the runner not protected (`access_level = "not_protected"`, also the default when unset), untagged jobs accepted (`run_untagged` in GitLab's API, `untagged` in its Terraform provider), or routing by tag alone | A protected runner (`access_level = "ref_protected"`) that refuses untagged jobs, and one pool per credential set; tags route, protection authorizes | CWE-266 · CICD-SEC-5; GitLab protected-runner docs; GitHub runner-group docs |
| RUN-5 | Instance metadata open to jobs on a pool whose instance role those jobs are not meant to hold: IMDSv1 allowed (`http_tokens = "optional"`), or `http_put_response_hop_limit` above 1 | `http_tokens = "required"` with a hop limit of 1, or no instance role on job machines | CWE-522 · AWS instance-metadata docs; GitHub and GitLab metadata-endpoint guidance; CICD-SEC-6 |
| RUN-6 | Long-lived cloud access keys in CI/CD variables or on the runner host, where the platform offers federated identity | GitLab `id_tokens` or GitHub OIDC to `AssumeRoleWithWebIdentity`, short-lived | CWE-522 · CICD-SEC-6; GitLab and GitHub OIDC docs |
| RUN-7 | A deploy role's federated trust policy whose `sub` condition wildcards the project, the ref or the ref type | Pin `sub` to the project and the protected ref — `project_path:<group>/<project>:ref_type:branch:ref:<branch>`, or a protected tag pattern under `StringLike` | CWE-863 · GitLab and GitHub OIDC docs; CICD-SEC-6 |

### Autoscaling and lifecycle

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| RUN-12 | `scale_factor` set above 0 and no higher than 1.0, or a `scale_factor_limit` set above 0 and no higher than `idle_count` — a setting the autoscaler's arithmetic never acts on | Leave `scale_factor` at 0 and size `idle_count`; or set `scale_factor` above 1, with no limit or a limit above `idle_count` | taskscaler source, `internal/capacity/capacity.go` at `1f87885729aa`; GitLab autoscaler docs |

RUN-11 is unused: a bare `retry` is PIPE-10's in `ci-pipelines.md`, wherever it is set. RUN-13 is unused too: the Docker Machine executor is deprecated, not broken, and its question is Advisory.

**Why RUN-12 holds.** taskscaler's `RequiredInstances` sets the desired capacity to the larger of `acquired + max(idle_count, pending)` and `ceil(scale_factor × acquired)`, the second capped by `scale_factor_limit` only where the limit is above 0. With `scale_factor` at or below 1.0 the second term never exceeds `acquired`, so it never wins; with a limit set at or below `idle_count`, it never exceeds the first term either.

### Fleet answers

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| RUN-T1 | A runbook, README or code comment the review read that states a fleet setting, or what a setting does, that the infrastructure code contradicts — an answer that read neither the live system nor the current code | Correct it from the live system or the current infrastructure code, and name which, with its commit or time | Terraform and CloudFormation drift docs |
| RUN-T2 | A runbook, README or recorded answer about the current fleet that cites configuration or documentation of a platform the fleet no longer runs on | Point it at the current infrastructure code or the live system; keep the retired platform only as history | Fowler "PhoenixServer"; drift docs — this rule's own extension of the drift literature |

A review keeps both rules itself: it records the commit it read, lists the live system as unread, and names a retired platform's configuration as history.

Checked against MITRE CWE 4.20 on 2026-10-21, each id by its vulnerability-mapping usage — CWE-653, -250 and -266 ALLOWED, CWE-522 and -863 ALLOWED-WITH-REVIEW; taskscaler `internal/capacity/capacity.go` read at `1f87885729aa`, the revision GitLab Runner 19.5.0 pins, on 2026-10-21, identical to `main`.

**One item per missing protection, filed where the edit goes**, as `ci-pipelines.md` counts: one setting that several pools inherit is one item at the setting; one pool with two defects is two items. One defect two rows describe is one item, under the row whose Violation names it more closely: a host daemon shared on reused machines is RUN-1, not also RUN-10.

---

## Advisory — judgment calls, not hard blocks

A reviewer raises these; the author decides. Each needs a measurement, an intent or the live system.

- **Reuse on a pool where RUN-1 and RUN-2 do not fire** (`max_use_count` above 1): does every job on the pool come from one trust class, and does any job there produce an artifact others consume?
- **Unbounded reuse** — `max_use_count` very large on a reused pool, or unset, where its default is unconfirmed. Drift and tampering live as long as the machine.
- **A warm floor sized without data** — an `idle_count` with no measured queue wait or boot time behind it — or an always-on machine whose monthly cost nobody named.
- **The socket on one-job machines**, where RUN-1 does not fire: a daemonless builder takes host root
  away from every job, and the machine stays the only boundary until then.
- **`capacity_per_instance` above 1** without the socket: concurrent jobs still share a kernel, a disk and a network.
- **A private CA trusted machine-wide on reused machines that give jobs host root**: any job can add a root to the store, and every later job trusts it.
- **Metadata a hop limit does not guard.** A hop limit of 1 stops a container on a bridge network; it does not stop a job with the socket, privileged mode or the shell or instance executor, which reach the host's network. On such a pool the instance role is every job's. Where `http_tokens` or the hop limit is unset, the AMI's and the account's defaults decide: ask what they are.
- **The Docker Machine executor**, deprecated since GitLab 17.5 and removed in 20.0: plan the move to `docker-autoscaler` or `instance`.
- **A long `prepare_executor`** in job logs — the machine starting and pulling the image — counted in job time, which a pre-baked image or a warm floor shortens.
- **Runner version skew** — the manager's major or minor version behind the GitLab server's — or a machine image older than the current golden image.
- **No distributed cache on a one-job-per-machine fleet**: every `cache:` restore misses.
- **A local cache on reused machines treated as a guarantee**: GitLab says caching "isn't guaranteed to always work".

---

## Do not flag

- **Reuse as such**, on a pool with one trust class, no credential beyond what its least-trusted job may hold, no socket or privileged mode, and no artifact others consume.
- **The socket or privileged mode on a one-job machine** — `max_use_count = 1` and `capacity_per_instance = 1`. The machine is the boundary, "a secure ephemeral instance that cannot be affected by other jobs", in GitLab's words. Do not file RUN-1 or RUN-2; the Advisory list asks about a daemonless builder, and RUN-4 about what the machine can reach.
- **`idle_count = 0`**, or no warm floor at all.
- **Local cache misses on one-job machines.** They are expected; the fix is a distributed cache, not reuse.
- **SLSA Build L3 isolation demands on a pool that builds nothing with provenance.** That is a choice, not a requirement.
- **A private CA trusted machine-wide**, by itself. The CA's key is not on the runner; the Advisory risk is write access to the store.
- **Tags absent on a single-pool fleet.** Routing needs more than one pool to matter.
- **A retired platform's configuration kept as history**, where a file the review read says it is retired and nothing live — a pipeline, a script, the live infrastructure code — applies it. Name it; review only what is live. Where something live still applies it, it is live.

---

## Sources and Synthesis

SLSA v1.0 supplies the isolation boundary each Isolation row rests on, and OWASP CICD-SEC-5 the test for when a machine may be shared, with NIST SP 800-190 and 800-204D behind both. Docker's engine-security page and the CIS socket control show why the socket is host root, and GitLab's runner and Docker-build documentation give each row's GitLab form. GitHub's hardening guidance corroborates them independently. The vendors' OIDC and AWS metadata documentation supply the credential rows. Gandhi, Harchol-Balter and Adan, Little, and AWS's warm-pool guidance frame warm capacity as setup time. The taskscaler source settles what `scale_factor` does where the documentation is ambiguous. The drift documentation and Fowler's "PhoenixServer" ground the fleet-answer rows.

**What is this rule's own:** the `RUN-n` ids and the wording of every row; the split into Principles, Always-flag, Advisory and Do not flag, which follows `ci-pipelines.md`; the reading that reuse is acceptable within one trust class and not across one, which reconciles SLSA L3's ephemeral demand with OWASP's permission to share; the CWE chosen for each row, by MITRE's mapping usage, where the research's two candidates, CWE-668 and CWE-269, are discouraged; and RUN-T2, which extends the drift literature from IaC drift to answering from a retired platform's documents. The rule draws on the research document; the research lists what it could not open under Knowledge Gaps, among them the CIS Benchmark's primary text and whether one job can re-tag another's base image through a shared daemon.

---

## The Mantra

> **One job per machine unless the jobs share a trust class, no host daemon on a reused machine, credentials minted per job, capacity measured before it is bought, and every answer naming what it read.**
