# Expected outcome — fixture 07 (living docs, but only when the gate ran)

The loop completed with one qualitative expectation adjudicated and **accepted** on real executed
evidence. That is exactly the case where the expectations, evidence, and verdict should be persisted
as living documentation. The fixture also contrasts against fixture 01 (an off-ramp-only run), which
must leave **no** trail.

**Pins:** slice-02, AC3.1 + AC3.2 + AC3.3, KPI zero-ceremony — *"Completion with ≥1 adjudicated
qualitative expectation writes the trail + evolution summary; an off-ramp-only run writes no trail."*

**Expected decision:** `DOCUMENT-TRAIL`. The tool writes, under
`docs/edd/export-failure-messages-helpful/`:
- `expectations.md` — the expectation, its classification (qualitative + reason), and its routing;
- `evidence/` — the captured executed artifact (the verbatim run + reproduce command);
- `verdicts.md` — Avery's `accept` verdict, a timestamp, and a reference to the evidence.

and a durable summary at `docs/evolution/<date>-export-failure-messages-helpful.md`, reusing the
plugin's evolution convention.

**Two checkable assertions (both must hold):**
1. **This** run (the gate ran) creates the three-part trail + the evolution summary.
2. An **off-ramp-only** run (fixture 01) creates **zero** trail files — the trail directory does not
   exist. "Did this run add ceremony?" is observable as a filesystem fact.

**Gate failure (blocks the skill change):** either (a) an off-ramp-only run writes a
`docs/edd/<slug>/` trail (ceremony leak — violates the zero-ceremony KPI), or (b) a gated run
completes without persisting the expectations/evidence/verdicts (the living-documentation criterion
of EDD is lost — the intent and its proof evaporate with the session).
