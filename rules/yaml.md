---
paths:
  - "**/*.yml"
  - "**/*.yaml"
---

# YAML Guide

Guidelines drawn from the YAML 1.1 type repository and the YAML 1.2.2 specification; the yamllint
documentation; the documentation of the tools that read YAML — GitLab CI/CD variables, Docker
Compose, Helm's values guide, the Kubernetes API reference and `actions/setup-python`; and each
consumer's parser source, read and run on 2026-11-06. Research:
`docs/research/iac/iac-terraform-bash-yaml-canonical-sources.md` § 2 and its Addendum.

This rule owns **what a YAML file's text parses to**: whether a plain scalar becomes the type its author
wrote, and whether a mapping holds each key once. Neighbouring rules keep what they already own:
`ci-pipelines.md` what a pipeline does, though its file is YAML; the infrastructure rules what a
manifest or a chart deploys; `security.md` unsafe loading (CWE-502) and a credential in a file
(CWE-798). A defect two rules describe is filed once, under the other rule. Complement those — do not
restate them.

**It applies to** every `.yml` and `.yaml` file — CI, Compose, Kubernetes manifests, Helm values,
Ansible and application config — except a Helm chart's `templates/`, which holds Go templates that no
YAML parser reads before they render.

**The consumer decides the type.** The same text parses to different values in different readers:

| Consumer | Parser | `no` | `0755` | `1:20` | `3.10` |
|---|---|---|---|---|---|
| GitHub Actions workflow or action metadata | the runner's YAML 1.2 core typing | string | 755 | string | 3.1 |
| GitLab CI | Psych, YAML 1.1 | false | 493 | 4800 | 3.1 |
| Kubernetes manifest, Helm values | `sigs.k8s.io/yaml` over yaml.v2, YAML 1.1 | false | 493 | string | 3.1 |
| Ansible, and any PyYAML reader | PyYAML, YAML 1.1 | false | 493 | 80 | 3.1 |
| Docker Compose v2 | yaml v4, YAML 1.2 | false in a boolean field, else string | 493 | string | 3.1 |
| ruamel.yaml, by default | YAML 1.2 | string | 755 | string | 3.1 |

Name the consumer from the file's path and its own keys — `.gitlab-ci.yml`, `.github/workflows/`,
`apiVersion:` and `kind:`, a `values.yaml` beside a `Chart.yaml`, a playbook's `hosts:` — or from the
code that loads it. **Where the review cannot name the consumer**, judge the file as YAML 1.1: a quoted
string reads alike under every parser.

**The two halves divide on checkability.** The reviewer half — Always-flag, Advisory and Do not flag —
names the defects a file shows, each by its `YAML-n` id. A row is a hazard when a miss changes what a
parser makes of the file, and a review files it at Priority 1. A defect no source names stays
Advisory. Each row names the yamllint rule that catches it, where one exists; the review reads and never
runs one. The Principles half is design and yields no finding on its own.

---

## Principles — design, not review criteria

### 1. Write the type you mean

Quote a string that looks like a boolean, a number or a time, and write `true` or `false` for a
boolean. YAML 1.2 "removed many of the problematic implicit typing recommendations", but the parsers in
use have not all followed it, and `3.10` is a float under both versions.

### 2. Know which YAML the consumer reads

A file has no version of its own; the tool that reads it has one. Read the table above before judging a
scalar, and never reason from the specification's version alone.

### 3. Give each key once

YAML 1.2.2 makes every key in a mapping unique, and says a processor should "flag the duplicate key as
an error". PyYAML and Psych keep the last value and say nothing; ruamel.yaml refuses the file.

### 4. Lint where the file is written

yamllint's default config rejects duplicate keys, warns on truthy values and disables
`octal-values`. A warning fails nothing unless CI runs yamllint with `--strict`.

---

## Always-flag — objective defects

Name each finding by its `YAML-n` id. Every row here is a hazard: the parser turns the text into
something its author did not write. A credential literal is `security.md`'s CWE-798 alone, whatever its
spelling.

| Id | Violation | Preferred form | Hazard | Linter | Cite |
|----|-----------|----------------|--------|--------|------|
| YAML-1 | A plain key or value spelled as a YAML 1.1 boolean other than `true` or `false` — `yes`, `no`, `on`, `off` in any listed case, and `y` or `n` under yaml.v2 — in a file whose consumer reads it as a boolean: GitLab CI, a Kubernetes manifest, Helm values, Ansible or another PyYAML reader, or a consumer the review cannot name | `true` or `false` where a boolean is meant; a quoted string (`"no"`) where a string is | hazard | yamllint `truthy` (default: warning) | YAML 1.1 `bool` type; GitLab, "CI/CD variables"; Helm, "Values" best practices; `sigs.k8s.io/yaml` |
| YAML-2 | A plain value meant as a string that parses as a number with a trailing zero after the point, which the number drops: a version (`3.10` becomes 3.1, `1.20` becomes 1.2) | Quote it (`"3.10"`) | hazard | none | YAML 1.2.2 § 10.3.2; `actions/setup-python` issues 160 and 249 |
| YAML-3 | A plain integer with a leading zero meant as a string (`007`), which every parser reads as a number and strips of its zero; or meant as an octal mode in a file a YAML 1.2 core reader parses, which reads `0755` as decimal 755 | A quoted string (`"007"`) where a string is meant; `0o755` where a YAML 1.2 core reader needs an octal | hazard | yamllint `octal-values` (off by default) | YAML 1.1 `int` type; YAML 1.2.2 § 10.3.2; GitLab, "CI/CD variables" |
| YAML-4 | A plain value of colon-separated digits whose later parts run 0 to 59 (`1:20`, `08:30`, `190:20:30`), in a file Psych or PyYAML reads — GitLab CI, Ansible — which turns it into a base-60 integer: PyYAML reads `1:20` as 80, and Psych as 4800, and Psych reads `08:30` too | Quote it (`"1:20"`) | hazard | none | YAML 1.1 `int` type (base 60); Psych `ScalarScanner` |
| YAML-5 | The same key twice in one mapping, a `<<` merge key included: PyYAML and Psych keep the last value without an error, ruamel.yaml refuses the file, and two `<<` keys merge in the reverse of a `<<: [*a, *b]` list's order | One key, its values merged by hand; for two merges, one `<<: [*a, *b]` listing the anchors in precedence order | hazard | yamllint `key-duplicates` (default: on; a `<<` key only with `forbid-duplicated-merge-keys: true`) | YAML 1.2.2 § 3.2.1.3; PyYAML issue 165 |

Checked 2026-11-06 by parsing each scalar under PyYAML 6.0.3, ruamel.yaml 0.18.10 and Psych 5.1.2,
and by reading the source of the GitHub Actions runner, compose-go v2.16.2, `sigs.k8s.io/yaml` v1.6.0
and go-yaml v2 and v3.

---

## Advisory — judgment calls, not hard blocks

A reviewer raises these; the author decides.

- **A mapping's own key that overrides a merged key** the author may have meant to keep. The YAML 1.1
  merge type lets the own key win by design; ask which value was meant.
- **A `<<` merge key in a file whose consumer does not document merge keys.** `<<` is a YAML 1.1 type,
  absent from YAML 1.2's core schema, where it is an ordinary key.
- **An anchor defined twice in one document**: an alias takes the later definition (yamllint `anchors`
  with `forbid-duplicated-anchors: true`, off by default).
- **`null`, `Null`, `~` or an empty value where a string was meant.**
- **A boolean spelling meant as a boolean in a GitHub Actions file** — `continue-on-error: yes` — which
  the runner reads as the string "yes". Ask whether `true` was meant.
- **A Compose `ports` entry of unquoted digits and a colon.** Docker: "`HOST:CONTAINER` should always be
  specified as a (quoted) string, to avoid conflicts with YAML base-60 float." Compose v2's parser
  keeps it a string, so ask.
- **A file with a published schema that nothing validates** — a Kubernetes manifest, a Compose file, a
  GitHub workflow. Raise it only where the review read the CI config.
- **No yamllint in the project's CI.** Raise it only where the review read the CI config. One item per
  project, not per file.

---

## Do not flag

- **GitHub Actions' `on:` key**, and any key the consuming tool defines. yamllint warns on it by
  default, and its maintainers call the warning intended.
- **YAML-1 and YAML-4 in a GitHub Actions workflow or action metadata file.** The runner types plain
  scalars by YAML 1.2's core schema, so `no` stays the string "no" and `1:20` a string.
- **A Helm chart's `templates/`**: a Go template, read by no YAML parser before it renders. Read a
  template to learn whether a value is meant as a string; file nothing in it.
- **A number meant as a number** — `cpus: 2.0`, `max: 1.0`, a weight of `0.0` — and a version field the
  consumer documents as a number.
- **A version whose number form keeps every character** — `3.9`, `18` — where the consumer turns it
  back into a string: the parse changes the type, not the text.
- **An octal mode the consumer documents in YAML**: Kubernetes' `defaultMode: 0644`, which "Must be an
  octal value between 0000 and 0777 or a decimal value between 0 and 511".
- **`true`, `false`, a quoted scalar**, and a `0o` octal under a YAML 1.2 reader.
- **A key a `<<` merge supplies, written again in the mapping**: the merge mechanism, not a duplicate
  (Advisory above when the override looks unintended).
- **A row the project's yamllint already enforces**: CI runs yamllint, and its config enables that
  row's rule at a level its CI reports. Read both: `octal-values` is off by default, and `truthy` warns,
  which fails nothing unless CI runs yamllint with `--strict`. A row whose Linter cell reads none never
  stands down.
