---
name: refactor
description: Skill bundle for phil:refactor command — iterative refactoring from backlog with test verification
---

# Refactor

You are performing systematic refactoring against the standards in `~/.claude/rules/coding.md`, `~/.claude/rules/refactoring.md`, and `~/.claude/rules/refactoring-catalog.md`. You work through a prioritized backlog, one item at a time, verifying with tests at every step.

**This is structure-only work. Preserve behavior absolutely.**

## Parse the Argument

| Pattern | Type | Action |
|---------|------|--------|
| No argument | Backlog mode | Read `.refactoring-backlog.md` and work through it |
| `--changes` | Inline mode | Run `/phil:review-code --changes` first, then refactor |
| Has a file extension | Inline mode | Run `/phil:review-code {file}` first, then refactor |
| Ends with `/` or directory | Inline mode | Run `/phil:review-code {dir}` first, then refactor |

---

## Prerequisites

### Locate the Test Runner

Before starting any refactoring, determine how to run tests:

1. **Check CLAUDE.md first.** Read the project's `CLAUDE.md` for a declared test command (look for headings or keys like "Test", "Testing", "Test Commands", "test runner", or shell commands like `npm test`, `pytest`, `cargo test`, `go test`). If found, use it — the user has told you the answer.
2. If CLAUDE.md has no test command, auto-detect:
   - Check for `package.json` scripts (`test`, `test:unit`)
   - Check for `pytest.ini`, `setup.cfg`, `pyproject.toml`
   - Check for `Makefile` test targets
   - Check for `go.test`, `cargo test`, etc.
3. Run the test command once to verify it works before starting.

If no test runner is found by either method, warn the user: "No test runner detected. Refactoring without tests is risky. Continue anyway?" Use AskUserQuestion and await confirmation before proceeding.

### Load the Backlog

Read `.refactoring-backlog.md`. If it doesn't exist and no inline argument was given, tell the user to run `/phil:review-code` first.

Parse all items with `Status: pending` into a working list, already sorted by priority.

Create a task list from the pending backlog items using TaskCreate for progress tracking.

---

## The Refactoring Loop

For each pending item in priority order:

### Phase 1: Understand

1. Read the file and lines referenced in the backlog item.
2. Read surrounding context — callers, callees, related tests.
3. Confirm the smell still exists (code may have changed since the review). If the smell is gone, mark the item `resolved (incidental)` and move on.
4. Identify the specific named refactoring to apply.

### Phase 2: Verify Tests Pass

Run the test suite (or relevant subset) **before** making changes. Tests must pass as a baseline. If tests fail before you touch anything, stop and report the failure — do not refactor on a red test suite.

### Phase 3: Apply the Refactoring

Apply the named refactoring in the **smallest possible step**:

- **Extract Function**: Identify the block, choose a name, extract, replace with call.
- **Guard Clauses**: Invert the condition, return early, remove nesting.
- **Move Function**: Cut from source, paste to destination, update all references.
- **Rename**: Change the name everywhere it appears.
- And so on — follow the mechanics described in the refactoring catalog.

Rules:
- One refactoring per step. Do not bundle.
- Do not change behavior. Do not fix bugs. Do not add features.
- Do not add comments, docstrings, or type annotations to code you didn't change.
- Preserve the existing code style (naming convention, formatting).

### Phase 4: Verify Tests Still Pass

Run the test suite again. If tests fail:
1. The refactoring broke something. **Undo the change immediately.**
2. Try a smaller step.
3. If the smaller step also fails, mark the item `blocked (test failure)` with a note explaining what happened. Move on.

### Phase 5: Inner Tidying Loop

After the primary refactoring succeeds, re-read the changed code. Ask:

- Does the extracted function itself need tidying? (Guard clauses, explaining variables, reading order)
- Does the calling code read better now, or does it need adjustment?
- Are there naming improvements that became obvious after extraction?

Apply small tidyings. Run tests after each one. Stop when the code respects the coding guide's standards for that function/area. Do not expand scope beyond the code you just changed.

### Phase 6: Commit

After the primary refactoring and inner tidyings pass tests, commit the changes. Stage only the files you modified for this backlog item.

Commit message format:
```
Refactor [{id}]: {named refactoring} — {one-line description}

{smell} in {file-path}:{lines}. Applied {named refactoring}.

Co-Authored-By: Claude <noreply@anthropic.com>
```

Example:
```
Refactor [R003]: Extract Function — pull discount logic from processOrder

Long Function in src/order.py:42-87. Applied Extract Function.

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Phase 7: Update the Backlog

1. Mark the current item's status as `done` in `.refactoring-backlog.md`.
2. Update the corresponding task via TaskUpdate.
3. **Prune pass**: Scan remaining `pending` items. For each, check if the refactoring you just performed incidentally resolved it:
   - Code was moved/renamed and the smell no longer exists at the referenced location
   - Duplicated code was extracted and the other instance now calls the shared function
   - A long function was broken up and sub-items about that function are now moot
4. Mark incidentally resolved items as `resolved (incidental)` with a note.
5. Report progress: "{N} of {total} items complete. {M} pruned. Next: [{id}] {description}"

### Phase 8: Repeat

Continue to the next `pending` item. Repeat the full cycle.

---

## Stopping Conditions

Stop the loop when:

1. **All items are `done` or `resolved`** — Report: "Backlog complete. All refactoring items addressed."
2. **All remaining items are `blocked`** — Report the blocked items and why.
3. **User interrupts** — Save progress to the backlog file so it can be resumed.

---

## Resuming

When invoked with no argument and a `.refactoring-backlog.md` exists with pending items, resume from where you left off. Do not re-review — just continue the loop.

---

## Final Report

When the backlog is complete, report:

1. Items completed (with brief description of each refactoring applied)
2. Items pruned (incidentally resolved)
3. Items blocked (with reasons)
4. Summary of structural improvements

Suggest: "Run `/phil:review-code` again to verify standards compliance, or review the changes with `git diff`."

---

## Safety Rules

- **Never refactor on a red test suite.** Verify green before and after every change.
- **Never bundle refactorings.** One atomic change, one test run.
- **Never change behavior.** If you notice a bug while refactoring, note it but do not fix it.
- **Never expand scope.** Only touch code directly related to the current backlog item and its immediate tidying.
- **Undo on failure.** If tests break, revert. Do not debug forward during a refactoring step.
- **Commit after each item.** One commit per backlog item (primary refactoring + inner tidyings). Never bundle multiple backlog items into one commit.
