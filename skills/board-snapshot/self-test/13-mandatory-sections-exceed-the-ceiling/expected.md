# Expected — BSNAP-SELFTEST-13

`SNAPSHOT-CLIPPED` · `READ-ONLY`

## What must happen

All 14 blocked cards print, each naming what it waits on. All 5 in-flight cards print. The queued section
prints nothing and says all 12 were withheld.

**The output breaches 200 words, and says so.** One clause states that the mandatory sections alone
exceeded the ceiling.

## What must NOT happen

No blocked or in-flight card is dropped, and none is collapsed into a count. A count is a dropped card
wearing a number.

The breach is not silent. A run that quietly overran would leave a reader believing a bound that did not
hold, which is worse than either the breach or the drop.

`SNAPSHOT-RENDERED` is wrong: it would read as a board that simply had nothing queued.

## Why this fixture exists

The ceiling and the never-drop rule are both stated as absolutes, and on a stuck board they cannot both
hold. Before this fixture the skill had no tiebreak, so the one case where the rules matter had no
defined answer.

Fixture 01 cannot cover it. There the mandatory sections fit and the queued section gives ground; here
they do not fit and the ceiling yields instead. The two have opposite outcomes, and a fixture asserting
both would be unsatisfiable — which is exactly what fixture 01's prose claimed before it was corrected.
