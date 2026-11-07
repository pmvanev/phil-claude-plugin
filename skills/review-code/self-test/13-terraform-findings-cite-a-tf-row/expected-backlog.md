# Refactoring Backlog — Terraform items expected

Scope: .

## Backlog

### [R001] TF-1 — the private subnets are addressed by position

- **File**: `network.tf`
- **Lines**: 11-20
- **Priority**: 1
- **Smell**: TF-1
- **Refactoring**: `for_each` over a map or a set keyed by a stable id, each existing instance moved to its key with a `moved` block — here: `for_each = toset(var.subnet_cidrs)` on `aws_subnet.private`, with `cidr_block = each.value` and a `moved` block from each `[n]` to its CIDR
- **Route**: report only
- **Rationale**: terraform.md — Brikman, "Terraform tips & tricks"; HashiCorp, `for_each`
- **Status**: pending

### [R002] TF-5 — the DNS module tracks its repository's default branch

- **File**: `network.tf`
- **Lines**: 37-38
- **Priority**: 1
- **Smell**: TF-5
- **Refactoring**: A git `?ref=` naming a tag or a commit; a registry `version` constraint — here: `source = "git::https://github.com/acme/terraform-aws-dns.git?ref=<tag>"`
- **Route**: report only
- **Rationale**: terraform.md — HashiCorp, "Version Constraints"; Google, reusable modules
- **Status**: pending

### [R003] TF-6 — the VPC's `Name` tag is given twice

- **File**: `network.tf`
- **Lines**: 5-7
- **Priority**: 1
- **Smell**: TF-6
- **Refactoring**: One key, holding the value meant — here: drop `Name = "orders"`; Terraform keeps the last value, `orders-${var.environment}-vpc`, and the plan does not say so
- **Route**: report only
- **Rationale**: terraform.md — HashiCorp, HCSEC-2023-26
- **Status**: pending

### [R004] TF-3 — `subnet_cidrs` accepts any type

- **File**: `variables.tf`
- **Lines**: 17-19
- **Priority**: 7
- **Smell**: TF-3
- **Refactoring**: The narrowest `type` that admits every value it takes — here: `type = list(string)`
- **Route**: `/phil:refactor`
- **Rationale**: terraform.md — HashiCorp, Style Guide; Google, style and structure
- **Status**: pending

### [R005] TF-4 — `environment` has no description

- **File**: `variables.tf`
- **Lines**: 7-9
- **Priority**: 7
- **Smell**: TF-4
- **Refactoring**: A one- or two-sentence `description` — here: `description = "Environment name, used in resource names and tags."`
- **Route**: `/phil:refactor`
- **Rationale**: terraform.md — HashiCorp, Style Guide; HashiCorp, "Standard Module Structure"
- **Status**: pending
