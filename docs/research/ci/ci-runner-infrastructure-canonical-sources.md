# Research: Canonical Sources for Configuring and Operating CI Runners

**Date**: 2026-10-21 | **Researcher**: nw-researcher (Nova) | **Confidence**: High for isolation, the Docker socket and credentials; Medium-High for autoscaler arithmetic; Medium for capacity sizing and the fleet-answer rule | **Sources**: 53

> Input to runner guidance in the `phil` plugin (a section of `rules/security.md` or
> `rules/continuous-delivery.md`, or a rule of its own — decided later) and to a skill that reviews or
> designs a runner fleet. Subject: **the machines and executors that run jobs** — isolation, lifecycle,
> autoscaling, capacity, cache locality, cost, credentials, and answering questions about a fleet
> truthfully. Pipeline shape (triggers, change-scoped tests, mutation in CI, job speed, rework) belongs to
> the sibling `docs/research/ci/ci-pipeline-canonical-sources.md`.
> Each finding uses: **Work** / **Evidence** / **Canonicity** / **Contributes** / **Checkable in runner config?** / **Caveats**.
> Access date for every web source: 2026-10-21 unless stated.

## Executive Summary

Runner isolation has one standard and one test. **SLSA's Build L3 "Isolated" requirement** (unchanged
from v1.0 to v1.2) says no build may "persist or influence the build environment of a subsequent build" or
"inject false entries into a build cache used by another build", and that "an ephemeral build environment
MUST be provisioned for each build". **OWASP's CICD-SEC-5** gives the test for anything less: share a node
only among pipelines "with identical levels of confidentiality" and the same resource access. NIST SP
800-190 (group containers by "purpose, sensitivity, and threat posture"; caches and local volumes are the
residue) and NIST SP 800-204D (a "secure isolated platform", control plane above the build) corroborate it,
as do GitHub's and GitLab's own hardening pages. So reuse is decided by two questions: who can run code on
the pool, and what the pool can reach.

**A fresh container per job is not isolation when the Docker socket is mounted.** Docker says whoever
controls the daemon is root on the host; CIS forbids mounting the socket in containers; GitLab says socket
binding means "you effectively disable the container's security mechanisms". On a VM that runs one job,
the VM is the boundary. On a reused VM, images, tags, build cache, Docker volumes, networks, sibling
containers and any host file a job changed — the host trust store included — carry over to the next job.
GitLab's own hosted runners, GitHub-hosted runners and the main self-hosted autoscalers all give untrusted
code one job per VM.

**Autoscaler semantics need the code, not the prose.** GitLab Runner v19.5.0's taskscaler computes total
capacity as `max(in-use + max(idle_count, pending), min(ceil(scale_factor × in-use), scale_factor_limit))`:
the factor *overlaps* the floor rather than adding to it, so `scale_factor = 1.0` does nothing. GitLab's
docs describe it two other ways. With `max_use_count = 1` a warm instance absorbs one job, and a burst
larger than the floor pays full boots — setup-time queueing (Gandhi, Harchol-Balter, Adan 2010, 140
Crossref citations). Credentials belong in per-job OIDC tokens scoped by `sub`, not in instance roles every
job inherits; tags route and protection authorizes. For truthful answers, Terraform's and CloudFormation's
drift docs separate declared, recorded and live state; no source covers the case of answering from a
retired platform's docs, which this document labels as its own extension. The synthesis yields 13 config
rows (`RUN-1`…`RUN-13`) and 2 fleet-answer rows (`RUN-T1`, `RUN-T2`), plus advisory and do-not-flag lists,
and applies them to the concrete case.

## Research Methodology

**Search Strategy**: Primary sources first — slsa.dev, csrc/nvlpubs.nist.gov, owasp.org, docs.docker.com,
docs.aws.amazon.com, and the vendors' own docs for their own products (docs.gitlab.com, docs.github.com,
developer.hashicorp.com). Where GitLab's prose was ambiguous, the executing source (`fleeting/taskscaler`)
and the release's `go.mod` were read to pin behaviour to Runner v19.5.0. Crossref's
`is-referenced-by-count` was taken for every paper or NIST SP with a DOI; none was guessed.
**Source Selection**: Types: official standards and government guidance, vendor product docs, academic
queueing papers, source code; vendor mappings (Datadog, Turbot) only to stand in for the gated CIS PDF,
marked medium. **Verification**: Each security claim cross-referenced across independent publishers (e.g.
the reuse test across SLSA, OWASP, NIST, GitHub and GitLab; the socket risk across Docker, CIS and GitLab).
Product-semantics claims rest on the product's docs and code, which are the only authority.
**Quality Standards**: Target 3 sources per major claim, 1 authoritative minimum; inferences labelled
"interpretation"; unconfirmed items marked in place and collected in Knowledge Gaps. All web content passed
adversarial screening; one page carrying prompt injection is flagged in Source Analysis.

---

## Findings

## 1. Ephemeral vs reused build machines and the trust boundary

### 1.1 SLSA v1.0, Build track requirements

**Work**: OpenSSF. *SLSA Specification* v1.0, "Producing artifacts" (requirements).
https://slsa.dev/spec/v1.0/requirements (trusted per task, high). The sibling security research records
v1.2 as the current "Approved" version. The text below was read from v1.0; the five Isolated bullets were
then checked against https://slsa.dev/spec/v1.2/build-requirements and are **word-for-word unchanged, still
at Build L3 only**.
**Evidence**: Build L2 and L3 require **Hosted**: "All build steps ran using a hosted build platform on
shared or dedicated infrastructure". Only L3 requires **Isolated**: "The build platform ensured that the
build steps ran in an isolated environment, free of unintended external influence." Its bullets, quoted:
"It MUST NOT be possible for a build to access any secrets of the build platform, such as the provenance
signing key"; "It MUST NOT be possible for two builds that overlap in time to influence one another";
"It MUST NOT be possible for one build to persist or influence the build environment of a subsequent
build"; "It MUST NOT be possible for one build to inject false entries into a build cache used by another
build"; "the output of the build MUST be identical whether or not the cache is used"; and "an ephemeral
build environment MUST be provisioned for each build." v1.0 has no separate Ephemeral requirement; a note
says the requirement "was split into 'Isolated' and 'Ephemeral Environment'" in draft v0.1 and later merged.
**Canonicity**: The industry's leveled build-integrity specification (Google-originated, OpenSSF-owned);
named in NIST SP 800-204D's keywords ("SLSA") and in its secure-build section (1.2).
**Contributes**: The sharpest statement of the trust boundary a runner fleet must hold for L3: no
persistence into the next build, no cross-build cache poisoning, no access to platform secrets. It is the
standard the phrase "one build cannot influence another" comes from.
**Checkable in runner config?** Yes, in part. `max_use_count=1` / `MaxBuilds=1` / `--ephemeral` show the
ephemeral half; a shared host Docker daemon (socket mount) or a writable shared cache shows a violation of
the persistence and cache bullets regardless of VM lifetime (see 2).
**Caveats**: SLSA scopes *builds that produce artifacts with provenance*. A test-only job on an open pool is
not a "build" in SLSA's sense; applying L3 there is a choice, not a requirement. L2 (hosted, signed
provenance) does **not** require isolation — reuse is compatible with L2.

### 1.2 NIST SP 800-204D, *Strategies for the Integration of Software Supply Chain Security in DevSecOps CI/CD Pipelines* (2024)

**Work**: Ramaswamy Chandramouli (NIST), Frederick Kautz (TestifySec), Santiago Torres-Arias (Purdue).
NIST SP 800-204D, final, February 2024. https://csrc.nist.gov/pubs/sp/800/204/d/final ; PDF
https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204D.pdf (official, high). PDF read
pages 15–17.
**Evidence**: §5 prerequisites: "Harden the CI/CD execution environment (e.g., VM or pod) to reduce its
attack surface." §5.1.1 Secure Build requires build policies covering "(a) the use of a secure isolated
platform for performing the build and hardening the build servers"; the build system "should be able to
confirm that the tools or processes used are in an isolated environment"; environment attestation's
platform components "must be hardened, isolated, and secure"; evidence generation must come from "a
process with a higher level of trust or isolation than the build itself". §5 also: "the driver tools or
build control plane execute at a higher level of trust than the individual functional steps, such as
build." Keywords include SLSA.
**Canonicity**: US federal guidance; the NIST document specific to CI/CD supply-chain security.
**Contributes**: Federal corroboration that the build executor is an isolated, hardened platform and that
the runner manager (control plane) sits at a higher trust level than the job — the reason a job must not
reach the runner manager's credentials or daemon.
**Checkable in runner config?** No directly; it states goals ("isolated", "hardened") without a lifetime or
reuse rule. Cite it as corroboration of SLSA, not as the source of a row.
**Caveats**: The document never says "ephemeral" in the pages read. Crossref count: not taken (NIST SPs
carry DOIs, e.g. 10.6028/NIST.SP.800-204D — **DOI not confirmed on the page read**).

### 1.3 OWASP Top 10 CI/CD Security Risks — CICD-SEC-5, -6, -7

**Work**: OWASP Foundation (project originated by Cider Security, Daniel Krivelevich and Omer Gil).
https://owasp.org/www-project-top-10-ci-cd-security-risks/ (308-redirects to owasp.github.io; owasp,
official for its own project). Version / date: **not shown on the pages read**; published 2022 per prior
knowledge, **not re-verified**.
**Evidence** (CICD-SEC-5 Insufficient Pipeline-Based Access Controls): "Pipeline execution nodes have
access to numerous resources and systems within and outside the execution environment." Recommendations,
quoted: "Do not use a shared node for pipelines with different levels of sensitivity / that require access
to different resources"; "Shared nodes should be used only for pipelines with identical levels of
confidentiality"; "Revert the execution node to its pristine state after each pipeline execution"; "Ensure
the execution node is appropriately patched"; "Ensure network segmentation in the environment the job is
running on"; "refrain from granting unlimited access towards the internet to build nodes". It names "the
AWS metadata service" as a place pipelines obtain secrets.
(CICD-SEC-6 Insufficient Credential Hygiene): "Prefer using temporary credentials over static
credentials"; "Avoid sharing the same set of credentials across multiple contexts"; credentials "scoped in
a manner that allows each pipeline and step to have access to only the secrets it requires"; "Are these
credentials accessible only in run-time, and only from the contexts where they are required?"
(CICD-SEC-7 Insecure System Configuration): example "A self-hosted system that has administrative
permissions on the underlying OS"; "Ensure permissions to the pipeline execution nodes are granted
according to the principle of least privilege"; "If a security patch is available, update the vulnerable
component."
**Canonicity**: The only named risk list specific to CI/CD; OWASP-hosted. Vendor-originated (Cider, later
acquired by Palo Alto Networks — prior knowledge) — note commercial origin.
**Contributes**: **The decision rule for reuse.** SEC-5 states it directly: a node may be shared only
among pipelines of *identical* sensitivity and resource access, and should be reverted to pristine after
each execution. That gives the two-question test the task asks for: who can run code on the pool, and what
the pool can reach (cloud roles, deploy credentials, internal networks).
**Checkable in runner config?** Partly: pool-to-project/branch routing (tags, protected runners, runner
groups) and instance roles are config; "identical sensitivity" is a judgment the reviewer must ask about.
**Caveats**: SEC-5's "revert to pristine after each execution" is stricter than its own "shared nodes ...
identical levels of confidentiality" — the first forbids reuse, the second permits it within a class. See
Conflicting Information.

### 1.4 GitHub Docs, "Security hardening for GitHub Actions" — self-hosted runners; "Autoscaling with self-hosted runners"

**Work**: GitHub. https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions
and https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/autoscaling-with-self-hosted-runners
(vendor docs, official for own product; living pages, no version).
**Evidence**: Self-hosted runners "should almost never be used for public repositories", because "any user
can open pull requests against the repository and compromise the environment"; the risk extends to
"anyone who can fork the repository and open a pull request". A self-hosted runner "can be persistently
compromised by untrusted code in a workflow"; "Some jobs will use secrets as command-line arguments which
can be seen by another job running on the same runner"; "there is no way to guarantee that a self-hosted
runner only runs one job" (for a persistent runner). JIT runners "perform at most one job before being
automatically removed", yet "Re-using hardware to host JIT runners can risk exposing information from the
environment." Runner groups "create boundaries". The doc's questions: "What sensitive information resides on
the machine configured as a self-hosted runner?"; "Does the machine have network access to sensitive
services?" — "For example, Azure or AWS metadata services"; "any user capable of invoking workflows has
access to this environment". Autoscaling page: "GitHub recommends implementing autoscaling with ephemeral
self-hosted runners"; with ephemeral runners one job per runner "can be guaranteed"; "In certain cases,
GitHub cannot guarantee that jobs are not assigned to persistent runners while they are shut down."
**Canonicity**: Platform owner's guidance; the source every GitHub-runner hardening guide repeats.
**Contributes**: (a) the "who can invoke a job" half of the reuse test — anyone who can open a PR on a
public repo; (b) the "what does the machine hold" half — secrets, network reach, cloud metadata; (c) that
an ephemeral *runner registration* on reused *hardware* is not an ephemeral *machine*.
**Checkable in runner config?** Yes: `--ephemeral` / JIT registration; a self-hosted runner group open to
public repositories; instance metadata reachable from jobs.
**Caveats**: GitHub-specific vocabulary; the principle transfers to GitLab (1.5).

### 1.5 GitLab Docs, "Security for self-managed runners"

**Work**: GitLab. https://docs.gitlab.com/runner/security/ (vendor docs, official for own product; page shows
tier/offering but **no runner version**).
**Evidence**: Shell executor: "High-security risks exist to your runner host and network when running
builds with the shell executor"; "Use it only for running trusted builds." Docker executor: "Docker can be
considered safe when running in non-privileged mode"; "It is not advised to run containers in privileged
mode, or with the --pid=host flag"; "By enabling privileged mode, you are effectively disabling all the
container's security mechanisms"; a privileged job "could gain full root access to the runner's host
system". Mitigation: "Run Docker containers with the --privileged flag enabled only on isolated and
ephemeral virtual machines", configure such runners "to execute jobs only on protected branches", and
(Docker Machine) set `MaxBuilds = 1` so "a single autoscaled VM ... is used to handle one and only one
job". On reuse: the `GIT_STRATEGY: fetch` risk "is even more acute if your self-managed runners are
non-ephemeral and used for multiple projects"; `FF_ENABLE_JOB_CLEANUP` cleans the host build directory
after each build. Network segmentation includes "Filtering access to cloud provider metadata endpoints".
Pull policy: "you should use always pull policy if you are hosting a public, instance runner" with "mixed
private, and public access levels", because `if-not-present` lets a job use a private image cached on the
host "even if the image could not be pulled because of missing credentials".
**Canonicity**: Platform owner's guidance.
**Contributes**: GitLab's own ladder: shell < docker unprivileged < privileged only on ephemeral VMs with
protected branches. And three named things that persist on a reused host: the build directory / `.git`
folder, cached images (pull-policy leak across projects), and whatever privileged mode lets a job write.
**Checkable in runner config?** Yes: `executor = "shell"`, `privileged = true`, `pull_policy`,
`protected` runner flag, `max_use_count` / `MaxBuilds`, metadata filtering.
**Caveats**: This page does **not** mention mounting `/var/run/docker.sock`; that trade-off lives on the
Docker-in-Docker page (2.3).

### 1.6 What decides when reuse is acceptable (interpretation, cross-referenced)

Four sources agree that reuse is a question of **who can run code on the pool** and **what the pool can
reach**, not of reuse as such:

- *Who runs code*: GitHub (anyone who can open a PR on a public repo or fork), GitLab (public instance
  runners with mixed-visibility projects; privileged only on protected branches), OWASP SEC-5 (identical
  sensitivity only).
- *What the pool reaches*: GitHub (secrets on the machine, metadata services, sensitive networks), OWASP
  SEC-5/-6 (metadata service, credentials scoped per pipeline and step), GitLab (metadata filtering).
- *The strict bar*: SLSA L3 forbids one build persisting into the next and requires an ephemeral
  environment per build; GitLab requires ephemeral VMs for privileged jobs; OWASP SEC-5 says revert to
  pristine after each execution.

Reading (interpretation): **reuse is acceptable on a pool whose every job comes from the same trust class
(same people able to push CI config that runs there), which holds no credential the least-trusted of
those people should not have, and which produces no artifact that claims SLSA L3.** Reuse is not
acceptable on a pool that holds deploy roles while open-branch or fork code can run there, nor on any pool
whose jobs get privileged mode or the host Docker socket from mixed trust classes. Confidence: High (four
independent publishers; the wording of the test is this document's).

## 2. A container per job is not isolation when the Docker socket is mounted

### 2.1 Docker Docs, "Docker Engine security" — Docker daemon attack surface; post-install warning

**Work**: Docker Inc. https://docs.docker.com/engine/security/ and
https://docs.docker.com/engine/install/linux-postinstall/ (docker.com docs, high; living pages).
**Evidence**: "This daemon requires `root` privileges unless you opt-in to Rootless mode"; "only trusted
users should be allowed to control your Docker daemon"; a container can be started "where the `/host`
directory is the `/` directory on your host", and it "can alter your host filesystem without any
restriction". The API uses "a Unix socket", so "traditional Unix permission checks" limit access to it.
Post-install page: "The `docker` group grants root-level privileges to the user." User namespaces are
"available but not enabled by default".
**Canonicity**: The daemon's maker; the source every container-security guide cites for "socket = root".
**Contributes**: The premise of the whole section: **whoever can talk to the daemon socket controls the
host as root.** A job given the socket can start a sibling container that mounts `/` and so reads or
writes anything on the host — including other jobs' files, the runner's config and token, and the
host's trust store.
**Checkable in runner config?** Yes: `volumes = ["/var/run/docker.sock:/var/run/docker.sock"]` in
`[runners.docker]`, or `-v /var/run/docker.sock` in a job.
**Caveats**: The Unix-permission control the doc names protects the socket *from host users*; it does
nothing once the socket is bind-mounted into a job container.

### 2.2 CIS Docker Benchmark — "Ensure that the Docker socket is not mounted inside any containers"

**Work**: Center for Internet Security. *CIS Docker Benchmark*; control 5.31 in v1.2.0, 5.32 in v1.6.0
(numbering from Datadog's CIS-mapped rule page https://docs.datadoghq.com/security/default_rules/cis-docker-1.2.0-5.31/
and Turbot's CIS v1.6.0 mapping https://hub.powerpipe.io/mods/turbot/docker_compliance/controls/control.cis_v160_5_32 —
both vendor, medium). **The CIS PDF itself was not read** (registration-gated); wording and numbering
are from secondary mappings.
**Evidence** (as reproduced by the mappings): mounting the socket "could allow processes running within the
container to execute Docker commands which would effectively allow for full control of the host"; default
"docker.sock is not mounted inside containers"; audit via `docker inspect ... Mounts | grep docker.sock`.
A DISA STIG for Mirantis/Docker Enterprise (ato-pathways.com mirror, medium) records the same control with
one exception, the UCP installer.
**Canonicity**: CIS benchmarks are the de facto hardening baselines that compliance scanners implement.
**Contributes**: A control id to cite beside the Docker doc for the socket row.
**Checkable in runner config?** Yes — the audit command is literally a config check.
**Caveats**: Control numbers shift between benchmark versions (5.31 vs 5.32); cite by title plus version.

### 2.3 GitLab Docs, "Use Docker to build Docker images" — socket binding vs Docker-in-Docker vs alternatives

**Work**: GitLab. https://docs.gitlab.com/ci/docker/using_docker_build/ and
https://docs.gitlab.com/ci/docker/docker_layer_caching/ (vendor docs, official for own product; no version
shown).
**Evidence**: Socket binding, "Known issues with Docker socket binding": "When you share the Docker daemon,
you effectively disable the container's security mechanisms and expose your host to privilege
escalation. This can cause container breakout." "Any containers created by Docker commands are siblings of
the runner, rather than children of the runner." "if you run `docker rm -f $(docker ps -a -q)` in a
project, it removes the GitLab Runner containers." "Concurrent jobs might not work. If your tests create
containers with specific names, they might conflict with each other." "Volume mounting is done in the
context of the host machine, not the build container." Shell executor section: adding `gitlab-runner` to
the `docker` group grants "full root permissions". Docker-in-Docker: requires `privileged` mode; "Each job
gets its own isolated Docker daemon, so concurrent jobs do not conflict"; "When you use Docker-in-Docker,
Docker downloads all layers of your image on every build." Alternatives: BuildKit "Includes rootless
BuildKit options that eliminate Docker daemon dependency"; Buildah builds OCI images "without requiring a
Docker daemon". GitLab Support recommends Kaniko where neither socket nor privileged mode is allowed
(support.gitlab.com article 16981770788892, vendor support, medium-high).
**Canonicity**: Platform owner's guidance.
**Contributes**: GitLab's own statement that **socket binding disables container isolation** — the direct
answer to "we still get a fresh container per job, right?": the job container is fresh, but everything
the job starts through the socket runs on the *host's* daemon, beside the runner, and shares the host's
image store, networks and volumes.
**Checkable in runner config?** Yes (socket volume; `privileged = true` for DinD).
**Caveats**: The current page does **not** state in so many words that images, networks and volumes persist
across jobs, nor that one job can re-tag a base image another job builds from. Those follow from Docker's
documented model (2.4) but are this document's inference for GitLab. A 2021 HackerOne report filed as
gitlab-org/gitlab#347404 showed a socket-bound job reading the runner host's `/etc/shadow` and asked for a
doc warning; the issue page showed no resolution. [Validation Warning: that issue page embedded
instructions addressed to an AI assistant; they were ignored and only the report's facts used.]

### 2.4 What persists across jobs on a reused VM despite a fresh container (documented mechanics)

**Work**: GitLab Docs, "Docker executor" https://docs.gitlab.com/runner/executors/docker/ ; Docker Docs,
`docker buildx build` reference https://docs.docker.com/reference/cli/docker/buildx/build/ ; NIST SP
800-190 (2.5). Vendor docs, official for own product.
**Evidence**: GitLab Docker executor: "All directories defined in `volumes =` are persistent between
builds"; "If you don't set `runners.docker.cache_dir`, the data persists in Docker volumes"; "The
`clear-docker-cache` script does not remove Docker images because they are not tagged by the GitLab
Runner"; `pull_policy` `if-not-present` "Pull an image only when a local version does not exist" (default
is `always`). The page warns "Do not mount the Podman socket ... into job containers through `volumes`" and
that sharing the PID namespace "is a breach of isolation". Docker build `--pull`: "Always attempt to pull all
referenced images" — without it, a build resolves `FROM` against the local image store.
**Contributes (interpretation from the documented mechanics)**: On a VM that runs more than one job, the
following outlive a job even though each job's container is new:
1. **Docker volumes**, including the runner's cache volumes and every path in `volumes =`.
2. **The host daemon's image store and build cache** — pulled images, built images, tags. With the socket
   mounted, any job can `docker tag` or `docker build -t` over a name a later job's `FROM` or `image:`
   resolves locally (when that later job's pull policy or `docker build` lacks `--pull`). This is the
   cross-build cache-injection SLSA L3 forbids ("inject false entries into a build cache used by another
   build").
3. **Sibling containers, networks and volumes** a job started through the socket and did not remove — they
   run on as host-level objects (GitLab: "siblings of the runner").
4. **The host filesystem and OS state** a socket-holding job wrote through a `/`-mounted sibling: trust
   store, runner `config.toml` and token, cron, binaries.
5. **The build directory and `.git`** unless `FF_ENABLE_JOB_CLEANUP` or a fresh volume is used (1.5).
6. **Locally cached private images** reachable by a later job under `if-not-present` (1.5).
With `max_use_count = 1` none of these reach a second job, because the VM is destroyed — which is why the
case fleet is isolated today *despite* the socket, and why reuse would remove that isolation.
**Checkable in runner config?** Yes: socket volume + `max_use_count > 1` together is the flaggable
combination.
**Caveats**: Items 2 and 4 are inferences from documented behaviour, not a sentence any vendor page
states; confidence Medium-High.

### 2.5 NIST SP 800-190, *Application Container Security Guide* (2017)

**Work**: Murugiah Souppaya, John Morello, Karen Scarfone. NIST SP 800-190, issued 2017-09-25. DOI
10.6028/NIST.SP.800-190. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf
(official, high). Executive summary read (pp. iv–v).
**Evidence**: "Only group containers with the same purpose, sensitivity, and threat posture on a single
host OS kernel to allow for additional defense in depth." "it may be an unnecessary risk to run apps of
different sensitivity levels together on the same host OS"; grouping makes it harder for an attacker "who
compromises one of the groups to expand that compromise to other groups" and "ensures that any residual
data, such as caches or local volumes mounted for temp files, stays within its security zone." Also: "Use
container-specific host OSs instead of general-purpose ones to reduce attack surfaces."
**Canonicity**: Crossref is-referenced-by-count **77** (queried 2026-10-21). The US federal container
security guide.
**Contributes**: Federal, vendor-neutral statement of the same trust-class rule OWASP SEC-5 gives for build
nodes — and it names *caches and local volumes* as the residue that crosses jobs on a shared kernel.
**Checkable in runner config?** Partly: pool routing by tag/protection is config; "same sensitivity" is a
judgment.
**Caveats**: Written for application containers under an orchestrator, not CI; applied here by analogy
(a job is a container workload on a shared host). 2017, but the kernel-sharing premise is unchanged.

### 2.6 Docker rootless mode and daemonless builders

**Work**: Docker Docs, "Rootless mode" https://docs.docker.com/engine/security/rootless/ (high); GitLab
alternatives (2.3).
**Evidence**: "Rootless mode lets you run the Docker daemon and containers as a non-root user to mitigate
potential vulnerabilities in the daemon and the container runtime." Requires `newuidmap`/`newgidmap` and
65,536 subordinate ids per user.
**Contributes**: The preferred-form column for the socket row: build images without a host daemon
(rootless BuildKit, Buildah, Kaniko), or give each job its own daemon (DinD, at the cost of privileged
mode, which GitLab confines to ephemeral VMs), or run the daemon rootless so a socket escape lands as an
unprivileged user.
**Caveats**: Rootless limits the *host-root* consequence but not cross-job sharing: a rootless daemon
shared by every job on a VM still shares its image store and volumes among them. Limitations of rootless
for CI were **not read** (linked pages not opened).

## 3. Autoscaling semantics (GitLab Runner; GitHub equivalents)

Current GitLab Runner release: **v19.5.0, released 2026-10-15** (GitLab releases API, queried 2026-10-21).
Its `go.mod` pins `gitlab.com/gitlab-org/fleeting/taskscaler v0.0.0-20260908152840-1f87885729aa`, the
library that does the scaling arithmetic.

### 3.1 GitLab Docs, `[runners.autoscaler]` and `[[runners.autoscaler.policy]]`

**Work**: GitLab. "Advanced configuration", https://docs.gitlab.com/runner/configuration/advanced-configuration/
(vendor docs, official for own product). `[runners.autoscaler]` "Introduced in GitLab Runner v15.10.0".
**Evidence** (definitions, quoted): `capacity_per_instance` "The number of jobs that can be executed
concurrently by a single instance." `max_use_count` "The maximum number of times an instance can be used
before it is scheduled for removal." `max_instances` "The maximum number of instances that are allowed, this
is regardless of the instance state (pending, running, deleting)" (0 = unlimited).
`instance_ready_command` runs on each new instance; failure removes it. `delete_instances_on_shutdown`
default false. Policy block: `periods` "An array of unix-cron formatted strings to denote the period this
policy is enabled for. Default: `* * * * *`"; `timezone` "The time zone used when evaluating the unix-cron
period. Default: The system's local time zone."; `idle_count` "The target idle capacity we want to be
immediately available for jobs."; `idle_time` "The amount of time that an instance can be idle before it is
terminated."; `scale_factor` "The target idle capacity we want to be immediately available for jobs, on
top of the `idle_count`," as a factor of in-use capacity, default `0.0`; `scale_factor_limit` "The maximum
capacity the `scale_factor` calculation can yield." Combination: "When `scale_factor` is set,
`idle_count` becomes the minimum `idle` capacity and the `scaler_factor_limit` the maximum `idle`
capacity." Idle removal: "Instances that exceed the configured `idle_time` are removed, unless needed to
maintain the required `idle_count` job capacity." `preemptive_mode`: "With preemptive mode turned on, jobs
are requested only when an instance is confirmed to be available. This action allows jobs to start almost
immediately without provisioning delays"; off, "jobs are requested first, and then the system attempts to
find or provision" capacity. The doc's example has two policies: an all-hours `idle_count = 0`, and a
weekday 08:00–15:59 `idle_count = 1`, `idle_time = "30m0s"`.
**Canonicity**: The product's reference. **Caveat**: the two doc sentences on `scale_factor` disagree with
each other ("on top of" reads as *add*; "minimum ... maximum" reads as *clamp*), and both disagree with the
code (3.2).

### 3.2 The taskscaler source — how idle_count and scale_factor actually combine

**Work**: GitLab. `fleeting/taskscaler`, `internal/capacity/capacity.go`, `RequiredInstances`
(https://gitlab.com/gitlab-org/fleeting/taskscaler/-/raw/main/internal/capacity/capacity.go; github-class
source host, primary for the code's behaviour). File last changed 2026-04-27 (commit 3e8ff986), before the
2026-09-08 taskscaler revision Runner v19.5.0 pins, so main is what v19.5.0 runs. The scale-factor lines
date from at least 2024-06 (commit 782c60b1, "Fix required instance calc preventing demand runaway").
**Evidence** (code lines, quoted):
```go
demand := max(info.IdleCount, pending)
desired := info.Acquired + demand
// use (acquired*scale factor) if it's greater than our existing desired
// capacity
if info.ScaleFactor > 0 {
    scale := int(math.Ceil(info.ScaleFactor * float64(info.Acquired)))
    if info.ScaleFactorLimit > 0 {
        scale = min(scale, info.ScaleFactorLimit)
    }
    desired = max(desired, scale)
}
desired += info.UnavailableCapacity
```
then divided by `CapacityPerInstance` (rounded up), less instances running or being created, capped at
`max_instances`.
**Reading** (this document's, from the code):
- **Total desired capacity = in-use + max(idle_count, pending)**, unless `ceil(scale_factor × in-use)`,
  capped at `scale_factor_limit`, is larger. `scale_factor` and `idle_count` **overlap (max), they do
  not add**; and the scale term is compared with *total* capacity, not idle capacity.
- Consequence: **`scale_factor ≤ 1.0` never changes the result**, because `ceil(1.0 × A) ≤ A + idle_count`
  for every A. Ignoring pending jobs, idle target = `max(idle_count, min(ceil(scale_factor × A),
  scale_factor_limit) − A)` for A slots in use, so the factor adds idle only when `scale_factor > 1`, and
  `scale_factor_limit` caps the *total* the factor can ask for, not the idle part. With `scale_factor = 2.0`, `idle_count = 2`, `limit = 8`: at 4 in use, desired is
  max(6, 8) = 8 (4 idle); at 6 in use, max(8, min(12, 8)) = 8 (2 idle) — the limit stops idle growth.
- `pending` (jobs waiting for capacity) raises demand above `idle_count`; queued jobs, not the factor,
  drive scale-up under burst.
**Canonicity**: The executing code; outranks the prose where they disagree.
**Contributes**: The overlap-vs-add answer the task asks for, and a doc/code conflict a fleet reviewer
must know (Conflicting Information 2).
**Checkable in runner config?** Yes: `scale_factor` in (0, 1.0] is a no-op worth flagging as a
misunderstanding; `scale_factor_limit` below `idle_count + typical in-use` is a no-op too.
**Caveats**: First read through a summarising fetch tool, line by line. **Confirmed 2026-10-21:** the
orchestrating session downloaded `capacity.go` from `main` with curl and read `RequiredInstances` whole
(lines 68–125). It matches the quoted lines: `demand := max(info.IdleCount, pending)`,
`desired := info.Acquired + demand`, then `desired = max(desired, min(ceil(ScaleFactor × Acquired),
ScaleFactorLimit))`. `Acquired` is still read as in-use job slots from the field name and call site.
`main` was read, not the revision Runner v19.5.0 pins; the two match only if no commit touched the file
after 2026-04-27. Confidence: High.

### 3.3 GitLab Docs, "Docker Autoscaler executor"

**Work**: GitLab. https://docs.gitlab.com/runner/executors/docker_autoscaler/ (vendor docs). "Introduced
in GitLab Runner 15.11.0 as an experiment", beta in 16.6, "Generally available in GitLab Runner 17.1."
**Evidence**: The executor "creates instances on demand to accommodate the jobs that the runner manager
processes"; it "uses fleeting plugins to autoscale"; on AWS it needs "An AWS autoscaling group. The runner
directly manages all scaling behavior." Example with `idle_count = 5`, `idle_time = "20m0s"`,
`capacity_per_instance = 1`: "the runner tries to keep 5 whole instances (because the capacity per
instance is 1) available for future demand. These instances stay for at least 20 minutes." With capacity
and use count both 1, "each job is given a secure ephemeral instance that cannot be affected by other
jobs" and "As soon the job is complete the instance it was executed on is immediately deleted."
`concurrent` is set to "maximum number instances * capacity per instance".
**Contributes**: (a) `idle_count` counts **job slots**, not instances — instances = idle_count ÷
capacity_per_instance; (b) GitLab's own wording ties "secure ephemeral instance" to
`capacity_per_instance = 1` **and** `max_use_count = 1`; (c) the ASG is a dumb pool: desired capacity is set
by the runner, so ASG scaling policies and EC2 warm pools are not in play (4.4).
**Warm-instance arithmetic (interpretation)**: with `max_use_count = 1`, an idle instance serves exactly
one job and is then deleted, so a floor of N idle slots absorbs **the first N arrivals of a burst**; the
(N+1)th waits a boot, and each consumed warm instance is replaced by a boot that helps the *next* arrival,
not the one that consumed it. With `max_use_count > 1`, a finished instance returns to idle, so the same
warm instance absorbs one arrival per job duration rather than one in total. This is the "absorbs one boot
only when max_use_count=1" claim: true, and it is the whole capacity case for reuse.

### 3.4 Legacy Docker Machine autoscaling (contrast)

**Work**: GitLab. "Docker Machine Executor autoscale configuration",
https://docs.gitlab.com/runner/configuration/autoscale/ (vendor docs).
**Evidence**: "The `IdleCount` parameter defines a static number of idle machines that the runner should
sustain." `IdleScaleFactor` (experimental) "defines the desired idle capacity as a factor of" machines in
use, applicable only if `IdleCount > 0`, with `IdleCount` the upper limit and `IdleCountMin` the floor
("no more than 50 (the value of IdleCount) and no less than 5 (the value of IdleCountMin)"). `MaxBuilds`
example: "Each machine can handle up to 100 jobs in a row (after this it will be removed)". "The Docker
Machine executor was deprecated in GitLab 17.5 and is scheduled for removal in GitLab 20.0 (May 2027)."
**Contributes**: The legacy semantics were a **clamp on idle machines** (IdleCountMin ≤ idle ≤ IdleCount);
the doc sentence in 3.1 ("idle_count becomes the minimum idle capacity ...") describes this legacy clamp,
not the taskscaler code. An assistant or engineer carrying Docker Machine intuitions to docker-autoscaler
will misread `scale_factor`. `MaxBuilds` ↔ `max_use_count`; `IdleCount` ↔ `idle_count` (machines vs slots).
**Caveats**: The inference that the 3.1 sentence was carried over from Docker Machine is this document's.

### 3.5 GitHub equivalents: ARC runner scale sets; Terraform AWS GitHub Runner module

**Work**: GitHub Docs, "Deploying runner scale sets with Actions Runner Controller",
https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners-with-actions-runner-controller/deploying-runner-scale-sets-with-actions-runner-controller
(vendor docs). Terraform module docs, https://github-aws-runners.github.io/terraform-aws-github-runner/
(github-aws-runners org, formerly philips-labs — rename from prior knowledge, **not re-verified**;
github.io, medium-high; **module version not shown on the page**).
**Evidence**: ARC `minRunners` "is the min number of idle runners. The target number of runners created will
be calculated as a sum of minRunners and the number of jobs assigned to the scale set"; `maxRunners` "the
max number of runners the auto scaling runner set will scale up to". Dind mode: "The Docker-in-Docker
container requires privileged mode", default image runs the daemon as root. Kubernetes mode without a job
container "can give the runner pod elevated privileges with the Kubernetes API server". Runner groups
"control which organizations or repositories have access to your runner scale sets"; run production
workloads isolated, as a shared cluster "could pose a security risk". Terraform module: ephemeral mode
creates "a new runner for each workflow job event" and "the instance is terminated immediately after the
workflow is finished"; "Use the ephemeral runners for org level runners to improve the security of your
runners"; "For ephemeral runners a pool can be configured. The pool maintains a minimum number of runners
based on a schedule" (org-level only, opt in); for non-ephemeral runners an idle config keeps "a minimum
number of runners based on a schedule"; scale-up is driven by `workflow_job` webhooks "with status
`queued`".
**Contributes**: Cross-platform confirmation that **a warm floor adds to in-use demand** (ARC: "sum";
GitLab code: `Acquired + max(idle_count, pending)`), and that the GitHub ecosystem's defaults pair a warm
pool with **ephemeral** runners — warmth without reuse.
**Checkable in runner config?** Yes: `minRunners`, `maxRunners`, `containerMode`, ephemeral flag, pool
schedule.

## 4. Capacity, queueing and cost

### 4.1 DORA, change lead time

**Work**: DORA (Google Cloud). "DORA's software delivery performance metrics", https://dora.dev/guides/dora-metrics/
("Last updated: January 5, 2026"; dora.dev listed DevOps research, high). Book lineage: Forsgren, Humble,
Kim, *Accelerate* (IT Revolution, 2018) — **not re-verified this session**.
**Evidence**: Change lead time is "The amount of time it takes for a change to go from committed to
version control to deployed in production." Five metrics: change lead time, deployment frequency, failed
deployment recovery time (throughput); change fail rate, deployment rework rate (instability).
**Contributes**: Runner queue wait sits inside commit-to-production, so it is lead time — every minute a
job waits for an instance is a minute of change lead time, paid on every stage that waits. The pipeline
sibling owns job *speed*; this document owns the *wait for a machine*.
**Checkable in runner config?** No; it is the metric the config is tuned against.
**Caveats**: DORA does not decompose lead time into queue vs run; the attribution to runner capacity is
this document's.

### 4.2 Little's law

**Work**: John D. C. Little. "OR FORUM — Little's Law as Viewed on Its 50th Anniversary". *Operations
Research* 59(3): 536–549, June 2011. DOI 10.1287/opre.1110.0940. Crossref is-referenced-by-count **192**
(queried 2026-10-21). (Original proof: Little, *Operations Research* 9(3), 1961 — prior knowledge, **count
not taken**.)
**Evidence**: L = λW — mean number in system equals arrival rate times mean time in system; holds for any
stationary queue regardless of arrival or service distribution (statement of the law from prior
knowledge; the 2011 paper's text was **not opened**, only its Crossref record).
**Contributes**: The sizing arithmetic for a warm floor. Busy slots ≈ arrival rate × job duration: at 12
jobs/hour of 10 minutes each, 2 slots are busy on average. A floor sized to the *mean* covers steady
load; a burst (a merge train, a scheduled pipeline, a monorepo fan-out) arrives faster than boots can
follow and is what the floor exists for.
**Caveats**: Little's law gives means, not tails; burst sizing needs the arrival distribution (4.3).

### 4.3 Queueing with setup time — Harchol-Balter and co-authors

**Work**: (a) Anshul Gandhi, Mor Harchol-Balter, Ivo Adan. "Server farms with setup costs". *Performance
Evaluation*, Nov 2010. DOI 10.1016/j.peva.2010.07.004. Crossref **140**. Author PDF at
https://www3.cs.stonybrook.edu/~anshul/perf_mmk_2010.pdf (academic, high; abstract read). (b) Jalani K.
Williams, Mor Harchol-Balter, Weina Wang. "The M/M/k with Deterministic Setup Times". *Proc. ACM Meas.
Anal. Comput. Syst.* 6(3), art. 56, Dec 2022 (SIGMETRICS '23). DOI 10.1145/3570617. Crossref **9**.
(c) Gandhi, Harchol-Balter, Adan. "Decomposition results for an M/M/k with staggered setup". *ACM
SIGMETRICS PER*, 2010. DOI 10.1145/1870178.1870195. Crossref **3**. Book: Harchol-Balter, *Performance
Modeling and Design of Computer Systems* (Cambridge UP, 2013), chs. 14 (M/M/k) and 15 (capacity
provisioning) per Cambridge Core chapter pages — **book text not read**.
**Evidence**: (a) "Setup costs always take the form of a time delay, and sometimes there is additionally a
power penalty"; the paper derives "the first closed-form solutions and approximations for the mean
response time and mean power consumption in server farms with setup costs", and asks "whether it pays to
turn servers off when they are idle". "For some variants, we find that the distribution of response time
can be decomposed into the sum of response time for a server farm without setup and the setup time."
(b) Gives a lower bound on delay from deterministic setup, "highly accurate when setup time is much larger
than job service time" (Crossref abstract, summarised).
**Canonicity**: Harchol-Balter (CMU) is the standard modern author on performance modelling; (a) is the
widely cited setup-cost paper.
**Contributes**: The academic form of the case's intuition. A CI instance boot is a **setup time**; in the
staggered-setup model, **response time = no-setup response time + setup time** — a job that misses warm
capacity pays the full boot on top of its run. And whether idle servers should stay on is the exact
trade-off a warm floor makes (cost of idle vs delay of setup).
**Interpretation for a fleet**: with `max_use_count = 1`, every job consumes a warm instance and triggers a
replacement boot; the replacement serves the *next* arrival, so under a burst of B jobs and a floor of N
slots, B − N jobs pay a boot (if `max_instances` allows) and the floor refills only after the burst. Warm
capacity therefore helps the next burst more than the current one once a burst exceeds the floor. Reuse
(`max_use_count > 1`) turns each finishing job's instance back into warm capacity *during* the burst.
**Checkable in runner config?** The inputs are: `idle_count`, `capacity_per_instance`, `max_use_count`,
`max_instances`, periods — plus measured boot time and arrival pattern, which config does not show.
**Caveats**: The models assume Poisson arrivals and exponential service; CI arrivals are bursty and
correlated. The papers support the *shape* of the trade-off, not a number.

### 4.4 AWS EC2 Auto Scaling warm pools

**Work**: AWS. "Decrease latency for applications with long boot times using warm pools",
https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-warm-pools.html (official, high).
**Evidence**: "A warm pool gives you the ability to decrease latency for your applications that have
exceptionally long boot times"; "Creating a warm pool when it's not required can lead to unnecessary
costs. If your first boot time does not cause noticeable latency issues for your application, there
probably isn't a need for you to use a warm pool." States: "With stopped instances, you pay only for the
volumes that you use and the Elastic IP addresses attached to the instances"; `Running` in the warm pool
"is highly discouraged to avoid incurring unnecessary charges". "If your warm pool is depleted when there
is a scale-out event, instances will launch directly into the Auto Scaling group (a cold start)." An
"instance reuse policy" can return scaled-in instances to the pool instead of terminating them.
**Contributes**: The cost axis: a **running** idle runner bills compute; a **stopped** pre-initialized
instance bills only EBS (and EIPs) and starts faster than a cold launch. AWS's own warning against warm
capacity "when it's not required" is the counterweight to always-on floors.
**Checkable in runner config?** Partly. **Caveat**: docker-autoscaler drives the ASG's desired capacity
directly ("The runner directly manages all scaling behavior", 3.3); whether an ASG warm pool composes with
the fleeting AWS plugin was **not found** in either vendor's docs (Knowledge Gaps). Note AWS's reuse policy
returns *instances* to a pool — on a runner fleet that is VM reuse, with the isolation cost of 2.4.

### 4.5 Measuring queue wait

**Work**: GitLab Jobs API https://docs.gitlab.com/api/jobs/ ; GitLab infrastructure runbook
https://runbooks.gitlab.com/ci-orchestration/alerts/CiOrchestrationServiceJobQueueDurationApdexSLOViolation/
(GitLab's own operations runbook, medium-high); GitHub REST "Workflow jobs"
https://docs.github.com/en/rest/actions/workflow-jobs (vendor docs).
**Evidence**: GitLab job objects carry `created_at`, `started_at`, `queued_duration` (e.g. `0.123`) and
`duration`; the API page **defines none of them** — they appear in examples only. GitLab's runbook defines
the server-side metric: "The `job_queue_duration_seconds` histogram measures the time between job creation
and runner assignment", emitted "when a runner picks up a job via `POST /api/v4/jobs/request`"; GitLab.com's
SLO uses a 1-second satisfied threshold for shared runners and 30 seconds for non-shared runners. GitHub
workflow jobs carry `created_at`, `started_at`, `completed_at`, `runner_name`, `runner_group_name`,
`labels` (types only; no prose definitions).
**Contributes**: The truthful measures: GitLab `queued_duration` per job (or `started_at − created_at`;
note a job in `created` state waiting on `needs:` is not runner wait), GitLab Runner's own metrics, and
GitHub `started_at − created_at` grouped by `runner_group_name` / labels. Measure per pool and per hour,
since the case's floor changes by `periods`.
**Caveats**: Neither API documents whether its timestamps exclude dependency waits; GitLab's runbook
metric starts at "job creation", which for a job behind `needs:` may include upstream time. **Unconfirmed**
— see Knowledge Gaps.

## 5. Cache locality

### 5.1 GitLab Docs, "Caching in GitLab CI/CD" and `[runners.cache]`

**Work**: GitLab. https://docs.gitlab.com/ci/caching/ ; `[runners.cache]` in
https://docs.gitlab.com/runner/configuration/advanced-configuration/ (vendor docs, official for own
product).
**Evidence**: "By default, the cache is stored on the machine where GitLab Runner is installed"; "Cache is
stored where GitLab Runner is installed and uploaded to S3 if distributed cache is enabled." For several
runners: "Use multiple runners that have distributed caching, where the cache is stored in S3 buckets";
with concurrent Docker runners "files cached by one runner instance are not found in the cache by another
runner instance". "Caching is an optimization, but it isn't guaranteed to always work." Protected
separation: "By default, protected and non-protected branches do not share the cache"; keys get a
`-protected` or `non_protected` suffix; "The cache separation with cache key names is a security feature"
that "should only be disabled in an environment where all users with Developer role are highly trusted."
`[runners.cache]`: `Type` "One of: `s3`, `gcs`, `azure`"; `Shared` "Enables cache sharing between runners.
Default is `false`." S3 `AuthenticationType` "Defaults to `iam` if `ServerAddress`, `AccessKey`, or
`SecretKey` are missing", in which case "the adapter uses the profile attached to the GitLab Runner
machine."
**Canonicity**: Product reference.
**Contributes**:
- **Why a local cache never restores on one-job-per-instance machines (interpretation from the quotes)**:
  the local cache lives on the instance (a Docker volume, 2.4); with `max_use_count = 1` the instance is
  deleted after its job, so every job starts with an empty local cache. Only a distributed cache (S3)
  survives. Reuse would make the local cache hit *sometimes* — whenever a job lands on an instance that
  ran a job with the same key — which is the "cheapest cache fix" and is unpredictable by design.
- **GitLab already partitions cache by trust**: protected and unprotected pipelines get different keys,
  and GitLab calls that "a security feature" — the cache-poisoning boundary SLSA L3 states (1.1). A reused
  VM with a local cache keeps that key separation only for `cache:`; it does nothing for the Docker image
  store and build cache on the same host (2.4), which have no protected/unprotected split.
- S3 cache with `iam` auth uses the **runner manager's** instance profile. Whether jobs reach the bucket
  directly or through manager-issued pre-signed URLs is from prior knowledge (pre-signed), **not verified
  this session**.
**Checkable in runner config?** Yes: `[runners.cache] Type`, `Shared`, the bucket's IAM, and the project
setting that disables protected cache separation.

### 5.2 Docker Docs, "Cache storage backends" and `docker buildx build` cache flags; GitLab layer caching

**Work**: Docker. https://docs.docker.com/build/cache/backends/ and the buildx reference (2.4); GitLab
"Make Docker-in-Docker builds faster with Docker layer caching",
https://docs.gitlab.com/ci/docker/docker_layer_caching/ (vendor docs).
**Evidence**: Backends: "`inline`: embeds the build cache into the image"; "`registry`: embeds the build
cache into a separate image"; "`local`: writes the build cache to a local directory"; `gha`; `s3` and
`azblob` (marked unreleased on the page). "The default `docker` driver supports the `inline`, `local`,
`registry`, and `gha` cache backends" only with the containerd image store; otherwise another driver is
needed. "In `min` cache mode (the default), only layers that are exported into the resulting image are
cached", while "in `max` cache mode, all layers are cached, even those of intermediate steps"; "`max` cache
is more likely to get more cache hits". CI needs external cache because "Such environments usually have
little-to-no persistence between runs." GitLab: "When you use Docker-in-Docker, Docker downloads all layers
of your image on every build"; registry cache "reads from a dedicated cache image with `--cache-from`, and
updates it with `--cache-to`"; for inline cache "The `--build-arg BUILDKIT_INLINE_CACHE=1` argument is
required. Without this argument, caching silently fails."
**Contributes**: The **isolation-preserving cache fix**: keep machines ephemeral and move layer cache to
the registry (`--cache-to type=registry,mode=max` / `--cache-from`), keyed or pushed per trust class
(protected branches write the cache; open branches read it or write their own). That restores layer reuse
without a shared daemon, so it needs neither the socket nor VM reuse.
**Checkable in runner config?** In CI config: `--cache-from`/`--cache-to`, `BUILDKIT_INLINE_CACHE`, which
jobs may push to the cache ref.
**Caveats**: Registry cache costs a pull per build and registry storage; it is slower than a warm local
cache. Who may write the cache ref is the poisoning question again — a cache image that open-branch jobs
can push is a shared cache across trust classes (SLSA L3 "inject false entries into a build cache").

### 5.3 When reuse is "the cheapest cache fix" (interpretation)

Reuse buys cache hits for free on the local `cache:` volume, the Docker image store and the BuildKit cache,
and it removes a boot from every reused job. What it costs, by source: SLSA L3 "persist or influence the
build environment of a subsequent build" (1.1); OWASP SEC-5 "Revert the execution node to its pristine
state" (1.3); NIST 800-190's "residual data, such as caches or local volumes" crossing groups (2.5); and,
with the socket mounted, host root shared among every job the VM ever runs (2.1–2.4). The isolation-
preserving alternatives are a distributed cache for `cache:` (5.1) and registry layer cache (5.2).
Confidence: High that the trade exists (five sources); the claim that reuse is the *cheapest* fix is
this document's.

## 6. Credentials on runners

`rules/security.md` already owns the CI *token* row ("a CI token with `write-all`", CWE-732/-250) and the
`pull_request_target` row (CWE-829). This section covers credentials that live on, or are reachable from,
the *machine*.

### 6.1 OIDC / workload identity federation instead of stored keys

**Work**: GitLab Docs, "Configure OpenID Connect in AWS to retrieve temporary credentials",
https://docs.gitlab.com/ci/cloud_services/aws/ ; GitHub Docs, "About security hardening with OpenID
Connect", https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect
(vendor docs); OWASP CICD-SEC-6 (1.3).
**Evidence**: GitLab: the aim is to "retrieve temporary credentials from AWS without storing secrets"; the
job requests a token with `id_tokens` and calls `sts:AssumeRoleWithWebIdentity`; `CI_JOB_JWT_V2` "was
removed in GitLab 17.0" — "Use ID tokens instead." Trust policies should "limit authorization to a
specific group, project, branch, or tag", e.g. `sub` =
`project_path:mygroup/myproject:ref_type:branch:ref:main`; on Self-Managed and Dedicated "only the `sub`
and `aud` claims are supported as AWS condition keys". GitHub: "You won't need to duplicate your cloud
credentials as long-lived GitHub secrets"; the provider "issues a short-lived access token that is only
valid for a single job, and then automatically expires"; the provider checks "the OIDC token's subject and
other claims" against the role's trust conditions; repositories created after 2026-07-15 get a new default
subject format with owner and repository ids. OWASP SEC-6: "Prefer using temporary credentials over static
credentials."
**Contributes**: The preferred form for a deploy credential: **a per-job token whose `sub` names the
project and protected ref, exchanged for a role** — not an access key in a CI variable, and not an instance
profile that every job on the VM inherits. The trust boundary moves from "which machine" to "which
project, ref and environment".
**Checkable in runner config?** In IaC: an IAM role trust policy with `sts:AssumeRoleWithWebIdentity` whose
`sub` condition is a wildcard over projects or refs is checkable; so is an `AKIA…` key in CI variables
(already `security.md`'s CWE-798 row for committed config).
**Caveats**: On GitLab Self-Managed the AWS condition can key only on `sub` and `aud`, so `ref_protected`
cannot be a condition there; scope by branch name in `sub` and protect that branch.

### 6.2 Instance roles, the metadata service, and pool separation

**Work**: AWS, "Use the Instance Metadata Service to access instance metadata",
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html (official,
high); GitHub hardening (1.4); GitLab runner security (1.5); OWASP SEC-5 (1.3).
**Evidence**: AWS: IMDSv2 is "session-oriented"; "By default, the response to `PUT` requests has a response
hop limit (time to live) of `1` at the IP protocol level", and "you might need a bigger hop limit for
backward compatibility with container services running on the instance." Instance metadata includes
`iam/` (the instance profile's credentials). GitHub names "Azure or AWS metadata services" as what a job on
a self-hosted runner can reach; GitLab lists "Filtering access to cloud provider metadata endpoints";
OWASP SEC-5 names "the AWS metadata service" as a credential source and says not to share nodes across
pipelines "that require access to different resources".
**Contributes**: **An instance role is a credential every job on that instance holds.** IMDSv2 with hop
limit 1 keeps a container on a bridge network from fetching it — but a job with the Docker socket can start
a sibling with `--network host` and fetch it anyway (interpretation from 2.1 + the hop-limit mechanics).
So a pool's role must be one its least-trusted job may hold. In the case fleet, the open pool carrying
**no role** is the right shape; the deploy and state pools carry roles, so **who can run a job there** is the
whole control.
**Checkable in runner config?** Yes: `instance profile` on the launch template per pool; IMDS
`HttpTokens = required` and `HttpPutResponseHopLimit = 1`; the runner manager's own role (it calls EC2
and S3) kept on the manager, not the job instances.
**Caveats**: The `--network host` bypass is this document's inference, not stated by AWS or GitLab.

### 6.3 Protected runners, tags, and separating deploy pools from open pools

**Work**: GitLab Docs, "Configuring runners", https://docs.gitlab.com/ci/runners/configure_runners/ ;
GitLab runner security (1.5); GitHub runner groups (1.4, 3.5).
**Evidence**: Protected runners: "To ensure runners don't reveal sensitive information, you can configure
them to only run jobs on protected branches"; they "can optionally run jobs in merge request pipelines".
Tags: "You can use tags to control the jobs a runner can run"; a runner can be "allowed to run untagged
jobs". GitLab runner security: privileged runners should "execute jobs only on protected branches". GitHub:
runner groups "control which organizations or repositories have access to your runner scale sets".
**Contributes (interpretation)**: **Tags route; protection authorizes.** Anyone who can edit
`.gitlab-ci.yml` on an unprotected branch can add any tag, so a tag alone never keeps open-branch code off a
deploy pool. The control is a **protected** runner (or a runner registered only to projects whose
pipelines are all trusted), backed by protected branches and protected variables. The optional
"run jobs in merge request pipelines" setting re-opens a protected runner to MR code and needs the same
scrutiny as `pull_request_target` in `security.md`.
**Checkable in runner config?** Yes: the runner's `access_level` / protected flag, `run_untagged`, and
project/group assignment (GitLab API `GET /runners/:id`); GitHub runner-group repository access.
**Caveats**: No GitLab page found that says in so many words "tags are not a security boundary"; that is
this document's reading of the tag and protection docs.

### 6.4 Machine-wide trust of a private CA, and instance lifetime

**Work**: GitLab Docs, "Self-signed certificates or custom Certification Authorities",
https://docs.gitlab.com/runner/configuration/tls-self-signed/ (vendor docs).
**Evidence**: By default "GitLab Runner reads the system certificate store and verifies the GitLab server"
against it; alternatives are `tls-ca-file` and the predefined PEM at `/etc/gitlab-runner/certs/`. "The
Docker container running the user scripts doesn't have the certificate files installed by default"; when a
certificate is mapped, the helper image "will automatically install it". Chain injection via
`CI_SERVER_TLS_CA_FILE` "is secure, but makes the Runner a single point of trust." Skipping verification
with `GIT_SSL_NO_VERIFY` is "a temporary and insecure workaround".
**Contributes (interpretation)**: Trusting the GitLab CA *machine-wide* means the host's system trust store
decides what the runner, the Docker daemon (registry pulls) and every tool on the host will accept. Adding a
trusted CA is not the risk — the CA's *private key* is not on the runner. The risk is **write access to
that trust store**: a job holding the Docker socket can mount `/` and add its own root, after which every
later TLS connection from that host — runner to GitLab, daemon to registry, later jobs to package mirrors —
trusts the attacker. With `max_use_count = 1` that tampering dies with the instance after one job; with
reuse it persists for the instance's lifetime, bounded by `max_use_count` and `idle_time`. **Instance
lifetime is the exposure window for host tampering of any kind**; the trust store is the sharpest example
because it silently downgrades every later connection.
**Checkable in runner config?** Partly: whether the CA is installed system-wide (AMI build / user data) vs
`tls-ca-file`; socket mount; `max_use_count`.
**Caveats**: No source found that discusses CI trust-store tampering as such; the chain is assembled from
Docker's "/ mounted" statement (2.1) and GitLab's CA mechanics. `security.md` already flags disabling TLS
verification (CWE-295); `GIT_SSL_NO_VERIFY=true` in CI config is that row.

## 7. Hygiene and lifecycle

### 7.1 Cleanup on reused hosts

**Work**: GitLab runner security (1.5); GitLab Docker executor (2.4).
**Evidence**: "When you enable `FF_ENABLE_JOB_CLEANUP`, the build directory your runner uses on the host is
cleaned up after each build." "All directories defined in `volumes =` are persistent between builds." "The
`clear-docker-cache` script does not remove Docker images because they are not tagged by the GitLab
Runner."
**Contributes**: GitLab's own cleanup tools cover the build directory and cache volumes, **not** the
daemon's images, build cache, or anything a socket-holding job did to the host. Cleanup narrows what
persists on a reused VM; it does not restore SLSA L3's "pristine" state.
**Checkable in runner config?** Yes: the feature flag, a scheduled `clear-docker-cache`, `docker system
prune` in a post-job hook or `instance_ready_command`.

### 7.2 Bounded reuse and immutable replacement

**Work**: GitLab `max_use_count` (3.1); Martin Fowler, "PhoenixServer", bliki, 2012-07-10,
https://martinfowler.com/bliki/PhoenixServer.html (martinfowler.com, medium-high); AWS warm pools "Update
the instances in a warm pool" (4.4); `rules/continuous-delivery.md` ("Environments are disposable and
reproducible"; anti-pattern "Snowflake servers").
**Evidence**: Fowler: "A server should be like a phoenix, regularly rising from the ashes"; configuration
drift is "ad hoc changes to a systems configuration that go unrecorded." `max_use_count` is "The maximum
number of times an instance can be used before it is scheduled for removal." AWS: with a new launch
template, "Any new instances are launched using the new AMI ... but existing instances are not affected";
an instance refresh is needed to replace them.
**Contributes**: `max_use_count` (and `idle_time`) is the **phoenix interval** of a runner instance: it
caps how many jobs' worth of drift, tampering and disk growth an instance accumulates, and how long an old
AMI keeps serving after a new one ships. `max_use_count = 1` is the limit case; reuse with a small bound
is a middle ground for a single trust class.
**Checkable in runner config?** Yes: `max_use_count` (0 means unlimited? — **default not confirmed on the
pages read**), `idle_time`, launch template AMI id vs the latest golden image.

### 7.3 Patching, golden images and runner versions

**Work**: OWASP CICD-SEC-5/-7 (1.3); NIST SP 800-190 (2.5); GitLab Runner docs, versions,
https://docs.gitlab.com/runner/ (vendor docs).
**Evidence**: OWASP: "Ensure the execution node is appropriately patched"; "If a security patch is
available, update the vulnerable component." NIST 800-190: "Use container-specific host OSs instead of
general-purpose ones to reduce attack surfaces." GitLab: the runner's major.minor "should stay in sync with
the GitLab major and minor version"; "Older runners may still work with newer GitLab versions, and vice
versa" but "features may not be available or work properly if a version difference exists"; on GitLab.com,
"keep GitLab Runner updated to the latest version". Docker Machine is deprecated (GitLab 17.5) and removed in
20.0 (May 2027) (3.4).
**Contributes**: Two version checks for a fleet review: runner manager version vs GitLab server version,
and the AMI's age vs its base OS patches. On ephemeral instances, patching *is* rebuilding the AMI; the
running fleet catches up at the pace of `max_use_count` / `idle_time`.

### 7.4 Retry only on infrastructure failures

**Work**: GitLab CI/CD YAML reference, `retry`, https://docs.gitlab.com/ci/yaml/#retry (vendor docs).
**Evidence**: `retry` accepts "`0` (default), `1`, or `2`". `retry:when` values include: `always` "Retry on
any failure (default)"; `script_failure` "Retry when: The script failed"; `runner_system_failure` "Retry if
there is a runner system failure (for example, job setup failed)"; `stuck_or_timeout_failure` "Retry when the
job gets stuck or times out. Deprecated in GitLab 19.1"; `job_execution_timeout` (also "Deprecated in GitLab
19.1"); `scheduler_failure` "Retry if the scheduler failed to assign the job to a runner"; `api_failure`;
`unknown_failure`; `data_integrity_failure`. Per gitlab-org/gitlab work item 602133 and MR 239415 (via
search snippets, gitlab.com, medium-high): GitLab 19.0 split `stuck_or_timeout_failure` into
`stuck_pending_with_matching_runners`, `stuck_pending_no_matching_runners`, `no_updates_running` and
`no_updates_canceling`, and `job_execution_timeout` into `server_timeout_running` and
`server_timeout_canceling`; the legacy names stay as aliases until removal in 20.0. **Breaking-changes entry
not opened.**
**Contributes**: The retry policy for a runner fleet: retry **infrastructure** failures
(`runner_system_failure`, `scheduler_failure`, the stuck/no-updates reasons — the failures a spot
interruption or a dead instance produces), never `script_failure` or bare `retry: 2` (`when` defaults to
`always`), which hides flaky tests — `continuous-delivery.md`'s "Fix flaky tests immediately". On GitLab
19.1+, name the split reasons rather than the deprecated `stuck_or_timeout_failure`.
**Checkable in runner config?** Yes, in `.gitlab-ci.yml`: `retry: N` with no `when`, or `when` containing
`always` or `script_failure`.
**Caveats**: Flaky-test policy as such is pipeline shape (sibling document); this row is about telling
machine failure from code failure.

### 7.5 Routing jobs to the right pool

See 6.3: tags route, protection authorizes; `run_untagged` decides whether an untagged job lands on a pool by
default. A deploy or state pool that accepts untagged jobs, or that is unprotected, will run open-branch
code.

## 8. Answering questions about a fleet truthfully

### 8.1 Declared state vs live state — Terraform and CloudFormation

**Work**: HashiCorp, "Manage resource drift" tutorial,
https://developer.hashicorp.com/terraform/tutorials/state/resource-drift ; `terraform plan` command
reference, https://developer.hashicorp.com/terraform/cli/commands/plan (vendor docs, official for own
product; tutorial requires "Terraform CLI, version 0.15.4 or later"). AWS, "Detect unmanaged configuration
changes to stacks and resources with drift detection",
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html (official,
high).
**Evidence**: Terraform: the state file can be "out of sync, or 'drift,' from the real infrastructure";
plan by default "Reads the current state of any already-existing remote objects to make sure that the
Terraform state is up-to-date"; `-refresh-only` "creates a plan whose goal is only to update the Terraform
state and any root module output values to match changes made to remote objects outside of Terraform", and
"A refresh-only operation does not attempt to modify your infrastructure". AWS: "users can change those
resources outside of CloudFormation"; drift detection checks "whether a stack's actual configuration
differs, or has *drifted*, from its expected configuration"; it "only determines drift for property values
that are explicitly set", and some properties cannot be compared at all.
**Canonicity**: The two dominant IaC tools' own docs; independent vendors agreeing.
**Contributes**: Three distinct sources of truth about a fleet, which can disagree: **(1) the IaC code**
(intent, at a commit), **(2) the IaC state** (what the tool last recorded), **(3) the live system** (what the
cloud API and the runner's `config.toml` say now). Both vendors say (2) can diverge from (3) and supply a
read-only way to compare (`plan -refresh-only`, drift detection). Neither tool sees settings it does not
manage — a runner's `config.toml` written by user data, a hand-edited policy.
**Checkable?** Yes, as a procedure: `terraform plan -refresh-only` (read-only) before stating the fleet's
configuration; GitLab `GET /runners/:id` for runner flags; `gitlab-runner --version` / the API's runner
`version` for versions.

### 8.2 Configuration drift as a named concept

**Work**: Fowler, "PhoenixServer" (2012) and "SnowflakeServer" (bliki, martinfowler.com, medium-high —
SnowflakeServer not opened this session); Kief Morris, *Infrastructure as Code*, 3rd ed. (O'Reilly; author
site https://infrastructure-as-code.com/book/ says "The third edition ... is available now, in print and
ebook editions"; 1st ed. 2016, 2nd ed. 2020; a Thoughtworks podcast of March 2025 dates the 3rd edition to
2025). `rules/continuous-delivery.md` anti-pattern: "Manual configuration changes — Drift between
environments".
**Evidence**: Fowler defines drift as "ad hoc changes to a systems configuration that go unrecorded." Morris's
book text on drift was **not read** (author site and search results only); the claim that it treats
"configuration drift" and "snowflake servers" as core anti-patterns is from knowledge of the 1st/2nd
editions, **not verified for the 3rd**.
**Contributes**: The vocabulary: any document about a fleet — a wiki page, a runbook, a README — is a
*recorded* configuration; the fleet drifts from it by every unrecorded change and, after a migration, by the
whole platform.

### 8.3 What the sources support — and what they do not (interpretation)

Supported (8.1, 8.2): the IaC state can lag the live system; the IaC code can lag the state; and the tools
provide read-only comparisons. So an answer about a fleet is only as current as the thing read, and the
reader must say which it was. Not found in any source: a statement that an assistant or engineer must
**refuse to answer from documentation of a decommissioned platform**. That rule — read the live system or the
current IaC, name which (with commit or timestamp), and treat docs about a retired platform (the Azure-era
runner docs after an AWS migration) as history, not evidence — is this document's extension of the drift
literature to *documents*. It is consistent with this repo's own CLAUDE.md practice ("Identify the
installed copy by `version` or `installPath` ... never by `gitCommitSha`", and every board line carrying
"its provenance and the query that produced it"). Confidence: Medium (the drift premise is High; the
extension to docs is unsourced).

---

## Synthesis

All of this section is **interpretation** built on the findings above. Each row names the finding it
rests on.

### What the platforms do for untrusted code (the "is reuse common?" evidence)

- GitLab.com hosted runners: "Each of your jobs runs in a newly provisioned VM, which is dedicated to the
  specific job"; "Ephemeral runner VMs serve a single job and are deleted right after the job execution";
  "Firewall rules do not permit communication between VMs" (https://docs.gitlab.com/ci/runners/hosted_runners/).
- GitHub-hosted runners: "each GitHub-hosted runner is a new virtual machine (VM)", except single-CPU
  runners, "hosted in a container on a shared VM" (about-github-hosted-runners).
- GitHub recommends ephemeral runners for autoscaling (1.4); the Terraform AWS module recommends ephemeral
  runners "to improve the security of your runners" (3.5); GitLab ties "secure ephemeral instance" to
  `capacity_per_instance = 1` and `max_use_count = 1` (3.3).
- Reuse exists and is documented: persistent self-hosted runners (GitHub's non-ephemeral registration),
  Docker Machine's `MaxBuilds` example of 100 (3.4), AWS's warm-pool "instance reuse policy" (4.4).

Reading: **one-job-per-VM is the platforms' own choice for code they do not trust, and the documented
default recommendation for autoscaled self-hosted fleets; reuse is a documented, supported option for
fleets whose jobs share a trust class.** No source gives prevalence figures (Knowledge Gaps).

### Ranked shortlist (the guidance's spine)

| Rank | Work | Half | Why it earns a place |
|---|---|---|---|
| 1 | **SLSA v1.0 Build track**, L3 "Isolated" (1.1) | Principle + flag | The only leveled spec that states the boundary: no build may "persist or influence the build environment of a subsequent build" or "inject false entries into a build cache used by another build"; "an ephemeral build environment MUST be provisioned for each build". |
| 2 | **OWASP Top 10 CI/CD Security Risks** — CICD-SEC-5, -6, -7 (1.3) | Flag ids | The CI-specific risk list; SEC-5 supplies the reuse test ("Shared nodes should be used only for pipelines with identical levels of confidentiality"; "Revert the execution node to its pristine state"). Ids for the table. |
| 3 | **Docker Engine security** + **CIS Docker Benchmark** socket control (2.1, 2.2) | Flag | "only trusted users should be allowed to control your Docker daemon"; the `docker` group "grants root-level privileges"; CIS 5.31/5.32 forbids mounting the socket in containers. |
| 4 | **GitLab Runner security** and **Docker build** docs (1.5, 2.3, 2.4) | Flag + preferred form | The vendor's own statement that socket binding means "you effectively disable the container's security mechanisms"; privileged only on "isolated and ephemeral virtual machines" with protected branches; what persists between builds. |
| 5 | **GitHub self-hosted runner hardening** + ephemeral/JIT (1.4) | Flag | "should almost never be used for public repositories"; "can be persistently compromised by untrusted code"; metadata services as a target. Independent vendor corroborating 4. |
| 6 | **NIST SP 800-190** (2017; 77 Crossref) (2.5) | Principle | "Only group containers with the same purpose, sensitivity, and threat posture on a single host OS kernel"; names caches and local volumes as the residue. Federal, vendor-neutral. |
| 7 | **NIST SP 800-204D** (2024; 20 Crossref) (1.2) | Principle | Federal CI/CD guidance: "a secure isolated platform", hardened build servers, control plane at higher trust than build steps. Corroborates 1. |
| 8 | **GitLab autoscaler docs + taskscaler source** (3.1–3.3) | Config semantics | What `idle_count`, `scale_factor`, `max_use_count`, `capacity_per_instance` actually do; the code settles the doc's ambiguity. |
| 9 | **Gandhi, Harchol-Balter, Adan (2010; 140 Crossref)** with Little (2011; 192) and DORA (4.1–4.3) | Capacity principle | Boot is setup time; a job that misses warm capacity pays the setup on top of its run; queue wait is lead time. |
| 10 | **Vendor credential docs**: GitLab/GitHub OIDC, AWS IMDS (6.1, 6.2) | Flag + preferred form | Per-job federated tokens scoped by `sub`; an instance role is held by every job on the instance. |
| 11 | **Terraform / CloudFormation drift docs** + Fowler "PhoenixServer" (8.1, 8.2, 7.2) | Truthfulness procedure | Declared state, recorded state and live state differ; read-only comparisons exist; bounded lifetime limits drift. |

**Background, not spine**: AWS warm pools (cost model; not used by docker-autoscaler), ARC and the
Terraform AWS module (GitHub-side equivalents), Docker rootless (a mitigation), Docker Machine docs (legacy
contrast), *Infrastructure as Code* 3rd ed. (vocabulary; text not read).

### Candidate always-flag list (runner configuration and fleet answers)

Ids are this document's (`RUN-n`). The OWASP CI/CD id is the primary citation; CWE fits are candidates
**not verified on cwe.mitre.org this session** (Knowledge Gaps). Rows that `rules/security.md` already owns
are cross-referenced, not restated, at the end of the table.

| # | Defect a reviewer flags in runner config, IaC or CI config | Preferred form | Cite |
|---|---|---|---|
| RUN-1 | Host Docker socket mounted into jobs (`volumes = ["/var/run/docker.sock:…"]`) on an instance that runs **more than one job** — `max_use_count` ≠ 1, `capacity_per_instance` > 1, or a persistent runner | Build without a host daemon (rootless BuildKit, Buildah, Kaniko) with registry layer cache; or keep one job per VM | CICD-SEC-7; CIS Docker 5.31 (v1.2.0) / 5.32 (v1.6.0); SLSA v1.0 L3 Isolated; GitLab "Known issues with Docker socket binding"; CWE-668 / CWE-250 (candidates) |
| RUN-2 | `privileged = true` (DinD, `--privileged`, ARC dind) on a pool that is not one-job-per-VM **or** not restricted to protected branches | Privileged only on ephemeral VMs that run protected refs; else a daemonless builder | GitLab runner security ("only on isolated and ephemeral virtual machines"; "only on protected branches"); CICD-SEC-7; CWE-250 (candidate) |
| RUN-3 | A self-hosted runner, runner group or instance runner that public-repository or fork pipelines can reach, with persistent (non-ephemeral) registration or reused hardware | Hosted runners for public code; else ephemeral/JIT runners on fresh VMs with no credentials | GitHub hardening ("should almost never be used for public repositories"); GitLab pull-policy warning for public instance runners; CICD-SEC-5 |
| RUN-4 | A pool whose instances carry a cloud role, deploy credential or network path to production that **unprotected-branch or MR** code can run on — runner not protected, `run_untagged = true` on the deploy pool, or tag-only routing | Protected runner (protected branches/tags only), protected variables, a separate pool per credential set; tags route, protection authorizes | CICD-SEC-5 ("Do not use a shared node for pipelines ... that require access to different resources"); GitLab protected runners; GitHub runner groups; CWE-269 (candidate) |
| RUN-5 | Instance metadata reachable from jobs on a pool with an instance role: IMDSv1 allowed (`HttpTokens = optional`) or `HttpPutResponseHopLimit` > 1 | `HttpTokens = required`, hop limit 1, metadata filtered from job networks, or no instance role on job instances | AWS IMDS docs; GitHub ("AWS metadata services"); GitLab ("Filtering access to cloud provider metadata endpoints"); CICD-SEC-5/-6 |
| RUN-6 | Long-lived cloud access keys in CI/CD variables or on the runner host where the platform supports OIDC | `id_tokens` (GitLab) / OIDC (GitHub) → `AssumeRoleWithWebIdentity`, short-lived | CICD-SEC-6 ("Prefer using temporary credentials over static credentials"); GitLab and GitHub OIDC docs; CWE-522 (candidate) |
| RUN-7 | A federated-identity trust policy on a deploy role whose `sub` condition wildcards the project, ref or ref type | Pin `sub` to `project_path:<group>/<project>:ref_type:branch:ref:<protected branch>` (and environment where available) | GitLab AWS OIDC ("limit authorization to a specific group, project, branch, or tag"); GitHub OIDC (subject claims); CICD-SEC-6; CWE-863 (candidate) |
| RUN-8 | `executor = "shell"` on a runner that serves more than one project or any untrusted branch | Docker or instance executor on per-job VMs | GitLab runner security ("Use it only for running trusted builds") |
| RUN-9 | `pull_policy` `if-not-present` or `never` on a reused runner shared by projects of different visibility or trust | `always` | GitLab runner security (private image served "even if the image could not be pulled because of missing credentials") |
| RUN-10 | A layer or dependency cache that lower-trust pipelines can write and higher-trust pipelines read — a registry cache ref pushed from MR jobs, a shared host daemon cache, or GitLab's protected-cache separation disabled | Protected refs write the cache; others read it or write their own key; keep "separate caches for protected branches" on | SLSA v1.0 L3 ("inject false entries into a build cache used by another build"); GitLab caching ("a security feature"); NIST 800-190 ("residual data, such as caches") |
| RUN-11 | `retry: N` with no `when` (defaults to `always`), or `when` including `always` or `script_failure` | `retry: {max: 2, when: [runner_system_failure, scheduler_failure, …stuck/no-updates reasons]}` | GitLab `retry` reference; `continuous-delivery.md` (fix flaky tests) |
| RUN-12 | `scale_factor` set in (0, 1.0], or `scale_factor_limit` ≤ `idle_count` + expected in-use slots — settings that cannot change the result | Leave `scale_factor` at 0 and size `idle_count`; or set `scale_factor` > 1 with a limit above the floor | taskscaler `capacity.go` (3.2) — confirmed on `main` 2026-10-21 |
| RUN-13 | Docker Machine executor (`docker+machine`) on GitLab ≥ 17.5 | docker-autoscaler / instance executor with a fleeting plugin | GitLab ("deprecated in GitLab 17.5 and is scheduled for removal in GitLab 20.0 (May 2027)") |
| **Fleet answers** | *Defects in a statement about a fleet, not in config* | | |
| RUN-T1 | An answer about a fleet's configuration that does not name what it read — live API, IaC at a commit, IaC state at a time | Name the source and its timestamp or commit; prefer the live system, then current IaC | Terraform drift docs; CloudFormation drift detection |
| RUN-T2 | An answer about the current fleet sourced from documentation of a platform the fleet no longer runs on | Read the current IaC or live system; cite the retired platform's docs only as history | 8.3 — **this document's extension**; drift sources support the premise only |

**Owned by `rules/security.md`, not restated**: mutable-tag CI actions and images (CWE-829), `curl | sh`
(CWE-494), `pull_request_target` running PR code (CWE-829), CI token `write-all` (CWE-732/-250), credential
literals in committed config (CWE-798), `GIT_SSL_NO_VERIFY=true` or other disabled TLS verification
(CWE-295). A runner guidance section should point to those rows.

### Candidate advisory list (judgment calls)

- **Reuse on a pool** (`max_use_count` > 1) where RUN-1 and RUN-2 do not fire: ask whether every job on the
  pool comes from the same trust class and whether any job there produces an artifact others consume
  (OWASP SEC-5 "identical levels of confidentiality"; SLSA L3 for provenance-bearing builds).
- **Unbounded reuse** — `max_use_count` unset or very large on a reused pool: drift and tampering live as
  long as the instance (Fowler; 7.2). Default value not confirmed.
- **A warm floor sized without data**: `idle_count` with no measured queue wait or boot time behind it
  (DORA lead time; Gandhi et al.; AWS "Creating a warm pool when it's not required can lead to unnecessary
  costs").
- **`capacity_per_instance` > 1** without the socket: concurrent jobs still share a kernel, disk and
  network — SLSA's "two builds that overlap in time".
- **Machine-wide private CA trust on reused hosts that grant host root to jobs** (6.4): the trust store is
  writable by any job; prefer `tls-ca-file` and one job per VM.
- **Runner version skew**: manager major.minor behind the GitLab server (7.3).
- **AMI age**: launch template AMI older than the current golden image; instances on reused pools lag
  further (7.2, 7.3).
- **No distributed cache on a one-job-per-VM fleet**: every `cache:` restore misses (5.1).
- **Local `cache:` on reused hosts treated as a guarantee**: GitLab says caching "isn't guaranteed to always
  work".
- **Retry policy naming deprecated reasons** (`stuck_or_timeout_failure`) on GitLab ≥ 19.1 (7.4).

### Candidate do-not-flag list

- **Reuse as such.** On a pool with one trust class, no credentials beyond what its least-trusted job may
  hold, no socket or privileged mode, and no provenance-bearing artifacts, the sources permit it (OWASP SEC-5;
  SLSA L2 does not require isolation).
- **The socket on a one-job, one-VM instance** (`max_use_count = 1`, `capacity_per_instance = 1`): the VM is
  the boundary GitLab calls "a secure ephemeral instance that cannot be affected by other jobs". Advise a
  daemonless builder; do not file RUN-1.
- **`idle_count = 0`** or no warm floor — AWS says warm capacity is only for boot times that cause
  "noticeable latency".
- **Local cache misses on ephemeral instances** — expected; the fix is a distributed cache, not reuse.
- **SLSA L3 isolation demands on a pool that builds nothing with provenance** — a choice, not a requirement.
- **Trusting a private CA machine-wide** by itself — the CA's key is not on the runner; the risk is write
  access to the store (advisory above), not the trust.
- **Retry on `runner_system_failure` or `scheduler_failure`** — the intended use.
- **Tags absent on a single-pool fleet** — routing needs more than one pool to matter.

### The concrete case, tested against the findings

Fleet: GitLab on AWS, docker-autoscaler; open pool `idle_count = 2` weekdays, `scale_factor = 1.0`,
`scale_factor_limit = 8`, `idle_time = 20m`, `max_instances = 16`, `capacity_per_instance = 1`,
`max_use_count = 1`; Docker socket mounted into every job; GitLab CA trusted machine-wide; deploy and state
pools carry AWS roles; open pool has none.

**What fires today.** RUN-1 does **not** fire: with `max_use_count = 1` and `capacity_per_instance = 1` each
VM runs one job and dies, so the socket's host-root reaches only that job's own VM. RUN-12 fires:
`scale_factor = 1.0` is a no-op in taskscaler (`ceil(1.0 × A) ≤ A + 2`), so the floor is exactly 2 idle
slots = 2 instances, with `scale_factor_limit = 8` doing nothing. For the deploy and state pools the
reviewer must ask RUN-4 (are they protected runners, do they refuse untagged jobs, is MR-pipeline access
off?), RUN-5 (IMDSv2 required, hop limit 1 — and note the socket lets a job reach IMDS through a
`--network host` sibling regardless), RUN-6/RUN-7 (OIDC with a pinned `sub` would let the deploy role leave
the instance profile entirely), and whether those pools also mount the socket.

**"Can warm instances be reused?"** Mechanically yes: raise `max_use_count`, and a finished instance returns
to idle instead of being deleted (3.1, 3.3). The capacity case is real — with `max_use_count = 1` the two
warm instances absorb only the first two jobs of a burst and every job after pays a boot (3.3, 4.3); reuse
turns each finished job's VM back into warm capacity during the burst, and it would make the local cache
hit (5.1). But on this fleet reuse **removes the only isolation boundary there is**, because the socket is
mounted: every later job on the VM would share the host daemon's images, build cache, volumes, networks and
any sibling containers, and run after a job that held host root (2.1–2.4). The sources' test (1.6) gives:
- *Open pool*: reuse only if its jobs are one trust class **and** RUN-1 is first removed (daemonless
  builds plus registry cache, 5.2). If protected-branch jobs that publish images also run on the open pool,
  reuse lets an MR job poison their base images or cache — SLSA L3's cache-injection case; keep
  `max_use_count = 1` there.
- *Deploy and state pools*: these run only protected refs (if RUN-4 is clean), so OWASP SEC-5 permits
  sharing among them; but a compromise on a reused deploy VM persists with the role's reach for the
  instance's lifetime, and any provenance-bearing build there must stay one-job-per-VM (SLSA L3).
- *The machine-wide CA*: with reuse, any socket-holding job can add a root to the host trust store and every
  later job's TLS — runner, daemon, package fetches — trusts it until the VM dies (6.4).
Cheaper ways to the same benefit, none of which needs reuse: raise `idle_count` in busy `periods` (and drop
`scale_factor` or set it > 1 with a limit above the floor), enable preemptive mode, cut boot time with a
pre-baked AMI, and move layer cache to the registry.

**"Is that common?"** For untrusted code, no: GitLab.com and GitHub-hosted runners give each job a new VM;
GitHub, the Terraform AWS module and GitLab's own docker-autoscaler page recommend one job per instance for
autoscaled fleets. Reuse is a supported, documented option (Docker Machine `MaxBuilds`, persistent
self-hosted runners) that the sources confine to a single trust class. No source quantifies prevalence.

**"If we reuse runner VMs we still get a fresh docker container for each job, right?"** The *job* container
is fresh; the isolation is not. GitLab: sharing the daemon means "you effectively disable the container's
security mechanisms and expose your host to privilege escalation"; containers a job starts are "siblings of
the runner"; volume mounts happen "in the context of the host machine". Docker: whoever controls the daemon
controls the host as root. On a reused VM with the socket mounted, a fresh container per job is a fresh
*workspace*, not a fresh *machine*: images and tags, build cache, Docker volumes (including the runner's
cache volumes), networks, leftover containers and any host file a previous job changed all carry over
(2.4). Without the socket and without privileged mode, a fresh container per job is real container
isolation on a shared kernel — acceptable within one trust class (NIST 800-190), short of SLSA L3.

**Truthfulness.** An answer to the owner should name its source: this case's facts would come from the
runner's `config.toml` and the AWS launch templates (live), or the IaC at a named commit — never from runner
docs written for the Azure-era platform (RUN-T1, RUN-T2).

### Versioned vs durable

| Will date (pin the version in every citation) | Durable (cite by title) |
|---|---|
| GitLab Runner settings and semantics (checked against v19.5.0, taskscaler 2026-09-08) | SLSA's isolation principle: no build influences another |
| `retry:when` reasons (split in 19.0, legacy deprecated 19.1, removal 20.0) | OWASP SEC-5's trust-class rule for shared nodes |
| Docker Machine executor (removal in GitLab 20.0, May 2027) | "Whoever controls the daemon is root on the host" |
| CIS Docker Benchmark control numbers (5.31 vs 5.32) | NIST 800-190's group-by-sensitivity rule |
| GitHub OIDC `sub` format (changed for repos created after 2026-07-15) | Setup-time queueing: a missed warm slot costs a full boot |
| SLSA version (v1.0 and v1.2 Isolated bullets identical, checked 2026-10-21) | Declared, recorded and live state differ; name which you read |

## Source Analysis

All accessed 2026-10-21. Reputation per the task's trusted-domain configuration.

| Source | Domain | Reputation | Type | Verification |
|---|---|---|---|---|
| SLSA v1.0 and v1.2 build requirements | slsa.dev | High | Standard | Verified (both versions) |
| NIST SP 800-204D (PDF pp. 15–17; Crossref) | csrc.nist.gov; nvlpubs.nist.gov; api.crossref.org | High | Official | Verified |
| NIST SP 800-190 (PDF pp. iv–v; Crossref) | nvlpubs.nist.gov; api.crossref.org | High | Official | Verified (exec summary only) |
| OWASP Top 10 CI/CD — SEC-5, -6, -7 | owasp.org → owasp.github.io | High (official for own project) | Standards body | Verified; version/date not shown; vendor-originated list |
| GitHub hardening; autoscaling; ARC; OIDC; hosted runners; REST workflow jobs | docs.github.com | Official for own product | Vendor docs | Verified |
| GitLab runner security; Docker build; layer caching; Docker executor; advanced config; docker-autoscaler; Docker Machine autoscale; caching; AWS OIDC; configure runners; TLS; CI YAML retry; Jobs API; runner versions; hosted runners | docs.gitlab.com | Official for own product | Vendor docs | Verified; most pages show no doc version |
| taskscaler `capacity.go`; commits API; runner releases API; runner `go.mod` | gitlab.com | Medium-high (primary code) | Source code | Verified line by line through a summarising fetch |
| GitLab work item 602133, MRs 239415/239456/250922 | gitlab.com | Medium-high | Issue tracker | Search snippets only |
| GitLab issue 347404 (HackerOne report) | gitlab.com | Medium-high | Issue tracker | Read; [Validation Warning] page embedded AI-directed instructions, ignored |
| GitLab infrastructure runbook | runbooks.gitlab.com | Medium-high | Vendor ops runbook | Verified |
| GitLab Support article (Kaniko) | support.gitlab.com | Medium-high | Vendor support | Search snippet |
| Docker Engine security; post-install; rootless; buildx reference; cache backends | docs.docker.com | High | Official | Verified |
| CIS Docker Benchmark socket control via Datadog and Turbot mappings; DISA STIG mirror | docs.datadoghq.com; hub.powerpipe.io; ato-pathways.com | **Medium** (secondary mappings) | Vendor | CIS PDF not read |
| AWS warm pools; IMDS; CloudFormation drift | docs.aws.amazon.com | High | Official | Verified |
| HashiCorp Terraform drift tutorial; `plan` reference | developer.hashicorp.com | Official for own product | Vendor docs | Verified |
| Terraform AWS GitHub Runner module docs | github-aws-runners.github.io | Medium-high | Open source | Verified; version not shown |
| DORA metrics guide | dora.dev | High | Research | Verified |
| Little 2011 (Crossref) | api.crossref.org | High | Academic | Metadata only |
| Gandhi, Harchol-Balter, Adan 2010 (author PDF p. 1; Crossref) | cs.stonybrook.edu; api.crossref.org | High | Academic | Abstract verified |
| Williams, Harchol-Balter, Wang 2022; Gandhi et al. staggered 2010 (Crossref) | api.crossref.org | High | Academic | Metadata + abstract summary |
| Harchol-Balter 2013 book (Cambridge Core chapter pages) | cambridge.org | High | Academic publisher | Search snippets; text not read |
| Fowler, PhoenixServer | martinfowler.com | Medium-high | Industry | Verified |
| Morris, *Infrastructure as Code* 3rd ed. (author site; Thoughtworks podcast) | infrastructure-as-code.com; thoughtworks.com | Medium-high | Author / industry | Edition verified; content not read |

Reputation: of ~55 sources, about 22 high (official government, standards, academic, docker/aws docs), about
25 official-for-own-product vendor docs (GitLab, GitHub, HashiCorp), 5 medium-high (source code, issue
trackers, Fowler, author site), 3 medium (CIS secondary mappings). Avg ≈ 0.87. No excluded domain used.
**Bias note**: GitLab and GitHub describe their own products, and both sell hosted runners — a commercial
reason to stress self-hosted risk. Every claim the always-flag rows rest on has a non-vendor source beside it
(SLSA, OWASP, NIST, Docker, CIS) except RUN-8, RUN-9, RUN-11, RUN-12 and RUN-13, which are product-semantics
rows where the vendor is the only authority. The OWASP CI/CD list originated at Cider Security, a vendor.

## Knowledge Gaps

### Gap 1: CWE fits for the runner rows
**Issue**: CWE-668, -250, -269, -522, -863 are candidate ids, not looked up. | **Attempted**: none this
session (budget). | **Recommendation**: resolve each through `cwe-api.mitre.org`, as the security research
did, before a rule ships; key rows by OWASP CICD-SEC id meanwhile.

**V2, closed 2026-10-21 (feature `ci-pipeline-standard`):** each id was read on cwe.mitre.org (CWE 4.20;
the API refused TLS that day) for its vulnerability-mapping usage. CWE-668 and CWE-269 are DISCOURAGED,
too abstract for a finding, and are dropped. CWE-250 is ALLOWED; CWE-522 and CWE-863 are
ALLOWED-WITH-REVIEW. Two replacements were read and are ALLOWED: CWE-653, Improper Isolation or
Compartmentalization, for the shared-machine rows (RUN-1, -3, -8, -9, -10); and CWE-266, Incorrect
Privilege Assignment, for a role-holding pool open to unprotected refs (RUN-4).

### Gap 2: CIS Docker Benchmark primary text
**Issue**: Control wording and numbers (5.31 in v1.2.0, 5.32 in v1.6.0) come from vendor mappings. |
**Attempted**: search; CIS PDFs are registration-gated. | **Recommendation**: read the current CIS Docker
Benchmark and cite its version.

### Gap 3: "One job can re-tag a base image another job builds from"
**Issue**: No vendor page states it; it is inferred from Docker's shared image store, `--pull` semantics and
GitLab's socket-binding notes (2.4). | **Attempted**: GitLab docs, search for tag overwrite / cache poisoning
via shared daemon. | **Recommendation**: demonstrate it on a scratch runner (two jobs, one socket) before
citing it as fact; until then cite SLSA's cache-injection bullet.

### Gap 4: taskscaler arithmetic read through a summariser — narrowed 2026-10-21
**Issue**: The `RequiredInstances` lines were first quoted piecewise by a fetch tool. They are now confirmed
by a whole read of `main` (3.2), and the reading that `scale_factor ≤ 1` is a no-op holds. What remains
open: `main` is not the revision Runner v19.5.0 pins (`1f87885729aa`). | **Recommendation**: diff the file
at that revision, and add a worked test; file a GitLab docs issue on the "on top of" vs "minimum/maximum"
wording.

**V3, closed 2026-10-21:** `internal/capacity/capacity.go` at `1f87885729aa` is byte-identical to `main`
(141 lines). `RequiredInstances` sets desired capacity to `max(acquired + max(idle_count, pending),
ceil(scale_factor × acquired))`, the second term capped by `scale_factor_limit` only where the limit is
above 0, so a `scale_factor` at or below 1.0 never wins.
The docs issue is not filed.

### Gap 5: `max_use_count` default; runner token location on docker-autoscaler instances
**Issue**: No default shown for `max_use_count`. Whether job instances hold the runner's authentication
token (they are reached by the manager, per prior knowledge) was not verified — it decides how much a
socket-holding job on a one-job VM can steal. | **Recommendation**: read the fleeting/docker-autoscaler
design docs.

### Gap 6: Queue-wait field semantics
**Issue**: GitLab's Jobs API and GitHub's REST API define `queued_duration`, `created_at`, `started_at` only
by example or type. Whether they include `needs:`/dependency waits is unstated. | **Recommendation**: read
the GraphQL schema descriptions (`CiJob.queuedDuration`, `queuedAt`) and GitLab Runner's queue metrics.

### Gap 7: Prevalence of VM reuse
**Issue**: No survey or vendor statistic on how many self-hosted fleets reuse VMs. | **Attempted**: platform
docs only. | **Recommendation**: treat "common" as unanswered beyond "platforms do not reuse for untrusted
code".

### Gap 8: Sources not read in full
OWASP CI/CD list version/date; NIST 800-204D beyond §5.1; NIST 800-190 beyond the executive summary;
Harchol-Balter's book; Little 2011's text; *Infrastructure as Code* 3rd ed.; Fowler's SnowflakeServer; Docker
rootless limitations; GitLab breaking-changes entry for `retry:when`; whether ASG warm pools compose with
the fleeting AWS plugin; the Terraform AWS module's version and `pool_config` syntax; *Accelerate*'s
bibliographic record.

### Gap 9: Answering from a retired platform's docs
**Issue**: No source states the rule RUN-T2 needs. | **Attempted**: Terraform, CloudFormation, Fowler,
Morris. | **Recommendation**: ground RUN-T2 in this repo's own provenance practice (CLAUDE.md) and the
incident that motivated it, and label it the guidance's own.

## Conflicting Information

### Conflict 1: May an execution node be shared?
**Position A**: OWASP CICD-SEC-5 — "Shared nodes should be used only for pipelines with identical levels of
confidentiality"; NIST 800-190 permits grouping by sensitivity. **Position B**: OWASP CICD-SEC-5 also —
"Revert the execution node to its pristine state after each pipeline execution"; SLSA L3 — "an ephemeral
build environment MUST be provisioned for each build". **Assessment**: Both hold at different bars. Sharing
within one trust class is permitted (OWASP, NIST, SLSA L2); a provenance-bearing build at L3 needs a fresh
environment each time. The guidance should state both bars and say which one a pool is held to.

### Conflict 2: How `idle_count` and `scale_factor` combine
**Position A** (GitLab docs): `scale_factor` is idle capacity "on top of the `idle_count`" (reads as add).
**Position B** (GitLab docs, next sentence): "`idle_count` becomes the minimum `idle` capacity and the
`scaler_factor_limit` the maximum `idle` capacity" (reads as clamp on idle). **Position C** (taskscaler code):
`desired = max(Acquired + max(IdleCount, pending), min(ceil(ScaleFactor × Acquired), ScaleFactorLimit))` —
the factor applies to *total* capacity and overlaps with the floor. **Assessment**: The code runs; it wins.
Position B matches the legacy Docker Machine `IdleScaleFactor` clamp (3.4), which suggests carried-over
prose.

### Conflict 3: Is a fresh container per job isolation?
**Position A**: GitLab — "Docker can be considered safe when running in non-privileged mode"; GitLab
calls one-job instances "secure ephemeral". **Position B**: GitLab — socket binding means "you effectively
disable the container's security mechanisms"; Docker — the daemon is root. **Assessment**: No conflict once
the socket is named: an unprivileged container without the socket is isolation on a shared kernel; with the
socket, the VM is the only boundary.

### Conflict 4: Warm capacity — always-on vs cost
**Position A**: GitLab examples keep warm floors (`idle_count = 5`, 20 minutes). **Position B**: AWS —
"Creating a warm pool when it's not required can lead to unnecessary costs"; running warm instances "highly
discouraged". **Assessment**: Both are conditional on measured boot latency and arrival bursts (4.3); size
the floor from queue-wait data, by `periods`.

## Full Citations

[1] OpenSSF. *SLSA Specification* v1.0, "Producing artifacts". https://slsa.dev/spec/v1.0/requirements ; v1.2 https://slsa.dev/spec/v1.2/build-requirements. Accessed 2026-10-21.
[2] Chandramouli, R.; Kautz, F.; Torres-Arias, S. *Strategies for the Integration of Software Supply Chain Security in DevSecOps CI/CD Pipelines*. NIST SP 800-204D. 2024-02-12. https://csrc.nist.gov/pubs/sp/800/204/d/final. Accessed 2026-10-21.
[3] Souppaya, M.; Morello, J.; Scarfone, K. *Application Container Security Guide*. NIST SP 800-190. 2017-09-25. DOI 10.6028/NIST.SP.800-190. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf. Accessed 2026-10-21.
[4] OWASP. "CICD-SEC-5: Insufficient PBAC". https://owasp.org/www-project-top-10-ci-cd-security-risks/CICD-SEC-05-Insufficient-PBAC. Accessed 2026-10-21.
[5] OWASP. "CICD-SEC-6: Insufficient Credential Hygiene". https://owasp.org/www-project-top-10-ci-cd-security-risks/CICD-SEC-06-Insufficient-Credential-Hygiene. Accessed 2026-10-21.
[6] OWASP. "CICD-SEC-7: Insecure System Configuration". https://owasp.org/www-project-top-10-ci-cd-security-risks/CICD-SEC-07-Insecure-System-Configuration. Accessed 2026-10-21.
[7] GitHub. "Security hardening for GitHub Actions". https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions. Accessed 2026-10-21.
[8] GitHub. "Autoscaling with self-hosted runners". https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/autoscaling-with-self-hosted-runners. Accessed 2026-10-21.
[9] GitHub. "Deploying runner scale sets with Actions Runner Controller". https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners-with-actions-runner-controller/deploying-runner-scale-sets-with-actions-runner-controller. Accessed 2026-10-21.
[10] GitHub. "About security hardening with OpenID Connect". https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect. Accessed 2026-10-21.
[11] GitHub. "About GitHub-hosted runners". https://docs.github.com/en/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners. Accessed 2026-10-21.
[12] GitHub. REST API "Workflow jobs". https://docs.github.com/en/rest/actions/workflow-jobs. Accessed 2026-10-21.
[13] GitLab. "Security for self-managed runners". https://docs.gitlab.com/runner/security/. Accessed 2026-10-21.
[14] GitLab. "Use Docker to build Docker images". https://docs.gitlab.com/ci/docker/using_docker_build/. Accessed 2026-10-21.
[15] GitLab. "Make Docker-in-Docker builds faster with Docker layer caching". https://docs.gitlab.com/ci/docker/docker_layer_caching/. Accessed 2026-10-21.
[16] GitLab. "Docker executor". https://docs.gitlab.com/runner/executors/docker/. Accessed 2026-10-21.
[17] GitLab. "Advanced configuration" (`[runners.autoscaler]`, `[[runners.autoscaler.policy]]`, `[runners.cache]`). https://docs.gitlab.com/runner/configuration/advanced-configuration/. Accessed 2026-10-21.
[18] GitLab. "Docker Autoscaler executor". https://docs.gitlab.com/runner/executors/docker_autoscaler/. Accessed 2026-10-21.
[19] GitLab. "Docker Machine Executor autoscale configuration". https://docs.gitlab.com/runner/configuration/autoscale/. Accessed 2026-10-21.
[20] GitLab. `fleeting/taskscaler`, `internal/capacity/capacity.go` (main; last change 3e8ff986, 2026-04-27). https://gitlab.com/gitlab-org/fleeting/taskscaler/-/raw/main/internal/capacity/capacity.go. Accessed 2026-10-21.
[21] GitLab. GitLab Runner releases (v19.5.0, 2026-10-15) and `go.mod` at v19.5.0. https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab-runner/releases ; https://gitlab.com/gitlab-org/gitlab-runner/-/raw/v19.5.0/go.mod. Accessed 2026-10-21.
[22] GitLab. "Caching in GitLab CI/CD". https://docs.gitlab.com/ci/caching/. Accessed 2026-10-21.
[23] GitLab. "Configure OpenID Connect in AWS to retrieve temporary credentials". https://docs.gitlab.com/ci/cloud_services/aws/. Accessed 2026-10-21.
[24] GitLab. "Configuring runners" (protected runners, tags). https://docs.gitlab.com/ci/runners/configure_runners/. Accessed 2026-10-21.
[25] GitLab. "Self-signed certificates or custom Certification Authorities". https://docs.gitlab.com/runner/configuration/tls-self-signed/. Accessed 2026-10-21.
[26] GitLab. "CI/CD YAML syntax reference", `retry`. https://docs.gitlab.com/ci/yaml/#retry. Accessed 2026-10-21.
[27] GitLab. Work item 602133 and MR 239415 (retry:when aliases for split failure reasons). https://gitlab.com/gitlab-org/gitlab/-/work_items/602133 ; https://gitlab.com/gitlab-org/gitlab/-/merge_requests/239415. Accessed 2026-10-21 (search snippets).
[28] GitLab. "Jobs API". https://docs.gitlab.com/api/jobs/. Accessed 2026-10-21.
[29] GitLab. Runbook "CiOrchestrationServiceJobQueueDurationApdexSLOViolation". https://runbooks.gitlab.com/ci-orchestration/alerts/CiOrchestrationServiceJobQueueDurationApdexSLOViolation/. Accessed 2026-10-21.
[30] GitLab. "GitLab Runner" (versions). https://docs.gitlab.com/runner/. Accessed 2026-10-21.
[31] GitLab. "Hosted runners". https://docs.gitlab.com/ci/runners/hosted_runners/. Accessed 2026-10-21.
[32] `jafarakhondali` (HackerOne report #1417211). "Installing Gitlab runner with Docker-In-Docker allows root access", gitlab-org/gitlab#347404. 2021-12-05. https://gitlab.com/gitlab-org/gitlab/-/issues/347404. Accessed 2026-10-21.
[33] GitLab Support. "GitLab Runner with Kubernetes executors using DIND services without enabling Privileged mode fails to run". https://support.gitlab.com/hc/en-us/articles/16981770788892. Accessed 2026-10-21 (search snippet).
[34] Docker. "Docker Engine security". https://docs.docker.com/engine/security/. Accessed 2026-10-21.
[35] Docker. "Linux post-installation steps for Docker Engine". https://docs.docker.com/engine/install/linux-postinstall/. Accessed 2026-10-21.
[36] Docker. "Rootless mode". https://docs.docker.com/engine/security/rootless/. Accessed 2026-10-21.
[37] Docker. "docker buildx build" reference. https://docs.docker.com/reference/cli/docker/buildx/build/. Accessed 2026-10-21.
[38] Docker. "Cache storage backends". https://docs.docker.com/build/cache/backends/. Accessed 2026-10-21.
[39] CIS. *CIS Docker Benchmark*, "Ensure that the Docker socket is not mounted inside any containers" (5.31, v1.2.0; 5.32, v1.6.0), via https://docs.datadoghq.com/security/default_rules/cis-docker-1.2.0-5.31/ and https://hub.powerpipe.io/mods/turbot/docker_compliance/controls/control.cis_v160_5_32. Accessed 2026-10-21.
[40] AWS. "Decrease latency for applications with long boot times using warm pools". https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-warm-pools.html. Accessed 2026-10-21.
[41] AWS. "Use the Instance Metadata Service to access instance metadata". https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html. Accessed 2026-10-21.
[42] AWS. "Detect unmanaged configuration changes to stacks and resources with drift detection". https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html. Accessed 2026-10-21.
[43] HashiCorp. "Manage resource drift". https://developer.hashicorp.com/terraform/tutorials/state/resource-drift. Accessed 2026-10-21.
[44] HashiCorp. "terraform plan command reference". https://developer.hashicorp.com/terraform/cli/commands/plan. Accessed 2026-10-21.
[45] github-aws-runners. *Terraform module for scalable GitHub Actions runners on AWS*. https://github-aws-runners.github.io/terraform-aws-github-runner/. Accessed 2026-10-21.
[46] DORA. "DORA's software delivery performance metrics". Updated 2026-01-05. https://dora.dev/guides/dora-metrics/. Accessed 2026-10-21.
[47] Little, J.D.C. "OR FORUM—Little's Law as Viewed on Its 50th Anniversary". *Operations Research* 59(3):536–549. 2011. DOI 10.1287/opre.1110.0940. Accessed 2026-10-21.
[48] Gandhi, A.; Harchol-Balter, M.; Adan, I. "Server farms with setup costs". *Performance Evaluation*. 2010. DOI 10.1016/j.peva.2010.07.004. https://www3.cs.stonybrook.edu/~anshul/perf_mmk_2010.pdf. Accessed 2026-10-21.
[49] Williams, J.K.; Harchol-Balter, M.; Wang, W. "The M/M/k with Deterministic Setup Times". *Proc. ACM Meas. Anal. Comput. Syst.* 6(3), art. 56. 2022. DOI 10.1145/3570617. Accessed 2026-10-21.
[50] Gandhi, A.; Harchol-Balter, M.; Adan, I. "Decomposition results for an M/M/k with staggered setup". *ACM SIGMETRICS PER*. 2010. DOI 10.1145/1870178.1870195. Accessed 2026-10-21.
[51] Harchol-Balter, M. *Performance Modeling and Design of Computer Systems*. Cambridge University Press. 2013. https://www.cambridge.org/core/books/performance-modeling-and-design-of-computer-systems/. Accessed 2026-10-21 (chapter pages via search).
[52] Fowler, M. "PhoenixServer". bliki. 2012-07-10. https://martinfowler.com/bliki/PhoenixServer.html. Accessed 2026-10-21.
[53] Morris, K. *Infrastructure as Code*, 3rd ed. O'Reilly. 2025. https://infrastructure-as-code.com/book/ ; https://www.thoughtworks.com/insights/podcasts/technology-podcasts/infrastructure-as-code-in-2025. Accessed 2026-10-21.

## Research Metadata

Examined: ~60 pages, 3 PDFs, 4 API records | Cited: 53 | Crossref counts taken: 6 (NIST 800-190: 77;
NIST 800-204D: 20; Little 2011: 192; Gandhi et al. 2010: 140; Williams et al. 2022: 9; Gandhi et al.
staggered 2010: 3) | Confidence by finding: High ≈ 55% (isolation, socket, credentials, drift), Medium-High
≈ 30% (autoscaler arithmetic, persistence inferences), Medium ≈ 15% (capacity sizing, RUN-T2, trust-store
exposure) | Tool failures: OWASP URLs 308-redirect (followed); NIST and Stony Brook PDFs unreadable by the
fetch tool (read as images instead); GitLab advanced-config page truncated (read with offsets); one fetched
issue page carried prompt injection (ignored, logged) | Output:
docs/research/ci/ci-runner-infrastructure-canonical-sources.md
