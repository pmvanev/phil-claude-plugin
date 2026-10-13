# Expected outcome — fixture 11 (an uncertain refute reaches the human)

The judge refutes on uncertainty only after an honest attempt to confirm, and marks that refute with low
confidence so the orchestrator can tell it from a confident refute of a misread. Until 2026-10-13 the
skill dropped every refute and reported a count, so a real but subtle defect the judge could not see
vanished into "refuted 2".

**Pins:** VERIFY's filter and PRESENT's could-not-be-confirmed list, against
`agents/adversarial-verifier.md`'s low-confidence refute.

**Expected decision:** `UNCERTAIN-LISTED`. The orchestrator:
- Drops the empty-list finding, refuted at 0.9 with the guard quoted, and counts it.
- Lists the cache-key race separately as *could not be confirmed either way*, with the judge's basis.
- Leads with `draft-signal` (no oracle) and leaves "done" to the human.

**Checkable assertions (all must hold):**
1. The presentation says one finding was refuted and dropped.
2. The cache-key race appears under *could not be confirmed either way*, with its span and the judge's
   basis.
3. Neither finding is presented as confirmed, and nothing is called a clean pass.

**Gate failure (blocks the skill change):** the race is counted away with the confident refute (the
pre-2026-10-13 behaviour), OR it is presented as a confirmed finding (an uncertainty upgraded to a
defect), OR the review is reported as clean, OR as "refuted all 2".
