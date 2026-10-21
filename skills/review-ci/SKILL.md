---
name: review-ci
description: This skill should be used when the user asks to "review the CI pipeline", "check our .gitlab-ci.yml", "audit the GitHub Actions workflows", "is our pipeline gating correctly", "lint our CI config for bad practices", or runs /phil:review-ci. It reviews GitLab and GitHub pipeline files against rules/ci-pipelines.md and the supply-chain, privilege and credential rows of rules/security.md, names each defect by its row id with the row's fix, leaves the documented false alarms alone, and writes a findings backlog without editing the pipeline.
---

# Review CI

Review a project's CI pipeline against `${CLAUDE_PLUGIN_ROOT}/rules/ci-pipelines.md` and the pipeline
rows of `${CLAUDE_PLUGIN_ROOT}/rules/security.md`, then write a findings backlog. Read
`rules/ci-pipelines.md` on every run, before gathering the pipeline: the rule defines what counts as a
defect, and a review from memory files impressions.

`ci-pipelines.md` owns when a pipeline runs, what it runs, how it fails and whether it rebuilds.
`security.md` owns what a pipeline trusts. From it, apply three things to every gathered file: the
**Supply chain and build** table, the privilege row (CWE-250, CWE-732) and the credential-literal row
(CWE-798). Review against no other rule here. `/phil:review-code` reviews the code the pipeline runs,
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
`${CLAUDE_PLUGIN_ROOT}/rules/security.md` named above. Then collect, from the target:

- **GitLab:** `.gitlab-ci.yml`; every file an `include:` names by `local:` or a bare path, and every
  child pipeline a `trigger: include:` names, followed recursively; and `.gitlab/ci/**`.
- **GitHub:** `.github/workflows/*.{yml,yaml}`, and every local reusable workflow or action a workflow
  names by `uses: ./…`.
- **Images:** every `Dockerfile*` a job builds.
- **Project files a row turns on:** the lockfile and the manifest a cache key or an install names, and
  any script a job calls whose behaviour decides a row — whether a deploy script rebuilds, whether a
  test script swallows its exit code.

With `--changes`, run `git diff HEAD --name-only`, `git diff HEAD~1 --name-only` and
`git ls-files --others --exclude-standard`. With no parent commit, skip the second and say so. Keep the
CI files and Dockerfiles, and gather the whole pipeline each belongs to.

**List each source the review cannot read:** a remote, template, project or component `include:`; a
reusable workflow in another repository; a forge setting, such as branch protection, required checks,
the merge queue, auto-cancel or the runner configuration; and any other forge's pipeline file (`azure-pipelines*`,
`.circleci/**`, `Jenkinsfile`), which the rule's rows do not cover. A row's guard or premise can live
in any of them.

## Step 2: Apply the Rules

Check every gathered file against each Always-flag row of `ci-pipelines.md`, against the `security.md`
rows named above, and against `ci-pipelines.md`'s Do not flag list.

- **Name each finding by its row's id** — `PIPE-n` for a `ci-pipelines.md` row, the CWE id for a
  `security.md` row. Where a `security.md` row cites two ids, take the id its Cite cell tags to the
  clause that matches. A Zampetti id is a citation, never the finding.
- **Copy the row's Preferred form verbatim**, as it renders: a `\|` in the table is `|`. Then, where the row offers a form per forge or this
  pipeline needs one specific change, write ` — here: ` and that change. A paraphrased fix cannot be
  traced to its row.
- **Count as the rule says:** one item per missing protection, filed where the edit goes. One edit
  that fixes several jobs — a template, a `default:` key, `workflow:rules` — is one item; a defect
  between a producing and a consuming job is one item, at the consumer; the same value at
  several sites in one file is one item listing the sites.
- **A row fires only on what the review read.** Where its guard can live in an unread source, file a
  **question** naming that source. Where its premise sits in an unread setting that no file read states, list the setting
  under Not read and file nothing, except a pipeline with no secret-scan job at all, which is a question.
- **Honour Do not flag**, in full.

## Step 3: Write the Backlog

Write `.ci-review.md` in the project root — the one file this review writes. **Edit none of the reviewed
files**, even for a one-token fix: this command reports and does not repair. If the backlog exists, add
the new items under a fresh `Scope:` line, continuing its id sequence; never drop or renumber an item.

```markdown
# CI Review Backlog

Generated: {date}
Scope: {argument}
Standard: rules/ci-pipelines.md; rules/security.md (Supply chain and build, the privilege row, the credential-literal row)
Not read: {each unread include, workflow, setting or other forge's file, or "nothing"}

## Summary

- **Total items**: {count}
- **Must-fix**: {count}
- **Questions**: {count}

## Backlog

### [C001] {row id} — {one-line description}

- **File**: `{file-path}`
- **Lines**: {start}-{end}, one line number, or each site of a value repeated in the file
- **Severity**: must-fix | question
- **Row**: {PIPE-n or CWE-n}
- **Preferred form**: {the row's form, verbatim, optionally followed by " — here: " and this change}
- **Cite**: {rule file} — {row id} · {the row's Cite cell}
- **Status**: pending
```

- Ids run `C001`, `C002`, and so on.
- Sort must-fix before questions; within each, by file, then line.
- Each item is one atomic fix.

## Step 4: Report

1. Totals by severity.
2. The first five must-fix items in backlog order, each in one line.
3. The backlog's path.
4. Every source under "Not read", since a clean result says nothing about them.
5. The files reviewed. A file skipped is not a file passed.

## What Not to Flag

- Anything on `ci-pipelines.md`'s Do not flag list.
- A supply-chain, privilege or credential defect as a `PIPE-n` item. File it under its CWE id.
- Speed. A pipeline without parallel jobs or caches is not defective; speed is a measured trade, and
  this review files none.
- A hypothetical defect in an unread source. Raise the question; do not guess the answer.

**Be precise, not exhaustive.** Eight traceable items beat forty vague ones.

## Self-test (regression gate)

`skills/review-ci/self-test/` holds fixtures that pin this review's behaviour.
`01-pipeline-findings-cite-a-row/` seeds pipeline defects beside look-alikes the Do not flag list
clears, defects one edit fixes across several jobs, and one supply-chain defect filed by CWE id.
`tests/test_ci_pipelines_rule.py` checks that every item a fixture expects takes its id and fix from one
row, and that no look-alike is expected.

Whenever this skill, `commands/review-ci.md` or `rules/ci-pipelines.md` changes, drive each fixture
per `self-test/README.md`. Drive this working tree's `SKILL.md` by hand, since `/phil:review-ci` runs
the released copy. A green repo suite says the fixtures are well-formed, not that a review passes them.
