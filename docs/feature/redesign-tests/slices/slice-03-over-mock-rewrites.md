# Slice 03 — Redesign over-mocked tests toward real collaborators

**Goal:** Extend the rewrite move set to replace excessive mocking with real collaborators or fakes,
under the same human-approved loop.

**IN scope**
- Detect the excessive-mocking smell (mocks everything; asserts on mock interactions).
- Propose a rewrite using a real collaborator or an existing fake.
- Same loop + safety guarantees as S1.
- If a needed fake/collaborator does not already exist → surface and SKIP the item (no unreviewed
  scaffolding).

**OUT scope**
- Building new fakes/test doubles as part of the rewrite (skip instead).
- Flakiness (S4).

**Learning hypothesis**
Disproves *"over-mock rewrites fit the same loop"* if they routinely require out-of-band fake
construction — signalling this family needs different handling.

**Acceptance criteria** — S3 AC3.1–AC3.2 (see feature-delta.md).

**Dependencies:** S1 loop; `rules/testing.md` Test Doubles guidance (mock/stub/fake definitions).

**Effort estimate:** ≤1 day.

**Reference class:** S1 (same loop, new move).

**Production data:** a real over-mocked test.

**Dogfood moment:** maintainer approves/rejects one real over-mock rewrite the same day.

**Pre-slice SPIKE:** none — but the skip-when-fake-missing rule is the key risk to watch.
