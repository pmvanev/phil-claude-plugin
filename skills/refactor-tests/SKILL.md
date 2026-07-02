---
name: refactor-tests
description: Skill bundle for phil:refactor-tests command — human-approved, structure-only test refactoring loop
---

# Refactor Tests

You clean test code to the structure standards in `~/.claude/rules/testing.md` (and the matching
language rules) **without silently weakening what the tests verify**. You work through a
prioritized backlog one item at a time, and **every change is applied only after the developer
approves the diff**.

**This is structure-only, assertion-preserving work.** The test *is* the safety oracle, so a
green suite alone cannot prove an assertion was not weakened — **the human is the oracle**
(a green suite is only a secondary sanity check). Never change what a test asserts, never split
or merge assertions, never delete a test, never fix determinism/flakiness. Those are behavior
changes and are out of scope.

## The five moves you may propose (D5)

Only these assertion-preserving structure moves. If a smell is not one of these, do **not**
report or apply it.

| Smell | Named move | Why it is assertion-preserving |
|-------|-----------|--------------------------------|
| Duplicated setup (same arrange across ≥2 tests) | **Extract Fixture/Helper** | moves setup into a shared fixture/helper; assertions unchanged |
| Missing AAA (arrange/act/assert interleaved) | **Reorder into Arrange-Act-Assert** | reorders statements; same asserts, same values |
| Vague test name | **Rename** | renames the test; body and asserts unchanged |
| Long test with a repeated/extractable block | **Extract Test Helper** | extracts a block to a helper; each assert preserved verbatim |

**Never in scope:** tightening loose assertions, assert-splitting, determinism fixes (static
timestamps, seeded RNG, injected clocks), deleting dead/duplicate tests, mocking changes. These
change what the suite verifies.

## Detection heuristics (per language)

Detect only test files matching the globs in `rules/testing.md` frontmatter — the **same set that
file scopes itself to** (AC1.3). Do not hand-maintain a divergent list; if `testing.md` changes,
this follows it. The current set: `**/*.test.{ts,tsx,js,jsx}`, `**/*.spec.{ts,tsx,js,jsx}`,
`**/test_*.py`, `**/*_test.{go,py,rs}`, `**/*.test.py`, `**/*Test.java`, `**/*_test.rb`, and
anything under `**/tests/**`, `**/__tests__/**`, `**/test/**`. Non-test files (the SUT) are never
scanned or refactored. v1 **acts on Python + TypeScript/React only** — files matched by the
Java/Ruby/Go globs are recognized as tests but skipped with a one-line note until their per-language
heuristics land (D6, extensible).

| Smell | Python signal | TypeScript/React signal |
|-------|---------------|-------------------------|
| Duplicated setup | identical arrange statements (same literals/construction) repeated in ≥2 `def test_*` bodies | same arrange repeated across ≥2 `it()`/`test()` blocks; no shared `beforeEach`/helper |
| Missing AAA | asserts interleaved between multiple acts; no arrange→act→assert separation | `expect(...)` calls interleaved with actions; no clear setup/act/assert grouping |
| Vague name | name that states no behavior: `test_1`, `test_it_works`, `test_case`, `test_foo`, `test_method`, `test_func` | `it("works")`, `it("test 1")`, `test("case")`, names with no behavior clause |
| Long test w/ extractable block | test body long (~>15 statements) or a repeated multi-line block usable as a helper | long `it()` body or a repeated build/assert block extractable to a helper |

When unsure whether a flag is a true D5 smell, **skip it** — false positives erode trust
(detection-precision KPI: ≤20% rejected on first review). Be precise, not exhaustive.

## Parse the argument

| Pattern | Mode | Action |
|---------|------|--------|
| `--review <path>` | Review | Detect smells under `<path>`, write `.test-refactoring-backlog.md`, **stop** (no changes). |
| A file path or `test-id` | Scoped loop | Run the approval loop scoped to that file/test only. |
| No argument | Backlog loop | Work the existing `.test-refactoring-backlog.md` one approved item at a time. |

---

## Prerequisites (all modes except review-only detection)

Run these three checks once, **in this order**, before the loop starts. Do not begin proposing
moves until all three pass.

### 1. Locate the test runner

Follow `skills/shared/test-runner-detection.md` (reuse). Prefer the `CLAUDE.md` test command;
else auto-detect (`package.json`, `pytest.ini`/`pyproject.toml`, `Makefile`, etc.). Run it once
to confirm it works before touching anything. If none is found, warn and use AskUserQuestion
before proceeding — refactoring tests without a runnable suite removes even the secondary sanity
check.

### 2. Confirm a clean working tree

The loop applies changes to the working tree and relies on `git checkout` to revert. If there
are uncommitted changes to the target test files, ask the developer to commit or stash first —
otherwise a revert could discard their work. Do this **before** the baseline run so no in-flight
work is ever at risk.

### 3. Establish a green baseline (safety rule — never refactor on red)

Run the suite **before** proposing any move. **If the baseline is red, STOP and report — do not
propose or apply anything.** A red baseline means the sanity check is meaningless and the repo
is mid-change; the developer must get to green first. (This is fixture `01-baseline-red-stop`.)

---

## Review mode — `--review <path>` (seeds the backlog)

1. Enumerate test files under `<path>` matching the `testing.md` globs. Ignore non-test files.
2. Detect only the four D5 smells (heuristics above). One backlog item per smell instance.
3. Write `.test-refactoring-backlog.md` in the project root, in `review-code`'s backlog format
   (by convention — do not modify `review-code`). Use this shape:

   ```markdown
   # Test Refactoring Backlog

   Generated: {date}
   Scope: --review {path}

   ## Summary

   - **Total items**: {count}
   - **Extract Fixture/Helper (duplicated setup)**: {count}
   - **Reorder into Arrange-Act-Assert (missing AAA)**: {count}
   - **Extract Test Helper (long test)**: {count}
   - **Rename (vague name)**: {count}

   ## Backlog

   ### [T001] {smell} — {one-line description}

   - **File**: `{file-path}`
   - **Lines**: {start}-{end}
   - **Priority**: {1-3}
   - **Smell**: {smell name} (D5)
   - **Move**: {named move}
   - **Rationale**: {which testing.md standard; note it is assertion-preserving}
   - **Status**: pending
   ```

   Rules: IDs sequential `T001`, `T002`, …; sort by priority then file; one atomic move per item;
   the move must be one of the four D5 moves; only D5 smells appear (no behavior-change or
   deletion items).
4. Report: total by move type, top items, and the backlog path. Suggest: "Run
   `/phil:refactor-tests` to work through this backlog." **Apply nothing in review mode.**

---

## The approval loop (scoped and backlog modes)

Load pending items (from `.test-refactoring-backlog.md`, or from a fresh scoped scan of the
target file/test). Create a task list with TaskCreate. For each pending item, in priority order:

### 1. Understand
Read the file and referenced lines plus surrounding context. Confirm the smell still exists
(code may have changed). If it is gone, mark `resolved (incidental)` and move on. Identify the
exact D5 move.

### 2. Verify green baseline
Run the suite (or the relevant subset). It must be green before you touch anything (see
Prerequisites). If it is red now, STOP and report.

### 3. Propose (leave a clean pre-screen seam)
Surface, to the developer:
- the **named move** (e.g. `Extract Fixture/Helper`),
- the **target** (`file:lines`),
- a **one-line rationale**.

**Do not print the diff in chat.** Apply nothing yet.

> Pre-screen seam (deferred critic, slice 04): before pausing for the human, this is where an
> automated test-diff critic would inspect the proposed change for assertion-set preservation
> and structure-only compliance. It is not built yet; the loop leaves the seam here and proceeds
> straight to apply-then-review.

### 4. Apply to the working tree
Apply the single move as the smallest possible edit. One move per item — never bundle. Preserve
existing style. Do not touch anything the move does not require.

### 5. Run the suite (sanity check)
- **If red → auto-revert immediately:** `git checkout -- <files>`, mark the item
  `blocked (post-apply red)` with the failing test as evidence, and continue to the next item.
  **Do not bother the developer with a broken change.** (Fixture `02-postapply-red-autorevert`.)
- **If green →** go to the human gate.

### 6. Human gate (the safety oracle — DD4 / ADR-002)
Pause and ask the developer to **review the uncommitted diff in their IDE/editor** (against git),
then answer via **AskUserQuestion** with four options:

- **approve** → the change preserves intent → commit it (step 7).
- **reject** → `git checkout -- <files>` revert; mark the item `skipped`; continue.
- **skip** → same revert as reject; mark `skipped`; continue.
- **quit** → `git checkout -- <files>` revert; stop the loop (progress is already saved in the
  backlog).

A green suite never overrides the human. Reject/skip/quit always revert cleanly and write
nothing. (Fixtures `03-approve-commit-on-green`, `04-reject-reverts-clean`.)

### 7. Commit (approve only)
Commit the single item — stage only the files this move touched. One commit per approved item.

```
Refactor tests [{id}]: {named move} — {one-line description}

{smell} in {file}:{lines}. Applied {named move}. Assertion-preserving; human-approved.

Co-Authored-By: Claude <noreply@anthropic.com>
```

### 8. Prune + report
Mark the item `done` (TaskUpdate too). **Prune pass:** re-scan each remaining `pending` item at
its referenced location and re-check its specific smell. If the smell no longer exists *because
the move you just landed removed it* (e.g. an Extract Fixture also removed the duplicated setup a
later item flagged in a sibling test, or a Rename made a "vague name" item moot), mark that item
`resolved (incidental) — by [{landed-id}]`. If the smell still exists, leave it `pending`. Report:
"{N} of {total} done, {M} pruned, next: [{id}] {description}".

### 9. Repeat
Continue to the next `pending` item.

---

## Scoped mode — a single file or test-id

Same loop, but detection and moves are scoped to that one target: scan only that file/test for
D5 smells, then run steps 1–9 over just those items. Same approve/suite/revert/commit
guarantees as the backlog loop. Use when the developer is working on one known-bad test and does
not want a full review.

---

## Stopping conditions
- All items `done`/`resolved` → "Backlog complete."
- All remaining items `blocked` → report them and why.
- Developer chooses **quit**, or interrupts → revert any in-flight change, save progress to the
  backlog, report where to resume. Re-invoking with no argument resumes from the next pending
  item (do not re-review).

---

## Safety rules (inherited from phil:refactor, adapted)
- **Never refactor on a red suite.** Verify green baseline before every item.
- **Auto-revert on post-apply red** — before the human is ever asked.
- **The human is the oracle.** A green suite is only a sanity check; reject/skip/quit always win.
- **One approved move, one commit.** Never bundle items or moves.
- **Structure-only.** Never change, split, or delete assertions; never fix behavior. Note bugs,
  do not fix them.
- **No chat diffs.** The developer reviews the real uncommitted diff in their editor.
- **Never expand scope.** Touch only what the current move requires.

---

## Self-test (regression gate)

`skills/refactor-tests/self-test/` holds golden fixtures that pin these safety behaviors
(baseline-red → stop; post-apply-red → auto-revert; approve → commit; reject → clean revert;
review → D5-only backlog). Whenever this skill changes, drive the fixtures per
`self-test/README.md` and confirm each produces its `expected.md` outcome — every edit here is
non-monotonic, so the skill is changed and regression-tested, never changed and eyeballed.
