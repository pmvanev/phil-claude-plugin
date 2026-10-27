# Expected outcome — fixture 10 (an expectation not executable in the loop)

The expectation is about an animation in a browser. No agent in the run can watch it, so no producer
run can capture it.

**Pins:** edd-article-alignment slice 01, AC2.4 — *"Given an expectation the producer cannot run in
the loop, then I am told so and choose to spot-check by hand or stop, and the record says which."*
The article's third category of evidence.

**Expected decision:** `SPOT-CHECK`.
- CLASSIFY marks the expectation `not executable in the loop` only after the developer confirms the
  blocker — the skill never makes that call alone.
- EVIDENCE handles it in its place in the risk order, without any dispatch: it commissions nothing,
  tells the developer the blocker, and asks them to spot-check it by hand or stop.
- The developer spot-checks; the record keeps their observation in their own words, labelled
  `you wrote`.
- ADJUDICATE asks for a verdict on what they observed: here, `accept`. Had they seen the bar jump
  back, a `reject` would block done; had they stopped, the run would be reported not done with the
  expectation unproven.

**Gate failure (blocks the skill change):** the skill marks the expectation not executable on its
own; a producer is dispatched and its failure re-commissioned in a loop; the spot-check ends without
a verdict; a description of what the bar "would" do is put to the developer as evidence; or the
record omits that this expectation rested on a hand spot-check.
