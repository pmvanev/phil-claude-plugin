# review-ci — Self-Test

`review-ci` writes a backlog, and its failures are silent: a finding filed under the wrong row, a
documented idiom flagged, or a supply-chain defect filed as a pipeline item all look like an ordinary
backlog. These fixtures hand the reviewer a known pipeline and state what its backlog must and must not
contain. Run them whenever `skills/review-ci/SKILL.md`, `commands/review-ci.md`, `rules/ci-pipelines.md`
or `rules/ci-runners.md` changes.

## What the fixtures pin

| Fixture | Situation | Rule under test | Expected outcome |
|---|---|---|---|
| `01-pipeline-findings-cite-a-row/` | twelve pipeline defects and one mutable image tag beside six look-alikes, on both forges, including defects one edit fixes across several jobs | `rules/ci-pipelines.md` Always-flag and Do not flag; `security.md`'s CWE-829 row | thirteen must-fix items, each with its row's id and Preferred form, each shared defect filed once; no look-alike filed |
| `02-trigger-matrix/` | a declared CI policy, and four defects only a job-by-source reading shows — a schedule that deploys, a rule on an empty variable, a `needs:` on a path-skipped job, a check skipped by any doc path — plus one policy departure, each beside a correct guard | the declared policy, the trigger matrix, PIPE-17 to PIPE-24 | five must-fix items and a matrix marking each one's cells; no look-alike filed |
| `03-runner-config/` | a GitLab runner fleet's configuration and Terraform beside a retired platform's, seeding a socket on reused machines, a no-op `scale_factor`, a role-holding pool open to unprotected refs, a bare `retry`, an install that drops the lockfile's hashes and a CA bundle fetched unchecked | `rules/ci-runners.md`, PIPE-10, and `security.md`'s CWE-1357 and CWE-494 rows | six must-fix items by RUN, PIPE and CWE id; the retired fleet and the safe look-alikes unflagged |
| `04-andon/` | a GitHub project declaring an Andon field, with one workflow whose last job pulls the cord on a red main and one with no such job | PIPE-25, and the Do not flag entries for an MR's failure and an andon job's write grant | one must-fix item, PIPE-25 at the workflow with no andon; the andon job read as `on failure`; its `issues: write` grant unflagged |
| `05-andon-unnamed/` | fixture 04's project with the default Andon text, which names no channel, and no andon job | PIPE-25's severity on GitHub | one question, PIPE-25 at `ci.yml`, since a chat app the review cannot read may pull the cord; no must-fix item |
| `06-notify/` | a GitLab project declaring a Notify field, whose `.post` job names the starter on failure while a job that gates nothing tolerates its own failure | PIPE-26, and PIPE-9's Do-not-flag entry | one must-fix item, PIPE-26 at `dependency-drift`; no PIPE-9 item; `tell-author` and its masked token unflagged |
| `07-deploy-what-passed/` | a GitHub API whose production deploy runs after a failed gate and whose hotfix workflow ships any ref with no gate, and a worker whose tests a dispatch input turns off while a `workflow_run` deploy still ships it, built per environment, deployed by a moving tag, with no rollback; beside a rollback workflow, a runtime matrix and a deploy by digest | PIPE-27 to PIPE-31, the rollback Advisory bullet, and the Do not flag entries for a rollback and a runtime matrix | five must-fix items and one Advisory item at `worker-deploy.yml`; `rollback.yml`, the `python-version` matrix and the digest deploy unflagged |

## Layout

Each fixture holds the pipeline under review — the CI files, any `Dockerfile` a job builds, and the
scripts its jobs call — plus:

- `manifest.json` — what the fixture pins, its look-alikes, and how many items it must yield;
- `expected.md` — the hard assertions, and what does not count as a failure;
- `expected-backlog.md` — the items the review must write.

## How to drive it

1. Copy the fixture's project files to a scratch directory — everything except `manifest.json`,
   `expected.md` and `expected-backlog.md`, which a review of `.` would otherwise read — and make the
   copy a git repository with one commit, since the review records the commit it read.
2. In that copy, follow this working tree's `skills/review-ci/SKILL.md` with `.` as the argument.
3. Compare the written `.ci-review.md` with `expected-backlog.md` on the criteria in `expected.md`. Any
   hard assertion that fails blocks the change.

## What runs automatically, and what does not

`tests/test_ci_pipelines_rule.py` and `tests/test_ci_runners_rule.py` check that every expected item
takes its id and fix from one row,
that every Zampetti id the rule cites was checked against the paper, and that each look-alike is in the
fixture and absent from its expected backlog. **Whether a review produces those items is model
judgement.** Step 2 needs an agent or a person, and step 3 needs a judge. A green repo suite says the
fixtures are well-formed, not that the reviewer passes them.
