# Expected outcome — fixture 15 (a stop over a standing challenge)

Avery challenges once, sees the new evidence, then stops instead of answering.

**Pins:** edd-article-alignment slice 02, AC3.4 — *"Given I stop over a standing reject or challenge,
then the run is reported not done and the record keeps it."*

**Expected decision:** `REPORT-NOT-DONE`.
- The stop is honoured at that round: nothing more is commissioned or asked.
- The trail under `docs/edd/export-failure-messages-helpful/` is written — the engine built — with the
  challenge, the evidence it brought, and the expectation recorded as unproven.
- The run is reported **not done**.

**Gate failure (blocks the skill change):** the stop is read as unanswered and the ask repeats; the
run is reported done; or the trail omits the standing challenge.
