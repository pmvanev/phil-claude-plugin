---
paths:
  - "**/.gitlab-ci*"
  - "**/.gitlab/ci/**"
  - "**/.github/workflows/**"
  - "**/Dockerfile*"
---

# CI Pipeline Guide

Guidelines drawn from Fiorella Zampetti et al.'s "An Empirical Characterization of Bad Practices in Continuous Integration" (EMSE 2020) and Carmine Vassallo et al.'s CD-Linter (ESEC/FSE 2020); Titus Winters, Tom Manshreck and Hyrum Wright's *Software Engineering at Google*; Martin Fowler's "Continuous Integration" (2024); Jez Humble and David Farley's *Continuous Delivery*, with SLSA v1.2's artifact verification; Atif Memon et al.'s "Taming Google-Scale Continuous Testing" (2017), Mateusz Machalica et al.'s "Predictive Test Selection" (2019) and Milos Gligoric et al.'s Ekstazi (2015) on change-scoped testing; Goran Petrović et al.'s two papers on mutation testing at Google (2018, 2022); Eliyahu Goldratt's *The Goal*, Donald Reinertsen's *The Principles of Product Development Flow* and Taher Ghaleb et al.'s "The Promise and Reality of CI Caching" (2026) on speed; Qingzhou Luo et al.'s "An Empirical Analysis of Flaky Tests" (FSE 2014); Michael Meli et al.'s "How Bad Can It Git?" (NDSS 2019); and the GitLab CI/CD and GitHub Actions documentation. Research: `docs/research/ci/ci-pipeline-canonical-sources.md`.

This rule owns **when a pipeline runs, what it runs for a given change, how it fails, and whether it does any work twice**. Neighbouring rules keep what they already own: `continuous-delivery.md` the stages, "build once, deploy many times", trunk-based development, fixing broken builds and fixing flaky tests; `security.md` mutable-tag actions and images, `pull_request_target`, CI token scope, lockfile installs and credential literals; `test-architecture.md` how long a suite may take. Complement those — do not restate them.

**The two halves divide on checkability.** The reviewer half — Always-flag, Advisory, Do not flag — names defects a pipeline file shows, each by its `PIPE-n` id. A Zampetti id stands beside it as the citation, never as the finding: BP11, "poor build triggering strategy", backs several rows, and a finding must point to one fix. The Principles half is design, and a review that files a principle as a defect lends it unearned authority.

---

## Principles — design, not review criteria

### Core Philosophy

> **"By ensuring we have a build with every push, should we get a failure, we know that the fault lies in that latest push."** — Martin Fowler

A pipeline earns trust by running the work each change needs and failing when that work fails. Run less by default, and name what makes each skip safe.

### Run less, and name the gate

*Software Engineering at Google* splits testing in two: presubmit holds "only fast, reliable" tests, and post-submit runs the rest. Memon et al. found that failing tests sit "closer" to the code they test, which is why change-scoped testing finds most breakages. It misses some by design: Facebook's predictive selector still reports "over 95% of individual test failures", not all of them. **So every skip names the gate that makes it safe.** A change-scoped MR pipeline needs a full run when its own inputs change — the lockfile, the CI configuration, shared test files, the build configuration — because Ekstazi showed that tracking code alone is unsafe. It also needs the full suite on every default-branch commit, and a merge gate so that nothing reaches main without an MR pipeline.

### Mutate the diff, and reset with a full run

Google mutates "only changed code during code review, rather than the entire code base" (Petrović et al.). Every incremental mutation tool admits it drifts: StrykerJS "will not detect any changes you've made in files other than mutated files and test files", and PIT calls its own assumption "unproven". **A scheduled full run is the reset that diff-scoped mutation needs**, not a build that replaces per-change pipelines. Its cadence is the project's choice; shard it so it finishes inside its window.

### Docs-only is an allow-list

Decide that a change is documentation by listing documentation paths, never by listing code paths. A new code directory then runs everything by default — the fail-safe default `security.md` takes from Saltzer and Schroeder. In a repository whose product is prose, the project says which markdown is product.

### Know what starts each job

Most pipeline surprises are jobs that ran when nobody expected it, or never ran. GitLab's `rules:changes` "always evaluates to true" in a pipeline with no push event; a `needs:` on a job the rules skipped stops the pipeline being created; a variable that is set but empty can satisfy a compound rule. **Read each job against each pipeline source** — MR, docs-only MR, main push, docs-only main, schedule, tag, web or API — and compare the result with the intent before the change merges. A linter shows that the file parses, not what its rules skip; GitLab's CI lint API with `dry_run` shows which jobs a pipeline would create.

### The CI file wires; scripts work

Keep triggers, stages and wiring in the CI file, and the work in the repository's own entry-point scripts. A job that calls a script runs the same way on a laptop, so a failure can be reproduced and fixed locally before the next push. `continuous-delivery.md` owns what happens when the build breaks.

### Speed: the constraint first

Goldratt's principle, as it reaches us through secondary sources: "an hour saved at a non-bottleneck is a mirage". Measure job durations and the time jobs wait for a runner, find the critical path, and shorten only that. Rank each change by the time it saves against the effort and runner cost it adds, make the large and medium ones, and stop where the curve flattens or the pipeline is within its budget — Reinertsen's U-curve says an optimum exists. Caching is a bet to measure: it paid off substantially for only about a third of the projects that adopted it (Ghaleb et al. 2026). `test-architecture.md` owns how long the suite itself may take.

### Prefer the documented pattern

Use the forge's documented pattern before designing a new one, and read the decisions the repository already records before reopening them.

---

## The declared policy

Some choices belong to the project, not the rule. GitLab's own pattern keeps branch pipelines, and a small codebase can afford full mutation in every MR. **A project declares its policy in its `CLAUDE.md` or `AGENTS.md`, under a `## CI policy` heading**, one field per bullet:

```markdown
## CI policy

- **Pipelines**: open MR only
- **Docs-only paths**: `docs/**`, `**/*.md`
- **MR**: tests and mutation for changed and affected code
- **Main**: everything except mutation
- **Schedule**: full mutation, weekly, off-hours, sharded
- **Merge**: a passing MR pipeline is required
- **Secret scan**: every pipeline, docs-only included
```

That block is the default policy offered to a project that has none.

| Field | Values | What it says |
|---|---|---|
| **Pipelines** | `open MR only` · `every branch` | Whether a push to a branch with no open MR starts a pipeline. The trigger matrix has no column for that push; `workflow:rules` shows it. |
| **Docs-only paths** | globs | A change whose every path matches one runs the secret scan and nothing else. With none declared, no change is docs-only. |
| **MR** | free text: `tests and mutation for changed and affected code`, `everything` | What tests and mutation an MR pipeline runs. |
| **Main** | free text: `everything except mutation`, `everything` | What a default-branch pipeline runs. |
| **Schedule** | free text | What a scheduled pipeline runs and how often. |
| **Merge** | `a passing MR pipeline is required` | A forge setting; the file cannot show it. |
| **Secret scan** | `every pipeline, docs-only included` | Where the secret scan runs. |

**A policy row fires only against a field the project declared.** With no `## CI policy` block, PIPE-24 is silent and the backlog says no policy was declared. Prose elsewhere that states a choice is not a declaration. Read each field as written; a job whose script skips the work for a source satisfies a field that excludes it. **Where a recorded decision contradicts a declared field** — an ADR, a dated decision in `CLAUDE.md` — raise a question naming both, not a PIPE-24 item: the block may be a pasted default the project never adopted. Where two declarations differ, raise a question and fire no policy row.

---

## Always-flag — objective defects

Name each finding by its `PIPE-n` id and take the fix from the row. Where the row offers a form per forge, copy the row's whole form, then write ` — here: ` and the change for this file's forge.

**A row fires only on what the review read.** A pipeline is more than one file. Where a row's guard can live in a file the review did not read — a remote or template `include:`, a reusable workflow in another repository, a forge setting — raise it as a question instead of an item, and name the unread source. **Where a row's premise, not its guard, sits in an unread setting** — a merge queue, a required status check, a pipeline schedule — list the setting under Not read and file nothing, unless a file the review read states the premise: a comment that says auto-cancel is on makes PIPE-6 fire, and a rule that admits `"schedule"`, or a declared Schedule field, says a schedule runs. A pipeline with no secret-scan job at all is the exception: file a question, since the forge's own secret scanning is a setting the file cannot show. A scan job that a path rule skips is a must-fix item.

### Triggering and gating

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| PIPE-1 | A commit on a branch can start both a branch pipeline and an MR pipeline — GitLab jobs that run for `push` and for `merge_request_event` with no `workflow:rules` choosing one; GitHub `on: [push, pull_request]` with `push` not limited to the default branch | One pipeline per commit: GitLab `workflow:rules` that skip the branch pipeline when `$CI_OPEN_MERGE_REQUESTS` is set; GitHub `push` limited to the default branch | Zampetti BP11 · GitLab `workflow` docs |
| PIPE-2 | A push to the default branch starts no pipeline, or one that runs less than the full test suite for a change outside the docs allow-list — the project's declared list of documentation paths; with none declared, no change is docs-only | Run the full test suite on every default-branch commit | Zampetti BP10, BP11 · Fowler 2024 |
| PIPE-3 | `rules:changes` decides whether a job runs in a pipeline that can start with no push event — schedule, tag, web, API, trigger — and neither a `$CI_PIPELINE_SOURCE` check, in the job's rules or `workflow:rules`, nor a `compare_to` makes it compare, so the job runs there whatever changed | Guard on `$CI_PIPELINE_SOURCE` before `changes`, or give `changes` a `compare_to` naming the branch to compare against | Zampetti BP11 · GitLab `rules:changes` docs |
| PIPE-4 | A required check that a path or branch filter can skip — a GitHub workflow whose job is a required status check, with `paths` or `paths-ignore`; a GitLab MR for which no pipeline is created while "Pipelines must succeed" is on | A workflow that always runs and skips inside the job; at least one job in every MR pipeline | Zampetti BP11 · GitHub required-checks docs; GitLab auto-merge docs |
| PIPE-5 | A merge queue in use while the required workflow does not trigger on `merge_group` | Add `merge_group` to the workflow's triggers | Zampetti BP11 · GitHub merge-queue docs |
| PIPE-6 | Cancellation of superseded runs that reaches the default branch — GitHub `concurrency` with `cancel-in-progress: true` in a group main's runs share; GitLab `interruptible: true` on a job that runs on main, with auto-cancel on and no `auto_cancel: on_new_commit: none` on the default branch's `workflow:rules` entry | Cancel only superseded MR runs: a GitHub group keyed on `github.head_ref \|\| github.run_id`; GitLab `auto_cancel: on_new_commit: none` on the default branch's `workflow:rules` entry, or `interruptible` only on MR-pipeline jobs | Zampetti BP6, read inversely · Fowler 2024; GitHub `concurrency` docs; GitLab `interruptible` and `workflow:rules:auto_cancel` docs |
| PIPE-7 | A manual step on the path from MR to merge, or from merge to the tests — `when: manual` on a test or check job, a check that runs only by `workflow_dispatch` | Run it automatically; keep manual starts for a production release or rollback | Zampetti BP13 · DORA continuous integration |
| PIPE-17 | A deploy job — one with an `environment:`, or whose script deploys — that a scheduled pipeline starts on its own, where neither a declared Schedule field nor a comment says the schedule deploys: GitLab rules or `only` that admit the default branch with no `$CI_PIPELINE_SOURCE` check, where a schedule runs on it; GitHub a deploy job in a workflow with `on: schedule` and no `github.event_name` condition | Keep schedules out of deploy jobs: GitLab `if: $CI_PIPELINE_SOURCE == "schedule"` with `when: never` as the first rule; GitHub `if: github.event_name != 'schedule'` | Zampetti BP11 · GitLab `rules` docs; GitHub `schedule` docs |
| PIPE-18 | A GitLab `needs:` naming a job whose rules can leave it out of a pipeline the needing job runs in, with no `optional: true`, so GitLab refuses to create that pipeline | Mark the edge `needs: [{job: …, optional: true}]`, or give both jobs the same rules so they skip together | GitLab `needs` docs |
| PIPE-19 | A GitLab rule that tests a variable by its bare name inside `&&` or `\|\|` — `$ROLLBACK_TAG && $CI_COMMIT_BRANCH == …` — where a file shows the variable can be set but empty, as a `variables:` default of `""` does: inside a compound rule an empty value counts as true, so `&&` matches and `\|\|` can miss | Compare the value: `$VAR != null && $VAR != ""`; a bare `$VAR` is safe only as the whole expression | GitLab expression evaluator, `lexeme/and.rb` and `statement.rb`, read 2026-10-21; its `rules:if` docs say otherwise |

### Every change

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| PIPE-8 | A secret-scanning job that a path rule skips for docs-only changes, or no secret scan in the MR or default-branch pipeline | Run the secret scan on every pipeline, docs-only changes included | Zampetti BP29 · Meli et al. 2019; GitHub secret-scanning docs |

### Every skip names its gate

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| PIPE-20 | Change-scoped tests — per-job `changes:` lists, an `affected` command, a test-selection step — with no full run forced when the lockfile or manifest, the CI configuration and the scripts that select the tests, shared test files or the build configuration changes, each that the repository has | Add those paths to every scoped job's trigger, or run the full suite when one of them changes | Zampetti Q10 · Nx `affected` docs; Gligoric et al. 2015 |
| PIPE-21 | A check skipped when any changed path is a doc — GitLab `changes:` on doc paths with `when: never`, `except: changes:` — so a change to code and docs together skips it. GitLab's `changes:` matches when any path matches | Skip only when every changed path is in the docs allow-list: GitHub `paths-ignore` with the allow-list, on a workflow that is not a required check; GitLab a step that compares the changed paths with the allow-list and exits early | Zampetti BP11 · GitLab `rules:changes` docs; GitHub workflow-syntax docs |
| PIPE-22 | Every test job chosen by lists of code paths, so that no test job runs when a changed path is one no list names and the docs allow-list does not cover — a change in a new directory runs no test, whatever else runs | Fail closed: run the full suite, or fail a guard job, when a changed path is in no list and outside the docs allow-list | Zampetti Q10 · Saltzer and Schroeder, fail-safe defaults |
| PIPE-23 | Diff-scoped or incremental mutation with no full mutation run on a schedule or on the default branch | Run full mutation on a schedule, sharded with `parallel:` or a matrix, or on the default branch | Zampetti BP10 · StrykerJS incremental docs; PIT incremental-analysis docs |

### Against the declared policy

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| PIPE-24 | A cell of the trigger matrix — or, for the Pipelines field, `workflow:rules` — that departs from the declared policy: a job runs for a source a field excludes, or does not run where a field requires it — mutation on main under `Main: everything except mutation`, a build on a docs-only change, whole-codebase mutation in an MR under `MR: changed and affected code`, a branch with no open MR starting a pipeline under `Pipelines: open MR only` | Change the job's rules so the cell matches the field, or change the declared field | Zampetti BP11, BP26 · the project's `## CI policy` block |

### Failure honesty

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| PIPE-9 | A test, lint or other gating job tolerates its own failure — GitLab `allow_failure: true`, GitHub `continue-on-error: true`, `\|\| true` on the command that runs the check — so the pipeline passes when the job fails | Let the job fail the pipeline; move a job meant only to inform out of the gate and name it so | Zampetti BP16, BP8 · CD-Linter |
| PIPE-10 | Job-wide retry on a test job — GitLab `retry` with neither `when` nor `exit_codes`, or a `when` that includes `script_failure` or `always`; a wrapper that reruns failed tests with no flaky marker | Retry only infrastructure failures (GitLab `when: [runner_system_failure, stuck_or_timeout_failure]`); fix or delete the flaky test | Zampetti Q11, BP17 · Luo et al. 2014; CD-Linter; GitLab `retry` docs |

### Rework

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| PIPE-11 | A deploy or release job rebuilds — compiles, installs build dependencies, runs `docker build` or the build script — instead of using the artifact or image the tested job produced | Deploy what was tested: pass the build output as an artifact, or push the image once and deploy it by digest | Zampetti BP28 · Humble and Farley; SLSA v1.2 |
| PIPE-12 | Build output passed between jobs through the cache — a GitLab `cache:` holding the build directory or package; GitHub `actions/cache` where an artifact belongs | Pass build output as an artifact (`artifacts:`; `upload-artifact` and `download-artifact`); keep the cache for dependencies | Zampetti BP28 · GitLab caching docs |
| PIPE-13 | A dependency cache whose key does not change when the lockfile or dependency manifest changes | Derive the key from the lockfile or manifest (`cache:key:files`; `hashFiles(...)`) | GitLab caching docs; GitHub caching docs |
| PIPE-14 | A Dockerfile that copies the whole source tree, or files built from it, before installing dependencies, so any source change reinstalls them | Copy the manifest and lockfile, install, then copy the source | Zampetti BP28 · Docker cache docs |

### Order and portability

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| PIPE-15 | A fail-fast check — lint, format, type check, secret scan — that waits for the long test job: a later stage with no `needs: []`, or a `needs:` on the tests | Run fail-fast checks first or beside the tests, never after them | Zampetti BP7 · GitLab pipeline-efficiency docs |
| PIPE-16 | An absolute path into the checkout or the runner's workspace (`/builds/…`, `/home/runner/work/…`) in a job's script | A path relative to the checkout (`$CI_PROJECT_DIR`, `$GITHUB_WORKSPACE`) | Zampetti BM1 |

Checked against Zampetti et al. (EMSE 2020) on 2026-10-21, against Tables 4–10 of the accepted manuscript; GitLab and GitHub documentation as read on 2026-10-21; GitLab's expression evaluator at 19.6.0-pre, read on 2026-10-21.

**One item per missing protection, filed where the edit goes.** A job with `allow_failure: true` and a bare `retry: 2` is two items, PIPE-9 and PIPE-10: either can be fixed without the other. A row that fires in three jobs needing three edits is three items; one edit that fixes them all — a shared template, a `default:` key, `workflow:rules` — is one item, filed at the lines the edit changes or governs. A defect between a producing and a consuming job is one item, filed at the consumer. The same value at several sites in one file — one image tag named by six jobs — is one item listing every site, since one edit fixes them all. One defect that two rows describe is one item, under the row whose Violation names it more closely. A field no job carries out — no mutation job at all under an MR field that asks for mutation — is one item, filed at the field.

**Supply-chain rows stay in `security.md`.** A pipeline file is also where `security.md`'s Supply chain and build rows fire — CWE-829 (an action or image pinned by a mutable tag), CWE-494 (fetched code run unchecked), the `pull_request_target` row, CWE-1357 (an install without the lockfile), CWE-427 (a public registry answering for an internal name) — with its privilege row (CWE-250, a CI token or container broader than the task) and its credential-literal row (CWE-798). File those by CWE id, with `security.md`'s fix. Where one row cites two ids, file the id its Cite cell tags to the clause that matches.

---

## Advisory — judgment calls, not hard blocks

A reviewer raises these; the author decides. Each needs a setting, a measurement or an intent the file does not show.

- **The merge gate** — GitLab's "Pipelines must succeed", a GitHub required check — is a forge setting. Ask whether it is on, unless a file states it. A change-scoped MR pipeline is safe only behind it.
- **A test or check job that reads a variable only deploy jobs need.** Protected variables reach only protected branches, so the test behaves differently in the MR from on main.
- **Logic in the CI file** — a `script:` of more than a few lines, or a decision in YAML that a script could make — where an entry-point script would let the job run locally too.
- **A test or gate job with no `timeout`**, where the project's default sits far above the pipeline's budget (Zampetti BP25). The default is a setting.
- **A superseded MR pipeline left running** — no `interruptible` with auto-cancel, no `concurrency` group on the PR ref. Waste, not a defect.
- **Speed, only with job durations in hand:** independent jobs serialised by stages on the critical path; one job whose work `parallel:` or a matrix would split; software installed in every job where a prebuilt image would serve; a cache never measured on the runners that use it, since a runner that runs one job per machine never restores a local cache. A file shows none of these costs.
- **Artifacts kept with no `expire_in`, or `expire_in: never`, by a job that runs in every pipeline.** Retention fills the forge's or the runner's disk.
- **Tests run against a different build target or image from the one deployed** — a `Dockerfile` stage the deploy does not ship.
- **A GitHub schedule at minute 0**, or one on a public repository that may go 60 days without activity, which disables it.
- **Quarantined tests with no cap on count or age.**

---

## Do not flag

- **Cancelling a superseded MR run** — `interruptible` on MR jobs, `cancel-in-progress` on a PR-keyed group. It is the documented idiom, and Zampetti's practitioners rejected BP6 as a smell.
- **A schedule that adds work** — full mutation, a long suite, a dependency audit — while every change still runs its own pipeline. A schedule is a defect only when it replaces per-change pipelines.
- **Retry limited to infrastructure failures**, or to tests individually marked flaky.
- **A manual start for a production release or rollback.** That is continuous delivery, not a gap in it; `continuous-delivery.md` owns release strategy.
- **A job that gates nothing tolerating its own failure** — a manual release, a trend report — where its name or a comment says it does not gate.
- **No parallelism, DAG or cache in a pipeline already inside its time budget.** Speed is a measured trade, not a defect a file shows.
- **`\|\| true` on a cleanup line inside a gating job** — `docker rm`, `pkill` — where the check itself still fails the job.
- **Build and test skipped for a change the docs allow-list covers**, while the secret scan runs and the merge gate still gets a status.
- **A branch pipeline for a branch with no open MR**, in a project that has not declared MR-only pipelines. GitLab's documented switch keeps those; PIPE-1 is the duplicate, not the branch pipeline.
- **Full tests or full mutation in an MR pipeline**, where no policy declares change-scoped MR work. Scoping is a cost measure, not a correctness rule.
- **A `changes:` rule that, in a pipeline with no push event, runs a job the project means to run there** — a hand-run main pipeline that runs everything, where a comment or a test says so. PIPE-3 is the job nobody meant to run.
- **A bare variable as a rule's whole expression** — `if: $ROLLBACK_TAG`. Alone, an empty value counts as false.
- **A mutable tag, an unpinned action or a broad token as a `PIPE-n` item.** Those are `security.md`'s rows; file them by CWE id.

---

## Sources and Synthesis

The rows cite the works named at the top: Zampetti et al. for the bad practice each row rests on, CD-Linter for a tolerated failure and a bare retry found mechanically in GitLab files, Fowler and *Software Engineering at Google* for running the suite on every mainline commit, Humble and Farley with SLSA for deploying what was tested, Luo et al. for retry hiding real failures — Zampetti's practitioners rejected Q11 and BP6 as smells, and the rule sides with Luo, Fowler and Google on retry and reads BP6 inversely, for main — Meli et al. for secrets leaking from any file. The Principles half draws on Google's presubmit split, Memon, Machalica and Gligoric for change-scoped testing and the full run behind it, Petrović and the mutation tools' own documentation for diff-scoped mutation and its drift, and Goldratt, Reinertsen and Ghaleb for speed. The vendor documentation supplies each row's GitLab and GitHub form, including two traps: `rules:changes` "always evaluates to true" in a pipeline with no push event, and a required check that a path filter skips stays pending and blocks the merge.

**What is this rule's own:** the `PIPE-n` ids and the wording of every row, which the research distilled from the catalogue and the docs rather than copied; the split into Principles, Always-flag, Advisory and Do not flag, which follows `ux.md` and `security.md`; the declared policy, without which a project's choice would read as a defect; and five readings. The catalogue places a tolerated test failure under BP8 beside BP16, and a `changes` rule firing on a schedule under BP11. A schedule exists to add work, so a deploy it starts on its own is a defect (PIPE-17). A path list fails closed only behind a guard (PIPE-22), which applies the fail-safe default to test selection. And PIPE-19 rests on GitLab's evaluator, not its documentation: the `rules:if` page says `$VAR1 && !$VAR2` is "True when `VAR1` exists and is not empty", but `And#evaluate` returns Ruby's `left && right`, Ruby counts an empty string as true, and only the whole result is tested for emptiness. A production rollback job ran on every default-branch pipeline that way until its rule compared the value.

This rule draws on the research document, not on the books in hand. Humble and Farley reach it through Humble's continuousdelivery.com; Goldratt and Reinertsen through secondary sources, so the rule cites them by title and quotes Goldratt as attributed. The research lists what it could not open under Knowledge Gaps, among them the catalogue's online appendix of definitions.

---

## The Mantra

> **One pipeline per commit, a test suite on every mainline commit, a gate no filter can skip, a failure that fails, every skip naming its gate, and the tested artifact — not a rebuild — deployed.**
