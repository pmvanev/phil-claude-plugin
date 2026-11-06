# Slice 03 — Infrastructure as Code, tool-agnostic

**Goal.** `/phil:review-code` names each infrastructure-code defect by its `IAC-n` row, in terms no
single tool owns.

**Story:** US-03 · **Job:** catch-infrastructure-and-script-defects-in-review

## IN scope
- `rules/iac.md`, holding:
  - frontmatter, Principles (Morris, and `continuous-delivery.md`'s four bullets cited, not restated);
  - Always-flag rows with `IAC-n` ids for state and locking, drift, pinned versions, plan before apply,
    secrets (pointing to `security.md`), one module per responsibility, and environments that differ
    only by input;
  - Advisory and Do not flag.
- `continuous-delivery.md` § *Infrastructure as Code* points to `iac.md`.
- `review-code` names `iac.md` for every IaC file it gathers (`*.tf` here; other tools when a tool rule
  arrives).
- A self-test fixture in Terraform: three or more violations, one decoy.
- README Rules list; version bump.

## OUT scope
- Terraform-specific rows (slice 04). CloudFormation, SAM, Pulumi and CDK rules.

## Learning hypothesis
Disproves "a tool-agnostic rule can be checked row by row" **if** a row cannot be judged from a
Terraform file without Terraform-specific knowledge. Such a row moves to `terraform.md`, and `iac.md`
shrinks to Principles plus the rows that survive.

## Acceptance criteria
See US-03 in `feature-delta.md`.

## Dependencies
- Research precursor, IaC section.

## Effort / reference class
≤ 1 day. Reference class: slice 01.

## Production data
`modive/infra`, `infrastructure/demo-platform` and `beatrix/infra/terraform`, including its `envs/`
tree.
