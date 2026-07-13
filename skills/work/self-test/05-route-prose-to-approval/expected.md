# Expected outcome — fixture 05 (prose wave → approval-based cleaner)

The wave changes a **non-test** prose artifact (`sample_skill.md` — a skill file) that has no
executable test suite, so there is no code oracle. Preservation falls back to the human-approval
diff (D9).

**Pins:** slice-05 + DDD3 (routing) + DDD4/D9 (inherited oracle) — prose waves are certified by a
human-approval diff review (ADR-002), never by an orchestrator-run check.

**v1 routing boundary (surfaced in DELIVER — see `distill/upstream-issues.md`):** `refactor-tests`
and `redesign-tests` handle **test** prose only. A skill/rule/agent file has no dedicated
refactoring delegate in v1, so the wave uses the **ADR-002 human-approval diff gate directly**:
apply the smallest change, pause for the developer to review the uncommitted diff in their editor,
commit on approve / `git checkout` on reject.

**Expected decision:** `DELEGATE-TO-APPROVAL-CLEANER`. EXECUTE certifies preservation via the
human-approval diff (whether through `refactor-tests`/`redesign-tests` for test prose, or the
ADR-002 gate directly for other prose). `phil:work` runs **no preservation gate of its own** — the
human is the oracle.

**Gate failure (blocks the skill change):** the tool routes a prose artifact to the code loop (and
then finds no suite to gate on), or invents its own preservation check for prose instead of
inheriting the human-approval oracle. Either breaks the artifact-aware routing (DDD3) and the
inherited-oracle rule (DDD4/D9) — and would let a prose change land with no real oracle at all.
