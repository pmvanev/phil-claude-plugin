# Expected outcome — fixture 04 (the same project on GitHub)

Fixture 01's TypeScript command-line tool, with no CI, whose remote names a GitHub repository that does
not exist. Its instruction file is `AGENTS.md`, which declares no policy.

**Pins:** on GitHub, a build carries out the default policy's Andon and Notify fields from the
pipeline: a last `andon` job pulls the cord on a red main, and a `tell-author` job names whoever started
a failed run. It reads the forge before writing to it, and here reads nothing.

**How to drive it:** per `../README.md`, with the remote `https://github.com/phil-fixture-invalid-org/tally.git`,
answering "adopt the default policy" to the policy question, "an issue" to the question of where the team
hears a red main, and "no" to any forge question.

**Expected:** the run writes `.github/workflows/`, an entry-point script, and the policy block and
workflow lines in `AGENTS.md`, and reports a trigger matrix matching `expected-matrix.md` job kind by job
kind. Fixture 01's table holds for the kinds both share, except that GitHub's default gives no hand-run
trigger, so every web or API cell is `—`; and:

| Kind | Job in `expected-matrix.md` | What its cells must say |
|---|---|---|
| andon | `andon` | on failure on a main push, a docs-only main push and the schedule; `—` elsewhere |
| tell the starter | `tell-author` | on failure on every pull request and main push; `—` on the schedule |

**Hard assertions (any failure blocks the change):**

- **The policy block** is the default block from `rules/ci-pipelines.md`, with Docs-only paths covering
  `docs/**` and `**/*.md`, and an Andon field naming an issue, written under `## CI policy` in `AGENTS.md`.
- **The `andon` job** needs every job but `tell-author`, runs on `if: failure() && github.ref == 'refs/heads/main'`,
  grants `contents: read` and `issues: write` on itself alone, and runs `./scripts/ci/run.sh andon`.
- **The `tell-author` job** needs every job but the andon, runs on `if: failure() && github.event_name != 'schedule'`,
  grants `contents: read` and `pull-requests: write` on itself alone, passes `PR_NUMBER`, and runs
  `./scripts/ci/run.sh tell-author`.
- **The workflow's top grants `contents: read` alone.**
- **Every action is pinned by a commit SHA read from GitHub**, with its tag in a comment, or listed under
  "To pin".
- **The entry-point script** keeps `examples/run.sh`'s decision and its `andon`, `tell-author` and
  `inform` tasks, and drops the GitLab CI paths. `sh -n` passes on it.
- **actionlint passes** on every workflow written, run as `actionlint` or reported missing.
- **No job tolerates its own failure**: no `continue-on-error`.
- **No `/phil:review-ci` must-fix item** fires on the written pipeline.
- **No forge setting is written, nothing is pushed, and no pipeline is started.** The report lists the
  merge gate and the repository's Issues setting as unread, each with the command that reads it.
- **`AGENTS.md` gains the workflow lines**, among them that a red main stops the line and that a failure
  or a warning names its author.

**Not a failure:** different job names; one workflow per concern, each with its own `(pipeline)` row,
provided the andon and the starter's comment cover every workflow that runs on main; a `workflow_run`
andon in place of the `andon` job; a shard count other than four; a lint that could not run because
`actionlint` is missing, said so in the report.
