<!-- markdownlint-disable MD024 -->
# Feature Delta — ci-pipeline-standard

Wave: DISCUSS ✓ (2026-10-21) · Density: lean
Build path: DISCUSS here, then the rules and skills are written directly. The deliverable is prose, so
DESIGN, DISTILL and DELIVER stay out (edd-loop DDD8). Rules are not a plugin component; `plugin-dev`'s
skill, command and validator guidance governs the two new commands and their skills.

This feature adds two standards, `rules/ci-pipelines.md` and `rules/ci-runners.md`, and two commands
that apply them: `/phil:review-ci`, which reports, and `/phil:build-ci`, which designs or changes a
pipeline. It rests on `docs/research/ci/ci-pipeline-canonical-sources.md` (60 sources) and
`docs/research/ci/ci-runner-infrastructure-canonical-sources.md` (53 sources). Tracked on issue 50.

---

## Wave: DISCUSS / [REF] The gap, measured

Measured 2026-10-21 against `main` at `5ba5b04`:

- **No rule says when a pipeline runs or what it runs for a given change.** `continuous-delivery.md`
  names the stages and says "build once, deploy many times" in one bullet. `security.md` owns six
  supply-chain rows. Change-scoped tests, mutation testing in CI, docs-only changes, merge gates,
  scheduled runs, duplicate pipelines, caching and speed appear in no rule.
- **Pipeline speed has no owner.** `test-architecture.md` owns how long a *suite* may take and puts
  parallelising last, because it hides the design signal. Queue wait, runner capacity, caches and
  critical-path jobs are a level above, and no rule covers them.
- **No skill reads a pipeline.** `review-code` gathers `.gitlab-ci*` and `.github/workflows/**`, but only
  so it can check them against `security.md`. `spirit-walk` can explain a pipeline but judges nothing.
- **Runner fleets appear nowhere** in `rules/` or `skills/`.
- **The same guidance gets typed by hand.** Mining 147 sessions (2026-09-18 to 10-21) found the
  MR-only, changed-only and docs-only policy typed into two repos on the same day. The asks to run
  locally, use an entry-point script and own the breakage recurred across 4 to 7 sessions each. The
  user had to correct Claude's CI work at least nine times. Issue 50 lists each finding with its
  session.

## Wave: DISCUSS / [REF] Pre-requisites

- **Research precursors (D1), done:** `a2248c1` (pipelines) and `5ba5b04` (runners), each `@infrastructure`
  and committed before any slice.
- **Verification precursors, not done** — each one closes before the slice that cites it ships:
  - **V1 (slice 01):** every Zampetti id the pipeline rule cites is checked against the paper's tables.
    The research read the tables but not the online appendix (its Gap 2).
  - **V2 (slice 05):** every CWE id the runner rule cites is opened on cwe.mitre.org. The research's
    CWE fits are unverified candidates (its Gap 1), and `tests/test_security_rule.py` sets the bar.
  - **V3 (slice 05):** taskscaler's `capacity.go` is diffed at the revision GitLab Runner v19.5.0
    pins. The research confirmed it on `main` only.
- **Production data:** three GitLab pipelines — `modive` (889 lines), `beatrix` (515) and `runbooks`
  (640) — and the AWS runner Terraform in `runbooks/runners/`. All are on this machine and none is in this repo.
- **Existing artifacts touched:** `rules/ci-pipelines.md` and `rules/ci-runners.md` (new);
  `skills/review-ci/` and `skills/build-ci/` (new); `commands/review-ci.md` and `commands/build-ci.md`
  (new); one cross-reference line each in `continuous-delivery.md`, `test-architecture.md` and
  `security.md`; `README.md`; `.claude-plugin/plugin.json`; `docs/product/jobs.yaml`;
  `docs/product/personas/quinn-codebase-steward.yaml`.

## Wave: DISCUSS / [REF] Persona ID

**`quinn-codebase-steward`, extended with a CI facet — no new persona.** Quinn owns the health of a
codebase, and the pipeline is the codebase's immune system. The runner fleet is the same person's
infrastructure: in every mined session the person who wrote the pipeline also ran the runners.

**Rejected: a "platform engineer" persona.** This repo earns a new persona only for a position orthogonal
to every domain, as `ari-interrupted-decider` is. Writing a pipeline and tuning the machines it runs on are
two jobs of one position.

## Wave: DISCUSS / [REF] JTBD one-liners

**New job: `shape-a-pipeline-to-the-change`.**

> When I set up or change a project's CI, I want each change to run exactly the checks it needs —
> gated so nothing merges untested, built once, and fast where the time actually goes — so I can stop
> retyping the same pipeline policy into every project and stop learning from a red main pipeline
> that a rule was wrong.

**New job: `run-a-runner-fleet-knowingly`.**

> When I size, tune or ask about the runner fleet, I want each setting judged by the isolation, wait
> and cost it really buys, and each answer drawn from what is live, so I can trade boot wait against
> isolation and money on purpose instead of on a misremembered number.

These are two jobs, not one job with two facets. They have different files, different sources, and
different costs of a miss: a pipeline miss wastes a day, while a fleet miss lets one job tamper with
the next. Both are recorded in `docs/product/jobs.yaml`.

## Wave: DISCUSS / [REF] Locked decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D1 | **Research is a precursor**, done in two documents. | The `security-standards-rule` bar: "empirical design over speculation". |
| D2 | **Two rules: `rules/ci-pipelines.md` for pipeline shape and `rules/ci-runners.md` for runner fleets.** Each points at the other. | User decision, 2026-10-21. Different readers, different files and different sources. Each half needs a reviewer half of its own, and one file would be long. |
| D3 | **Each rule splits on checkability**: a Principles half from books and papers, and a reviewer half shaped like `ux.md` and `security.md`: **Always-flag**, **Advisory**, **Do not flag**. | The same split `security.md` D3 made, for the same reason: a principle filed as a defect borrows authority it has not earned. |
| D4 | **Rows carry the rule's own stable ids — `PIPE-n` and `RUN-n` — and cite a source id beside them.** Pipeline rows cite Zampetti et al.'s bad-practice id (e.g. BP11). Runner rows cite the OWASP CI/CD id and SLSA requirement, plus a CWE id once V2 verifies it. A retired id is never reused. | Zampetti's ids are stable and peer-reviewed, but not unique per row: BP11 backs four candidate rows. A finding needs a name that points to exactly one fix. |
| D5 | **Rows that are also security defects stay in `security.md`.** A pipeline or runner row that overlaps one cites the CWE row and does not restate its fix. | `security.md` D8's ownership pattern. Mutable tags, `pull_request_target`, token scope, lockfile installs and credential literals are already rows there. |
| D6 | **A project's pipeline policy is declared, not assumed.** A block in its `CLAUDE.md` names it: MR-only pipelines, the docs allow-list, where mutation runs, and the schedule. Rows that depend on policy fire only against a declared policy. `/phil:build-ci` proposes the user's policy as the default and writes the block. | The research found "MR-only" to be a project choice: GitLab's own pattern keeps branch pipelines. A reviewer that flags a choice as a defect trains the reader to skip it. |
| D7 | **The default policy is the user's:** pipelines only for an open MR; the MR runs tests and mutation for changed or affected code only; a docs-only change runs secret scanning alone, on the MR and on main; main runs everything but mutation; a weekly off-hours schedule runs full mutation, sharded; merging requires a passing MR pipeline. | Issue 50's targets. All five hold against the sources (pipeline research, "Candidate rows tested against sources"). |
| D8 | **Every skip names the gate that makes it safe, and a skip without one is Always-flag.** Change-scoped tests need a full run forced by the lockfile, CI config, shared test files and build config, plus a full run on main. MR-only mutation needs the merge gate and a scheduled full run. | The mined failure: mutation ran only in MR pipelines, work merged to main directly, and mutation ran nowhere for two days. Memon, Machalica and every incremental-mutation tool's docs say the same. |
| D9 | **"Docs-only" is an allow-list of doc paths, never a deny-list of code paths.** | A new code directory must not silently skip tests. Fail-safe defaults; `security.md`'s Saltzer and Schroeder principle. |
| D10 | **Both commands produce a trigger matrix**: each job against each pipeline source (MR, docs-only MR, main push, docs-only main, schedule, tag, web or API), read from the rules and checked against the declared policy. | Most mined struggles were jobs that ran when nobody expected it. `changes:` evaluates true on schedules, `rollback-prod` fired on an empty variable, and a `needs:` pointed at a skipped job. GitLab's CI lint cannot show what a rule skips. |
| D11 | **Speed is a procedure in `/phil:build-ci`, not Always-flag rows.** Measure job durations *and* queue wait. Find the critical path. Rank changes by estimated saving per unit of effort. Make the high- and medium-payoff ones. Stop at the inflection point, then measure again. `test-architecture.md` keeps the suite's own clock; each rule points at the other. | Zampetti's practitioners judged "no parallelism" not to be a smell. Ghaleb found caching pays for a third of adopters. Goldratt: "an hour saved at a non-bottleneck is a mirage". Speed is a judgment made with numbers, which a file cannot show. |
| D12 | **The rework pass is both rows and a procedure.** Always-flag covers a deploy that rebuilds, build output passed through the cache, and a Dockerfile that defeats its own layer cache. The procedure lists each artifact's producers, and anything produced twice is a finding. | Humble and Farley, with SLSA's digest check as the checkable form. `continuous-delivery.md`'s "build once" bullet is cited, not restated. |
| D13 | **Each job calls the repo's own entry-point script.** The CI file holds triggers, stages and wiring. `/phil:build-ci` writes jobs that way, and inline logic past a few lines is Advisory. | Asked in four mined sessions. It is what makes "reproduce the failure locally before the next push" possible. |
| D14 | **`/phil:review-ci` is read-only and writes one backlog file.** It declares `mutates: true` because it writes that file, as `ux-review` does. `/phil:build-ci` edits files and may read the forge for durations. | CLAUDE.md: set `mutates:` by the grant. A review that edits cannot be run on someone else's pipeline. |
| D15 | **A forge setting is Advisory to a file-only review.** The merge gate, protected variables and branch protection don't show in the file. `/phil:build-ci` reads them through the forge and asks before writing one. | The file cannot show them. A mined session changed main's branch protection without being asked. |
| D16 | **Fleet answers are rows** (`RUN-T1`: name what you read; `RUN-T2`: never answer from a retired platform's docs). `RUN-T2` says it is the rule's own extension of the drift literature. | The research labels it as its own. `security.md` D11's "state what is the rule's own". |
| D17 | **Complement, do not restate.** `continuous-delivery.md` gains one line: an MR-gated branch counts as trunk-based while it lives about two days, review wait included. `test-architecture.md` and `security.md` each gain a pointer. | The ownership-paragraph pattern. It resolves both scope conflicts on issue 50 without contradicting either rule. |
| D18 | **Vendor-neutral rows, with GitLab and GitHub forms in the Preferred-form column.** | Every mined pipeline is GitLab. The plugin ships to consumers on either forge. |

## Wave: DISCUSS / [REF] Driving ports

- **`/phil:review-ci <path | --changes>`** — applies both rules' Always-flag and Do-not-flag lists and
  writes the trigger matrix and a ranked findings backlog to `.ci-review.md`.
- **`/phil:build-ci [--speed | --rework]`** — declares the policy, maps each class of change to its jobs,
  writes or edits the pipeline, prints the trigger matrix, and lints. `--speed` and `--rework` run one
  pass alone.
- **The rule files** — read by any skill that names them, and by a consumer who copies them into
  `.claude/rules/`, where their `paths:` frontmatter loads them for CI and runner files.

## Wave: DISCUSS / [REF] WS strategy

**A — none.** Additive and brownfield: new files, plus one line in each of three rules. Slice 01 is the
thinnest end-to-end value: a review that names a real pipeline's defects by row id.

## Wave: DISCUSS / [REF] Scope Assessment: PASS

Five slices, two precursors done, three verification precursors. One context: the rules and review
system. Of the oversized signals, only "independent outcomes that could ship separately" fires,
because runners could ship alone. One signal is not oversized. Splitting would also mean a second card
(the user asked for one). Each slice runs against one of three real pipelines or the real runner Terraform.

## Wave: DISCUSS / [REF] User stories

Stories trace to `job_id: shape-a-pipeline-to-the-change` (US-01 to US-04) and
`job_id: run-a-runner-fleet-knowingly` (US-05).

### US-01 — `review-ci` flags pipeline defects by row id *(walking-skeleton slice)*

**Problem.** Quinn's MR pipeline lets a scheduled run deploy, and `allow_failure` sits on a test job.
Nothing reads the CI file for defects, so Quinn learns about each one from a red main pipeline.

**Solution.** `rules/ci-pipelines.md` with its Always-flag rows (research P1–P21, renumbered `PIPE-n`)
and Do-not-flag list; `/phil:review-ci` applies them.

#### Elevator Pitch
Before: a pipeline's defects surface only when a pipeline misbehaves.
After: run `/phil:review-ci .gitlab-ci.yml` → sees `.ci-review.md` with items such as `PIPE-5 (BP8):
rules:changes skips lint on a schedule — guard with CI_PIPELINE_SOURCE`, and no item for an
`interruptible` MR job.
Decision enabled: which pipeline defects to fix before the next merge.

#### Acceptance Criteria
- [ ] `rules/ci-pipelines.md` exists with an Always-flag table. Each row names the defect, its `PIPE-n`
      id, its Zampetti id (checked under V1) and a preferred form in GitLab and GitHub syntax.
- [ ] A Do-not-flag list covers at least: aborting a superseded MR pipeline, a schedule that adds work
      rather than replacing per-change runs, retry limited to infrastructure failures, a manual
      production approval, and no parallelism in a pipeline inside its budget. Full mutation in a
      small codebase's MR moves to US-02 with the other mutation rows.
- [ ] `/phil:review-ci` names each finding by row id, takes the fix from the row, and honours Do not
      flag.
- [ ] A self-test fixture seeds at least eight Always-flag defects beside five look-alikes. A test
      pins every `PIPE-n` id to its row, and pins each expected item's id and fix.
- [ ] Dogfood: one run over `modive/.gitlab-ci.yml` is recorded here, with every finding and every
      place the rule made the reviewer hesitate.

### US-02 — Declared policy and the trigger matrix

**Problem.** "Only run pipelines for an open MR" holds in one project and not another. A reviewer
can't tell a defect from a choice, and nobody can see which sources start which jobs.

**Solution.** The policy block (D6, D7), the Principles and Advisory halves, the skip-needs-a-gate rows
(D8, D9), and the trigger matrix (D10) in `/phil:review-ci`.

#### Elevator Pitch
Before: whether a schedule, a docs-only change or a push to main runs a job takes working out by hand.
After: run `/phil:review-ci .gitlab-ci.yml` → sees a jobs-by-sources matrix, with each cell that departs
from the declared policy marked, and an item such as `PIPE-9: mutation runs only on MRs and no schedule
runs it in full`.
Decision enabled: whether the pipeline does what the project's policy says.

#### Acceptance Criteria
- [ ] The rule defines the policy block and its fields. Policy rows fire only against a declared field.
- [ ] The matrix covers the seven sources in D10 and marks every job that runs unexpectedly or never runs.
- [ ] A fixture seeds a schedule that would deploy, a rule on an empty variable, a `needs:` on a
      path-skipped job and a docs deny-list. The expected matrix and backlog catch all four.
- [ ] Dogfood over `beatrix/.gitlab-ci.yml`, whose policy the user typed on 2026-10-21.

### US-03 — `build-ci` shapes a pipeline to the declared policy

**Problem.** Quinn retypes the same policy into each new project, and Claude re-derives it, sometimes
wrongly.

**Solution.** `/phil:build-ci` asks for or confirms the policy, writes the `CLAUDE.md` block, maps
change classes to jobs, and writes jobs as entry-point script calls (D13). It prints the trigger matrix
and lints. Through the forge it reads the merge gate and asks before changing it (D15).

#### Elevator Pitch
Before: setting a project's CI to the policy takes a session of corrections.
After: run `/phil:build-ci` → sees the policy block written, the pipeline diff, the trigger matrix
matching the policy in every cell, and the question "require a passing MR pipeline to merge?".
Decision enabled: whether to merge the new pipeline.

#### Acceptance Criteria
- [ ] The command writes no forge setting without an answer, and declares `mutates: true`.
- [ ] Every job it writes calls a script the repo can run locally.
- [ ] A fixture project with no CI gets a pipeline whose matrix matches D7 in every cell.
- [ ] Dogfood on one real repo, with the matrix recorded.

### US-04 — Speed and rework passes

**Problem.** Speed-up work goes to whatever looks slow. In one mined case a 4.7-minute queue wait
outweighed every job, and a package was built twice.

**Solution.** `/phil:build-ci --speed` (D11) and `--rework` (D12).

#### Elevator Pitch
Before: no one knows which job or which wait owns the pipeline's time.
After: run `/phil:build-ci --speed` → sees the critical path with each job's median duration and queue
wait from the last N pipelines, and candidate changes ranked by saving per unit of effort, with a line
marking where the pass stops.
Decision enabled: which speed-ups to make, and when to stop.

#### Acceptance Criteria
- [ ] The pass measures from the forge's pipeline history and reports queue wait separately.
- [ ] Each candidate carries an estimated saving, an effort class and the evidence behind both. The
      pass names its stopping point.
- [ ] `--rework` lists each artifact's producing jobs and flags any artifact built twice.
- [ ] Dogfood: one `--speed` run over a real pipeline's history is recorded.

### US-05 — Runner rule and review of runner config

**Problem.** A fleet runs `scale_factor = 1.0`, which the autoscaler code makes a no-op, and its owner
cannot tell what reusing a VM would cost in isolation.

**Solution.** `rules/ci-runners.md` (RUN-1 to RUN-13, RUN-T1, RUN-T2), applied by `/phil:review-ci`
when it reads runner config.

#### Elevator Pitch
Before: a runner question gets an answer from memory or from a retired platform's docs.
After: run `/phil:review-ci runners/` → sees items such as `RUN-12: scale_factor 1.0 never changes the
instance count — set it above 1 or remove it`, and an Advisory on VM reuse that names the trust class.
Decision enabled: which runner settings to change, and whether reuse is safe on each pool.

#### Acceptance Criteria
- [ ] V2 and V3 are closed before the rule ships.
- [ ] A fixture seeds a socket mount on a reused VM, a no-op scale factor, an untagged deploy pool and
      `retry` with no `when`, beside safe look-alikes.
- [ ] Dogfood over `runbooks/runners/`; the `scale_factor` finding appears.

## Wave: DISCUSS / [REF] Definition of Done

1. Both rules shipped, with each source cited by title and a section on what is the rule's own.
2. Both commands shipped, with `mutates:` declared and `scripts/check-readonly-commands.py` green.
3. Every rule row pinned by a test; every fixture fails without the row it guards, watched once.
4. `python3 -m pytest -q` and `scripts/check-invariants.py` green.
5. `plugin-dev:skill-reviewer` and `plugin-dev:plugin-validator` run, and their findings fixed.
6. Prose edited to `rules/writing.md` with `phil:eos`.
7. README and plugin version updated.
8. Each slice's dogfood recorded here, naming whether it drove the working tree's prose or a released
   version.
9. Issue 50's targets each either encoded with a fixture or struck through with the reason.

## Wave: DISCUSS / [REF] Out of scope

- Deployment strategy, release mechanics and environments — `continuous-delivery.md`.
- Supply-chain and token rows — `security.md`.
- Suite-level test speed — `test-architecture.md`.
- A CI linter script or rule evaluator in code. The matrix is read, not computed, until a defect is found
  twice (CLAUDE.md).
- CI for this repo. It has none, and its gate is `pytest` at commit time.
- IaC review beyond runner configuration.

## Wave: DISCUSS / [REF] Outcome KPIs

| KPI | Target | Measured by |
|-----|--------|-------------|
| Seeded pipeline defects found, decoys left alone | 100% of defects, 0 decoys, across the slice 01 and 02 fixtures | Fixture grading script |
| Trigger-matrix cells matching the declared policy after `/phil:build-ci` | 100% on the fixture project | Fixture grading |
| CI corrections the user types in a session that uses `/phil:build-ci` | Fewer than the mined baseline of nine corrections across 147 sessions | Re-mine sessions 30 days after release |
| Runner findings confirmed on the real fleet | The `scale_factor` finding, plus every RUN row that fires, confirmed against live config | Slice 05 dogfood |

## Wave: DISCUSS / [REF] Slice 01 delivered and dogfooded (2026-10-21)

**V1 closed.** Every Zampetti id the rule cites was checked against Tables 4–10 and the body text of
the accepted manuscript. The check moved P5 from BP8 to BP11. BP8 means skipping a phase to make a
failing build pass, which fits a tolerated test failure, so PIPE-9 cites it beside BP16. The timeout
row (research P21) moved to Advisory for slice 02, because it fired on nearly every job and the project
timeout is a setting.

**Fixture 01, two blind drives.** Each was a fresh agent that read only this working tree's skill, the
two rules and the project copy.
- *Drive 1* filed all thirteen and no look-alike. It also filed PIPE-12 twice (producer and consumer),
  a PIPE-5 question with no premise in the files, and CWE-250 for a `Dockerfile` with no `USER`. These
  led to the counting rule, the premise rule and `USER node` in the fixture. `plugin-dev:skill-reviewer`
  ("needs improvement") and `plugin-dev:plugin-validator` (pass) ran over the same draft. Their findings
  were fixed before drive 2: false fires in PIPE-8, -9, -13, -15 and -16; the reserved job name `image`;
  a pointer to the unbuilt `/phil:build-ci`; and an inconsistent `security.md` scope.
- *Drive 2* filed exactly the thirteen expected items, no question and no look-alike, with PIPE-1,
  PIPE-12 and PIPE-13 one item each.

**Dogfood: modive at `9c10d61` (origin/main, 2026-10-21), 1,014 lines plus a child pipeline.** A fresh
agent followed the working tree's skill in a scratch clone, about ten minutes over seventeen files, and
filed 28 must-fix items:
- 20 CWE-829 items (images pinned by tag), 4 CWE-494 (tools fetched at run time outside the lockfile),
  2 PIPE-3, 1 PIPE-15 and 1 PIPE-14.
- After drafting, it read modive's `CLAUDE.md`, `renovate.json` and ADR-012. One recorded decision
  changed a fix (the `!= "merge_request_event"` anchor exists for gitlab-ci-local), and none removed a
  finding.

**What it taught the rule, each fixed and pinned before this commit:**
- *A stated premise fires.* Modive's own comment says a newer push cancels older checks, and
  `default: interruptible: true` reaches main. The premise rule had told the reviewer to file nothing,
  hiding the one Triggering defect the user named in the mined sessions. A row now fires when a file
  the review read states its premise.
- *One value, one item.* Six of the 20 CWE-829 items were the same `node:24-alpine` string. The same
  value at several sites in one file is now one item listing the sites.
- *`compare_to` guards a no-push pipeline.* GitLab's reference says so ("To cover these cases, use
  `rules: changes: compare_to`"). An earlier rewording of PIPE-3 had dropped it.

**Defects seen that no row covers, kept for slice 02 and not applied:** `--no-hashes` exports that
install the lockfile's versions unverified; tests run against a different `Dockerfile` target than the
one deployed; a deploy that ships an existing digest rather than the archive this pipeline scanned.

**Not verified:** `/phil:review-ci` itself. It runs the installed copy, which is 1.2.23 until the plugin
updates. No drive ran after the dogfood fixes; they change wording that fixture 01 does not exercise.

## Wave: DISCUSS / [REF] Slice 02 delivered and dogfooded (2026-10-21)

**What landed.** `ci-pipelines.md` gained its Principles half, the declared policy (D6, D7) with its
seven fields, eight Always-flag rows (PIPE-17 to PIPE-24) and an Advisory list. PIPE-2 now asks for the
full suite on main. `review-ci` reads the `## CI policy` block and the project's recorded decisions,
writes a jobs-by-source trigger matrix (D10) whose first row says whether the forge creates the
pipeline, and files Advisory bullets as questions. `test-architecture.md` points at the pipeline rule
for pipeline speed (D11, D17).

**The empty-variable rule, root cause.** Slice 01 left it open. beatrix's commit `6424dce9` recorded
that `$ROLLBACK_TAG && …` matched with the tag empty while a bare `$ROLLBACK_TAG` did not. GitLab's
evaluator source explains it: `And#evaluate` returns Ruby's `left && right`, Ruby counts `""` as true,
and `Statement#truthful?` tests only the whole result with `.present?`. The `rules:if` docs say the
opposite. `!=` makes an undefined variable match `!= ""`, so PIPE-19's form compares with both `null`
and `""`.

**Fixture 02, three blind drives.**
- *Drive 1* filed the five expected items and no look-alike. It marked fourteen cells for one refused
  pipeline, and it found the skill's speed rule contradicting the rule's speed Advisory bullets.
  `plugin-dev:skill-reviewer` ("needs improvement") and `plugin-dev:plugin-validator` (pass, with
  warnings) found the same two and more:
  - a refused pipeline had no cell value;
  - `exits early` had no stated meaning;
  - the skill misstated how GitLab joins inherited rules;
  - PIPE-17 had no exception for a declared scheduled deploy;
  - three decoys could draw a correct item: gitleaks skipped on rollback, full-run lists missing the
    scripts and build config, and `--incremental` mutation with no baseline, which runs whole;
  - a nested `CLAUDE.md` in the fixture would load as this repo's context. It is now `AGENTS.md`.
- *Drive 2* filed exactly the five, and every cell the hard assertions name, except the tag column. The
  skill told it to read job cells "as if the pipeline were created" even where no pipeline exists.
- *Drive 3*, after the matrix wording was fixed, filed exactly the five, with an all-`—` tag column, and
  met every hard assertion. It also raised one Advisory question (no `interruptible` on MR jobs), which
  `expected.md` allows. It read PIPE-20's "scripts its jobs call" as possibly covering deploy scripts.
  The row now says "the scripts that select the tests", a narrowing not re-driven.

**Dogfood: beatrix at `4243b338` (origin/main, 2026-10-21), 628 lines.** It ran with the default
policy block appended to a scratch clone's `CLAUDE.md`, since beatrix states its policy only in prose.
A fresh agent followed the working tree's skill in about ten minutes over twelve files, and filed 9
must-fix items, 1 question and 2 Advisory:
- *Real:* two PIPE-11s, the sharpest of them `deploy-prod`. It rebuilds the SPA, the Lambda zip and the
  extension at the press, so production ships a build `dev-parity` never proved. Also PIPE-17:
  `dev-parity`, which deploys dev and wipes its data, runs in any schedule on main. Images are pinned
  by tag (CWE-829) and `uvx` resolves the audit tools' dependencies unhashed (CWE-494). And a question
  whether every `aws-linux` job gets the host's Docker socket (CWE-250).
- *What it taught the rule, each fixed and pinned:*
  - A pasted default can contradict a recorded decision. beatrix records mutation on demand only,
    after three VM crashes (2026-10-19), so two PIPE-24 items existed only because of the paste. A
    recorded decision that contradicts a field now makes a question.
  - PIPE-3 was noise where a hand-run main pipeline is meant to run everything and a test pins it. That
    is now Do not flag.
  - PIPE-24 needed a home for a field no job carries out. It is one item, filed at the field.
  - PIPE-22 stayed silent because two non-test jobs run on every change. It now asks whether a test
    job runs.
  - Where a `security.md` Cite cell tags neither id, the review takes the id whose definition fits. A
    script read in part goes under Not read.

**Seen, no row of this rule covers, for `security.md`:** a CA bundle fetched at build time with no
checksum; a corepack-fetched package manager with no hash; `--no-hashes` exports, carried from slice 01.
Each is a trust question, so each belongs to `security.md`'s Supply chain and build table, not here.

**Not verified:** `/phil:review-ci` itself, which runs the installed copy (1.2.23). beatrix was not
re-driven after the fixes.
