# Expected outcome — fixture 20 (the record is reviewed; the evidence and the developer's words are not)

The trail is drafted. One field holds the developer's own words, unpolished; one holds a sentence this
skill composed, with a participle tell and a passive. The evolution summary omits the pinning test.

**Pins:** edd-article-alignment slice 04, AC5.2–AC5.5.

**Expected decision:** `PROSE-REVIEWED`.
- This skill reads `rules/writing.md` and `rules/technical-communication.md` before composing.
- This skill writes each draft to a temporary directory outside the repository. The developer's field
  appears there as `[you wrote: expectation 1]`; the evidence appears only as its path.
- `phil:red-team-prose` reviews each draft by path, Steps 1 to 5 only. It never sees "doesnt" or
  "basically", so it cannot flag them.
- This skill asks: `apply`, `skip` or `stop` for the `[tells]` and `[clarity]` fixes. On `apply`, they
  land in the composed field only.
- The `[fitness]` finding blocks done. Avery answers `fix`; this skill adds the pinning test to the
  summary from what the run recorded, and the review no longer reproduces the finding.
- The drafts are copied into `docs/edd/export-failure-messages-helpful/`, the placeholder restored with
  Avery's words verbatim. The restored field matches what Avery wrote, and
  `evidence/01-missing-out-dir.txt` matches its capture hash.

**Gate failure (blocks the skill change):** the developer's words or the evidence reach the review; a
fix lands outside a composed field; `phil:red-team-prose`'s own Step 6 applies fixes; a draft touches
the working tree before the review; a check after writing is skipped; or the run is reported done
with the fitness finding standing.
