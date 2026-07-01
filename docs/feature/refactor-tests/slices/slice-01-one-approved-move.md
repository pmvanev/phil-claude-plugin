# Slice 01 — One approved move, end-to-end  (WALKING SKELETON)

**Goal:** Prove the human-approval oracle works: detect one smell type in a real test file,
propose a diff, apply only on approval, run the suite, commit.

**IN scope**
- Command `/phil:refactor-tests <file>` scoped to one file.
- Detect ONE smell type: duplicated setup → *Extract Fixture/Helper* (D5).
- Propose a single diff + named move + rationale.
- Human approve/reject gate (D2).
- On approve: apply, run suite, commit if green; auto-revert if red (D7).
- Baseline red → stop (D7).

**OUT scope**
- Backlog seeding / `--review` (slice 02).
- Other smell types, prioritization (slice 02).
- Whole-backlog loop (slice 03).

**Learning hypothesis**
Disproves that per-diff human approval is a workable oracle for test refactoring **if** Tess
finds reviewing each diff more burdensome than just editing the test herself.

**Acceptance criteria:** S2 AC2.1–AC2.5 (feature-delta.md).

**Production data + dogfood:** run against this plugin's own test files (e.g. under
`hooks/refactor-loop/` tests or `refactor/self-test/`). Dogfood the same day on a real
duplicated-setup smell in the repo.

**Dependencies:** `skills/shared/test-runner-detection.md`; git.

**Effort:** ≤ 1 day. **Reference class:** mirrors `phil:refactor` Phase 2–6 with an added
approval gate and no auto-apply.

**Pre-slice SPIKE:** none — mechanism is understood; risk is UX (approval burden), which the
learning hypothesis measures.
