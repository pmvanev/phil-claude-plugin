# Refactoring Backlog — YAML items expected

Scope: .

## Backlog

### [R001] YAML-2 — GitLab reads the Python version as 3.1

- **File**: `.gitlab-ci.yml`
- **Lines**: 6
- **Priority**: 1
- **Smell**: YAML-2
- **Refactoring**: Quote it (`"3.10"`) — here: `PYTHON_VERSION: "3.10"`
- **Route**: report only
- **Rationale**: yaml.md — YAML 1.2.2 § 10.3.2; `actions/setup-python` issues 160 and 249
- **Status**: pending

### [R002] YAML-3 — the archive prefix loses its zeros

- **File**: `.gitlab-ci.yml`
- **Lines**: 7
- **Priority**: 1
- **Smell**: YAML-3
- **Refactoring**: A quoted string (`"007"`) where a string is meant; `0o755` where a YAML 1.2 core reader needs an octal — here: `ARCHIVE_PREFIX: "007"`, which Psych otherwise reads as octal 7
- **Route**: report only
- **Rationale**: yaml.md — YAML 1.1 `int` type; YAML 1.2.2 § 10.3.2; GitLab, "CI/CD variables"
- **Status**: pending

### [R003] YAML-4 — GitLab reads the maintenance window as 9000

- **File**: `.gitlab-ci.yml`
- **Lines**: 8
- **Priority**: 1
- **Smell**: YAML-4
- **Refactoring**: Quote it (`"1:20"`) — here: `MAINTENANCE_WINDOW: "2:30"`
- **Route**: report only
- **Rationale**: yaml.md — YAML 1.1 `int` type (base 60); Psych `ScalarScanner`
- **Status**: pending

### [R004] CWE-798 — a registry password committed in the CI file

- **File**: `.gitlab-ci.yml`
- **Lines**: 9
- **Priority**: 1
- **Smell**: CWE-798
- **Refactoring**: Load from a secrets manager, or the runtime environment where none exists; rotate the leaked value
- **Route**: report only
- **Rationale**: security.md — CWE-798 · v5.0.0 V13
- **Status**: pending

### [R005] YAML-1 — Helm reads the log level `off` as false

- **File**: `chart/values.yaml`
- **Lines**: 8
- **Priority**: 1
- **Smell**: YAML-1
- **Refactoring**: `true` or `false` where a boolean is meant; a quoted string (`"no"`) where a string is — here: `level: "off"`
- **Route**: report only
- **Rationale**: yaml.md — YAML 1.1 `bool` type; GitLab, "CI/CD variables"; Helm, "Values" best practices; `sigs.k8s.io/yaml`
- **Status**: pending

### [R006] YAML-5 — the second `resources` key drops the limits

- **File**: `chart/values.yaml`
- **Lines**: 11, 20
- **Priority**: 1
- **Smell**: YAML-5
- **Refactoring**: One key, its values merged by hand; for two merges, one `<<: [*a, *b]` listing the anchors in precedence order — here: one `resources:` holding both `limits` and `requests`
- **Route**: report only
- **Rationale**: yaml.md — YAML 1.2.2 § 3.2.1.3; PyYAML issue 165
- **Status**: pending
