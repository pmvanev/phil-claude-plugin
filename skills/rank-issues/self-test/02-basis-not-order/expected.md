# Expected outcome — fixture 02 (the why, never the order)

**The sharpest fixture in the suite.** Writing the resulting order into the milestone description
alongside the real positions is the most tempting mistake available here: it looks like thorough
documentation, and it creates a second authority over the same fact.

**Expected decision:** `WRITE-BASIS-NOT-ORDER`. The milestone description carries the reasoning:

```
Ranked first because it unblocks ranking for everything else, and the board
is re-cut by hand until it lands.
```

The sequence `8, 5, 12` is written **only** as board position.

**Gate failure:** a description that also lists the order — `1. #8  2. #5  3. #12` — or names any
issue's rank in prose. Position is authoritative; the prose copy diverges the first time anyone
reorders a card in the UI, and then the board and its own documentation disagree with no signal
saying which is right.

The rule is narrow and worth stating exactly: the description holds *why this goal ranks here*, never
*which issue comes third*.
