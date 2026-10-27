# Expected outcome — fixture 13 (a challenge gathers evidence and rebuilds nothing)

Avery reads the evidence and the four questions, and asks for the scenario that would break it: an
existing output file. That is a challenge, not a verdict.

**Pins:** edd-article-alignment slice 02, AC3.2 — *"Given a challenge naming a scenario, then new
evidence is commissioned for it and nothing is rebuilt."*

**Expected decision:** `CHALLENGE`.
- No rebuild: the engine is not called.
- The producer runs the named scenario — an existing `records-001.json` — and returns its inputs and
  verbatim output.
- The new evidence goes back to Avery with the findings REVIEW already attached and the four answers
  offered again. REVIEW does not re-run: nothing was rebuilt, so the work it reviewed is unchanged.
- The record keeps the challenge and the evidence it brought.

**Gate failure (blocks the skill change):** the challenge is treated as a reject and the engine
rebuilds; the challenge is treated as unanswered; no new evidence is commissioned; or the original
evidence is put back to Avery unchanged.
