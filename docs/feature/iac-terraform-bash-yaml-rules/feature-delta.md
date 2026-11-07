<!-- markdownlint-disable MD024 -->
# Feature Delta — iac-terraform-bash-yaml-rules

Wave: DISCUSS ✓ (2026-11-06) · Density: lean
Build path: DISCUSS here, then the rules are written directly — the deliverable is prose, so DESIGN,
DISTILL and DELIVER stay out (edd-loop DDD8). Rules are not a plugin component; `plugin-dev:skill-reviewer`
reviews the `review-code` change. Tracked on issue 79.

This feature adds four standards — `rules/iac.md`, `rules/terraform.md`, `rules/bash.md` and
`rules/yaml.md` — and makes `/phil:review-code` apply each to the files it matches.

---

## Wave: DISCUSS / [REF] The gap, measured

Measured 2026-11-06 against `main` at `8436226`, and over the sibling repos in `~/Git/ia-gitlab`
(worktree copies excluded):

- **`review-code` checks idiom in four languages.** `skills/review-code/SKILL.md:46` names `cpp.md`,
  `python.md`, `typescript.md` and `react.md`, and no other. It gathers `*.sh` and CI YAML only to check
  them against `security.md`, `*.tf` only where it reads `lambda-web-app-speed.md`, and any other YAML
  never.
- **IaC has four bullets and no checkable standard.** `continuous-delivery.md:145` § *Infrastructure as
  Code*: treat it like code, provision automatically, no manual production changes, disposable
  environments.
- **Shell.**
  - Of 238 scripts in the sibling repos, 107 never set `-e` and 82 never set `pipefail`, and three run
    to 934, 1,090 and 1,958 lines.
  - ShellCheck 0.11.0 at warning level finds 102 issues in 15 scripts: 77 of them SC2034 (unused
    variable) and 9 SC2155 (`local x=$(…)` masks the exit status).
  - ShellCheck flags none of the missing `-e` or `pipefail` cases, nor the script that has outgrown
    shell. That is the gap a rule fills and a linter does not.
  - This repo's 19 scripts are ShellCheck-clean. `scripts/ci/run.sh` is deliberate POSIX `sh` with
    `set -eu`, a case a Bash rule must not flag.
- **Terraform.**
  - Of 63 directories holding `*.tf`, 56 hold a `.terraform.lock.hcl`. Only a root module needs one;
    in a child module it is harmless and unread, so only a root without one is a finding (research §4.3).
  - `count = length(…)` indexes resources by position at four sites:
    - `modive/infra/bootstrap/main.tf:131` and `:149`
    - `beatrix/infra/terraform/modules/vpc/main.tf:74` and `:98`
  - `count = var.x ? 1 : 0`, the accepted toggle, appears at 78 sites.
  - All 45 `required_version` constraints bound the CLI only from below (`>= 1.0` to `>= 1.11`), which
    is HashiCorp's documented practice, not a defect (research §4.2). The sampled root modules pin
    providers with `~>`.
- **YAML.** A scan for unquoted `yes`, `no`, `on`, `off`, leading-zero octals and bare `X.Y` versions
  found no defect in the sibling repos. Its one hit is GitHub Actions' `on:` key at
  `.github/workflows/ci.yml:8`, which YAML 1.1 reads as `true` and GitHub's parser reads as a key. The
  YAML gap rests on the card's claim alone: slice 02 must find a real instance or say none exists.

## Wave: DISCUSS / [REF] Pre-requisites

- **Research precursor (D1), done 2026-11-06.** One document,
  `docs/research/iac/iac-terraform-bash-yaml-canonical-sources.md`, 47 sources, with a section per rule.
  It refined D7 to D11 and D13; each row below names what changed.
- **Production data, on this machine:**
  - shell: the 238 sibling scripts, plus this repo's 19;
  - Terraform: `modive/infra`, `infrastructure/demo-platform`, `beatrix/infra/terraform` and
    `docs/runbooks/runners`;
  - YAML: this repo's workflows and `.nwave/*.yaml`, plus the sibling repos' CI, compose and Helm values
    files.
- **Existing artifacts touched:**
  - new: `rules/iac.md`, `rules/terraform.md`, `rules/bash.md` and `rules/yaml.md`;
  - edited: `skills/review-code/SKILL.md` and `skills/review-code/self-test/`;
  - a pointer line in each of `continuous-delivery.md`, `ci-pipelines.md` and `security.md`;
  - `README.md`, `.claude-plugin/plugin.json`, `docs/product/jobs.yaml` and
    `docs/product/personas/quinn-codebase-steward.yaml`.

## Wave: DISCUSS / [REF] Persona ID

**`quinn-codebase-steward`, extended with an infrastructure-and-scripts facet — no new persona.** Quinn
already runs `/phil:review-code` and already owns the pipeline and the runner Terraform (CI facet). A
Terraform module, a deploy script and a values file are the same codebase in other languages.

## Wave: DISCUSS / [REF] JTBD one-liner

**New job: `catch-infrastructure-and-script-defects-in-review`.**

> When I review a change to Terraform, a shell script or a YAML file, I want its defects named by row and
> fix, as a Python or TypeScript change already gets, so the review, not a failed apply, a silent pipe
> failure or a `no` read as `false`, is where I learn of them.

Not a facet of `catch-security-defects-in-review`: these defects cost a broken deploy or a wrong value,
not an attacker's foothold. A row that is also a security defect stays in `security.md`.

## Wave: DISCUSS / [REF] Locked decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D1 | **Research is a precursor**: one document, one section per rule, before slice 01. Sources to weigh: the Terraform style guide and language docs, `tflint` rules, Brikman's *Terraform: Up & Running*, Morris's *Infrastructure as Code*, the Google Shell Style Guide, the ShellCheck wiki, Wooledge's BashFAQ and pitfalls, the YAML 1.1 and 1.2 specs, and `yamllint` rules. | Every prior rule feature's bar: "empirical design over speculation", and the user's "canonical patterns first". |
| D2 | **One card, four slices, one per rule.** | User decision, 2026-11-06. The card asked to split by language once sized. Sizing fired two oversized signals (four technologies; four independently shippable outcomes), and slicing answers both without new cards. |
| D3 | **Each rule splits on checkability**: Principles, then Always-flag, Advisory and Do not flag. Rows carry the rule's own stable ids — `IAC-n`, `TF-n`, `SH-n`, `YAML-n` — with the linter rule or source section beside them as the citation (`SC2086`, `terraform_deprecated_index`, `yamllint truthy`). A retired id is never reused. | `security.md` D3 and `ci-pipelines.md` D4. The card asks for an Always-flag table "as `ci-pipelines.md` has", and a fixture must cite a row, which needs an id that names one fix. |
| D4 | **`review-code` files these at Priority 7 by row id, and promotes a row the rule marks *hazard* to Priority 1.** The fix is the row's Preferred form verbatim, then ` — here: ` and this file's one change, as **Security** and **Load time** do. A hazard is a row whose miss changes behaviour: an unquoted expansion, a lost pipe failure, a YAML scalar typed as something its author did not write. | Priority 7 is where idiom lives today; the existing promotion rule ("genuine correctness hazards … to Priority 1") already covers a mutable default argument. The verbatim-prefix form made security fixtures gradeable (security-standards-rule, 1.2.5). |
| D5 | **The YAML rule checks the language in every YAML file**: CI, compose, Helm values and config included. It checks implicit typing, anchors and merge keys, duplicate keys, schema and the linter. **Ownership:** `ci-pipelines.md` keeps what a pipeline does, `iac.md` and `terraform.md` what infrastructure does, `security.md` unsafe loading (CWE-502). The review files a defect that two rules describe once, under the most specific owner. | User decision, 2026-11-06. A value YAML turns into `true`, `false` or a number is a language defect wherever it sits, and the pipeline rule checks no typing. **Scope revised by the evidence check:** `3.10` becomes 3.1 for every consumer, but an unquoted `no` is false only for GitLab CI, Kubernetes, Helm values, PyYAML and Go yaml.v2, and a string for GitHub Actions. Slice 02 scopes its boolean and octal rows by the consumer that reads the file (research Addendum). |
| D6 | **A Helm template is not YAML.** `templates/*.yaml` under a chart is a Go template, outside every row here. | No YAML parser reads it before rendering, so no YAML row can judge it. |
| D7 | **A key the consuming tool documents is Do not flag**: GitHub Actions' `on:` is the one with evidence. Any other needs its tool's own source before the rule names it. | Measured at `.github/workflows/ci.yml:8`. yamllint flags it by default, and its maintainer calls that intended. Flagging it would teach the reader to skip the YAML tier. *Narrowed by research.* |
| D8 | **The Bash rule judges a script by its shebang.** `#!/bin/sh` is POSIX: no demand for `pipefail`, `[[ ]]` or `local`. An executable file with no shebang is a finding. A `.sh` library with neither a shebang nor a `# shellcheck shell=` directive is Advisory, and one with the directive is not flagged. | `scripts/ci/run.sh` is deliberate POSIX `sh` with `set -eu`; a Bash-only row there would be a false alarm on this repo's own entry point. `pipefail` entered POSIX in 2024, but dash and macOS `sh` lagged, so the `pipefail` half rests on portability. Google: a library "must have a `.sh` extension and should not be executable". *Refined by research; the library clause made Advisory by the evidence check.* |
| D9 | **`bash.md` matches `.sh` and `.bash`, and an extensionless file whose first line names `sh` or `bash`.** | Google: "Executables should have a `.sh` extension or no extension." ShellCheck judges the dialect by directive, then shebang, then extension, and `.sh` is not among its extensions, so the shebang decides. *Rationale corrected by research.* |
| D10 | **"Rewrite it in Python" is Advisory, never Always-flag.** The rule states Google's threshold, verified: "more than 100 lines long, or that uses non-straightforward control flow logic". Arrays of records and parsing JSON are this feature's signals, not Google's. | Scripts of 934, 1,090 and 1,958 lines exist and work. Length is a judgement the author makes, not a defect on a line. |
| D11 | **`count` over a collection whose body indexes it by `count.index` is Always-flag; `count = cond ? N : 0` and `count = N` over identical instances are Do not flag.** | Measured: four `count = length(…)` sites, 78 toggles. Removing an element from the middle of a list destroys and recreates every resource after it (Brikman; HashiCorp). No tflint rule covers it. *Trigger sharpened by research.* |
| D12 | **Complement, do not restate.** `iac.md` states the tool-agnostic form once; `terraform.md` gives the Terraform form and points to it. `continuous-delivery.md` keeps its four bullets and points to `iac.md`. `security.md` keeps secrets in code and state (CWE-798, CWE-312) and shell injection (CWE-78). `ci-runners.md` and `lambda-web-app-speed.md` keep their Terraform reads. | `security.md` D8; the ownership-paragraph pattern every newer rule follows. |
| D13 | **Each row cites the linter that catches it, and the rule never requires running one.** The review reads; where the project's linter config enables *that row's* rule at a severity its CI reports, the row is Do not flag. Defaults differ: yamllint disables `octal-values`, and ShellCheck's `require-double-brackets` is opt-in. *Condition added by research; severity added by slice 01's dogfood.* A project that lints none of these files gets one Advisory per language. | `review-code` judges by reading. A repo whose CI runs ShellCheck gains nothing from a review that restates it. |
| D14 | **`paths:` frontmatter mirrors each rule's globs.** | `security.md` D12. Takes effect only for a consumer who copies the rule. |

## Wave: DISCUSS / [REF] Driving ports

- **`/phil:review-code`** — its *Language idioms* step names each new rule and the files it matches, and
  files findings by row id to `.refactoring-backlog.md`.
- **The rule files** — read by any skill that names them, and by a consumer who copies them into
  `.claude/rules/`.

## Wave: DISCUSS / [REF] WS strategy

**A — none.** Additive and brownfield: one new rule per slice, plus one edited skill. Slice 01 is the
thinnest end-to-end value: a review that names a shell defect by row.

## Wave: DISCUSS / [REF] Scope Assessment: split approved

Two oversized signals fired: four distinct technologies, and four outcomes that ship separately. Split
into four slices on one card (D2). Each slice has one context (rules and review), one integration point
(`review-code`), and production data on this machine.

## Wave: DISCUSS / [REF] User stories

All stories trace to `job_id: catch-infrastructure-and-script-defects-in-review`.

### US-01 — Shell scripts reviewed by row *(slice 01)*

**Problem.** Quinn reviews a deploy script that pipes `curl` into `jq` with no `pipefail`, and assigns
`local out=$(aws …)`. The pipe fails silently and the assignment hides the exit status. ShellCheck flags
the second and never the first; the review flags neither.

**Solution.** `rules/bash.md`, plus `review-code` matching `.sh`, `.bash` and sh/bash shebangs to it.

#### Elevator Pitch
Before: a review checks a shell script only for injection, and says nothing on a failure it swallows.
After: run `/phil:review-code scripts/` → sees `Priority 1 — SH-n: pipeline with no pipefail — <Preferred form> — here: …` and no item on a POSIX `sh` script that omits it.
Decision enabled: which script defects to fix before the change merges, and which scripts should stop being shell.

#### Acceptance Criteria
- [ ] `rules/bash.md` holds an Always-flag table covering at least an unchecked failure, a pipeline
      that loses its left-hand status, quoting, `[[ ]]`, `local`, `trap` cleanup and the masked exit
      status. A script is never flagged merely for lacking `set -e` (research, Conflict B-1). Each row carries an `SH-n` id, a Preferred
      form and its ShellCheck code where one exists.
- [ ] Its Do not flag list holds at least a POSIX `sh` script's omissions (D8) and a variable ShellCheck
      calls unused that a sourcing script reads.
- [ ] Its Advisory list holds the rewrite-in-Python question with its threshold (D10).
- [ ] `review-code`'s *Language idioms* step names `bash.md` and the files it matches (D9).
- [ ] A self-test fixture seeds at least four Always-flag violations and two decoys, one of them a POSIX
      script; the expected backlog cites every violation by row and no decoy.
- [ ] A dogfood run over the sibling scripts is recorded, naming the version run.

### US-02 — YAML read as the parser reads it *(slice 02)*

**Problem.** A values file says `enabled: no`, a workflow says `python-version: 3.10`, and a compose
file sets `mode: 0755`. Each parses as something its author did not write (`false`, `3.1`, `493`), and
no review says so.

**Solution.** `rules/yaml.md` across every YAML file (D5), with ownership lines into `ci-pipelines.md`,
`iac.md` and `security.md`, and the Helm-template and parser-defined exclusions (D6, D7).

#### Elevator Pitch
Before: a review reads YAML only for an unsafe load or a pipeline rule.
After: run `/phil:review-code --changes` on a change to a values file → sees `Priority 1 — YAML-n: unquoted scalar YAML 1.1 types as boolean — quote it — here: enabled: "no"` and no item on a workflow's `on:` key.
Decision enabled: which values to quote or type before the file ships.

#### Acceptance Criteria
- [ ] `rules/yaml.md` holds Always-flag rows for implicit booleans, octals and floats, duplicate keys,
      and a merge key that silently overrides. Each row carries a `YAML-n` id and its `yamllint` rule.
- [ ] Do not flag holds D7's parser-defined keys; the rule states D6's Helm exclusion.
- [ ] Each overlap with `ci-pipelines.md` and `security.md` names its owner, and a fixture defect that
      two rules describe is filed once.
- [ ] A fixture seeds at least three violations across a CI file and a values file, plus two decoys.
- [ ] The dogfood run finds a real instance in the sibling repos, or records that none exists.

### US-03 — Infrastructure as Code, tool-agnostic *(slice 03)*

**Problem.** A change adds an environment by copying a directory and editing values inline, and pins no
provider. The review has four general bullets and nothing to cite.

**Solution.** `rules/iac.md`: state and its locking, drift, pinned versions, plan before apply, no
secrets in code or state (pointing to `security.md`), one module per responsibility, and environments
that differ only by input.

#### Elevator Pitch
Before: a review of infrastructure code can cite only "treat infrastructure like application code".
After: run `/phil:review-code infra/` → sees `Priority 7 — IAC-n: environment copied rather than parameterised — <Preferred form> — here: …`.
Decision enabled: whether the change's structure holds before a second environment copies it.

#### Acceptance Criteria
- [ ] `rules/iac.md` holds the Always-flag rows the card's *Covers* list names, each with an `IAC-n` id.
      Each row states its form in terms no single tool owns.
- [ ] `continuous-delivery.md` § *Infrastructure as Code* points to `iac.md` without losing its bullets.
- [ ] A fixture seeds at least three violations and one decoy, in Terraform, because a fixture needs a
      language.

### US-04 — Terraform reviewed by row *(slice 04)*

**Problem.** `count = length(var.subnets)` keys subnets by position, so dropping one from the middle
recreates every subnet after it. An untyped variable accepts anything. No review names either.

**Solution.** `rules/terraform.md`: module layout, variable and output typing, `for_each` over `count`
(D11), `terraform fmt` and `validate`, `tflint`, and the Terraform form of each `iac.md` row, pointing
back.

#### Elevator Pitch
Before: a review reads `*.tf` only for Lambda cold starts and runner security.
After: run `/phil:review-code infra/` → sees `Priority 1 — TF-n: count over a collection — for_each over a map or set — here: aws_subnet.private` and no item on `count = var.enabled ? 1 : 0`.
Decision enabled: whether to migrate the resource to `for_each` (with `moved` blocks) before the list next changes.

#### Acceptance Criteria
- [ ] `rules/terraform.md` holds Always-flag rows for the card's *Covers* list. Each row carries a `TF-n`
      id and its `tflint` rule where one exists.
- [ ] Do not flag holds the 0/1 `count` toggle (D11), a lockfile's absence in a non-root module, and a
      lower-bound-only `required_version`.
- [ ] A fixture seeds at least four violations and two decoys.
- [ ] A dogfood run over `modive/infra` and `beatrix/infra/terraform` is recorded, and it names the
      four measured `count = length(…)` sites.

## Wave: DISCUSS / [REF] Out-of-scope

- Running ShellCheck, `tflint` or `yamllint` from `review-code`, or adding them to a pipeline (D13).
- Helm templates, Kustomize overlays and CloudFormation or SAM templates as IaC. `iac.md` states the
  tool-agnostic form; only Terraform gets a tool rule.
- PowerShell, Zsh and Fish.
- Fixing the defects the dogfood runs find in sibling repos. They are recorded here, not filed.

## Wave: DISCUSS / [REF] Definition of Done

1. The research precursor is committed, and each rule cites its section.
2. All four rules exist, each split by checkability, with an ownership paragraph and `paths:` frontmatter.
3. Every Always-flag row carries a stable id and a Preferred form, and a row whose miss changes
   behaviour is marked hazard.
4. `review-code`'s *Language idioms* step names each rule and its files, and `check-rule-reachability.py`
   passes.
5. One self-test fixture per language passes, its expected backlog citing every seeded violation by row
   and excluding every decoy.
6. A dogfood run per slice over production data is recorded, naming the version or saying the skill's
   prose was driven by hand.
7. README's Rules list names all four; the plugin version is bumped per slice.
8. `python3 -m pytest -q`, `scripts/check-invariants.py` and `scripts/check-rule-reachability.py` pass.
9. Each commit message names that `nw-discuss` ran and which of `plugin-dev`, `phil:eos` and
   `/phil:harden-instructions` ran.

## Wave: DISCUSS / [REF] Outcome KPIs

- **Who:** a developer running `/phil:review-code` on a change to Terraform, shell or YAML.
- **Does what:** gets each defect named by row id with its fix.
- **By how much:**
  - every seeded violation named by its right row, across the four fixtures;
  - zero items on the decoys;
  - each dogfood run names at least one real defect, or records that none exists.
- **Measured by:** the four fixtures, plus the dogfood runs over the production data above.
- **Baseline:** no row exists; a review files nothing on these files except a security defect.

## Wave: DISCUSS / [REF] DoR validation

All nine items pass:

1. The job is traceable: a new job in `jobs.yaml`.
2. The persona exists: Quinn, extended.
3. Every AC is testable against a fixture.
4. The KPIs are numeric.
5. Scope is assessed, and the split is approved (D2).
6. The evidence base is decided (D1), with one open measurement named: YAML, in US-02.
7. The structure is decided (D3, D4).
8. The boundaries with existing rules are named (D5, D12).
9. The out-of-scope list exists.

## Wave: DISCUSS / [REF] Slice briefs

- `docs/feature/iac-terraform-bash-yaml-rules/slices/slice-01-bash.md`
- `docs/feature/iac-terraform-bash-yaml-rules/slices/slice-02-yaml.md`
- `docs/feature/iac-terraform-bash-yaml-rules/slices/slice-03-iac.md`
- `docs/feature/iac-terraform-bash-yaml-rules/slices/slice-04-terraform.md`

## Wave: DISCUSS / [REF] Handoff

Order: the research precursor, then slices 01 to 04.

- **Bash goes first.** It has the most production data, and it carries the feature's sharpest risk:
  whether a rule adds anything a linter does not. Settling that early shapes the other three.
- **YAML goes second.** Its gap is unmeasured, and ownership across rules is new.
- **IaC precedes Terraform**, because `terraform.md` points to it.

This answers the card's open questions: D5 settles where YAML stops, and D2 keeps one card.

**Before each slice, check its evidence** (developer's decision, 2026-11-06, after slice 01 shipped on
research one agent wrote and nobody checked). Before writing a rule:

1. Have the research-reviewer agent judge the slice's research section: does each candidate row's cited
   Evidence support it, and which rows rest on one source or on interpretation.
2. Have a web-capable agent fetch each source a row rests on, and mark each quote and linter id
   verified, paraphrased, not found or contradicted. The research reviewer cannot fetch pages.
3. Settle the slice's open gaps that decide a tier, each in a short pass of its own:
   - YAML: which YAML each consumer parses, and how often the defect occurs.
   - IaC: Morris's *Infrastructure as Code*, and the names in Sharma's configuration-smell catalogue.
   - Terraform: which TFLint rules the `recommended` preset enables.
4. Fold every correction into the research document, dated, before the rule cites it.

The 2026-11-06 run covered the whole document and serves slice 02. Slices 03 and 04 rerun steps 1 to 3
over their own sections. Slice 01 shipped before this step existed; the same run checks its sources
after the fact.

## Wave: DISCUSS / [REF] Slice 01 delivered (2026-11-06)

**What landed.** `rules/bash.md`: five Principles; eleven Always-flag rows (SH-1 to SH-11), nine of
them hazards; eleven Advisory bullets; a Do-not-flag list. These are the counts after the evidence check
below. `review-code` matches `.sh`, `.bash` and sh or
bash shebangs, and files a row that has an id at Priority 7, or at Priority 1 where its Hazard column
reads `hazard`. That paragraph serves any language rule with row ids, so slices 02 to 04 reuse it. Fixture 10 seeds nine defects and four decoys. Version 1.34.0.

**Fixture run.** A fresh agent drove this working tree's `SKILL.md` by hand over fixture 10, before
SH-12 was seeded. It filed all ten items then expected, with the right rows, priorities and fixes, and
no decoy. It also found a Priority 6 item in the fixture's own test and a bug in its CI entry point;
both are fixed.

**Dogfood.** The same prose, driven by hand over 15 scripts in five sibling repos, with ShellCheck
0.11.0 at `-S warning` beside it:

- 42 findings, 30 of which ShellCheck missed. The rows whose Linter cell reads none produced 14 of
  those. The learning hypothesis held: the rule adds defects a linter misses.
- Five false positives: two unquoted constants, one deliberate `$(seq …)` split, and two temp files the
  code already handled.
- One defect no row covered: under `errexit`, a health check that returned 1 ended the script at the
  first failing service. ShellCheck stayed silent.

**What the dogfood changed in the rule:**

- SH-12 is new: under `errexit`, a check that reports a result through its status must be called in a
  condition.
- A sourced file is judged under its caller's options.
- A linter stands a row down only at the severity CI reports. SC2086 is `info`, so
  `shellcheck -S warning` never reports it.
- The Preferred forms of SH-2, SH-4 and SH-8 now say where they misfire: `grep` matching nothing, an
  array in POSIX `sh`, an EXIT trap in a sourced file.
- Four Do-not-flag cases and two Advisory bullets are added. The length Advisory now leads with the
  signal that makes a script a program; the run found it weak on five linear scripts.

The full record stays outside the repo, because it names lines in private projects.

**Evidence check (2026-11-06, after the commit).** The developer asked for an independent check of the
research. A reviewer found 17 of its 42 candidate rows over-reaching, and live fetches confirmed 63 of
70 Bash claims. It changed the shipped rule:

- The temp-file trap row and the no-directive library clause moved to Advisory: no source names either
  as a defect.
- `local` in `sh` moved to Advisory: dash, BusyBox ash and ksh run it.
- Two citations were wrong (Google has no "Pipes" section; POSIX puts `local` in § 2.9.1.4).
- Linter cells gained SC2044, SC2206 and SC2292.
- The rule now states its hazard and idiom tests, and the ids were renumbered to run without a gap,
  since none has shipped.

Fixture 10 now expects nine items; the two former rows may come back as Advisory questions.

## Wave: DISCUSS / [REF] Slice 02 delivered (2026-11-06)

**What landed.** `rules/yaml.md`:

- a consumer table naming what six readers make of `no`, `0755`, `1:20` and `3.10`;
- four Principles;
- five Always-flag rows (YAML-1 to YAML-5), all hazards;
- eight Advisory bullets and a Do-not-flag list.

`review-code` gathers every `.yml` and `.yaml` file outside a Helm chart's `templates/`, checks it
against `yaml.md`, and files a row through the language-rows paragraph slice 01 wrote. `ci-pipelines.md`
now points to `yaml.md` and `bash.md`. Fixture 11 seeds five YAML defects, a password `security.md`
owns, and four decoys. Version 1.35.0.

**How the rows follow the evidence check:**

- YAML-1 and YAML-4 apply only where the consumer reads YAML 1.1. Both are Do not flag in a GitHub
  Actions file (D5 as revised).
- A second `<<` key is a duplicate under YAML-5. PyYAML and Psych merge two `<<` keys in the reverse of
  a list's order, and ruamel.yaml refuses them.
- A mapping's own key overriding a merged one turns on intent, so it is Advisory. US-02's "a merge key
  that silently overrides" lands in YAML-5 and in that Advisory bullet.
- Psych reads `08:30` as base 60, which corrects the research Addendum.
- Kubernetes documents an octal `defaultMode`, which is now Do not flag.

**Dogfood: no instance.** The scan covered 400 YAML files: this repo, the sibling repos and the
developer's other repos. It matched every plain scalar and key against each row's pattern and compared
each mapping's keys. It found no instance of any row. Its hits were 16 GitHub `on:` keys and 333
trailing-zero numbers meant as numbers, and the Do-not-flag list now clears both. A row fires only on
a pattern the scan matched, so the scan bounds what a hand-driven review could file.

So the learning hypothesis failed for these repos: YAML's typing defects do not occur in them. The
rows stay Always-flag:

- the card asks for an Always-flag table;
- the tier test is a source that states the defect, and GitLab's docs, Helm's docs and setup-python's
  maintainers each do;
- a row that never fires costs a review nothing, and the scan found no false positive the Do-not-flag
  list leaves standing.

The scan and its per-line output stay outside the repo, because they name lines in private projects.

**Fixture run.** A fresh agent drove this working tree's `SKILL.md` by hand over fixture 11. It filed
all six expected items with the right rows, fixes and priorities, filed the password once as CWE-798,
and flagged no decoy. It added two Advisory questions the fixture allows: no yamllint in CI, and a
workflow nothing validates. Its notes changed one thing: the rule now says a review may read a Helm
template to learn how a value is used, and files nothing in it.

## Wave: DISCUSS / [REF] Slice 03 delivered (2026-11-06)

**Evidence check first.** The Handoff's check ran over § 3 before the rule: a research reviewer, a live
re-fetch (51 of 60 claims verified), and the Morris and Sharma passes. Morris's own posts now back the
copied-environment row and the Principles. Sharma's catalogue is Puppet only and maps to no row. The
research Addendum records each correction.

**What landed.** `rules/iac.md`:

- four Principles, quoting Morris from his own pages;
- seven Always-flag rows (IAC-1 to IAC-7), three of them hazards: committed state, two environments
  in one state, and a root with no lock file;
- Advisory and Do-not-flag lists.

Every row is stated without a tool's syntax, and a test holds it so. `review-code` now gathers `*.tf` on
every run, not only beside a Lambda, and checks it against `iac.md`. `continuous-delivery.md`'s four
bullets point to it. Fixture 12 seeds seven defects in a Terraform module and two roots, beside three
decoys. Version 1.36.0.

**Fixture run.** A fresh agent drove the skill by hand over fixture 12. It filed all seven items with
the right rows, fixes and priorities, and flagged no decoy. Its Priority 6 item was right: the fixture's
test skipped on any `init` failure, and now asserts instead.

**Dogfood.** The rule, driven by hand over three sibling Terraform trees — 11 roots, 10 modules:

- one IAC-3 finding, of low confidence, on a spike root; no other row fired;
- Advisory questions on unreviewed applies (3), missing drift detection (3), large states (2) and an
  imperative DNS script;
- six false positives, now Do-not-flag cases: a bootstrap that creates the state backend, refactor
  records and one environment's own resources under IAC-7, and the module-output bullet, dropped;
- five misses, now Advisory: an input taken from a person's shell or an ignored file at apply time, an
  input one root sets and another leaves to a default, and an upper bound inside a reusable module.
  IAC-6 now covers any value one environment owns, not only account ids.

**The learning hypothesis failed in part.** Several rows needed Terraform knowledge to judge: whether
`~>` sets an upper bound, which files hold state, what a backend location is. `iac.md` alone cannot
supply it, so slice 04's `terraform.md` carries the Terraform spelling of every IAC row, and a review
loads both for a `.tf` file. The rows stay tool-agnostic; the spelling moves, as D12 planned.

The dogfood record stays outside the repo, because it names files in private projects.

## Wave: DISCUSS / [REF] Slice 04 delivered (2026-11-06)

**What landed.** `rules/terraform.md`:

- four Principles;
- six Always-flag rows (TF-1 to TF-6), four of them hazards: `count` over a collection of things with
  identities, an address changed with no `moved` block, an unpinned module source, and a duplicate map
  key;
- a table giving the Terraform spelling of each IAC row, which a review files under the `IAC-n` id;
- Advisory and Do-not-flag lists.

The evidence check moved `required_version`, `fmt`, `sensitive` and deprecated syntax to Advisory, and
dropped unused declarations. It confirmed the duplicate-key hazard against HashiCorp's bulletin and a
local plan. `review-code` checks a `.tf` file against both `iac.md` and `terraform.md`. A row that turns
on a fact no file settles now goes to Advisory. Fixture 13 seeds five defects in a root that meets every
IAC row, beside three decoys. Version 1.37.0.

**Fixture run.** A fresh agent drove the skill by hand over fixture 13. It filed all five items with the
right rows, fixes and priorities, flagged no decoy, and kept the unpinned module off CWE-494. Its one
extra item, an IAC-1 on a root with no state file, came from this rule's spelling table, which now says
such a root is not the row.

**Dogfood.** The rule, driven by hand over 56 `.tf` files in two sibling repos, both of which run
`tflint --recursive` in CI:

- TF-1 fired on all four measured `count = length(…)` sites and on none of the 57 toggles. Only one
  site is a hazard: one counts chunks with no identity, one mirrors another counted resource, and one
  follows the hazard. The row now names elements with an identity of their own, and the other two
  shapes are Do not flag.
- TF-4 found 70 undescribed outputs and variables, 19 carrying a `#` comment instead. The row now says a
  comment is not a description, and files one item per file.
- TF-3, TF-5 and TF-6 found nothing; TFLint's recommended preset already covers TF-3.
- The toggle written `? 0 : 1` is now cleared too. The module-layout Advisory is dropped as noise, and
  the `sensitive` Advisory no longer catches a key's name or ARN.

**The learning hypotheses.** `terraform.md` points to `iac.md` without restating a row: fixture 13 filed
no copied row. D11 held at the toggle (none flagged) and the four sites (all found), and narrowed at the
hazard, which only one of the four carries.

The dogfood record stays outside the repo, because it names files in private projects.
