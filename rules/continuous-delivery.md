---
paths:
  - "**/.github/**"
  - "**/Dockerfile*"
  - "**/docker-compose*"
  - "**/Jenkinsfile"
  - "**/.gitlab-ci*"
  - "**/azure-pipelines*"
  - "**/.circleci/**"
  - "**/Makefile"
  - "**/Taskfile*"
  - "**/.dockerignore"
  - "**/Procfile"
  - "**/Caddyfile"
  - "**/nginx.conf"
  - "**/k8s/**"
  - "**/helm/**"
  - "**/terraform/**"
  - "**/pulumi/**"
---

# Continuous Delivery Guide

Guidelines for continuous delivery and DevOps practices, extracted from Jez Humble and David Farley's *Continuous Delivery*, Gene Kim et al.'s *The DevOps Handbook*, Dave Farley's *Modern Software Engineering*, and the minimum practices of MinimumCD.org.

---

### Core Philosophy

> **"If it hurts, do it more frequently, and bring the pain forward."**

---

### The Three Ways

DevOps rests on three principles:

1. **Flow** — Optimize the path from development to production to customer
2. **Feedback** — Create fast feedback loops at every stage
3. **Continual Learning** — Experiment, fail safely, and improve continuously

---

### The Deployment Pipeline

Every change flows through the same automated path from commit to production.

| Stage | Purpose | Speed |
|-------|---------|-------|
| **Commit** | Compile, unit test, static analysis | Minutes |
| **Acceptance** | Verify business requirements | Minutes |
| **Performance** | Validate capacity and response times | Minutes to hours |
| **Production** | Deploy to users | Minutes |

#### Pipeline Principles

- The pipeline is the only way to deploy, to any environment
- Build once, deploy many times—no human changes an artifact after the pipeline builds it
- Same process for every environment
- Every commit is a release candidate
- Stop the line when trunk is red—all feature work halts, and nothing merges but the fix or its revert until trunk is green

`ci-pipelines.md` names the defects in a pipeline file that break these principles, such as a deploy job that rebuilds or build output passed through the cache, each by its `PIPE-n` id.

#### The Pipeline Decides

The team agrees on a definition of deployable, and the pipeline enforces every criterion in it with an automated check. A green pipeline means the artifact is deployable; a red one means it is not, and no human overrides its verdict. A human may choose when a green artifact ships, never whether a red one does.

#### Production-Like Environments

Test in production-like environments. Match production wherever it shapes behavior: platform, network topology, database engine and version, operating system, runtime and libraries, and downstream services at production's versions or faithful test doubles of them. Scale may differ; architecture may not.

#### Deterministic Pipeline

- Same inputs produce same outputs—repeatable, authoritative, trustworthy
- Version control everything: code, infrastructure, pipeline definitions, lockfiles
- Pin exact dependency versions; eliminate environmental variance
- Fix flaky tests immediately—they destroy determinism

---

### Configuration Management

- **Version everything** — Code, configuration, scripts, infrastructure
- **Manage dependencies explicitly** — Pin versions; use artifact repositories
- **Ship application configuration with the artifact** — Settings that hold in every environment, such as routing rules, default flag values and timeouts, deploy inside the artifact
- **Inject environment configuration at deploy time** — Values that vary by target, such as connection strings and service URLs, stay out of the build and live in version control per environment; credentials come from a secret store, never the repository
- **Reproduce any environment** — From scratch, using only version control

---

### Continuous Integration

- Integrate code at least daily—one commit per developer per day minimum
- Every commit triggers the pipeline
- Test every change automatically before it merges to trunk, and again with everyone else's work after it merges
- Delivered work keeps working when new work lands—a change that breaks an existing test does not merge
- Fix broken builds immediately—target < 1 hour
- Keep the build under ten minutes

**Trunk-based development enables continuous integration.** Long-lived branches delay integration and hide problems. A branch merged through an MR still counts as trunk-based while it lives about two days, review wait included (trunkbaseddevelopment.com); past that, it is a long-lived branch. Every branch starts from trunk, merges back to it, and is deleted after the merge.

#### Evolutionary Coding Practices

- **Branch by Abstraction** — Gradually replace behavior while continuously integrating
- **Connect Last** — Build complete features, wire up in final commit
- **Feature Flags** — Control visibility without blocking integration (use sparingly; remove within 2-4 weeks)

---

### Automated Testing

| Level | What It Tests | Who Writes It |
|-------|---------------|---------------|
| **Unit** | Isolated logic | Developers |
| **Integration** | Component collaboration | Developers |
| **Acceptance** | Business requirements | Developers + QA + Business |
| **Performance** | Capacity and response times | Developers + Ops |

#### Testing Principles

- Automate everything that can be automated
- Run tests on every commit
- Fix broken tests immediately
- Manual testing is for exploration, not regression
- **QA should find nothing** — Your tests should catch defects first

---

### Release Strategies

| Strategy | How It Works | When to Use |
|----------|--------------|-------------|
| **Blue-Green** | Two identical environments; switch traffic instantly | Zero-downtime deployments |
| **Canary** | Route small percentage of traffic to new version | Validate in production with limited risk |
| **Feature Toggles** | Deploy code disabled; enable when ready | Decouple deployment from release |
| **Rolling** | Update instances incrementally | Large deployments with gradual rollout |

**Separate deployment from release.** Deployment puts code on servers. Release makes it available to users.

**Roll back on demand.** A rollback redeploys the previous artifact, unchanged in the artifact repository, and restores service within five minutes of the decision. The on-call engineer rolls back without waiting for approval. Roll back by default; fix forward only when the cause is clear and the fix can pass the pipeline sooner than a rollback restores service.

---

### Infrastructure as Code

- Treat infrastructure like application code
- Provision environments automatically
- Never make manual changes to production
- Environments are disposable and reproducible

---

### Deployability

Deployability is a design property, not an afterthought. Code that resists deployment signals design problems.

- **Design for deployment** — Small, independent services deploy independently
- **Make the change easy, then make the easy change** — Refactor before adding features
- **Keep deployments boring** — Routine deployments mean fewer surprises

---

### Telemetry and Feedback

- Instrument everything
- Monitor business, application, and infrastructure metrics
- Create dashboards visible to everyone
- Alert on anomalies before customers notice

**If you cannot see it, you cannot fix it.**

---

### Database Changes

- Version database schemas
- Use migrations, not manual scripts
- Test data changes in the pipeline
- Change a schema by expand, then contract, in separate releases: expand it so old and new code both run, then contract it once no release you might roll back to needs the old shape

---

### Organizational Practices

- Embed operations in development teams
- Share on-call responsibilities
- Conduct blameless postmortems
- Allocate time for improvement work

**DevOps is a culture, not a role.** Shared responsibility between Dev and Ops.

---

### Delivery Checklist

- [ ] Is everything in version control?
- [ ] Does every commit trigger the pipeline?
- [ ] Can you deploy to any environment on demand?
- [ ] Can you recreate any environment from scratch?
- [ ] Do you deploy at least weekly?
- [ ] Can you roll back within five minutes of deciding to?
- [ ] Is production telemetry visible to developers?
- [ ] Is your build success rate > 95%?
- [ ] Is your development cycle time < 2 days?

---

### Anti-Patterns to Avoid

- **Manual deployments** — Error-prone and unrepeatable
- **Snowflake servers** — Environments that cannot be reproduced
- **Long-lived branches** — Delay integration and hide problems
- **Leaving production-like environments to the end** — Problems found late cost more
- **Manual configuration changes** — Drift between environments
- **Blaming individuals for failures** — Blame the process, not the person
- **Bypassing CI for "urgent" hotfixes** — Urgency does not justify skipping the pipeline
- **Stale feature flags** — Flags left in code become technical debt

---

### The Mantra

**Automate everything. Deploy frequently. Make releases boring.**
