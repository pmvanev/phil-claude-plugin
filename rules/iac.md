---
paths:
  - "**/*.tf"
---

# Infrastructure as Code Guide

Guidelines drawn from Kief Morris's writing on infrastructure as code (infrastructure-as-code.com and
Thoughtworks, 2016–2025); Google Cloud's "Best practices for using Terraform"; AWS Prescriptive
Guidance, "Backend best practices"; Yevgeniy Brikman's "How to manage Terraform state"; and HashiCorp's
Version Constraints, Dependency Lock File, providers-in-modules, `plan` and `apply` pages. The vendors
write their guidance for Terraform; each row here states the principle in terms no single tool owns.
Research: `docs/research/iac/iac-terraform-bash-yaml-canonical-sources.md` § 3 and its Addendum.

This rule owns **how infrastructure code keeps state, pins what it depends on, and shapes one
definition into many environments**. Neighbouring rules keep what they already own:
`continuous-delivery.md` the practice — treat infrastructure like application code, never change
production by hand; `security.md` secrets in code and in state (CWE-798, CWE-312); `ci-pipelines.md`
how a pipeline job runs the tool; `terraform.md` each row's Terraform spelling and the defects only
Terraform has. Complement those — do not restate them.

**It applies to** every file of a tool that declares infrastructure. Today `review-code` matches it to
Terraform's `.tf`, and `terraform.md` gives each row's Terraform form; another tool joins when its own
rule does. A **root** is the unit a person or a pipeline applies, holding an environment's state; a
**reusable module** is code a root calls.

**The two halves divide on checkability.** The reviewer half — Always-flag, Advisory and Do not flag —
names the defects the files show, each by its `IAC-n` id. A row is a hazard when a miss changes what an
apply does or what state it writes, and a review files it at Priority 1. A row with no hazard is an
idiom: a cited source names its preferred form, and a review files it at Priority 7. A defect no source
names stays Advisory. The Principles half is design and yields no finding on its own.

---

## Principles — design, not review criteria

### 1. One definition, many environments

Morris calls separate copies of the code per environment "an antipattern, Snowflakes as Code", and
gives the remedy: "reuse a single instance of infrastructure code for multiple instances of the
infrastructure, and manage necessary variation between environments with parameters." An environment
is a set of inputs, not a directory of edits.

### 2. Change an environment only through the pipeline

"The only changes made to an environment you care about are the ones that have been fed into the
pipeline" (Morris). A change made by hand is drift, "inconsistency between code and the infrastructure
deployed in an environment", and the next apply either reverts it or trips over it.

### 3. State is the tool's memory of the world

Keep it remote, locked and apart per environment. Committed to version control, it invites "conflicts,
data loss, and state file corruption" (Brikman); shared between environments, it lets one
environment's apply rewrite another's record.

### 4. Pin what the root depends on

A root that bounds its provider versions and commits the tool's lock file applies the same code the
same way tomorrow. A reusable module states only the oldest versions it works with and leaves the
choice to the root.

---

## Always-flag — objective defects

Name each finding by its `IAC-n` id, and give the tool's spelling after ` — here: `, from that tool's
rule. Where the defect is a missing file, name the root's directory as the File; where two roots show
one defect, file it once, against either. A secret in the code or in state is `security.md`'s alone.

| Id | Violation | Preferred form | Hazard | Linter | Cite |
|----|-----------|----------------|--------|--------|------|
| IAC-1 | State committed to version control, or a state file left where a commit picks it up | State in a remote backend; state files ignored by version control | hazard | none | Brikman, "How to manage Terraform state"; HashiCorp, Style Guide; AWS, "Backend best practices" |
| IAC-2 | Two environments that share one state: two roots configured with the same backend location, or one root applied to both | One state per environment, each at a location no other environment's state uses | hazard | none | AWS, "Backend best practices"; Brikman, "How to manage Terraform state"; Google, root modules |
| IAC-3 | A root with no committed dependency lock file, so the next initialisation may install different provider versions | Commit the tool's lock file in every root | hazard | none | HashiCorp, "Dependency Lock File"; HashiCorp, Style Guide; Google, root modules |
| IAC-4 | A root that constrains a provider from below only, or not at all | A lower and an upper bound on each provider, in the root | — | none | HashiCorp, "Version Constraints"; Google, root modules |
| IAC-5 | A reusable module that configures its own backend or provider | Configure backends and providers in the root, and pass providers in | — | none | Google, reusable modules; HashiCorp, "Providers Within Modules" |
| IAC-6 | A reusable module that hard-codes, or gives a default to, a value one environment owns — an account or project id, a cluster, a domain | An input with no default, set by each environment's root | — | none | Google, style and structure |
| IAC-7 | An environment root that repeats another root's or a shared module's resource definitions with values edited inline, instead of calling one shared definition | One shared module; each environment a root that passes its own inputs | — | none | Morris, "Snowflakes as Code"; Google, root modules |

Each quote was checked against its live page on 2026-11-06.

---

## Advisory — judgment calls, not hard blocks

A reviewer raises these; the author decides.

- **A shared remote backend with locking off.** Brikman: "Most of the remote backends natively support
  locking." AWS says locking "prevents concurrent write operations"; ask why it is off.
- **Environments separated only by a switch inside one backend** — Terraform's workspaces. AWS:
  "distinct backends provide stronger isolation"; Brikman calls workspaces "not a suitable mechanism
  for isolating one environment from another."
- **A pipeline that applies changes without the plan a person or a gate reviewed.** HashiCorp's `apply`
  page recommends that you "first perform a plan operation and review the proposed changes". Raise it only
  where the review read the pipeline file.
- **No drift detection**: nothing plans each environment on a schedule and tells someone when the plan
  is not empty. Raise it only where the review read the pipeline file.
- **An imperative script doing what a declared resource can do.** Google: "Avoid custom scripts, if
  possible"; Sharma et al. name the smell Imperative Abstraction.
- **One state holding more than about a hundred resources**, counting each instance. Google: "Don't
  include more than 100 resources (and ideally only a few dozen) in a single state."
- **Production state that people, not only the pipeline, can write.** Raise it only where the code
  shows who can write the state — a bucket policy, a role — and never for a bootstrap root.
- **An input an environment's apply takes from outside version control** — a variable exported in a
  person's shell, an ignored variables file — so an apply from anywhere else changes the environment.
  Morris: "The only changes made to an environment you care about are the ones that have been fed into
  the pipeline."
- **An input one environment root sets and another leaves to the module's default.** The roots differ
  in a value nobody chose for the second; ask whether the default is meant.
- **A reusable module that bounds a provider from above.** HashiCorp: "Reusable modules should
  constrain only their minimum allowed versions"; an upper bound there blocks every root from moving
  on.

---

## Do not flag

- **A reusable module that bounds a provider or the tool from below only**: HashiCorp asks exactly
  that of a reusable module.
- **A lower bound alone on the tool's own version**, in any root: HashiCorp, Google and AWS each write
  one.
- **A module never applied as a root** with no lock file, or with one: the lock file belongs to the
  root that applies it.
- **A secret in the code or in state**: `security.md`'s CWE-798 or CWE-312, filed once there.
- **A project with one environment**, which owes no per-environment roots.
- **Two roots that call one shared module and differ only in their inputs** — values, sizes, names —
  however many lines those take, **in records of a past refactoring**, or **in resources one
  environment alone needs**, such as test fixtures.
- **A bootstrap**: the script or root that creates the state backend itself, which must run, by a
  person or with local state, before any root can keep its state remotely. It owes no imperative-script
  or state-writer question.
