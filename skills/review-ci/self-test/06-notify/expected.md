# Expected outcome — fixture 06 (a warning that names nobody)

A GitLab library that declares a Notify field in `AGENTS.md`. Its pipeline's last job, `tell-author`,
runs in the `.post` stage on failure and names whoever started the pipeline. `coverage-trend` gates
nothing and says so, but tolerates its own failure with `allow_failure: true`.

**Pins:** under a declared Notify field, a job meant only to inform that tolerates its own failure is
PIPE-26: GitLab marks the pipeline passed and tells nobody, and `when: on_failure` never starts for an
allowed failure. PIPE-9's Do-not-flag entry still clears the job as PIPE-9, because it gates nothing and
says so.

**How to drive it:** per `../README.md`, over a copy holding only the project's files.

**Expected:** a `.ci-review.md` whose Policy line lists the seven declared fields, whose matrix reads
`tell-author` as `on failure` in every created pipeline but the schedule's, and whose backlog holds the one must-fix item in
`expected-backlog.md`, matched on the Row and on a Preferred form that is the row's form verbatim, alone
or followed by ` — here: ` and this pipeline's change.

**Hard assertions (any failure blocks the change):**

- **PIPE-26 is filed once, at `coverage-trend`.**
- **No PIPE-9 item**: the job gates nothing, and its comment says so.
- **No item names `tell-author`**, and none files `NOTIFY_TOKEN`, a masked variable, as a credential.
- **"Not read" names the `NOTIFY_TOKEN` variable** or the project's CI/CD variables.
- **No reviewed file is edited.** The run writes `.ci-review.md` and nothing else.

**Not a failure:** an Advisory item, such as the merge gate, a superseded MR pipeline left running, or
an andon the policy does not declare; listing "Pipelines must succeed" and auto-cancel under "Not read";
line numbers within ±2; a differently worded title.
