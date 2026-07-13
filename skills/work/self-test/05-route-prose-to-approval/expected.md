# Expected outcome — fixture 05 (prose wave → approval-based cleaner)

The wave changes a prose artifact (`sample_skill.md`) that has no executable test suite, so there
is no code oracle. Preservation falls back to the human-approval diff (D9).

**Pins:** slice-05 + DDD3 (routing) + DDD4/D9 (inherited oracle) — prose waves route to the
approval-based cleaner (`refactor-tests` / `redesign-tests`), whose human diff review IS the
preservation oracle (ADR-002).

**Expected decision:** `DELEGATE-TO-APPROVAL-CLEANER`. EXECUTE hands the wave to the prose delegate
and relies on that delegate's human-approval gate to certify preservation. `phil:work` runs **no
preservation gate of its own**.

**Gate failure (blocks the skill change):** the tool routes a prose artifact to the code loop (and
then finds no suite to gate on), or invents its own preservation check for prose instead of
inheriting the human-approval oracle. Either breaks the artifact-aware routing (DDD3) and the
inherited-oracle rule (DDD4/D9) — and would let a prose change land with no real oracle at all.
