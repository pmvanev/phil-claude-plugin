---
name: extract-method
description: Skill bundle for phil:extract-method command — method extraction rules
---

# Extract Method

You are performing the **Extract Function** refactoring. This is a structure-only change — preserve behavior absolutely. Follow the standards in `~/.claude/rules/refactoring.md` and `~/.claude/rules/coding.md`.

## Parse the Argument

Determine what `$ARGUMENTS` refers to:

| Pattern | Type | Example |
|---------|------|---------|
| Digits separated by `-` or `:` | Line range | `42-67`, `42:67` |
| Has a file extension | File path | `src/order.py`, `lib/utils.ts` |
| Ends with `/` or has no extension and is a directory | Directory path | `src/`, `src/services` |
| Otherwise | Method/function name | `processOrder`, `handle_request` |

If the argument contains both a file and a line range (e.g., `src/order.py:42-67`), split them.

---

## Line Range

1. Read the file (use surrounding context from the argument or the current working file).
2. Identify the selected block. Determine:
   - A descriptive **verb-phrase name** revealing intent (not mechanics).
   - Parameters the block needs (prefer passing objects over extracted values).
   - Return value, if any.
3. Extract into a new function. Replace the original block with a call.
4. Place the extracted function to maintain **reading order** (stepdown rule — callers above callees).
5. Verify: no logic changes, no behavior changes. Structure only.

---

## Method/Function Name

1. Find the method using Grep and Glob. Read it with full context.
2. Analyze for extraction candidates — look for:
   - **Comment-delimited sections** — a comment header followed by a block is the Comments smell; the name is the cure.
   - **Multiple abstraction levels** — high-level orchestration mixed with low-level detail.
   - **Blocks >10 lines doing one thing** — cohesive chunks that deserve a name.
   - **Repeated patterns** — similar logic appearing in sequence.
3. Extract the **smallest block first**, then re-read and repeat. Small steps.
4. After all extractions, verify the **stepdown rule**: the original method reads as a high-level narrative, each extracted method sits below it at a lower level of abstraction.

---

## File Path

1. Read the entire file.
2. Identify methods longer than 20 lines.
3. For each long method, apply the **Method/Function Name** analysis above.
4. Report a summary: which methods were found, what was extracted from each, and the new function names.

---

## Directory Path

1. Glob recursively for code files (`**/*.{ts,tsx,js,jsx,py,go,rs,java,cs,rb,kt,swift,cpp,c,h,hpp,scala,clj,ex,exs,hs,ml,fs,fsx}`).
2. Apply the **File Path** analysis to each file.
3. Summarize all extractions: file, original method, extracted methods.

---

## Naming Rules

- **Verb phrases** that reveal intent: `calculateDiscount`, `validate_email`, `fetchUserPermissions`.
- Never name after mechanics: not `doLoop`, `handleData`, `processStuff`.
- Match the language's naming convention (camelCase, snake_case, etc.).

## Parameter Rules

- Minimize arguments — zero is ideal, three requires justification.
- **Preserve Whole Object** — pass the object, not extracted fields.
- Avoid flag arguments — they signal the extracted method does two things.

## Safety

- Run tests after every extraction if tests exist.
- If a test fails, undo. Try a smaller step.
- Each extraction is a separate, reversible change.
- This is a **structure change only**. Do not fix bugs, add features, or change logic during extraction.
