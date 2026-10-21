# The Speed Pass (`/phil:build-ci --speed`)

Speed is a measured trade: shorten the pipeline's constraint and nothing else, and stop where the next
change buys too little. Read the Speed principle in `${CLAUDE_PLUGIN_ROOT}/rules/ci-pipelines.md`, and
"The Speed Budget" and "Getting Back Under Budget" in `${CLAUDE_PLUGIN_ROOT}/rules/test-architecture.md`,
before measuring. Find the forge and the default branch as `SKILL.md` Step 1's first bullet does.

## 1. Fetch the history

Measure one population at a time, never mixed: the default branch's pipelines, and separately the MR
pipelines the author waits on. On GitHub, measure one workflow at a time, since one commit can start
several.

| | GitLab | GitHub |
|---|---|---|
| Default branch | `glab api "projects/:id/pipelines?ref=<default branch>&source=push&status=success&per_page=20"`, and again with `status=manual` | `gh api "repos/{owner}/{repo}/actions/workflows/<file>/runs?branch=<default branch>&event=push&status=success&per_page=20"` |
| MR | `glab api "projects/:id/pipelines?source=merge_request_event&status=success&per_page=20"` | `gh api "repos/{owner}/{repo}/actions/workflows/<file>/runs?event=pull_request&status=success&per_page=20"` |
| One pipeline's jobs | `glab api "projects/:id/pipelines/<id>/jobs?per_page=100"` | `gh api "repos/{owner}/{repo}/actions/runs/<id>/jobs?per_page=100"` |

GitLab marks a pipeline that holds an unplayed manual job `manual`, not `success`, and a production
deploy is manual; hence the second default-branch query. Write each pipeline's jobs to its own file with
`glab api … > <file>` or `gh api … > <file>`, one call per pipeline, under the session's scratch
directory: one directory per population, each file named by the pipeline's id zero-padded to twelve
digits, so the files sort oldest first. Fetch any empty file again, and fetch the next page of a job list
that returns 100 jobs. A GitLab child pipeline is measured on its own; its trigger job is in `/bridges`.

## 2. Measure

Run, once per population:

```
python3 -I ${CLAUDE_PLUGIN_ROOT}/skills/build-ci/scripts/pipeline-timings.py --forge <gitlab|github> \
  --latest-shape --exclude <each job a person starts> <dir>/*.json
```

Exclude every job the CI file starts by hand — a manual deploy, release or rollback — since its wait is a
person's. `--latest-shape` keeps the pipelines that ran the newest pipeline's jobs. Where path rules make
every MR's jobs differ, measure MR pipelines without it and say how many shapes they came in. Fewer than
five pipelines in a population is too few to rank on: say so, and measure again later.

The script reports each population's median wall clock split into execution, queue wait and other time on
the critical path; the commonest critical path; each job's median duration and queue wait; and the
**runner-up**, the latest job off the path, which caps any saving.

## 3. Name the budget

A pipeline that deploys and tests the deployment is an acceptance stage, with a limit of an hour. Any
other pipeline — every MR pipeline, and a default-branch pipeline that deploys nothing — is a commit
stage: aim under five minutes, limit ten (`test-architecture.md`'s Speed Budget). **Within its budget**
means within its limit. A population within its budget needs no speed pass: say so and stop.

## 4. Queue wait is mostly the runners' time

Where queue wait is more than a fifth of the median wall clock, or exceeds the best candidate's saving
below, report it first. Name what the wait was: runners, an environment approval, a `concurrency` group,
a `resource_group`. On GitLab, a job log's `prepare_executor` section — the runner starting and pulling
the image — counts in the job's duration, not its queue; read it from the log and count it as the
runners' time too. Runner capacity is the fix, or fewer jobs competing for it.

## 5. Find candidates only from jobs on the critical path

Take candidates only from jobs on the critical path in most of the pipelines measured. A job off the path,
however slow, shortens nothing (Goldratt) — until the path is shorter than the runner-up. For each, read
the CI file, the scripts the job calls and its log — GitLab `glab api projects/:id/jobs/<id>/trace`, whose
`section_start` and `section_end` lines time each step; GitHub `gh api repos/{owner}/{repo}/actions/jobs/<id>/logs`
— for where its time goes:

- dependency install or tool setup → a cache keyed on the lockfile, or a prebuilt image — which saves
  nothing while the script's install, such as `npm ci`, deletes what the image holds, so change the
  script with it;
- independent work in one job, other than a test suite → `parallel:` or a matrix;
- a wait on a job whose output it never reads → a shorter `needs:`, but **a wait that gates is no
  candidate**: a deploy after the tests, or any job that must not run unless the other passed;
- work another job already did → the rework pass;
- a test suite past its budget → "Getting Back Under Budget" in `test-architecture.md`, whose ladder puts
  parallelising last; cite it and fix nothing here.

## 6. Estimate each one

- **Saving per pipeline**, in seconds: from the log's step times or the job's measured median, and never
  more than the median wall clock minus the runner-up — unless the change also shortens the runner-up's
  jobs, when the cap is the next chain it leaves untouched. A cache saves only what a restore skips; with no
  evidence of that, leave it unranked and say why.
- **Effort**: S, a few lines in the CI file or the script; M, a day, a new image, or a change that needs
  its own test; L, more.
- **Runner cost**: the runner minutes it adds per pipeline, which `parallel:` and a matrix always do.
- **Evidence** for each figure.

## 7. Rank and draw the line

Weigh effort S = 1, M = 3, L = 8. Score each candidate as its saving's share of the median wall clock,
divided by its weight; rank by score. A score of at least 0.2 is High, at least 0.1 Medium, and below that
Low. **The stopping line** falls before the first Low, or as soon as the pipeline is projected within its
budget, whichever comes first. Savings interact: after the top candidate, the path may move, so re-score
the rest against the new path and the projected wall clock before drawing the line. The weights, the bands, the twenty pipelines and
the floor of five are this skill's own reading of Reinertsen's U-curve, not sourced numbers.

## 8. Ask, change, re-measure

Ask once whether to make the changes above the line. Make them as `SKILL.md` Step 5 writes any job, then
lint as Step 6.3 does. **Report** the population, the budget, the measured split, the critical path with
each job's median duration and queue wait, the runner-up, the ranked candidates with the line drawn, and
the command to re-measure, run only over pipelines after the change's commit, once ten have run. No change
is proved until then.
