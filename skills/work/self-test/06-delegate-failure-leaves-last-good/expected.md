# Expected outcome — fixture 06 (delegate failure mid-sequence)

A 3-wave roadmap. Wave 1's delegate lands green; wave 2's delegate fails (its suite goes red — or,
for a prose wave, its self-test breaks / its diff is rejected). This is the single most important
safety behaviour of the whole feature: **a run that broke something must never be reported as a
clean success.**

**Pins:** slice-02 + DDD4 sequencing gate — *"a wave failing its gate stops the sequence and names
the failed wave; the tree stays in its last-good state; the run is not reported as done."*

**Expected decision:** `STOP-LAST-GOOD`. On wave 2's delegate failure, the tool:
1. lets the delegate revert its own change (the delegates already `git checkout` on red / rejection),
2. **stops the sequence** — wave 3 is NOT run,
3. leaves the working tree in its **last-good** state (wave 1's committed result), never red,
4. records the failure in the decision trail (which wave, why),
5. reports the run as **stopped / incomplete** — never "done."

**Gate failure (blocks the skill change):** the tool continues to wave 3 after wave 2 failed; or
leaves the tree red; or reports the run as done/success despite the failed wave. Any of these is
the decorative-gate, silent-failure class this entire suite exists to catch — it would let
`/phil:work` claim victory over a broken tree.
