# Expected outcome — fixture 15 (the check cannot run, and refuses to imply it did)

**This is the branch that will execute most often.** Most repositories carrying this skill have no
forge board — no project constants in `CLAUDE.md`, no `project` scope on the token, or no network. If
that branch is unhandled, the divergence check silently skips on the majority of runs while every
report looks complete, which is precisely the defect `#24` was filed against, relocated into its own
fix.

**Pins:** issue #24 — the check is a named outcome on every read-back, or it is not a check.

**The reason must be one `/phil:resume` can actually reach.** Its grant is `Read`, `Glob`, `Grep`,
read-only `git`, and `gh api graphql` — so *no board constants in `CLAUDE.md`* is reachable by `Read`,
and *the board query failed* is reachable from the call itself. A reason that would need a verb the
command does not hold — `gh auth status`, say — pins output the command cannot produce, and the
fixture would be unsatisfiable while reading as though it had been thought through. Caught by
`plugin-dev:plugin-validator` on 2026-08-17, in this fixture's first draft.

## Expected decision

1. **`RESUME-CURRENT`** — the fingerprint matches. Unchanged, and independent of the board.
2. **`BOARD-UNREADABLE`** — named, with the reason:

```
BOARD-UNREADABLE — no board constants in CLAUDE.md, so there is no board to query.
The snapshot's Next was NOT checked against a board.
```

The second line is the load-bearing one. It says what was *not* done, so the reader does not read the
report's completeness as coverage.

## Gate failure (blocks the skill change)

- **`BOARD-AGREES` is reported.** An unreadable board is not an agreeing board. This is the same
  distinction fixture `12` draws between `unknown` and empty, and fixture `03`/`05`'s rule that
  unknown is stated and never defaulted: *`unknown` is a claim about the record, agreement is a claim
  about the work.*
- **nothing is reported at all** and the run proceeds to the briefing. Silence is indistinguishable
  from a check that ran and found nothing.
- the read-back **fails** or refuses to present the briefing. A missing board is the normal condition,
  not an error; the freshness verdict, the content and the owner are all still correct and still owed.
- the skill tries a second, unsanctioned route to the board — `gh project item-list`, a scrape, a
  cached copy — to avoid reporting the branch. `CLAUDE.md` forbids `item-list` for board reads because
  it can under-report, and an under-report here is a **missed divergence**, which is worse than a
  stated gap.

## Why this fixture is not scope creep

Issue #24 requires two fixtures, divergent and agreeing, *"so the check cannot pass by never firing."*
Those two pin the check when a board exists. This one pins the case where the check **genuinely cannot
fire** and must say so — without it, the two required fixtures would both be satisfiable by a spine
that quietly does nothing on every repository that has no board.
