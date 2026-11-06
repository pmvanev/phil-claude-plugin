# Slice 04 — Terraform reviewed by row

**Goal.** `/phil:review-code` names each Terraform defect by its `TF-n` row and fix, and leaves the 0/1
`count` toggle alone.

**Story:** US-04 · **Job:** catch-infrastructure-and-script-defects-in-review

## IN scope
- `rules/terraform.md`, holding:
  - frontmatter, and an ownership paragraph pointing to `iac.md`, `security.md`, `ci-runners.md` and
    `lambda-web-app-speed.md` (D12);
  - Always-flag rows with `TF-n` ids and `tflint` rules, for module layout, variable and output typing,
    `for_each` over `count` (D11), `fmt` and `validate`;
  - Advisory and Do not flag.
- `review-code` gathers `*.tf` on every run, not only Lambda repos, and names `terraform.md` for it.
- A self-test fixture: four or more violations, two or more decoys.
- README Rules list; version bump.

## OUT scope
- Running `terraform` or `tflint` (D13). Provider-specific rows (AWS, Azure).

## Learning hypothesis
Disproves "`terraform.md` can point to `iac.md` without restating it" **if** the fixture needs a row
copied from `iac.md` to file a finding. It also disproves D11's line **if** the dogfood run misses any
of the four measured `count = length(…)` sites, or flags any of the 78 toggles.

## Acceptance criteria
See US-04 in `feature-delta.md`.

## Dependencies
- Slice 03 (`iac.md`). Research precursor, Terraform section.

## Effort / reference class
≤ 1 day. Reference class: slice 01.

## Production data
`modive/infra` and `beatrix/infra/terraform`. The four `count = length(…)` sites are the known
defects; the 78 toggles and the 45 lower-bound-only `required_version` constraints are the known
Do-not-flag cases.
