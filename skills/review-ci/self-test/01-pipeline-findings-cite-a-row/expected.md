# Expected outcome — fixture 01 (pipeline findings cite a row)

A Node service mirrored to GitLab and GitHub: `.gitlab-ci.yml`, two GitHub workflows, a `Dockerfile`,
`package.json` with its lockfile, and the deploy script its jobs call. It holds twelve pipeline defects,
each on lines an Always-flag row of `rules/ci-pipelines.md` describes, and one supply-chain defect that
`rules/security.md` owns. Six look-alikes sit beside them, each cleared by the Do not flag list or by a
correct guard.

**Pins:** a pipeline finding names its `PIPE-n` row and takes the row's Preferred form as its fix; a
supply-chain finding names its CWE id; a defect that one edit fixes is one item, filed where the edit
goes; nothing on the Do not flag list is filed.

**How to drive it:** per `../README.md`, over a copy holding only the project's files.

**Expected:** a `.ci-review.md` holding the thirteen must-fix items in `expected-backlog.md`, matched on
the Row and on a Preferred form that is the row's form verbatim, alone or followed by ` — here: ` and
this pipeline's change:

1. **PIPE-6** — `ci.yml`'s concurrency group is the workflow name, so a newer run cancels a main run.
2. **PIPE-8** — `secrets.yml` skips the secret scan on PRs that touch only docs.
3. **PIPE-13** — the default cache's key is the constant `deps`. One item, though every job inherits it.
4. **PIPE-1** — `.mr-tests` runs for `merge_request_event` and for any branch, with no `workflow:rules`.
   One item at the template, though three jobs extend it.
5. **PIPE-9** — `unit-tests` is `allow_failure: true`.
6. **PIPE-10** — `integration-tests` retries twice on any failure.
7. **CWE-829** — the `gitleaks` job's image is `:latest`.
8. **PIPE-15** — `lint` sits in a stage after `test`, with no `needs: []`.
9. **PIPE-16** — `package` cds into `/builds/acme/storefront/dist`.
10. **PIPE-3** — `deploy-dev`'s `changes` rule has no source guard, so a scheduled pipeline on main
    deploys dev.
11. **PIPE-12** — `deploy-dev` takes no artifacts and reads `dist/` from the cache `package` writes. One
    item, filed at the consumer.
12. **PIPE-11** — `deploy-staging` runs `npm ci` and `npm run build` instead of deploying `package`'s
    output.
13. **PIPE-14** — the `Dockerfile` copies the source before `npm ci`.

**Hard assertions (any failure blocks the change):**

- **No item names a look-alike:**
  - `release-prod` — a manual start for a production release, taking the tested artifact.
  - `mutation-full` — a schedule that adds full mutation while per-change pipelines still run, with a
    retry limited to infrastructure failures.
  - `mr-smoke` — `interruptible` on a job that runs only in MR pipelines.
  - `coverage-trend` — tolerates its own failure, gates nothing, and says so.
  - `key: npm-` — `ci.yml`'s cache keyed on the lockfile's hash.
  - `group: secret-scan-` — `secrets.yml`'s group keyed on the PR ref.
- **CWE-829 is filed under its CWE id, never as a `PIPE-n` item.**
- **PIPE-1, PIPE-12 and PIPE-13 are one item each.**
- **No reviewed file is edited.** The run writes `.ci-review.md` and nothing else.
- **An extra must-fix item fails** if it names a look-alike or cites a row that does not describe it. An
  extra item that a row does describe is not a failure: record it here, and pin it if it holds.

**Not a failure:** naming under "Not read" the branch protection, required status checks, merge queue,
auto-cancel and project timeout settings, with no item for them; line numbers within ±2; a differently
worded title.

**Driven 2026-10-21** against this working tree's `SKILL.md` before the counting rule and the fixture's
package files existed, by a fresh agent that read only the skill, the rules and the project. It filed
all thirteen, flagged no look-alike, and edited nothing. It also filed PIPE-12 twice (producer and
consumer), a PIPE-5 question with no premise in the files, and CWE-250 for a `Dockerfile` with no
`USER`. Each led to a change: the counting rule, the premise rule, and `USER node` in the fixture.
