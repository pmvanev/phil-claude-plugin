---
name: review-ci
description: This skill should be used when the user asks to "review the CI pipeline", "check our .gitlab-ci.yml", "audit the GitHub Actions workflows", "is our pipeline gating correctly", "which jobs run on a schedule", "why wasn't my MR pipeline created", "does anyone hear when main breaks", "check the pipeline against our CI policy", "review our GitLab runner config", "is our runner fleet isolated", or runs /phil:review-ci. It applies rules/ci-pipelines.md, rules/ci-runners.md for runner configuration, and the pipeline rows of rules/security.md, builds a jobs-by-source trigger matrix against the project's declared CI policy, and writes a findings backlog without editing what it reviews.
---

# Review CI

Review a project's CI pipeline against `${CLAUDE_PLUGIN_ROOT}/rules/ci-pipelines.md` and the pipeline
rows of `${CLAUDE_PLUGIN_ROOT}/rules/security.md`, then write a findings backlog. Read
`rules/ci-pipelines.md` on every run, before gathering the pipeline: the rule defines what counts as a
defect, and a review from memory files impressions.

`ci-pipelines.md` owns when a pipeline runs, what it runs, how it fails and whether it rebuilds.
`${CLAUDE_PLUGIN_ROOT}/rules/ci-runners.md` owns how the machines that run the jobs are configured; apply
it whenever the target holds runner configuration. `security.md` owns what a pipeline trusts. From it, apply three things to every gathered file: the
**Supply chain and build** table, the privilege row (CWE-250, CWE-732) and the credential-literal row
(CWE-798). Review against no rule beyond these three. `/phil:review-code` reviews the code the pipeline runs,
and it also applies `security.md` to pipeline files, so the two backlogs can share a CWE item.

## Parse the Argument

| Pattern | Type | Example |
|---------|------|---------|
| `--changes` | Pipelines touched by uncommitted work or the latest commit | `--changes` |
| Is a directory (test this first) | The pipeline rooted there | `.`, `services/api/` |
| Is a file | That file, and the pipeline it belongs to | `.gitlab-ci.yml`, `Dockerfile` |
| No argument | The repository root's pipeline | |

Judge a pipeline whole. Jobs, `workflow:rules`, includes and triggers interact, so a file read alone
misses the defects between files.

## Step 1: Read the Rules, Then Gather the Pipeline

Read `${CLAUDE_PLUGIN_ROOT}/rules/ci-pipelines.md` whole, and the three parts of
`${CLAUDE_PLUGIN_ROOT}/rules/security.md` named above; with runner configuration in the target,
`${CLAUDE_PLUGIN_ROOT}/rules/ci-runners.md` whole as well.

Read the project's declared policy: the `## CI policy` block, in the shape `ci-pipelines.md` gives under
"The declared policy", from the `CLAUDE.md` or `AGENTS.md` nearest the target. Read the project's
recorded decisions that bear on a field — its ADRs, and dated decisions in `CLAUDE.md` about mutation,
schedules or which jobs run — since a decision that contradicts a field turns a departure into a
question.

Then collect, from the target:

- **GitLab:** `.gitlab-ci.yml`; every file an `include:` names by `local:` or a bare path, and every
  child pipeline a `trigger: include:` names, followed recursively; and `.gitlab/ci/**`.
- **GitHub:** `.github/workflows/*.{yml,yaml}`, and every local reusable workflow or action a workflow
  names by `uses: ./…`.
- **Images:** every `Dockerfile*` a job builds.
- **Runner configuration**, when the target holds any: any file with a `[[runners]]` table — GitLab
  Runner's `config.toml` and its templates — and the infrastructure code that provisions the runners' machines — launch templates,
  instance profiles, IAM trust policies, cloud-init, a GitHub runner scale set's values. Read
  `ci-runners.md` whole before judging it. Decide **which platform is live** from the README and the
  recorded decisions: a directory a file calls retired, and that nothing live applies, is history,
  named on the backlog's History line and not reviewed. Where something live still applies it, review it. Record the commit the review read with `git rev-parse HEAD`, and list the live system — the
  runner manager, the cloud account — under Not read (RUN-T1).
- **Project files a row turns on:** the lockfile and the manifest a cache key or an install names, and
  any script a job calls whose behaviour decides a row — whether a deploy script rebuilds, whether a
  test script swallows its exit code, whether a script skips the work for a docs-only change.

With `--changes`, run `git diff HEAD --name-only`, `git diff HEAD~1 --name-only` and
`git ls-files --others --exclude-standard`. With no parent commit, skip the second and say so. Keep the
CI files, Dockerfiles and runner configuration, and gather the whole pipeline or fleet each belongs to.

**List each source the review cannot read:** a remote, template, project or component `include:`; a
reusable workflow in another repository; a forge setting, such as branch protection, required checks,
the merge queue, auto-cancel, pipeline schedules, notification integrations, chat-app subscriptions or
runner settings the target does not hold; a file a job calls that the target does not hold; a script
read only in part, with the part read; and any other forge's
pipeline file (`azure-pipelines*`, `.circleci/**`, `Jenkinsfile`), which the rule's rows do not cover. A
row's guard or premise can live in any of them.

## Step 2: Build the Trigger Matrix

Where the target holds runner configuration and no pipeline file, write no matrix, and say so in its
place.

Write one row per job and one column per pipeline source, in this order: **MR**, **docs-only MR**,
**main push**, **docs-only main**, **schedule**, **tag**, **web or API**.

- **On GitLab** these are `merge_request_event`, a `push` to the default branch, `schedule`, a pipeline
  with `$CI_COMMIT_TAG`, and `web`, `api`, `trigger` or `pipeline`.
- **On GitHub** they are `pull_request` (with `merge_group`, which PIPE-5 checks on its own), a `push`
  to the default branch, `schedule`, a tag `push` or `release`, and `workflow_dispatch` or
  `repository_dispatch`. Name each row `workflow.yml: job`.
- **MR** is a change with a path outside the docs allow-list; **docs-only** is a change whose every path
  matches the declared Docs-only paths. With none declared, write `n/a` in both docs-only columns.
- **Web or API** reads a pipeline started on the default branch, and so does **schedule**, whose
  existence is a forge setting; note where another ref differs.
- **A child pipeline** gets a matrix of its own; its trigger job's cells say whether it exists.

**The first row, `(pipeline)`, says whether the forge creates the pipeline** for each source: `created`,
`—`, or `refused` with the condition, as a `needs:` on a job the rules leave out makes it. Under a `—`,
write `—` in every job's cell. Under `refused`, read each job's cell as if the pipeline were created,
so the matrix still shows what each job's own rules say.

Read a GitLab job's cell in GitLab's order. `workflow:rules` decides whether the pipeline exists; then
the job's rules apply — its own `rules:` if it has them, otherwise those from `extends:`, with each
`!reference` inlined where it stands — or its `only` and `except`. `default:` holds no rules. Read a
GitHub job's cell from the workflow's `on:` filters, then the job's `if:`, then its `needs:`: a needed
job that is skipped skips the jobs after it unless their `if:` says otherwise. Write one of:

- `runs` — the job is created and starts on its own;
- `manual` — the job is created and waits for a person;
- `on failure` — the job is created and runs only when an earlier job fails, as an andon job does;
- `exits early` — the job is created, and the script it calls skips the work for this source, as a
  docs-only check inside the script does;
- `if paths` — whether the job runs turns on which paths the change touches;
- `—` — the job is not created;
- `?` — the answer turns on an unread source or a variable's value, named in a note;
- `n/a` — a docs-only column where no Docs-only paths are declared.

Read three traps as GitLab evaluates them: `changes:` is true in a pipeline with no push event unless a
`compare_to` makes it compare (PIPE-3); a `needs:` on a job the rules leave out stops the pipeline being
created (PIPE-18); and a bare variable inside `&&` or `||` counts an empty value as true (PIPE-19). Take
a variable's value from its `variables:` default, and note any other value that would change a cell.

## Step 3: Apply the Rules

Check every gathered file against each Always-flag row of `ci-pipelines.md`, against the `security.md`
rows named above, against the trigger matrix and the declared policy for PIPE-24, against the Advisory
list, and against `ci-pipelines.md`'s Do not flag list. Check gathered runner configuration against
`ci-runners.md`'s Always-flag rows, its Advisory list and its Do not flag list. A runner setting is
`ci-runners.md`'s: `privileged = true` in a runner's config is RUN-2, not `security.md`'s privilege row,
which keeps a pipeline file's privileges; a credential literal in a committed file is CWE-798 wherever it
sits, and a long-lived key held as a variable or on the host is RUN-6.

- **Name each finding by its row's id** — `PIPE-n` for a `ci-pipelines.md` row, `RUN-n` for a
  `ci-runners.md` row, the CWE id for a `security.md` row. Where a `security.md` row cites two ids, take the id its Cite cell tags to the
  clause that matches; where the cell tags neither, take the id whose CWE definition fits. A Zampetti
  id is a citation, never the finding.
- **Copy the row's Preferred form verbatim**, as it renders: a `\|` in the table is `|`. Then, where the
  row offers a form per forge or this pipeline needs one specific change, write ` — here: ` and that
  change. A paraphrased fix cannot be traced to its row.
- **Count as the rule says:** one item per missing protection, filed where the edit goes. One edit
  that fixes several jobs — a template, a `default:` key, `workflow:rules` — is one item; a defect
  between a producing and a consuming job is one item, at the consumer; the same value at
  several sites in one file is one item listing the sites; a policy field no job carries out is one
  item, at the field.
- **A row fires only on what the review read.** Where its guard can live in an unread source, file a
  **question** naming that source. Where its premise sits in an unread setting that no file read
  states, list the setting under Not read and file nothing, except a pipeline with no secret-scan job
  at all, which is a question.
- **A policy row fires only against a declared field.** With no `## CI policy` block, file no PIPE-24
  item, and write "none declared" on the backlog's Policy line. Where a recorded decision contradicts
  the field, file a question naming both instead of a PIPE-24 item.
- **An Advisory bullet is a question for the author, not a defect.** File it with Severity `advisory`,
  Row `Advisory`, Preferred form `none — the author decides`, and a Cite naming the bullet's bold lead.
  Raise one only where the file shows its subject, and file a defect a row names under that row, not as Advisory.
- **Honour Do not flag**, in full.

## Step 4: Write the Backlog

Write `.ci-review.md` in the project root — the one file this review writes. **Edit none of the reviewed
files**, even for a one-token fix: this command reports and does not repair. If the backlog exists, add
the new items under a fresh `Scope:` line, continuing its id sequence and keeping every earlier item under its id.

Once the items are numbered, mark the matrix. For an item about when a job runs — a Triggering, Every
change, skip-gate or policy row — put `✗` and the item's id on each cell where the defect shows, in the
row of the job whose rule or edge the fix changes, and on each `(pipeline)` cell the item refuses. Leave
the cells of every other job alone, even where a refused pipeline means it never starts. Items about
what a job does — a rebuild, a cache, a CWE — mark no cell.

```markdown
# CI Review Backlog

Generated: {date}
Scope: {argument}
Standard: rules/ci-pipelines.md; rules/ci-runners.md, where runner configuration was read; rules/security.md (Supply chain and build, the privilege row, the credential-literal row)
Read at: {the commit `git rev-parse HEAD` printed, with "and uncommitted changes" where `git diff HEAD` shows any, and the branch where it is not the default branch, since the live fleet most likely runs the default branch's code; "not a git repository" where it fails}
History: {each retired platform's configuration, named and not reviewed, or "none"}
Policy: {each declared field as `Field: value`, or "none declared"}
Not read: {each unread include, workflow, setting, missing or part-read file, or other forge's file, or "nothing"}

## Summary

- **Total items**: {count}
- **Must-fix**: {count}
- **Questions**: {count}
- **Advisory**: {count}

## Trigger matrix

| Job | MR | docs-only MR | main push | docs-only main | schedule | tag | web or API |
|---|---|---|---|---|---|---|---|
| (pipeline) | {created, —, or refused with its condition} | … |
| {job} | {runs, manual, on failure, exits early, if paths, —, ? or n/a, with ✗ C00n where an item marks it} | … |

{a note for each `?` cell, each refused pipeline and each value that would change a cell; for each `on failure` cell, note the jobs whose failure starts it; then: "Read from the rules, not run; GitLab's CI lint API with `dry_run` confirms a cell."}

## Backlog

### [C001] {row id} — {one-line description}

- **File**: `{file-path}`
- **Lines**: {start}-{end}, one line number, or each site of a value repeated in the file
- **Severity**: must-fix | question | advisory
- **Row**: {PIPE-n, RUN-n, CWE-n or Advisory}
- **Preferred form**: {the row's form, verbatim, optionally followed by " — here: " and this change}
- **Cite**: {rule file} — {row id} · {the row's Cite cell}
- **Status**: pending
```

- Ids run `C001`, `C002`, and so on.
- Sort must-fix, then questions, then advisory; within each, by file, then line.
- Each item is one atomic fix.

## Step 5: Report

1. Totals by severity.
2. The first five must-fix items in backlog order, each in one line.
3. Each matrix cell marked `✗`, as `job × source`.
4. The backlog's path.
5. Every source under "Not read", since a clean result says nothing about them.
6. The files reviewed. A file skipped is not a file passed.

## What Not to Flag

- Anything on `ci-pipelines.md`'s or `ci-runners.md`'s Do not flag list.
- A supply-chain, privilege or credential defect as a `PIPE-n` item. File it under its CWE id.
- Speed as a must-fix item. A pipeline without parallel jobs or caches is not defective; raise a speed
  bullet from the Advisory list only with job durations in hand.
- A hypothetical defect in an unread source: raise the question and leave the answer to the author.

**Be precise, not exhaustive.** Eight traceable items beat forty vague ones.

## Self-test (regression gate)

`skills/review-ci/self-test/` holds fixtures that pin this review's behaviour.
`01-pipeline-findings-cite-a-row/` seeds pipeline defects beside look-alikes the Do not flag list
clears, defects one edit fixes across several jobs, and one supply-chain defect filed by CWE id.
`02-trigger-matrix/` declares a policy and seeds a schedule that deploys, a rule on an empty variable,
a `needs:` on a path-skipped job, a check skipped by any doc path and a departure from the policy, each
beside a correct guard; its expected backlog holds the matrix. `03-runner-config/` holds a GitLab
runner fleet's configuration and its infrastructure code, seeding a socket on reused machines, a no-op
`scale_factor`, a deploy pool open to unprotected refs and a bare `retry`, beside a retired platform's
configuration and safe look-alikes. `04-andon/` holds a GitHub project that declares an Andon field,
with one workflow pulling the cord on a red main and one that never does; `05-andon-unnamed/`, the
same project with an Andon field that names no channel, where a missing andon is a question; and
`06-notify/`, a GitLab project under a Notify field, where a job that gates nothing tolerates its own
failure.
`tests/test_ci_pipelines_rule.py` and `tests/test_ci_runners_rule.py` check that every item a fixture
expects takes its id and fix from one row, and that no look-alike is expected.

Whenever this skill, `commands/review-ci.md`, `rules/ci-pipelines.md` or `rules/ci-runners.md` changes, drive each fixture
per `self-test/README.md`. Drive this working tree's `SKILL.md` by hand, since `/phil:review-ci` runs
the released copy. A green repo suite says the fixtures are well-formed, not that a review passes them.
