---
name: refactor
description: Skill bundle for phil:refactor command — iterative refactoring from backlog with test verification
---

# Refactor

Refactor systematically against the standards in `${CLAUDE_PLUGIN_ROOT}/rules/coding.md`, `${CLAUDE_PLUGIN_ROOT}/rules/refactoring.md`, and `${CLAUDE_PLUGIN_ROOT}/rules/refactoring-catalog.md`. Work through a prioritized backlog, one item at a time, verifying with tests at every step. A Priority 6 item takes its route from the Smell Catalogue in `${CLAUDE_PLUGIN_ROOT}/rules/test-patterns.md`, and no row routes here, so this loop skips every one (below).

**This is structure-only work. Preserve behavior absolutely.**

## Parse the Argument

| Pattern | Type | Action |
|---------|------|--------|
| No argument | Backlog mode | Read `.refactoring-backlog.md` and work through it |
| `--changes` | Inline mode | Review with `--changes` first, then refactor |
| Is a directory | Inline mode | Review `{dir}` first, then refactor |
| Has a file extension | Inline mode | Review `{file}` first, then refactor |

Inline mode reviews by reading and following `${CLAUDE_PLUGIN_ROOT}/skills/review-code/SKILL.md` over the
argument — this command's grant cannot invoke `/phil:review-code` — then works only the items under the
`Scope:` line the review just wrote.

---

## Prerequisites

### Confirm a clean working tree

Run `git status --porcelain -- . ':!.refactoring-backlog.md'`. If it prints anything, stop and ask the
developer to commit or stash (`git stash -u`) first: an undo restores files from HEAD and would discard
their edits.

### Locate the Test Runner

Follow `${CLAUDE_PLUGIN_ROOT}/skills/shared/test-runner-detection.md`. If it finds no runner, ask
before proceeding, and stop on any answer but a clear yes.

**This ask follows `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`.** Load it before the call.

- **What turns on it is that nothing will catch a behaviour change.** Say that, not "risky" — the
  consequence is the whole content of this decision.
- **The detection attempt goes in the context block**: what was looked for and where. The ask itself
  names no filenames.

### Load the Backlog

Read `.refactoring-backlog.md`. If it doesn't exist and no inline argument was given, tell the user to run `/phil:review-code` first.

Parse the items with `Status: pending` into a working list — in inline mode, only the items under the
`Scope:` line the review just wrote. Sort the working list by Priority: an extended backlog holds one
sorted block per review, not one sorted list.

**Work only the items routed to this command.** An item whose **Route** names another command —
`/phil:refactor-tests`, `/phil:redesign-tests` — or `report only` is not this loop's to apply. Mark it
`skipped (routed to {route})` and name it in the final report with the command that owns it. A backlog
written before routes existed carries no Route field; treat its Priority 6 items the same way, because
changing what a test asserts is behaviour change and this loop preserves behaviour.

Create a task list from the pending backlog items using TaskCreate for progress tracking.

---

## The Refactoring Loop

For each pending item in priority order:

### Phase 1: Understand

1. Read the file and lines referenced in the backlog item. Earlier commits in this run may have moved
   code, so where those lines no longer hold it, find the smell by its content before judging it gone.
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
1. The refactoring broke something. **Undo the change immediately**: `git checkout -- <files>` for the
   files the step modified, and remove any file the step created.
2. Try a smaller step.
3. If the smaller step also fails, mark the item `blocked (test failure)` with a note explaining what happened. Move on.

### Phase 5: Inner Tidying Loop

After the primary refactoring succeeds, re-read the changed code. Ask:

- Does the extracted function itself need tidying? (Guard clauses, explaining variables, reading order)
- Does the calling code read better now, or does it need adjustment?
- Are there naming improvements that became obvious after extraction?

Apply small tidyings. Run tests after each one; if a tidying goes red, undo only that tidying — reverse
its own edit, leaving the green primary refactoring — and stop tidying. Stop when the code respects the
coding guide's standards for that function/area. Do not expand scope beyond the code you just changed,
and leave a tidying that another pending item names to that item.

### Phase 6: Commit

After the primary refactoring and inner tidyings pass tests, commit only the files modified for this
backlog item — `git commit -m <message> -- <files>` — so nothing already staged rides along.

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
2. **All remaining items are `blocked` or `skipped (routed to …)`** — Report them, why, and for each routed item the command that owns it.
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
4. Items skipped as routed elsewhere, each with its route — the command to run, or `report only` for a human to apply. Those commands re-detect with their own rules and never read this backlog, so an item may not reappear there
5. Summary of structural improvements

Suggest: "Run `/phil:review-code` again to verify standards compliance, or review the changes with `git diff`."

---

## Safety Rules

- **Never refactor on a red test suite.** Verify green before and after every change.
- **Never bundle refactorings.** One atomic change, one test run.
- **Never change behavior.** If you notice a bug while refactoring, note it but do not fix it.
- **Never expand scope.** Only touch code directly related to the current backlog item and its immediate tidying.
- **Undo on failure.** If tests break, revert. Do not debug forward during a refactoring step.
- **Commit after each item.** One commit per backlog item (primary refactoring + inner tidyings). Never bundle multiple backlog items into one commit.
