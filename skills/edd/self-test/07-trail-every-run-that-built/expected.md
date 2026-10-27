# Expected outcome — fixture 07 (a trail for every run that built)

The loop completed with one qualitative expectation adjudicated and **accepted** on real executed
evidence. The fixture contrasts two other runs: fixture 01's opt-out run, which built, and a run the
developer stopped at CAPTURE, which did not.

**Pins:** edd-article-alignment AC5.1 (pulled into slice 01, because retiring the off-ramp leaves no
other rule for an opt-out run), edd-loop AC3.1 + AC3.3 — *"Given a run that built, opt-out runs
included, then the trail and evolution summary are written; given a run that stopped at capture,
nothing is."*

**Expected decision:** `DOCUMENT-TRAIL`. The tool writes, under
`docs/edd/export-failure-messages-helpful/`:
- `expectations.md` — the expectation, its provenance, its classification (qualitative + reason), and
  its routing;
- `evidence/` — the captured executed artifact (the verbatim run + reproduce command);
- `verdicts.md` — Avery's `accept` verdict, a timestamp, and a reference to the evidence.

and a durable summary at `docs/evolution/<date>-export-failure-messages-helpful.md`.

**Three checkable assertions (all must hold):**
1. **This** run creates the trail — `expectations.md`, `evidence/`, `verdicts.md`, and `stabilize.md`
   with the pin and the review findings — plus the evolution summary.
2. Fixture 01's opt-out run creates a trail whose `verdicts.md` names each checkable expectation as
   `trusted to the tests`.
3. A run stopped at CAPTURE creates **zero** trail files.

**Gate failure (blocks the skill change):** a run that built leaves no trail (an opt-out recorded
nowhere is the silent trust this feature removes); or a capture-only stop writes one.
