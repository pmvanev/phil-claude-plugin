# Refactoring Backlog — infrastructure items expected

Scope: .

## Backlog

### [R001] IAC-1 — staging's state file is committed

- **File**: `envs/staging/terraform.tfstate`
- **Lines**: 1-9
- **Priority**: 1
- **Smell**: IAC-1
- **Refactoring**: State in a remote backend; state files ignored by version control — here: delete `envs/staging/terraform.tfstate` and ignore `*.tfstate` and `*.tfstate.*`; the S3 backend already holds the state
- **Route**: report only
- **Rationale**: iac.md — Brikman, "How to manage Terraform state"; HashiCorp, Style Guide; AWS, "Backend best practices"
- **Status**: pending

### [R002] IAC-2 — staging and prod write one state

- **File**: `envs/prod/main.tf`
- **Lines**: 2-7
- **Priority**: 1
- **Smell**: IAC-2
- **Refactoring**: One state per environment, each at a location no other environment's state uses — here: give prod its own state, at least a distinct `key` (`prod/network/terraform.tfstate`), and better a bucket of its own; both roots now use `acme-billing-tfstate` at `network/terraform.tfstate`
- **Route**: report only
- **Rationale**: iac.md — AWS, "Backend best practices"; Brikman, "How to manage Terraform state"; Google, root modules
- **Status**: pending

### [R003] IAC-3 — the prod root commits no lock file

- **File**: `envs/prod/`
- **Lines**: —
- **Priority**: 1
- **Smell**: IAC-3
- **Refactoring**: Commit the tool's lock file in every root — here: run `terraform init` in `envs/prod/` and commit its `.terraform.lock.hcl`, as staging does
- **Route**: report only
- **Rationale**: iac.md — HashiCorp, "Dependency Lock File"; HashiCorp, Style Guide; Google, root modules
- **Status**: pending

### [R004] IAC-4 — the prod root bounds the AWS provider from below only

- **File**: `envs/prod/versions.tf`
- **Lines**: 7
- **Priority**: 7
- **Smell**: IAC-4
- **Refactoring**: A lower and an upper bound on each provider, in the root — here: `version = "~> 5.80"`, as staging pins it
- **Route**: `/phil:refactor`
- **Rationale**: iac.md — HashiCorp, "Version Constraints"; Google, root modules
- **Status**: pending

### [R005] IAC-5 — the network module configures its own provider

- **File**: `modules/network/main.tf`
- **Lines**: 1-3
- **Priority**: 7
- **Smell**: IAC-5
- **Refactoring**: Configure backends and providers in the root, and pass providers in — here: delete the `provider "aws"` block and the `region` variable; the calling root's provider already sets the region
- **Route**: `/phil:refactor`
- **Rationale**: iac.md — Google, reusable modules; HashiCorp, "Providers Within Modules"
- **Status**: pending

### [R006] IAC-6 — the network module defaults the account id

- **File**: `modules/network/variables.tf`
- **Lines**: 1-5
- **Priority**: 7
- **Smell**: IAC-6
- **Refactoring**: An input with no default, set by each environment's root — here: delete `default = "111122223333"` from `account_id`
- **Route**: `/phil:refactor`
- **Rationale**: iac.md — Google, style and structure
- **Status**: pending

### [R007] IAC-7 — prod copies the network module's resources instead of calling it

- **File**: `envs/prod/main.tf`
- **Lines**: 14-38
- **Priority**: 7
- **Smell**: IAC-7
- **Refactoring**: One shared module; each environment a root that passes its own inputs — here: replace prod's `aws_vpc` and `aws_subnet` with a `module "network"` call like staging's, passing prod's CIDR blocks, name and account, and move the resources with `moved` blocks
- **Route**: `/phil:refactor`
- **Rationale**: iac.md — Morris, "Snowflakes as Code"; Google, root modules
- **Status**: pending
