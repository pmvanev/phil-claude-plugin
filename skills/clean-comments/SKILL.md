---
name: clean-comments
description: Skill bundle for phil:clean-comments command — comment cleanup rules
---

# Clean Comments

You are applying the comment rules from `~/.claude/rules/coding.md` and the writing standards from `~/.claude/rules/writing.md`. The best comment is code that needs no comment.

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

1. Read the file with surrounding context.
2. Apply the **comment rules** below to the selected block only.

---

## Method/Function Name

1. Find the method using Grep and Glob. Read it with full context.
2. Clean its docstring and all inline comments using the rules below.

---

## File Path

1. Read the entire file.
2. Apply the comment rules to every comment and docstring in the file.
3. Report a summary: how many comments deleted, how many rewritten, how many kept.

---

## Directory Path

1. Glob recursively for code files (`**/*.{ts,tsx,js,jsx,py,go,rs,java,cs,rb,kt,swift,cpp,c,h,hpp,scala,clj,ex,exs,hs,ml,fs,fsx}`).
2. Apply the **File Path** analysis to each file.
3. Summarize changes per file.

---

## Comment Rules

Apply these in order:

### 1. Delete Commented-Out Code

Version control remembers. Commented-out code is dead code. Remove it.

```
// const oldValue = calculateLegacy(x);
// if (oldValue > threshold) { ... }
```

Delete entirely.

### 2. Delete Redundant Comments

Comments that restate what the code already says. The code is the source of truth.

```python
i += 1  # increment i
```
```javascript
// Set the name
setName(name);
```
```python
def get_user():  # gets the user
```

Delete these. The code speaks for itself.

### 3. Keep or Improve "Why" Comments

Comments explaining business logic, non-obvious decisions, workarounds, or constraints are valuable. Keep them. If the wording is unclear, rewrite for clarity.

Good examples to keep:
```python
# Retry 3 times because the payment gateway drops connections under load
```
```javascript
// Must sort before filtering — the API returns inconsistent order
```
```go
// HACK: upstream API returns 200 with error body; fixed in v3.2
```

### 4. Simplify Verbose Docstrings

Remove boilerplate. Keep: purpose, parameters, return value, exceptions. Cut filler.

**Before:**
```python
def calculate_tax(amount, rate):
    """
    This function is used to calculate the tax amount.
    It takes in the amount and the rate and returns the
    calculated tax value by multiplying them together.

    Args:
        amount: The amount to calculate tax on.
        rate: The tax rate to use.

    Returns:
        The calculated tax amount.
    """
```

**After:**
```python
def calculate_tax(amount, rate):
    """Calculate tax by applying rate to amount."""
```

If the function name and signature already reveal everything, the docstring may be unnecessary. Delete it.

### 5. Tighten Remaining Comments

Apply writing standards to surviving comments:
- **Active voice** — "Retries on timeout" not "This is retried when a timeout occurs"
- **No needless words** — Cut filler: "basically", "actually", "in order to", "note that"
- **Definite and specific** — "Caches for 5 minutes" not "Caches for a while"
- **No qualifiers** — Drop "very", "really", "quite", "rather"

### 6. Flag JSX Stanza Comments

`{/* Section Label */}` comments preceding a JSX block are the **Comments smell** in React form. The block lacks a name of its own.

**Do not extract** — that is `/extract-method`'s job. Instead:
- If the comment is the only issue, leave a note: `{/* TODO: extract to <ComponentName> */}`
- If the commented block is trivial (single expression, positional marker), leave it alone.
- If the comment is genuinely redundant with a nearby component name, delete it.

---

## Safety

- This is a **structure change only**. Do not change logic, fix bugs, or add features.
- Deleting a comment never changes behavior. But read carefully — some comments contain `TODO`, `FIXME`, `HACK`, or `@ts-ignore` directives that serve a purpose. Preserve those unless they are clearly stale.
- When uncertain whether a comment is redundant, keep it. False deletions cost more than false keeps.
