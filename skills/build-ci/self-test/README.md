# build-ci — Self-Test

`build-ci` writes a pipeline, and a pipeline that looks right can still run the wrong jobs for some
source, or none. These fixtures hand the build a known project and state the trigger matrix it must
reach and what it must never do. Run them whenever `skills/build-ci/SKILL.md`, `examples/run.sh`,
`commands/build-ci.md` or `rules/ci-pipelines.md` changes.

## What the fixtures pin

| Fixture | Situation | Expected outcome |
|---|---|---|
| `01-empty-project/` | a TypeScript CLI with tests, mutation and docs, and no CI; its remote unreachable | the default policy in `AGENTS.md`, a GitLab pipeline whose matrix keeps it in every cell, every job calling one entry-point script, no forge write, no push |
| `02-rework/` | a pipeline that builds its bundle twice, once inside the Dockerfile, and its image twice, once in the deploy job | a producers table marking both, the image as PIPE-11; the single-producer package and per-job installs left alone |
| `03-speed/` | five recorded main pipelines and their job logs; the slowest job is off the critical path | the path traced by the timing script, queue wait apart, one High candidate above a stopping line drawn at the budget, `lint` never ranked |
| `04-github-project/` | fixture 01's project on GitHub; its remote names a repository that does not exist | the default policy in `AGENTS.md`, one workflow whose matrix keeps it in every cell, an `andon` job and a `tell-author` job on failure, no forge write, no push |
| `05-deploy/` | fixture 01's project with a `Dockerfile` and a deploy script that falls back to `:latest`; a recorded decision sends main to staging and production by hand | one image pushed once per main pipeline and handed on by digest; a staging deploy after every gate and a manual production deploy of the same digest, settings injected per environment, rollback through the environment's button; no forge write, no push |
| `06-github-deploy/` | fixture 05's project on GitHub | one image pushed after every gate that runs on a push; staging deployed in the gated run; production by a dispatch that names a commit and ships the image its green run built; no forge write, no push |

## Layout

Each fixture holds the project under `project/`, plus:

- `manifest.json` — what the fixture pins, its mode (`build`, `rework` or `speed`), and what the tests
  check it against;
- `expected-matrix.md` (build) or `expected-producers.md` (rework) — what the pass must produce;
- `expected.md` — the hard assertions, how to drive the fixture, and what does not count as a failure.

## How to drive it

1. Copy the fixture's `project/` to a scratch directory, then in it run `git init -q -b main`, `git add -A`
   and `git commit -qm init`. Fixture 01 also needs
   `git remote add origin git@gitlab.example.invalid:acme/tally.git`; fixture 04,
   `git remote add origin https://github.com/phil-fixture-invalid-org/tally.git`; fixture 05, fixture 01's; fixture 06, fixture 04's.
2. In that copy, follow this working tree's `skills/build-ci/SKILL.md` with the argument the fixture's
   `expected.md` names — `.`, `--rework` or `--speed` — answering each question as it says.
3. Compare the run's files and report with the fixture's `expected-*.md` files. Any hard assertion that
   fails blocks the change.

## What runs automatically, and what does not

`tests/test_build_ci.py` holds fixture 01's expected matrix to the default policy cell by cell, checks
that each build-mode project holds no pipeline yet, checks that every job fixture 02's producers table
names is a job in its pipeline, and runs `scripts/pipeline-timings.py` over fixture 03's history to
confirm its path and medians. It also pins the skill's refusals. **Whether a run reaches those outcomes
is model judgement.** Step 2 needs an agent or a person, and step 3 needs a judge.
