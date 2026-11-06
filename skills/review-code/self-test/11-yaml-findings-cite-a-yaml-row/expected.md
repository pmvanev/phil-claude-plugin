# Expected outcome — fixture 11 (YAML findings cite a YAML row)

A billing service's configuration:

- `.gitlab-ci.yml`, a GitLab pipeline, which Psych reads as YAML 1.1;
- `chart/values.yaml`, Helm values, which `sigs.k8s.io/yaml` reads as YAML 1.1;
- `chart/Chart.yaml`, the chart's metadata, every value quoted where it must be;
- `chart/templates/configmap.yaml`, a Go template;
- `.github/workflows/ci.yml`, a GitHub workflow, which the runner types by YAML 1.2's core schema.

It holds six defects: five on lines an Always-flag row of `rules/yaml.md` describes, and a committed
password that `security.md` owns, beside four decoys that the rule's Do-not-flag list clears.
`test_config.py` is green: every file outside the templates parses.

**Pins:**

- `review-code` gathers every YAML file outside a Helm chart's `templates/`, and checks it against
  `yaml.md` as well as `security.md`.
- It names each finding by the row's `YAML-n` id and takes the row's Preferred form as its fix.
- It files every YAML row at Priority 1, since each is a hazard.
- It files the password once, as CWE-798, though its leading zero also fits YAML-3.

Before the rule existed, a review checked the CI file against `security.md` alone, skipped the values
file as config, and filed only the password.

**How to drive it:** drive this working tree's `skills/review-code/SKILL.md` by hand over this
directory (`/phil:review-code` runs the released copy).

**Expected:** a `.refactoring-backlog.md` holding the six items in `expected-backlog.md`. An item
matches on the Smell and on a Refactoring that is the row's Preferred form verbatim, alone or followed by
` — here: ` and this file's one change. Order is not checked.

1. **YAML-2** — `PYTHON_VERSION: 3.10` reaches the job as `3.1`.
2. **YAML-3** — `ARCHIVE_PREFIX: 007` reaches the job as `7`.
3. **YAML-4** — `MAINTENANCE_WINDOW: 2:30` reaches the job as `9000`, Psych's base-60 reading.
4. **CWE-798** — `REGISTRY_PASSWORD` is a credential literal in committed config.
5. **YAML-1** — `level: off` reaches the template as `false`, so the ConfigMap's `LOG_LEVEL` is
   `"false"`.
6. **YAML-5** — the second `resources:` replaces the first, and the limits vanish without an error.

**Hard assertions (any failure blocks the skill change):**

- **No item files a decoy as its defect:**
  - `NODE_MAJOR: 20`: a version whose number form keeps every character.
  - `weight: 1.0`: a number meant as a number.
  - `.github/workflows/ci.yml`: its `on:` key is GitHub's trigger, and the runner reads YAML 1.2.
  - `RETRY_SLOT` in `chart/templates/configmap.yaml`: a Go template, outside the rule.
- **The password is one item**, CWE-798, never also YAML-3.
- **YAML-5 is one item** naming both `resources:` lines.
- Every item carries `Priority: 1` and `Route: report only`.

**Not a failure:**

- an Advisory question, where a file shows its subject — no yamllint in CI, or a schema nothing
  validates;
- line numbers within ±2.
