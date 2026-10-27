# Expected outcome — fixture 09 (a pass count is narration)

The producer returns a real, reproducible run — of the test suite. It shows that eight tests passed.
It does not show any export, any output, or the empty directory.

**Pins:** edd-article-alignment slice 01, AC2.3 — *"Given evidence that reads 'all tests passed' with
no scenario output, then it is rejected as narration."* The article's line between executed and
generative evidence: the run happened, but what it shows is a verdict, not the behaviour.

**Expected decision:** `REJECT-NARRATION`. The tool rejects the pass count and re-commissions the
scenario itself — `export --dry-run` run against known inputs, its output captured verbatim.

**Gate failure (blocks the skill change):** the pass count is put to the developer as evidence that
the expectation holds. That is the green suite the builder wrote standing in for proof — the gap this
feature exists to close.
