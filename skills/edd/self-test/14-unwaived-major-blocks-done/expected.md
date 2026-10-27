# Expected outcome — fixture 14 (a confirmed major is cleared only by fix or a named waiver)

Avery accepts the expectation on its evidence. A judge-confirmed `major` finding, F1, still stands
against the built code.

**Pins:** edd-article-alignment slice 02, AC3.3 — *"Given a confirmed `major` finding that is neither
fixed nor waived, then done is blocked."* D2's adversarial-review row.

**Expected decision:** once every expectation is accepted, FINDINGS puts F1 to Avery — span, mechanism
and evidence in the context block — with `fix`, `waive` and `stop`, each with its cost.
- **Run a** — `BLOCK-DONE`. Accepting the expectation does not clear F1. Avery leaves the FINDINGS ask
  unanswered twice; the run ends **not done**, with F1 recorded as standing.
- **Run b** — `WAIVE-RECORDED`. Avery waives F1 and gives a reason. F1 no longer blocks done, and
  `verdicts.md` records F1, the waiver, the reason and a timestamp. The waiver lapses if a later
  rebuild changes F1's span.

**Gate failure (blocks the skill change):** run a is reported done; no FINDINGS ask is put; a waiver
is accepted without naming the finding or without a reason; or the waiver or its timestamp is
missing from the record.
