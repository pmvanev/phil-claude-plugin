# Rendering a projected snapshot

Part of the `nwave-issue-board` skill. Read it whole before rendering the why, the next action and the stack from `.session-handoff.md`, whether `phil:session-handoff` handed them over at a capture or a refresh re-read them. Its `SKILL.md` governs this file too.

`phil:session-handoff` hands over three things from `.session-handoff.md`, each with the snapshot's capture
timestamp: the **why** (decisions reached, approaches ruled out), the **next action**, and the **work
stack** — the diversion chain, innermost last. Render them below the tables:

```
Why (captured 2026-08-14T02:07Z)
- Ruled out re-running JTBD for the slice: a second job statement over a validated job is the
  duplicate-authority defect this feature exists to detect.
- Work stopped mid-dogfood, deliberately, not because it failed.

Next — finish the dogfood on #2, asking only the missing done-condition.

Stack
1. Slice 04 elicitation · the task in hand · open since 2026-08-13T21:10Z · crossed 2   ⚠ stale
2. └ The observed population · it was partial, so the rule needed changing first · open since 2026-08-14T02:02Z · crossed 0
```

Four rules, and the first is the one that makes this legal:

- **Write-only, like everything else in the block.** `/phil:resume` reads the local snapshot; nothing reads
  this. The local file stays the single authority, so no second authority exists to drift — which is the
  whole reason the reasoning can live on a board at all.
- **Absent renders as `unknown`, never as empty** — under *Project the reasoning, not just the position* in `SKILL.md`.
- **A frame whose `crossed` is 2 or more is marked `⚠ stale`.** A push that survived two wind-downs is
  stale, and a stale stack is worse than none for the same reason a stale snapshot is: the next reader
  trusts it.

  The rule's source is `skills/session-handoff/SKILL.md` § *The snapshot*; if the two disagree, the
  recorder wins. The threshold is two because every carried frame has already survived one wind-down.
  **Render `crossed` verbatim; never compute it here.**
- **The capture timestamp is the snapshot's, not the block's.** They differ whenever a refresh happens
  without a capture, and a reader deciding whether to trust the reasoning needs the age of the reasoning.

**The accepted cost:** a teammate sees only what the last capture projected, the price of one
authority.
