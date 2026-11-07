---
paths:
  - "**/*.tf"
---

# Terraform Guide

Guidelines drawn from HashiCorp's Terraform documentation — the Style Guide, Version Constraints,
Dependency Lock File, the `count` and `for_each` meta-arguments, Refactoring, Standard Module Structure
and Providers Within Modules — and its security bulletin HCSEC-2023-26; Yevgeniy Brikman's *Terraform:
Up & Running*, through his "Terraform tips & tricks"; Google Cloud's "Best practices for using
Terraform"; and the TFLint terraform ruleset. Research:
`docs/research/iac/iac-terraform-bash-yaml-canonical-sources.md` § 4 and its Addendum.

This rule owns **the defects only Terraform has**, and the Terraform spelling of each `iac.md` row.
Neighbouring rules keep what they already own: `iac.md` the tool-agnostic rows — state, locks, provider
bounds, module boundaries and environments — which a review files under their `IAC-n` ids;
`security.md` secrets in code, in state and in `.tfvars` (CWE-798, CWE-312); `ci-runners.md` and
`lambda-web-app-speed.md` the Terraform they read for runners and cold starts. Complement those — do not
restate them.

**It applies to** every `.tf` file outside `.terraform/`, beside `iac.md`. Tell the directories apart
before judging a row:

- a **root** is a directory Terraform is run in: it holds a `backend` block, or sits where a person or a
  pipeline runs `terraform apply` — an `envs/<name>/`, a `bootstrap/`, a pipeline job's working
  directory;
- a **child module** is a directory some `module` block's `source` names;
- a **test harness** holds only `*.tftest.hcl` files and the modules they call; it is neither.

Count a state's resources as its instances, `count` and `for_each` expanded.

**The two halves divide on checkability.** The reviewer half — Always-flag, Advisory and Do not flag —
names the defects the files show, each by its `TF-n` id. A row is a hazard when a miss changes what a
plan or an apply does, and a review files it at Priority 1. A row with no hazard is an idiom: a cited
source names its preferred form, and a review files it at Priority 7. A defect no source names stays
Advisory. Each row names the TFLint rule that catches it, where one exists; the review reads and never
runs one. The Principles half is design and yields no finding on its own.

---

## Principles — design, not review criteria

### 1. Address instances by what they are, not where they sit

`count` numbers instances from 0, so an instance's address is its position. `for_each` keys each
instance by a value that does not move when a neighbour is removed. Use `count` for a toggle or for
identical copies, and `for_each` for anything with its own identity (Brikman: "you should almost always
prefer to use `for_each` instead of `count` to create multiple copies of a resource").

### 2. Tell Terraform when an address moves

Renaming a resource, moving it into a module or switching it from `count` to `for_each` changes its
address. Without a `moved` block, "Terraform interprets a change as an instruction to destroy the
existing resource."

### 3. Type and describe every input

"Define a `type` and a `description` for every variable", and "Include a description for every
output" (Style Guide). A type rejects a wrong value at plan time; a description tells a caller what to
pass.

### 4. Run the checks the tool provides

"Run `terraform fmt` and `terraform validate` before committing your code to version control", and use
TFLint for the rest (Style Guide). Leave to them what they enforce.

---

## Always-flag — objective defects

Name each finding by its `TF-n` id. File a defect `iac.md` names under its `IAC-n` id, spelled as the
next table gives it, never also here. A secret is `security.md`'s alone; an unpinned
module source is TF-5 alone, never also `security.md`'s CWE-494.

| Id | Violation | Preferred form | Hazard | Linter | Cite |
|----|-----------|----------------|--------|--------|------|
| TF-1 | `count` over a collection whose elements each have an identity of their own — CIDRs, names, ids — and whose body reads it by `count.index`, as `count = length(var.subnets)` with `var.subnets[count.index]` does, so removing an element from the middle shifts every later instance onto its neighbour's values, updating or replacing each, and destroys the last | `for_each` over a map or a set keyed by a stable id, each existing instance moved to its key with a `moved` block | hazard | none | Brikman, "Terraform tips & tricks"; HashiCorp, `for_each` |
| TF-2 | A change that alters a resource or module address — a rename, `count` to `for_each`, a move into a module — with no `moved` block for it | A `moved { from = … to = … }` block for each changed address, kept after the apply | hazard | none | HashiCorp, "Refactoring" |
| TF-3 | A `variable` with no `type` | The narrowest `type` that admits every value it takes | — | `terraform_typed_variables` (recommended) | HashiCorp, Style Guide; Google, style and structure |
| TF-4 | A `variable` or an `output` with no `description`; a `#` comment above it is not one. File one item per file, its Lines listing each | A one- or two-sentence `description` | — | `terraform_documented_variables`, `terraform_documented_outputs` (`all` preset only) | HashiCorp, Style Guide; HashiCorp, "Standard Module Structure" |
| TF-5 | A module called from a git source with no `?ref=`, or from a registry with no `version`, so the next `init` installs whatever is newest | A git `?ref=` naming a tag or a commit; a registry `version` constraint | hazard | `terraform_module_pinned_source`, `terraform_module_version` (recommended) | HashiCorp, "Version Constraints"; Google, reusable modules |
| TF-6 | A map or object literal with a duplicate key, which Terraform resolves to the last value without a warning | One key, holding the value meant | hazard | `terraform_map_duplicate_keys` (recommended; skips a key it cannot evaluate) | HashiCorp, HCSEC-2023-26 |

Checked 2026-11-06: TF-1 and TF-6 by plan on Terraform 1.15.3, the rest against each page live.
TF-2 needs the change, so it fires under `--changes` alone.

---

## The Terraform form of each IAC row

File each under its `IAC-n` id, with the row's Preferred form from `iac.md`, then ` — here: ` and the
Terraform change below.

| IAC row | The defect in Terraform | The change |
|---------|-------------------------|------------|
| IAC-1 | A committed `terraform.tfstate` or `*.tfstate.backup`, or one present in a root and not ignored; a root with no state file at all is not this row | Delete it; ignore `*.tfstate` and `*.tfstate.*`; a `backend` block |
| IAC-2 | Two roots whose `backend` blocks name the same bucket and `key`, or a root applied to two environments; a shared bucket with distinct keys is two locations | A distinct `key`, and better a bucket, per environment |
| IAC-3 | A root's directory with no committed `.terraform.lock.hcl` | Run `terraform init` there and commit the lock file |
| IAC-4 | A root's `required_providers` entry with no `version`, or with `>=` alone | `version = "~> X.Y"` |
| IAC-5 | A `provider` or `backend` block in a child module. HashiCorp: "A module intended to be called by one or more other modules must not contain any provider blocks." | Delete it; configure the provider in the root and pass it in through `providers` |
| IAC-6 | A child module's `variable` for an account or project id with a `default` | Delete the `default`; set it in each root |
| IAC-7 | An environment root that repeats a module's or another root's `resource` blocks with values edited inline; `moved`, `import` and `removed` blocks are records, not definitions | A `module` call passing the environment's inputs, and `moved` blocks into it |

---

## Advisory — judgment calls, not hard blocks

A reviewer raises these; the author decides.

- **A `terraform` block with no `required_version`.** The Style Guide: "We also recommend that you set
  a minimum required version of the Terraform binary." TFLint's `terraform_required_version` checks
  presence.
- **A file not in `terraform fmt` form.** A formatting check belongs in CI, and the `fmt` page says
  "you may choose not to use this command".
- **A variable or output whose value is a password, a private key or a token, with no `sensitive =
  true`** — not one that names a key or holds its ARN. It hides the value in output, not in state; the
  secret itself is `security.md`'s.
- **Deprecated syntax** — legacy dot index (`list.0`), a two-argument `lookup()` — which TFLint's
  recommended preset catches.
- **A declaration nothing uses** (`terraform_unused_declarations`).
- **A change of a resource's type with no `moved` block**: a `moved` block crosses types only where
  the provider supports the move, so ask how the old resource leaves state.
- **`count` or `for_each` where one plain block would do**: "Use `count` and `for_each` sparingly."
- **An S3 backend locked through `dynamodb_table` alone**: AWS calls it deprecated in favour of
  `use_lockfile = true` on Terraform 1.11 and later.
- **`iac.md`'s Advisory bullets, in Terraform's words**: environments kept apart by workspaces alone;
  an S3 backend without `use_lockfile = true`; `terraform apply -auto-approve`, or an apply that runs a
  fresh plan instead of the `plan -out` file a person or gate reviewed; a variable taken from a
  `TF_VAR_` export or an ignored `.tfvars` at apply time; a child module's `required_providers` entry
  with `~>` or `<`.
- **No `tflint` or `terraform validate` in the project's CI.** Raise it only where the review read the
  CI config. One item per project, not per file.

---

## Do not flag

- **`count = <condition> ? 1 : 0`**, `? 0 : 1`, or `? N : 0` over identical instances: the toggle
  HashiCorp, Google and Brikman each document, either way round.
- **`count = N` over identical instances** whose body reads `count.index` only to name them.
- **`count` over elements with no identity of their own** — fixed-size chunks of a document, a
  `range()` — where no stable key exists for `for_each`.
- **A `count` that mirrors another counted resource one for one** — `count = length(aws_subnet.private)`
  read by `count.index`: list its lines in that resource's TF-1 item, never a second item.
- **A lower bound alone on `required_version`**, in any root or module: the Style Guide asks for a
  minimum, and AWS writes `>= 1.11`.
- **`>=` provider constraints in a child module**: HashiCorp asks exactly that of a reusable module.
- **A child module with no `.terraform.lock.hcl`**, or with one: Terraform reads the root's.
- **A variable with no `validation`**, unless its values have "uniquely restrictive requirements".
- **A row or an Advisory bullet the project's TFLint already enforces**: CI runs TFLint, and its
  config enables the rule it names. Read both: the bundled default preset is `recommended`, which
  leaves out TF-4's rules, and most rules lint only the directory TFLint runs in, so TFLint checks a
  child module only under `--recursive`.
  A row whose Linter cell reads none never stands down.
