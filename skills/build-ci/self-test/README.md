# build-ci — Self-Test

`build-ci` writes a pipeline, and a pipeline that looks right can still run the wrong jobs for some
source, or none. These fixtures hand the build a known project and state the trigger matrix it must
reach and what it must never do. Run them whenever `skills/build-ci/SKILL.md`, `commands/build-ci.md`
or `rules/ci-pipelines.md` changes.

## What the fixtures pin

| Fixture | Situation | Expected outcome |
|---|---|---|
| `01-empty-project/` | a TypeScript CLI with tests, mutation and docs, and no CI; its remote unreachable | the default policy in `AGENTS.md`, a GitLab pipeline whose matrix keeps it in every cell, every job calling one entry-point script, no forge write, no push |

## Layout

Each fixture holds the project under `project/`, plus:

- `manifest.json` — what the fixture pins, and the kind of each job in the expected matrix;
- `expected-matrix.md` — the trigger matrix a build must reach;
- `expected.md` — the hard assertions, and what does not count as a failure.

## How to drive it

1. Copy the fixture's `project/` to a scratch directory, then in it run `git init -q -b main`, `git add -A`,
   `git commit -qm init` and `git remote add origin git@gitlab.example.invalid:acme/tally.git`.
2. In that copy, follow this working tree's `skills/build-ci/SKILL.md` with `.` as the argument,
   answering each question as the fixture's `expected.md` says.
3. Compare the run's files and report with `expected-matrix.md` and `expected.md`. Any hard assertion
   that fails blocks the change.

## What runs automatically, and what does not

`tests/test_build_ci.py` holds each expected matrix to the default policy cell by cell, checks that each
project holds no pipeline yet, and pins the skill's refusals. **Whether a run reaches that matrix is
model judgement.** Step 2 needs an agent or a person, and step 3 needs a judge.
