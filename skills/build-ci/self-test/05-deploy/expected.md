# Expected outcome — fixture 05 (a project that deploys, on GitLab)

Fixture 01's TypeScript project, now also a service: a `Dockerfile`, and `scripts/deploy.sh
<environment> [image]`, which points a Kubernetes deployment at an image and falls back to
`:latest` when handed none. `AGENTS.md` records a decision: every green main commit goes to staging,
and production is deployed by hand; each environment sets its own `KUBE_CONTEXT` and
`TALLY_LEDGER_DIR`. No CI. Its remote names a GitLab host the run cannot reach.

**Pins:** a build deploys only what passed. Each main pipeline pushes one image, after every gate, and
hands it on by digest; the staging deploy and the manual production deploy both take that digest, with
each environment's settings injected at deploy time. The deploy script's `:latest` default is never
what ships.

**How to drive it:** per `../README.md`, with `git remote add origin
git@gitlab.example.invalid:acme/tally.git`, answering as fixture 01 does: "adopt the default policy",
"email dev@tally.invalid" for the andon, "yes" to the `NOTIFY_TOKEN` question, and "no" to any forge
question.

**Expected:** the run writes `.gitlab-ci.yml`, an entry-point script and the `AGENTS.md` lines fixture 01
expects, and reports a trigger matrix matching `expected-matrix.md` job kind by job kind:

| Kind | Jobs in `expected-matrix.md` | What its cells must say |
|---|---|---|
| fixture 01's kinds | `gitleaks` to `build`, `mutation-diff`, `mutation-full`, `tell-author` | as fixture 01's |
| image | `build-image` | runs on main and in a pipeline started by hand on main; exits early on a docs-only main commit; absent from MRs and the schedule |
| staging deploy | `deploy-staging` | the same cells as `image` |
| production deploy | `deploy-production` | waits for a person on main; absent from MRs and the schedule |

**Hard assertions (any failure blocks the change), beside every one of fixture 01's:**

- **One image, built once.** One job builds and pushes the image, on the default branch only, in a stage
  after every gate's, with no `needs:`. It hands on the digest through `artifacts: reports: dotenv:`,
  with an `expire_in`, and its image holds `git`. No deploy job builds (PIPE-11), and nothing builds an
  image per environment (PIPE-29).
- **Each deploy takes that digest.** Both deploy jobs run `./scripts/ci/run.sh deploy <environment>`,
  which refuses an `IMAGE` that names no `@sha256:` digest of the project's registry repository and
  passes the digest to `scripts/deploy.sh`. No job, and no line of the entry-point script, lets
  `scripts/deploy.sh` fall back to `:latest` (PIPE-30). On a docs-only commit the image job builds
  nothing and each deploy exits early (PIPE-24), and the report says a rollback picks a deployment whose
  pipeline built an image.
- **Each deploy waits for every gate.** No deploy job carries `when: always`, and each reaches every
  gate through the image job (PIPE-27). No variable or input turns a gate off (PIPE-28).
- **Staging deploys itself; production waits.** `deploy-staging` runs on its own on main, under
  `environment: staging`. `deploy-production`, under `environment: production`, needs the image job and
  `deploy-staging`, and its rules end in `when: manual` with no `allow_failure`. The report, and a line
  under `## CI workflow`, say a main pipeline blocked at it has passed every gate.
- **Settings at deploy time.** `KUBE_CONTEXT` and `TALLY_LEDGER_DIR` come from CI/CD variables scoped to
  each environment. Neither is written in the CI file or built into the image. The report lists both,
  for each environment, as variables for the user to create, and reads none.
- **A rollback the report names.** The report names the environment's Rollback environment button,
  which reruns an earlier pipeline's deploy job, and lists `ci_forward_deployment_enabled` and
  `ci_forward_deployment_rollback_allowed` as unread, with the command that reads them.
- **The registry login reads CI variables**, its password through stdin, never in the CI file.
- **Nothing deploys from an MR or the schedule.** The entry-point script has no `andon` or `promote`
  task.
- **No `/phil:review-ci` must-fix item** fires, and none of PIPE-27 to PIPE-31. The Advisory question
  about rollback may fire, since the button is a forge feature no file shows.

**Not a failure:** fixture 01's allowances; another image builder than Buildah that needs no host
daemon; a `resource_group:` on each deploy, or none; a manual rollback job that takes an earlier digest
with `needs: []` and builds nothing; one more environment the run asked about and was told "none"; the
Dockerfile's base image digest left as the project wrote it; the Dockerfile rebuilding `dist/`, reported
as rework the project owns; a `.gitignore` entry for `image.env` and `image.ref`.

**Driven 2026-10-22** blind, twice, against this working tree. The first run held every assertion then
in force — one image job with no `needs:` after every gate, a 90-day dotenv digest, `deploy-production`
manual with no `allow_failure`, `resource_group` on both deploys, settings listed by environment and
unread — and found the example script had no registry login. The second, after the login and the
promotion task landed, held every assertion above but one: it built and deployed on a docs-only commit,
as the skill then said to, which PIPE-24 forbids. It also found that GitLab reserves `image` as a job
name. Both are fixed in the skill since. A third drive, after that fix, held every hard assertion:
`build-image` with no `needs:` after every gate, a 90-day dotenv digest, both deploys exiting early on a
docs-only commit, production manual with no `allow_failure`, settings listed by environment and unread.
It found the Buildah image holds no `git`, which the skill now says to install from the image's own
package manager.
