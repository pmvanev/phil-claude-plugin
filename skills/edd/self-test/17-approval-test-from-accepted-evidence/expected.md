# Expected outcome — fixture 17 (an approval test pinned to the accepted evidence)

Avery accepted the qualitative expectation on the captured error message. No assertion captures
"helpful" — but the exact output Avery judged can be pinned.

**Pins:** edd-article-alignment slice 03, AC4.2 — *"Given an accepted qualitative output, then it is
pinned by an approval test whose approved output is the evidence I accepted."*

**Expected decision:** `PIN-APPROVAL`.
- STABILIZE asks the engine for an approval test whose approved output is the accepted evidence,
  verbatim: the two-line message and `exit=2`.
- Avery's accept counts as the approval test's first human read; no second approval is asked.
- STABILIZE checks the approved-output file against the accepted evidence byte for byte, and checks
  that the approval test passes in the oracle run the engine returns, asked for once the pins are
  committed; that run becomes `oracle_result`.
- Any later change to the message fails the test as a diff Avery sees.
- `stabilize.md` names the approval test and its approved-output file.

**Gate failure (blocks the skill change):** the qualitative expectation is left unpinned; the engine
is asked to assert "helpfulness" with a hand-written assertion; or an approved output that differs
from the evidence Avery accepted is counted as a pin.
