# Expected outcome — fixture 04 (andon)

A Python command-line tool on GitHub that declares its CI policy in `CLAUDE.md`, including an Andon
field: a failed main pipeline opens an issue the repository's watchers are emailed about. `ci.yml` runs
the secret scan and the tests, and its last job pulls the cord when either fails on main. `build.yml`
builds the zipapp on the same triggers, and nothing tells the team when it fails there.

**Pins:** under a declared Andon field, a GitHub workflow that runs on main with no job that pulls the
cord on its failure is PIPE-25, filed at that workflow, because GitHub notifies only the user who
triggered the run. The workflow that pulls the cord, its job's write grant and a failed MR are not
flagged.

**How to drive it:** per `../README.md`, over a copy holding only the project's files.

**Expected:** a `.ci-review.md` whose Policy line lists the seven declared fields, whose trigger matrix
reads `ci.yml: andon` as `on failure` in both main columns and `—` in every other, and whose backlog holds
the one must-fix item in `expected-backlog.md`, matched on the Row and on a Preferred form that is the
row's form verbatim, alone or followed by ` — here: ` and this pipeline's change.

**Hard assertions (any failure blocks the change):**

- **PIPE-25 is filed once, at `build.yml`.** One edit — a last job, or one `workflow_run` workflow —
  fixes it.
- **`ci.yml` gets no PIPE-25 item.** Its `andon` job needs every other job and runs on failure on main.
- **No item names the look-alike** `issues: write`: the grant sits on the andon job alone, which its task
  needs, while the workflow's top keeps `contents: read`. No CWE-250 item.
- **No item says an MR's failure reaches only its author.** The cord is for main.
- **No reviewed file is edited.** The run writes `.ci-review.md` and nothing else.
- **An extra must-fix item fails** if it names a look-alike or cites a row that does not describe it.

**Not a failure:** an Advisory item for an MR run left running when a newer one starts; a PIPE-8
question about `build.yml`, which runs no secret scan of its own while `ci.yml` scans every pull request
and main push; listing branch protection, the required checks and the repository's watchers under "Not
read"; line numbers within ±2; a differently worded title.

**Driven 2026-10-22** blind, against this working tree's `SKILL.md` at 1.8.0: exact. One PIPE-25 item at
`build.yml` 15-26 with the row's form verbatim; `ci.yml: andon` read as `on failure` on main and `—`
elsewhere; no item on the write grant or on an MR's failure. The drive gave each workflow its own
`(pipeline)` row, which no assertion names.

**Driven again 2026-10-22**, after the skill review's and plugin validator's fixes, against the corrected
`workflow_run` form: exact on every hard assertion. Two extra Advisory items, one per workflow, for a
superseded pull-request run left running.
