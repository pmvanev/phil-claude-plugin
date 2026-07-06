# Slice 04 — Redesign flaky / nondeterministic tests *(last, most tentative)*

**Goal:** Rewrite flaky tests deterministically (inject clock, seed RNG, remove hidden shared
state) under the same human-approved loop, with an added stability check.

**IN scope**
- Detect the flakiness/determinism smell (`datetime.now()`, unseeded random, order-dependence).
- Propose a deterministic rewrite (static timestamp, seeded RNG, injected clock) per
  `rules/testing.md` §Achieving Determinism.
- Same loop + safety guarantees as S1.
- Add an **N-run stability sanity check** before the human gate (confirm the flake is gone).
- Report if the smell class appears to want a different oracle.

**OUT scope**
- Concurrency-race fixes requiring production-code changes (SUT is out of scope).
- Any automated coverage oracle.

**Learning hypothesis**
Disproves *"flakiness belongs in this skill"* if the re-run stability oracle proves a poor fit for
the coverage-oriented loop — in which case flakiness spins off into its own skill.

**Acceptance criteria** — S4 AC4.1–AC4.3 (see feature-delta.md).

**Dependencies:** S1 loop; `rules/testing.md` determinism table.

**Effort estimate:** ≤1 day.

**Reference class:** S1 (same loop, new move + stability check).

**Production data:** a real flaky test (or a deterministically-seeded reproduction).

**Dogfood moment:** maintainer approves one real determinism fix and confirms N-run stability.

**Pre-slice SPIKE:** none, but this slice is explicitly the go/no-go for keeping flakiness in-scope.
