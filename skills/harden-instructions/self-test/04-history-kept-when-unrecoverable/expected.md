# Expected outcome — fixture 04 (history kept when nothing can recover it)

**Situation.** Run this fixture from a copy that is **not committed** — untracked, or outside any
repository. A rule carries a long incident history.

**Pass.** The rule leads with its reflex: set `TZ=UTC` before the integration tests. The wound is
compressed to one line beneath it. The rest of the history stays in the file, and the report flags it
as recoverable nowhere, because git reports the file untracked, or finds no repository at all.

**Fail.**
- The history is deleted while no commit holds it.
- The report names a `git show` recovery command for a file no commit holds.
- The reflex loses `UTC` or the integration-test scope.

Run against a committed copy, the same input may cut the history; the report must then name
`git show <hash>:<path>`.
