# Expected outcome — fixture 12 (infrastructure findings cite an IAC row)

A billing service's network, in Terraform:

- `modules/network/`, a reusable module: a VPC and its private subnets;
- `envs/staging/`, a root that calls the module, with an S3 backend, a lock file and, left behind, a
  local state file;
- `envs/prod/`, a root made by copying the module's resources and editing their values.

It holds seven defects, each an Always-flag row of `rules/iac.md`, beside three decoys that the rule's
Do-not-flag list clears. `test_fixture.py` is green where Terraform is installed: every file is in
`terraform fmt` form, and each directory validates.

**Pins:**

- `review-code` gathers `*.tf` on every run, not only where it reads `lambda-web-app-speed.md`, and
  checks it against `iac.md`. It lists each root's directory for its lock and state files.
- It names each finding by the row's `IAC-n` id and takes the row's Preferred form as its fix, with the
  Terraform spelling after ` — here: `.
- It files a hazard row at Priority 1 and every other row at Priority 7.

Before the rule existed, a review held these files to no standard: a repo with no Lambda gathered no
Terraform.

**How to drive it:** drive this working tree's `skills/review-code/SKILL.md` by hand over this
directory (`/phil:review-code` runs the released copy).

**Expected:** a `.refactoring-backlog.md` holding the seven items in `expected-backlog.md`. An item
matches on the Smell and on a Refactoring that is the row's Preferred form verbatim, alone or followed by
` — here: ` and this code's one change. Order is not checked.

1. **IAC-1** (Priority 1) — `envs/staging/terraform.tfstate` is committed.
2. **IAC-2** (Priority 1) — both roots name the same bucket and key, so each apply rewrites the other
   environment's state.
3. **IAC-3** (Priority 1) — `envs/prod/` commits no `.terraform.lock.hcl`.
4. **IAC-4** (Priority 7) — prod's AWS provider is `>= 5.0`, with no upper bound.
5. **IAC-5** (Priority 7) — the network module carries its own `provider "aws"` block.
6. **IAC-6** (Priority 7) — the module defaults `account_id`.
7. **IAC-7** (Priority 7) — prod repeats the module's resources with values edited inline.

**Hard assertions (any failure blocks the skill change):**

- **No item files a decoy as its defect:**
  - `>= 1.11`: a lower bound alone on Terraform's own version, in every root and the module.
  - `>= 5.40`: a reusable module bounds its provider from below, as HashiCorp asks.
  - `modules/network/versions.tf`, and the module's missing lock file: a module never applied as a
    root owes none.
- **IAC-2 is one item**, though two files show it.
- **No item names a secret**: the account ids are identifiers, not credentials.
- Every hazard item carries `Priority: 1`, and every other item `Priority: 7`. Every item carries
  `Route: report only`: no test suite checks a plan, so `/phil:refactor` cannot prove a change safe.

**Not a failure:**

- an Advisory question, where a file shows its subject — no drift detection, no pipeline read;
- line numbers within ±2, and IAC-2 filed against either root's backend block.
