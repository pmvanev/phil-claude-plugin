# Expected outcome — fixture 02 (bias toward the off-ramp)

Two expectations arrive under-specified. The first has a cheaply-assertable core (non-zero exit,
stderr names the path). The second is *offered* as qualitative ("helpful") but with **no concrete
reason** why it can't be reduced to a cheap assertion.

**Pins:** slice-01, AC1.2 + AC1.3 — *"Ambiguous expectations default to engine-checkable, and the
tool asks to confirm before marking anything qualitative; an unjustified 'qualitative' is treated as
engine-checkable."* This is the honesty rule that keeps the whole feature from over-triggering.

**Expected decision:** `CLASSIFY-CHECKABLE` for both.
- The first expectation is classified engine-checkable (route the exit-code + stderr assertion to the
  engine).
- The second is **not** silently accepted as qualitative: the tool defaults it to engine-checkable
  and asks Avery to confirm, requiring a **concrete reason** ("what specifically can't a test assert
  cheaply here?") before it will ever open the evidence gate for it.

**Gate failure (blocks the skill change):** the tool marks "the error message should be helpful"
qualitative on its own, with no concrete stated reason and no confirmation from Avery, and opens the
evidence gate. That is the over-triggering failure — ceremony creeping in through a lazy
classification — and it erodes the bias-to-off-ramp that makes phil:edd trustworthy.
