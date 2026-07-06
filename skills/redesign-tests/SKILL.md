---
name: redesign-tests
description: Skill bundle for phil:redesign-tests command — human-approved, behaviour-changing test redesign loop with a coverage-equivalence claim per rewrite
---

# Redesign Tests

You rewrite tests that verify **how** the code works into tests that verify **what** it does —
turning implementation-coupled, over-mocked, and flaky tests into behaviour-focused ones. You work
a prioritized backlog one item at a time, and **every rewrite is applied only after the developer
approves the diff *and* its coverage-equivalence claim.**

**This is behaviour-CHANGING, human-gated work — the opposite pole from `phil:refactor-tests`.**
`refactor-tests` is structure-only and can promise coverage never shrank. This skill deliberately
changes *what a test asserts*, so it **cannot** make that promise automatically. The test is the
oracle, and here we are changing the test — so **the human is the sole oracle** (ADR-004). A green
suite is only a secondary sanity check; it can never prove a rewrite preserved coverage. That is
why every proposal carries a **coverage-equivalence claim** and why nothing is committed without
per-diff human approval.

> **Relationship to `phil:refactor-tests`.** If the smell is a structure-only one (duplicated setup,
> missing AAA, vague name, long test), that is `refactor-tests`' job — do not handle it here. This
> skill handles only behaviour-changing smells (below). The two use **separate** backlog files and
> never collide (ADR-003).

## The behavioural smells in scope (and their moves)

Only these three families. If a smell is not one of these, do **not** report or rewrite it.

| Smell family | Signal | Named move(s) | What the rewrite does |
|--------------|--------|---------------|------------------------|
| **Implementation-coupling** | asserts on a mock interaction (`mock.x.assert_called`), a private member (`obj._field`), or an internal call — not on an observable outcome | **Assert on observable outcome** | replace the how-assertion with one on the public result / persisted state / returned value |
| **Excessive-mocking** | mocks a collaborator that could be real (or a fake exists) and asserts only on the mock | **Replace mock with real collaborator**, **Replace mock with fake** | drive the real collaborator/fake; assert on the resulting state |
| **Flakiness / determinism** | depends on `datetime.now()`, unseeded RNG, UUIDs, wall-clock, ordering, or hidden shared state | **Inject clock / static timestamp**, **Seed RNG**, **Isolate shared state** | make the test deterministic while preserving what it checks |

**Never in scope:** structure-only cleanup (that is `refactor-tests`); deleting dead/duplicate
tests; splitting or merging test files; changing non-test (SUT) code; concurrency-race fixes that
require production changes. When unsure whether a flag is a true behavioural smell, **skip it** —
false positives erode trust (detection-precision KPI: ≤20% rejected on first review).

## Detection (reuse `review-code` Priority 6)

Detect against `review-code`'s **Priority 6 — Test Quality** taxonomy (tests coupled to
implementation, excessive mocking, flaky patterns) — do not fork a divergent list. Detect only test
files matching the globs in `rules/testing.md` frontmatter (the same set `testing.md` scopes itself
to). Non-test files (the SUT) are never scanned or rewritten. v1 acts on **Python + TypeScript/React
only**; files matched by other globs are recognized as tests but skipped with a one-line note.

## Parse the argument

| Pattern | Mode | Action |
|---------|------|--------|
| `--review <path>` | Review | Detect behavioural smells under `<path>`, write `.test-redesign-backlog.md`, **stop** (no changes). |
| A file path or `test-id` | Scoped loop | Run the approval loop scoped to that file/test only. |
| No argument | Backlog loop | Work the existing `.test-redesign-backlog.md` one approved item at a time. |

---

## Prerequisites (all modes except review-only detection)

Run these three checks once, **in this order**, before the loop starts.

### 1. Locate the test runner
Follow `skills/shared/test-runner-detection.md` (reuse). Prefer the `CLAUDE.md` test command; else
auto-detect. Run it once to confirm it works before touching anything. If none is found, warn and
use AskUserQuestion before proceeding — redesigning tests without a runnable suite removes even the
secondary sanity check.

### 2. Confirm a clean working tree
The loop applies changes to the working tree and relies on `git checkout` to revert. If there are
uncommitted changes to the target test files, ask the developer to commit or stash first — otherwise
a revert could discard their work. Do this **before** the baseline run.

### 3. Establish a green baseline (safety rule — never redesign on red)
Run the suite **before** proposing any rewrite. **If the baseline is red, STOP and report — do not
propose or apply anything.** (Fixture `01-baseline-red-stop`.)

---

## Review mode — `--review <path>` (seeds the backlog)

1. Enumerate test files under `<path>` matching the `testing.md` globs. Ignore non-test files.
2. Detect only the three behavioural smell families (above), reusing `review-code` Priority 6. One
   backlog item per smell instance.
3. Write `.test-redesign-backlog.md` in the project root, in `review-code`'s backlog **format** (by
   convention — do not modify `review-code`). Keep it **separate** from `.test-refactoring-backlog.md`
   (ADR-003) so the two tools never collide. Use this shape:

   ```markdown
   # Test Redesign Backlog

   Generated: {date}
   Scope: --review {path}

   ## Summary

   - **Total items**: {count}
   - **Implementation-coupling**: {count}
   - **Excessive-mocking**: {count}
   - **Flakiness/determinism**: {count}

   ## Backlog

   ### [RD001] {smell family} — {one-line description}

   - **File**: `{file-path}`
   - **Lines**: {start}-{end}
   - **Priority**: {1-3}
   - **Smell**: {smell family} (review-code P6)
   - **Rewrite intent**: {what the test should verify instead — the behaviour}
   - **Status**: pending
   ```

   Rules: IDs sequential `RD001`, `RD002`, …; sort by priority then file; one atomic rewrite per
   item; only behavioural smells appear (**no** structure-only D5 smells — those are `refactor-tests`);
   the SUT is never flagged.
4. Report: total by family, top items, and the backlog path. Suggest: "Run `/phil:redesign-tests`
   to work through this backlog." **Apply nothing in review mode.**

---

## The approval loop (scoped and backlog modes)

Load pending items (from `.test-redesign-backlog.md`, or a fresh scoped scan of the target). Create
a task list with TaskCreate. For each pending item, in priority order:

### 1. Understand
Read the file and referenced lines plus surrounding context. Confirm the smell still exists. If it
is gone, mark `resolved (incidental)` and move on. Identify the exact behavioural move and, for the
excessive-mocking family, whether the rewrite needs a real collaborator or fake.

### 2. Check the rewrite is constructible (skip-not-scaffold)
If the rewrite needs a **fake or collaborator that does not already exist** (e.g. a
`FakePaymentGateway` to observe charges, with no real gateway safe to call), **surface that and
mark the item `skipped (missing fake)`** — move on. **Never invent unreviewed test scaffolding**
and never edit the SUT to add one. (Fixture `06-missing-fake-skips`.)

### 3. Verify green baseline
Run the suite (or the relevant subset). It must be green before you touch anything. If it is red
now, STOP and report.

### 4. Propose (with the coverage-equivalence claim)
Surface, to the developer:
- the **named move** (e.g. `Assert on observable outcome`),
- the **target** (`file:lines`),
- a **one-line rationale**, and
- the **coverage-equivalence claim** — the load-bearing element (ADR-004):
  > *"The old test caught {regression class} by asserting {implementation detail X}. The rewrite
  > catches {the same regression class} by asserting {observable behaviour Y}."*

**Do not print the diff in chat.** Apply nothing yet.

> Pre-screen seam (deferred oracle): before pausing for the human, this is where a future automated
> coverage oracle (mutation testing / deliberate-break-and-confirm) would validate the
> coverage-equivalence claim. It is not built yet (v1 is human-only, DISCUSS D7); the loop leaves
> the seam here and proceeds to apply-then-review.

### 5. Apply to the working tree
Apply the single rewrite as the smallest possible edit. One rewrite per item — never bundle.
Preserve existing style. Touch only the test file the rewrite requires; **never the SUT.**

### 6. Run the suite (sanity check)
- **If red → auto-revert immediately:** `git checkout -- <files>`, mark the item
  `blocked (post-apply red)` with the failing test as evidence, and continue. **Do not bother the
  developer with a broken rewrite.** (Fixture `02-postapply-red-autorevert`.)
- **Flakiness family only:** additionally run the suite **N times** (default 5) to confirm the flake
  is gone. If it is not stable, treat as red → auto-revert, mark `blocked (unstable)`. (AC4.2.)
- **If green (and stable) →** go to the human gate.

### 7. Human gate (the sole oracle — ADR-004)
Pause and ask the developer to **review the uncommitted diff in their IDE/editor** (against git),
having shown them the **coverage-equivalence claim**. Then answer via **AskUserQuestion** with four
options:

- **approve** → the rewrite preserves the coverage the claim describes → commit it (step 8).
- **reject** → `git checkout -- <files>` revert; mark `skipped`; continue.
- **skip** → same revert as reject; mark `skipped`; continue.
- **quit** → `git checkout -- <files>` revert; stop the loop (progress saved in the backlog).

A green suite **never** overrides the human. Reject/skip/quit always revert cleanly and write
nothing. (Fixtures `03-approve-commit-on-green`, `04-reject-reverts-clean`.)

### 8. Commit (approve only)
Commit the single item — stage only the test file this rewrite touched. One commit per approved item.

```
Redesign tests [{id}]: {named move} — {one-line description}

{smell family} in {file}:{lines}. Rewrote to assert on behaviour. Human-approved;
coverage-equivalence claim validated at the gate.

Co-Authored-By: Claude <noreply@anthropic.com>
```

### 9. Prune + report
Mark the item `done` (TaskUpdate too). **Prune pass:** re-scan each remaining `pending` item and
re-check its smell. If a landed rewrite incidentally resolved it, mark `resolved (incidental) — by
[{landed-id}]`. Report: "{N} of {total} done, {M} pruned, {K} skipped, next: [{id}] {description}".

### 10. Repeat
Continue to the next `pending` item.

---

## Scoped mode — a single file or test-id

Same loop, but detection and rewrites are scoped to that one target. Same
approve/suite/revert/commit guarantees as the backlog loop.

---

## Stopping conditions
- All items `done`/`resolved` → "Backlog complete."
- All remaining items `blocked`/`skipped` → report them and why.
- Developer chooses **quit**, or interrupts → revert any in-flight change, save progress, report
  where to resume. Re-invoking with no argument resumes from the next pending item.

---

## Safety rules
- **Never redesign on a red suite.** Verify green baseline before every item.
- **The human is the sole oracle.** A green suite is only a sanity check; every commit requires
  approval of the diff *and* its coverage-equivalence claim. Reject/skip/quit always win.
- **Auto-revert on post-apply red** (and on flakiness-instability) — before the human is ever asked.
- **Skip, do not scaffold.** If a rewrite needs a fake/collaborator that does not exist, skip the
  item; never invent unreviewed test doubles and never edit the SUT.
- **One approved rewrite, one commit.** Never bundle items or moves.
- **Behaviour-changing, but honest.** You cannot prove coverage was preserved automatically (v1
  accepted risk, D7) — that is exactly why the human validates the coverage-equivalence claim.
- **No chat diffs.** The developer reviews the real uncommitted diff in their editor.
- **Never expand scope.** Touch only the test the current rewrite requires; never the SUT.

---

## Self-test (regression gate)

`skills/redesign-tests/self-test/` holds golden fixtures that pin these safety behaviours
(baseline-red → STOP; post-apply-red → auto-REVERT; approve → COMMIT; reject → clean REVERT;
`--review` → behavioural-only backlog; missing-fake → SKIP). Whenever this skill changes, drive the
fixtures per `self-test/README.md` and confirm each produces its `expected.md` outcome — every edit
here is non-monotonic, so the skill is changed and regression-tested, never changed and eyeballed.
