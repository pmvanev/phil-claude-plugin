# Expected outcome — fixture 02 (trigger matrix)

A GitLab web app that declares its CI policy in `AGENTS.md`: MR-only pipelines, a docs allow-list,
change-scoped tests and mutation in the MR, everything but mutation on main, and a weekly full mutation
run. Its jobs call `scripts/ci/run.sh`, which exits early for a docs-only change and forces a full test
run when the selector's own inputs change. The pipeline seeds four defects that turn on which source starts a
pipeline or which paths a change touches, and one departure from the declared policy. A correct guard
sits beside each.

**Pins:** the review reads the `## CI policy` block and writes the trigger matrix; each seeded defect is
filed under its row and marked in the matrix; a policy departure is PIPE-24; a script the job calls
counts as the job's guard.

**How to drive it:** per `../README.md`, over a copy holding only the project's files.

**Expected:** a `.ci-review.md` whose Policy line lists the seven declared fields, whose trigger matrix
has the seven source columns in order, and whose backlog holds the five must-fix items in
`expected-backlog.md`, matched on the Row and on a Preferred form that is the row's form verbatim, alone
or followed by ` — here: ` and this pipeline's change:

1. **PIPE-21** — `lint` is skipped by `changes:` on doc paths with `when: never`, so an MR touching a
   doc and code together skips it.
2. **PIPE-18** — `accessibility` needs `e2e`, which an MR outside `web/` leaves out; GitLab refuses that
   pipeline, docs-only MRs included, so the secret scan never runs there either. One item, not a PIPE-8,
   shown on the matrix's `(pipeline)` row.
3. **PIPE-24** — `mutation-diff` runs on main under `Main: everything except mutation`.
4. **PIPE-17** — `deploy-staging` admits the default branch with no source check, and the schedule runs
   on main. One item, not also a PIPE-24 for the schedule's field.
5. **PIPE-19** — `rollback-prod` tests `$ROLLBACK_TAG &&` with a `""` default, so every main pipeline,
   the schedule's included, offers a production rollback nobody asked for. The item rests on the rule's
   shape: `scripts/deploy.sh` happens to refuse an empty tag, and a script is no guard on a rule.

**Hard assertions (any failure blocks the change):**

- **The matrix marks** `deploy-staging` × schedule, `accessibility` × MR, `mutation-diff` × main push,
  `lint` × MR and `rollback-prod` × main push, each with its item's id, and its `(pipeline)` row reads
  the MR column as refused for some paths.
- **No `exits early` cell is marked** as a policy departure: a job whose script skips the work satisfies a
  field that excludes it.
- **The matrix reads** `deploy-dev` × schedule as `—`, `mutation-full` as running on the schedule
  alone, and every tag cell as `—`.
- **No item names a look-alike:**
  - `deploy-dev` — an automatic deploy whose rules start with `.not-on-schedule`.
  - `deploy-prod` — a manual production release.
  - `mutation-full` — the scheduled full run that diff-scoped mutation needs, sharded, retrying
    infrastructure failures only.
  - `e2e-report` — a `needs:` on `e2e` marked `optional: true`.
  - `.unless-rollback` — a bare `$ROLLBACK_TAG` as the whole expression, which reads empty as false.
  - `.web-changes` — a path list that compares against main and includes the lockfile, this file, the
    scripts it calls, the build configuration and the shared test support.
- **PIPE-19 is not cleared** by the Do not flag entry for a manual rollback: the defect is the rule, not
  the manual start.
- **No reviewed file is edited.** The run writes `.ci-review.md` and nothing else.
- **An extra must-fix item fails** if it names a look-alike or cites a row that does not describe it.

**Not a failure:** an Advisory item, such as an MR pipeline left running when a newer one starts, or a
question whether the end-to-end tests exercise the `dist/` that `deploy-dev` ships;
`runs` where this file reads `exits early`, or the reverse, in a cell no assertion names; listing the
pipeline schedule, "Pipelines must succeed", auto-cancel and the project timeout under "Not read"; line
numbers within ±2; a differently worded title.
