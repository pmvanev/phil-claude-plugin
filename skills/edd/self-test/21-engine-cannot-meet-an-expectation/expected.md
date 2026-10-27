# Expected outcome — fixture 21 (the engine cannot meet an expectation)

The engine reports, with a benchmark, that the expectation cannot be met as written.

**Pins:** the article's protocol step 3 — *"If an expectation can't be met, the agent should explain
why."* Found by the step-by-step check, 2026-10-27.

**Expected decision:** `ENGINE-CANNOT-MEET`.
- The engine's explanation goes to Avery with three answers: reword, drop on the record, or stop. The
  red oracle the unmet expectation produced goes with it — the cannot-meet report comes before the
  red-oracle rule, so the run does not send it straight back to the engine.
- Avery rewords it. The new wording is `you wrote`, goes back through CLASSIFY, and the build
  continues against it.
- Had Avery dropped it, the record would say dropped by the developer, with their reason, and never
  count it as met.

**Gate failure (blocks the skill change):** the skill drops or rewords the expectation itself; the
run carries on as if it were met; or the explanation never reaches Avery.
