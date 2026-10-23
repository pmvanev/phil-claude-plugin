# Expected outcome — fixture 07 (deploy what passed)

A Python project on GitHub with two deployables and no declared CI policy. `ci.yml` tests, builds and
deploys the API, to staging and then production, by the digest its build job pushed; `rollback.yml`
redeploys an earlier API digest by hand, and `hotfix.yml` builds and ships any ref it is handed. `worker.yml` tests the worker and builds one image per
environment from `worker.Dockerfile`; once a `worker.yml` run succeeds, `worker-deploy.yml` deploys each
image by the tag `run.sh` gives it.

**Pins:** the four rows `rules/ci-pipelines.md` takes from MinimumCD.org's single path to production,
definition of deployable and immutable artifacts — PIPE-27 to PIPE-31 — and the Advisory bullet for a
deploy with no rollback, each beside a look-alike the Do not flag list or a correct form clears.

**How to drive it:** per `../README.md`, over a copy holding only the project's files.

**Expected:** a `.ci-review.md` whose backlog holds the five must-fix items and the one Advisory item in
`expected-backlog.md`, matched on the Row and on a Preferred form that is the row's form verbatim, alone
or followed by ` — here: ` and this pipeline's change:

1. **PIPE-27** — `deploy-production`'s `if:` holds `!cancelled()`, so it starts when `deploy-staging`
   failed, or when a gate failed and skipped `build`. GitHub skips every job down a chain from a failed
   or skipped job, unless its `if:` says otherwise.
2. **PIPE-28** — the `skip_tests` dispatch input skips `test-worker`; `build-worker`'s `!failure()`
   lets the skipped need through, the run succeeds, and `worker-deploy.yml` deploys. One item: removing
   the switch is one edit, after which `build-worker`'s `!failure()` never sees a skipped test.
3. **PIPE-29** — `build-worker`'s matrix builds a staging and a production image, each baking its own
   `config/<env>.toml`. The File may be `worker.yml`, `run.sh` line 20 or `worker.Dockerfile`: one edit
   spans them.
4. **PIPE-30** — `run.sh` builds and deploys the worker as `$WORKER:<env>`, a tag the next push moves.
   One item, at `run.sh`, though two jobs call it.
5. **PIPE-31** — `hotfix.yml` builds whatever ref it is handed and deploys it to production, in a run
   where no gate runs.
6. **Advisory** — nothing redeploys an earlier worker image: `rollback.yml` takes an API digest only.

**Hard assertions (any failure blocks the change):**

- **No item names a look-alike:**
  - `rollback.yml` — a rollback that redeploys a digest an earlier run built and tested, with no tests
    of its own.
  - `python-version` — a test matrix over runtimes, not a build per environment.
  - `DIGEST: ${{ needs.build.outputs.digest }}` — the API deploys by the digest its build job pushed.
- **`deploy-staging` gets no PIPE-27 item.** Its `needs:` reach every gate through `build`.
- **`worker-deploy.yml` gets no PIPE-27 item.** Its first job tests the run's `conclusion` and that
  it was no pull-request run, and its second job needs the first. The worker's pipeline is a `worker.yml`
  run with the `worker-deploy.yml` run it starts; `ci.yml`'s gates belong to another pipeline.
- **`rollback.yml` gets no PIPE-31 item.** It ships a digest a gated run built; `hotfix.yml` builds
  what it ships.
- **No PIPE-11 item.** No deploy job builds: each deploys an image a build job pushed.
- **No reviewed file is edited.** The run writes `.ci-review.md` and nothing else.
- **An extra must-fix item fails** if it names a look-alike or cites a row that does not describe it.

**Not a failure:** a PIPE-8 question about `worker.yml`, which runs no secret scan of its own while
`ci.yml` scans every pull request and main push; Advisory items for an undeclared Andon or Notify field,
for a superseded pull-request run left running, or for tests that run from source rather than the
deployed image; listing the environments' protection rules and `DEPLOY_TOKEN` under "Not read"; line
numbers within ±2, or a line inside the expected range; a differently worded title.

**Driven 2026-10-22** blind, three times, against this working tree's `SKILL.md`: every hard assertion
held each time. Between drives the fixture was reseeded twice — PIPE-28 now stands on its own through
`workflow_run`, since a GitHub job that needs a skipped test skips with it, and `hotfix.yml` seeds
PIPE-31. The last drive filed exactly the six expected items; fixtures 01 and 02, driven blind after
PIPE-27 was narrowed, filed none of PIPE-27 to PIPE-31.
