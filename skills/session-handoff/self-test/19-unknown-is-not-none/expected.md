# Expected — 19 (the two empties, which are not the same empty)

**Pins:** slice-01 AC5, and the `unknown` / `none` distinction inherited from the projection rule.

**Expected decisions:** run A reports `STACK-UNKNOWN`; run B reports `STACK-EMPTY`. Two runs, two outcomes,
and collapsing them is the failure:

```
Run A:  STACK-UNKNOWN — no snapshot at this worktree root.
          Nobody has written anything down. This says nothing about whether there were diversions.

Run B:  STACK-EMPTY — snapshot present (captured 2026-08-12T17:30Z), no diversions recorded.
          That session recorded its state and had none to record.
```

**Why this distinction is load-bearing rather than pedantic.** `unknown` is a claim about the **record**;
`none` is a claim about the **work**. Rendering an absent record as "no diversions" asserts something nobody
established — that the work was straightforward. It is the same error as an empty `## Stack` heading, and the
same error the projection already forbids on the card side, where the rule reads: *empty asserts there were
no diversions, which is a claim; `unknown` asserts nobody wrote them down, which is the truth.*

**Why it recurs.** Both render as nothing on screen, so the cheap implementation — check whether the frame
list is empty — passes both cases identically and looks correct. The discriminator is one level up: does the
file exist at all.

**Gate failures:**

- The same outcome for both runs, in either direction.
- Run A rendering as "no diversions", "none", "0 deep", or an empty list.
- Run B rendering as `unknown`. A capture ran; the record is not missing.
- Creating a snapshot on run A. `show` writes nothing, including a placeholder.
- Erroring on run A. An absent snapshot is an ordinary state, not a fault.
