# Expected outcome — fixture 19 (numbers are assigned at creation)

One card, three outcomes, split on approval. Every hard part of this fixture is about ordering.

**Expected decision:** `APPLY-SPLIT`, in two passes with the board add between them:

```
Pass 1 — create. Three cards, each with the label and milestone you chose carried over,
         and no Chain lines yet:
           #41  (created)   #42  (created)   #43  (created)

         Added to project 3. Status is unset on all three — placing them in the queue is
         phil:rank-issues, and this command holds no gh project item-edit.

Pass 2 — cross-reference, now that the forge has numbered them:
           #41  ## Chain — blocks #42
           #42  ## Chain — blocked by #41 · blocks #43
           #43  ## Chain — blocked by #42
           #28  ## Chain — split into #41, #42, #43

Not carried, because you did not ask for it: the `documentation` label, and #28's
"relates to #7" line, which stays on the container.
```

**Why two passes and not one.** A card's number does not exist until the forge assigns it, so a `## Chain`
line written during creation is a reference to a number nobody has issued. The failure is not a broken
link — it is a *working* one: the forge renders `#42` as a live link to whatever else eventually claims
that number, and the card reads as correctly cross-referenced to every future reader.

**Why the original is a second question.** A split leaves a card that no longer describes work. Closed as
superseded or kept as the container are both defensible and they are not the same board, so the split is
unfinished until it is answered. An original left open beside its own three pieces is now the duplicate
this command exists to find, created by this command.

**Gate failures:**

- Writing any cross-reference in pass 1.
- Inheriting labels, milestone, or chains without asking. Nothing follows a split automatically; carrying
  `documentation` onto three cards because the original had it is a decision taken silently.
- Leaving `#28` open with no statement of what it now is.
- Creating the three issues and stopping. An issue that was never `item-add`ed has no Status and does not
  appear in a kanban grouped by it — the split reports three new cards and the board shows none.
- Setting Status on the new cards to make them visible. Where they sit in the queue is an ordering
  decision, and `phil:rank-issues` owns it.
- Writing `#28`'s own chain line before `#41`–`#43` exist. The container's reference is a cross-reference
  like any other and belongs in pass 2.
