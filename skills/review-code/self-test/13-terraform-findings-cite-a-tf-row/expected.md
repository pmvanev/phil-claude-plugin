# Expected outcome — fixture 13 (Terraform findings cite a TF row)

An orders service's staging network, one Terraform root: `versions.tf` holds the backend and the pinned
provider, `.terraform.lock.hcl` is committed, and `network.tf`, `variables.tf` and `outputs.tf` hold the
resources. The root meets every row of `rules/iac.md`.

It holds five defects, each an Always-flag row of `rules/terraform.md`, beside three decoys that the
rule's Do-not-flag list clears. `test_fixture.py` is green where Terraform is installed: every file is in
`terraform fmt` form.

**Pins:**

- `review-code` checks a `.tf` file against both `iac.md` and `terraform.md`.
- It names each finding by the row's `TF-n` id and takes the row's Preferred form as its fix.
- It files a hazard row at Priority 1 and every other row at Priority 7.
- It leaves the `count` toggle and `count` over identical instances alone (D11).

Before the rule existed, a review gathered no Terraform in a repo without a Lambda, and filed none of
these.

**How to drive it:** drive this working tree's `skills/review-code/SKILL.md` by hand over this
directory (`/phil:review-code` runs the released copy).

**Expected:** a `.refactoring-backlog.md` holding the five items in `expected-backlog.md`. An item
matches on the Smell and on a Refactoring that is the row's Preferred form verbatim, alone or followed by
` — here: ` and this code's one change. Order is not checked.

1. **TF-1** (Priority 1) — `aws_subnet.private` is `count = length(var.subnet_cidrs)`, read by
   `count.index`; removing a CIDR from the middle shifts every later subnet.
2. **TF-5** (Priority 1) — `module "dns"` comes from a git source with no `?ref=`.
3. **TF-6** (Priority 1) — the VPC's `tags` give `Name` twice, and Terraform keeps the last.
4. **TF-3** (Priority 7) — `subnet_cidrs` has no `type`.
5. **TF-4** (Priority 7) — `environment` has no `description`.

**Hard assertions (any failure blocks the skill change):**

- **No item files a decoy as its defect:**
  - `count = var.enable_nat ? 1 : 0`: the documented toggle.
  - `count = var.replica_count`: identical replicas, whose body reads `count.index` only to name them.
  - `>= 1.11`: a lower bound alone on Terraform's own version.
- **No IAC item**: the root has a remote backend, a committed lock file and a bounded provider.
- **TF-5 is one item**, never also `security.md`'s CWE-494.
- Every hazard item carries `Priority: 1`, and every other item `Priority: 7`. Every item carries
  `Route: report only`: no test suite checks a plan, so `/phil:refactor` cannot prove a change safe.

**Not a failure:**

- an Advisory question, where a file shows its subject — no TFLint in CI, no pipeline read;
- line numbers within ±2.
