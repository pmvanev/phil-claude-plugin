# The board divergence check — why it exists and what each branch looks like

Reference for `skills/session-handoff/SKILL.md` § BOOTSTRAP step 5. The **rules** live there and are
authoritative; this file carries the reasoning and the worked output, which change no decision at
runtime. Read it when changing the check, not when running it.

Issue #24, shipped 2026-08-17.

## The gap it closes

**The freshness verdict compares the snapshot against the tree. It can never compare it against the
board, and the board is where the rest of the team records the same fact.** So a snapshot can be
`RESUME-CURRENT` — same commit, same clean tree, every check green — while the board says something
different is in flight, and nothing says so.

Observed 2026-08-13 and carded as #24: the snapshot's `Next` named a dogfood run; the board's top Todo
was #15, different work entirely. It was harmless, because the dogfood had happened in an intervening
session. **A human noticed it. Nothing else could have.**

The two sources fail in opposite directions and a session cannot tell which it is holding:

- **Snapshot ahead of the board** — work was claimed and the card never moved. Following the board
  restarts work already under way.
- **Board ahead of the snapshot** — the card advanced in another session. Following the snapshot redoes
  spent work.

## Where it sits, and where it deliberately does not

Report beside the freshness verdict and **before** the recorded content, on `RESUME-CURRENT` and
`RESUME-STALE` alike. `RECONSTRUCT` reports none of them: with no snapshot there is no recorded next
action, so there is nothing to compare. Reporting the board's in-flight card there as *reconstructed
position* is defensible and is deliberately **out of scope** for #24, not argued against.

## The three branches, as output

**`BOARD-AGREES`** — the recorded next action and the board's in-flight claim name the same work:

```
BOARD-AGREES — snapshot Next and the board's in-flight card (#24, In Progress) name the same work.
```

**Report agreement out loud.** A detector silent on the agreeing branch is indistinguishable from one
that is broken, mis-wired, or reading an empty board — the *check nobody runs reports compliance by
staying quiet* defect this repository keeps rediscovering.

**`BOARD-DIVERGES`** — they name different work. Name **both**, label each with its source, and stop:

```
BOARD-DIVERGES — the two records of what is in flight disagree.
  snapshot Next (captured 2026-08-13T21:10Z):
    dogfood /phil:groom-issues against this repo's own board
  board, top Todo (no card In Progress):
    #15 groom-issues slice 03 — set-level operations, all ask-first
Neither is authoritative over the other. Resolve before proceeding.
```

**`BOARD-UNREADABLE`** — there is no board, or it cannot be reached. Name the reason, and say plainly
what was not checked:

```
BOARD-UNREADABLE — no board constants in CLAUDE.md and no `project` scope on the token.
The snapshot's Next was NOT checked against a board.
```

Most repositories carrying this skill have no board, so **this is the branch that runs most often.** An
unreadable board is not an agreeing board, for the same reason an absent stack renders `unknown` rather
than empty: one is a claim about the record, the other a claim about the work.

## Why each of the four rules is drawn where it is

- **`In Progress` where one exists, top Todo otherwise.** Comparing against the top Todo alone reports a
  session that correctly claimed its card as diverging from whatever sits above it. Where `In Progress`
  goes unused the branch never fires. Worked through in
  `../self-test/14-board-agrees-with-snapshot/expected.md`.
- **Semantic match, biased toward divergence.** The outcome is advisory and resolves nothing: a false
  positive costs the reader one line, a false negative is the silent failure the check exists to kill.
- **Detect; never resolve.** Neither source is authoritative, so picking one silently discards the
  other's work while reporting success — the same boundary slice 03 drew for competing claims.
- **Read; never write.** Reconciling is a human's act. Where the forge's mirror workflows are enabled a
  Status write is also an issue write, so there is no small correction available here either.

## The one failure this check cannot notice about itself

An under-reporting board read is a **missed divergence**. `phil:issue-board` owns which call is
trustworthy on each forge and which under-reports; delegate rather than inlining the mechanics. This is
also why `/phil:resume` declares `mutates: true` while writing nothing — `gh api graphql` can carry a
mutation, and the read-only alternative under-reports.
