# Expected outcome — fixture 16 (an unpinned accepted expectation blocks done)

Both expectations were accepted. Asked to pin them, the engine names a test for the first and none
for the second.

**Pins:** edd-article-alignment slice 03, AC4.1 — *"Given an accepted expectation with no test
pinning it, then done is blocked."*

**Expected decision:** `BLOCK-DONE` until the pin lands.
- STABILIZE sends both accepted expectations to the engine; `/phil:edd` writes no test itself.
- "writes nothing" comes back pinned by nothing, so it goes to FINDINGS as a blocker.
- Avery answers `fix`: the engine writes the pinning test. That is not a rebuild — REVIEW does not
  re-run and no expectation is re-asked — but `phil:review-code` reviews the new test.
- `stabilize.md` records each expectation and the test that pins it.

**Gate failure (blocks the skill change):** the run is reported done with "writes nothing" unpinned;
`/phil:edd` writes the test itself; or the pinning fix triggers a rebuild and re-asks the developer.
