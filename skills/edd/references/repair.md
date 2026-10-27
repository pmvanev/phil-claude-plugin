# REPAIR — the grouping, each skill's argument and gate, and the clean tree

The full REPAIR step of `skills/edd/SKILL.md`. Read in full before offering any repair.

## Group by smell, not by route

`phil:review-code` routes every structural item — comments and dead code included — to
`/phil:refactor`, and names no other repair skill. So group them by Smell and Priority, not by Route:

| Advisory finding | Owner | Invoke with | Its gate |
|---|---|---|---|
| A structural smell (Priorities 2–4, 7); dead or commented-out code (Priority 5) | `phil:refactor` | each file's path | the suite after each item, then a commit; no human approval |
| The same, when the developer wants one loop over several files | `phil:refactor-loop` | — | its own, under the Workflow tool — see below |
| A structural test smell (Priority 6, not on a pinning test) | `phil:refactor-tests` | each test file's path | the developer approves each diff |
| A test coupled to its implementation (Priority 6, not on a pinning test) | `phil:redesign-tests` | each test file's path | the developer approves each diff and its coverage claim |
| A redundant or unclear comment (Priority 5) | `phil:clean-comments` | the file's path and the item's lines | none of its own — see below |
| An item routed `report only`, or a `phil:ux-review` `consider` | none | — | listed and recorded, never run |

Run `phil:redesign-tests`, and any other skill that changes what a test asserts, never over a pinning
test: the pin was recorded against what it asserts now. Each repair skill re-detects with its own
rules, so an item may not reappear when it runs; record that too.

`phil:clean-comments` has no gate of its own: it runs no suite and asks no approval. Supply one: run
the suite after it, put its diff to the developer, and revert the change on a red suite or a reject.

`phil:refactor-loop` runs under the Workflow tool, which this command is not granted and which a
developer must opt into. When the structural items span several files and the developer wants one
gated loop over them, recommend `/phil:refactor-loop` with those paths for the developer to run after
this run ends; this skill never runs it.

## Order, and what each run touches

Run the `phil:clean-comments` group first, and commit each diff the developer approves, with a message
naming the backlog item: the next skills need a clean tree. Then the `phil:refactor` group. Given a
file's path, `phil:refactor` reviews that file again and works every item it routes to itself, so it
also removes the comment items in that file — `phil:review-code` routes them there. Say so in the
`phil:refactor` group's cost when the developer skipped a comment item in the same file. Then
`phil:refactor-tests`, then `phil:redesign-tests`, each scoped to its test files.

## The offer

Put one question per owner group, at most four to an ask, splitting into more asks when needed. Each
question offers `run` or `skip`, with its cost — the gate above, and the time it takes — and every
ask offers `stop`. Run only the groups the developer answered `run`.

## A clean tree first

Every repair skill except `phil:clean-comments` stops on a dirty tree. Before the first repair:

- the engine has committed the pins;
- record every finding from both backlogs in the draft of `stabilize.md`, held in the conversation,
  never on disk until DOCUMENT;
- note what each backlog file held before this run's first write: `.refactoring-backlog.md`,
  `.ux-review-backlog.md`, and the `.test-refactoring-backlog.md` and `.test-redesign-backlog.md`
  that a scoped `phil:refactor-tests` or `phil:redesign-tests` run writes. Keep `.refactoring-backlog.md`
  while the `phil:refactor` group runs — that skill works it and excludes it from its own check.

After the last repair, restore each to what it held before this run: delete a file the run created,
and put back the earlier content of one that existed. A developer's pending items are theirs.

If a repair skill still reports a dirty tree, stop and tell the developer what is uncommitted.

A repair changes no behaviour, and its gate keeps every pinning test green; it is not a rebuild.
