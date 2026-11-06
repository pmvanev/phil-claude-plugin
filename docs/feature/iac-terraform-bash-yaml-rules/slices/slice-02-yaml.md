# Slice 02 — YAML read as the parser reads it

**Goal.** `/phil:review-code` names each YAML language defect, in every YAML file, by its `YAML-n` row,
and files a defect another rule owns only under that rule.

**Story:** US-02 · **Job:** catch-infrastructure-and-script-defects-in-review

## IN scope
- `rules/yaml.md`, holding:
  - frontmatter, Principles, and ownership lines into `ci-pipelines.md`, `iac.md` and `security.md`
    (D5);
  - Always-flag rows with `YAML-n` ids and `yamllint` rules;
  - Advisory, and Do not flag (D7);
  - the Helm-template exclusion (D6).
- `review-code` gathers every `*.{yml,yaml}` outside a chart's `templates/`, and checks it against
  `yaml.md`.
- A pointer line in `ci-pipelines.md`.
- A self-test fixture: a CI file and a values file, three or more violations, two or more decoys,
  including an `on:` key.
- README Rules list; version bump.

## OUT scope
- Helm templates, Kustomize semantics, and what a pipeline or a manifest does.

## Learning hypothesis
Disproves "YAML's typing defects occur in real repos often enough to earn a rule" **if** the dogfood run
over this repo and the sibling repos finds no instance. The DISCUSS scan found none. A null result is
recorded, and it puts the rule's Always-flag tier in question.

## Acceptance criteria
See US-02 in `feature-delta.md`.

## Dependencies
- Research precursor, YAML section. Slice 01's hazard promotion in `review-code`.

## Effort / reference class
≤ 1 day. Reference class: slice 01.

## Production data
This repo's 50 YAML files, and the sibling repos' CI, compose and Helm values files.
