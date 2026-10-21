---
paths:
  - "**/.gitlab-ci*"
  - "**/.gitlab/ci/**"
  - "**/.github/workflows/**"
  - "**/Dockerfile*"
---

# CI Pipeline Guide

Guidelines drawn from Fiorella Zampetti et al.'s "An Empirical Characterization of Bad Practices in Continuous Integration" (EMSE 2020) and Carmine Vassallo et al.'s CD-Linter (ESEC/FSE 2020); Titus Winters, Tom Manshreck and Hyrum Wright's *Software Engineering at Google*; Martin Fowler's "Continuous Integration" (2024); Jez Humble and David Farley's *Continuous Delivery*, with SLSA v1.2's artifact verification; Qingzhou Luo et al.'s "An Empirical Analysis of Flaky Tests" (FSE 2014); Michael Meli et al.'s "How Bad Can It Git?" (NDSS 2019); and the GitLab CI/CD and GitHub Actions documentation. Research: `docs/research/ci/ci-pipeline-canonical-sources.md`.

This rule owns **when a pipeline runs, what it runs for a given change, how it fails, and whether it does any work twice**. Neighbouring rules keep what they already own: `continuous-delivery.md` the stages, "build once, deploy many times", trunk-based development and fixing flaky tests; `security.md` mutable-tag actions and images, `pull_request_target`, CI token scope, lockfile installs and credential literals; `test-architecture.md` how long a suite may take. Complement those — do not restate them.

**The reviewer half names defects a pipeline file shows**, each by its `PIPE-n` id. A Zampetti id stands beside it as the citation, never as the finding: BP11, "poor build triggering strategy", backs several rows, and a finding must point to one fix.

---

## Always-flag — objective defects

Name each finding by its `PIPE-n` id and take the fix from the row. Where the row offers a form per forge, copy the row's whole form, then write ` — here: ` and the change for this file's forge.

**A row fires only on what the review read.** A pipeline is more than one file. Where a row's guard can live in a file the review did not read — a remote or template `include:`, a reusable workflow in another repository, a forge setting — raise it as a question instead of an item, and name the unread source. **Where a row's premise, not its guard, sits in an unread setting** — a merge queue, a required status check — list the setting under Not read and file nothing, unless a file the review read states the premise: a comment that says auto-cancel is on makes PIPE-6 fire. A pipeline with no secret-scan job at all is the exception: file a question, since the forge's own secret scanning is a setting the file cannot show. A scan job that a path rule skips is a must-fix item.

### Triggering and gating

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| PIPE-1 | A commit on a branch can start both a branch pipeline and an MR pipeline — GitLab jobs that run for `push` and for `merge_request_event` with no `workflow:rules` choosing one; GitHub `on: [push, pull_request]` with `push` not limited to the default branch | One pipeline per commit: GitLab `workflow:rules` that skip the branch pipeline when `$CI_OPEN_MERGE_REQUESTS` is set; GitHub `push` limited to the default branch | Zampetti BP11 · GitLab `workflow` docs |
| PIPE-2 | A push to the default branch starts no pipeline, or one that skips the test suite for a change outside the docs allow-list — the project's declared list of documentation paths; with none declared, no change is docs-only | Run the test suite on every default-branch commit | Zampetti BP10, BP11 · Fowler 2024 |
| PIPE-3 | `rules:changes` decides whether a job runs in a pipeline that can start with no push event — schedule, tag, web, API, trigger — and neither a `$CI_PIPELINE_SOURCE` check, in the job's rules or `workflow:rules`, nor a `compare_to` makes it compare, so the job runs there whatever changed | Guard on `$CI_PIPELINE_SOURCE` before `changes`, or give `changes` a `compare_to` naming the branch to compare against | Zampetti BP11 · GitLab `rules:changes` docs |
| PIPE-4 | A required check that a path or branch filter can skip — a GitHub workflow whose job is a required status check, with `paths` or `paths-ignore`; a GitLab MR for which no pipeline is created while "Pipelines must succeed" is on | A workflow that always runs and skips inside the job; at least one job in every MR pipeline | Zampetti BP11 · GitHub required-checks docs; GitLab auto-merge docs |
| PIPE-5 | A merge queue in use while the required workflow does not trigger on `merge_group` | Add `merge_group` to the workflow's triggers | Zampetti BP11 · GitHub merge-queue docs |
| PIPE-6 | Cancellation of superseded runs that reaches the default branch — GitHub `concurrency` with `cancel-in-progress: true` in a group main's runs share; GitLab `interruptible: true` on a job that runs on main, with auto-cancel on | Cancel only superseded MR runs: a GitHub group keyed on `github.head_ref \|\| github.run_id`; GitLab `interruptible` only on MR-pipeline jobs | Zampetti BP6, read inversely · Fowler 2024; GitHub `concurrency` docs; GitLab `interruptible` docs |
| PIPE-7 | A manual step on the path from MR to merge, or from merge to the tests — `when: manual` on a test or check job, a check that runs only by `workflow_dispatch` | Run it automatically; keep manual starts for a production release or rollback | Zampetti BP13 · DORA continuous integration |

### Every change

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| PIPE-8 | A secret-scanning job that a path rule skips for docs-only changes, or no secret scan in the MR or default-branch pipeline | Run the secret scan on every pipeline, docs-only changes included | Zampetti BP29 · Meli et al. 2019; GitHub secret-scanning docs |

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
| PIPE-14 | A Dockerfile that copies the whole source tree before installing dependencies, so any source change reinstalls them | Copy the manifest and lockfile, install, then copy the source | Zampetti BP28 · Docker cache docs |

### Order and portability

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| PIPE-15 | A fail-fast check — lint, format, type check, secret scan — that waits for the long test job: a later stage with no `needs: []`, or a `needs:` on the tests | Run fail-fast checks first or beside the tests, never after them | Zampetti BP7 · GitLab pipeline-efficiency docs |
| PIPE-16 | An absolute path into the checkout or the runner's workspace (`/builds/…`, `/home/runner/work/…`) in a job's script | A path relative to the checkout (`$CI_PROJECT_DIR`, `$GITHUB_WORKSPACE`) | Zampetti BM1 |

Checked against Zampetti et al. (EMSE 2020) on 2026-10-21, against Tables 4–10 of the accepted manuscript; GitLab and GitHub documentation as read on 2026-10-21.

**One item per missing protection, filed where the edit goes.** A job with `allow_failure: true` and a bare `retry: 2` is two items, PIPE-9 and PIPE-10: either can be fixed without the other. A row that fires in three jobs needing three edits is three items; one edit that fixes them all — a shared template, a `default:` key, `workflow:rules` — is one item, filed at the lines the edit changes or governs. A defect between a producing and a consuming job is one item, filed at the consumer. The same value at several sites in one file — one image tag named by six jobs — is one item listing every site, since one edit fixes them all. One defect that two rows describe is one item, under the row whose Violation names it more closely.

**Supply-chain rows stay in `security.md`.** A pipeline file is also where `security.md`'s Supply chain and build rows fire — CWE-829 (an action or image pinned by a mutable tag), CWE-494 (fetched code run unchecked), the `pull_request_target` row, CWE-1357 (an install without the lockfile), CWE-427 (a public registry answering for an internal name) — with its privilege row (CWE-250, a CI token or container broader than the task) and its credential-literal row (CWE-798). File those by CWE id, with `security.md`'s fix. Where one row cites two ids, file the id its Cite cell tags to the clause that matches.

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
- **A mutable tag, an unpinned action or a broad token as a `PIPE-n` item.** Those are `security.md`'s rows; file them by CWE id.

---

## Sources and Synthesis

The rows cite the works named at the top: Zampetti et al. for the bad practice each row rests on, CD-Linter for a tolerated failure and a bare retry found mechanically in GitLab files, Fowler and *Software Engineering at Google* for running the suite on every mainline commit, Humble and Farley with SLSA for deploying what was tested, Luo et al. for retry hiding real failures — Zampetti's practitioners rejected Q11 and BP6 as smells, and the rule sides with Luo, Fowler and Google on retry and reads BP6 inversely, for main — Meli et al. for secrets leaking from any file. The vendor documentation supplies each row's GitLab and GitHub form, including two traps: `rules:changes` "always evaluates to true" in a pipeline with no push event, and a required check that a path filter skips stays pending and blocks the merge.

**Three things are this rule's own:** the `PIPE-n` ids and the wording of every row, which the research distilled from the catalogue and the docs rather than copied; the split into Always-flag and Do not flag, which follows `ux.md` and `security.md`; and the readings of the catalogue that place a tolerated test failure under BP8 beside BP16, and a `changes` rule firing on a schedule under BP11. This rule draws on the research document, not on the books in hand. Humble and Farley reach it through Humble's continuousdelivery.com, not the book's text. The research lists what it could not open under Knowledge Gaps, among them the catalogue's online appendix of definitions.

---

## The Mantra

> **One pipeline per commit, a test suite on every mainline commit, a gate no filter can skip, a failure that fails, and the tested artifact — not a rebuild — deployed.**
