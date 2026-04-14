---
name: review-code
description: Skill bundle for phil:review-code command — code review against coding standards with prioritized refactoring backlog
---

# Review Code

You are reviewing code against the standards in `~/.claude/rules/coding.md`, `~/.claude/rules/refactoring.md`, `~/.claude/rules/architecture.md`, and `~/.claude/rules/testing.md`. Your job is to identify refactoring opportunities and produce a prioritized backlog.

Use `~/.claude/rules/refactoring-catalog.md` as your dictionary of named refactorings.

## Parse the Argument

Determine what `$ARGUMENTS` refers to:

| Pattern | Type | Example |
|---------|------|---------|
| `--changes` | Latest git changes | `--changes` |
| Has a file extension | File path | `src/order.py` |
| Ends with `/` or has no extension and is a directory | Directory path | `src/`, `src/services` |
| No argument | Default to `--changes` | |

---

## Step 1: Gather Code

### `--changes` (default)

Run `git diff HEAD~1 --name-only` to get changed files. Filter to code files only (exclude configs, lockfiles, generated files). Read each changed file in full, plus run `git diff HEAD~1 -- <file>` to see what changed.

### File Path

Read the entire file.

### Directory Path

Glob recursively for code files (`**/*.{ts,tsx,js,jsx,py,go,rs,java,cs,rb,kt,swift,cpp,c,h,hpp,scala,clj,ex,exs,hs,ml,fs,fsx}`). Read each file. For large directories (>20 files), use an Explore agent to parallelize reading.

---

## Step 2: Analyze Against Standards

For each file, check against the coding guide. Look for these categories of violations, in priority order:

### Priority 1 — Correctness & Safety
- Missing error handling at system boundaries
- Null/undefined hazards
- Resource leaks (missing cleanup, unclosed connections)
- Security vulnerabilities (injection, unsanitized input)

### Priority 2 — Structural Smells (High Impact)
- **Long Functions** — Functions longer than 20 lines
- **Large Class** — A class with many fields and methods. Look for cohesion clusters: groups of fields and methods that are used together but independent of other groups. Each cluster is a candidate for Extract Class. Signs: subsets of fields appear together in method signatures, methods only touch a subset of the class's fields, comments or naming prefixes that partition the class ("// payment fields", "// shipping methods")
- **Feature Envy** — Function uses another module's data more than its own
- **Shotgun Surgery** — One change would touch many files
- **Divergent Change** — One module changes for multiple reasons
- **Mixed Abstraction Levels** — High-level orchestration mixed with low-level detail
- **Dependency direction violations** — Business rules importing infrastructure

### Priority 3 — Naming & Readability
- Names that don't reveal intent
- **Long Parameter List** — Functions with more than 3 arguments. Check whether parameters could be replaced by a query the callee can make itself (Replace Parameter with Query), or whether an existing object already holds the values being passed (Preserve Whole Object)
- Flag arguments (boolean parameters that fork behavior)
- Missing explaining variables for complex expressions
- Magic numbers without named constants
- Violation of stepdown rule / reading order

### Priority 4 — Duplication & Design
- **Duplicated Code** — Same structure in multiple places
- **Data Clumps** — The same group of parameters (e.g., `startDate, endDate, timezone`) appears together across multiple function signatures. Scan for repeating parameter subsets across the file and module. Each recurring group is a candidate for Introduce Parameter Object or Extract Class. Also check for groups of fields that always appear together in classes
- **Primitive Obsession** — Primitives where domain objects belong
- **Message Chains** — `a.getB().getC().doSomething()`
- **Speculative Generality** — Code for futures that haven't arrived

### Priority 5 — Comments & Dead Code
- Commented-out code
- Redundant comments (restating what code says)
- Comments compensating for unclear code (fix the code, not the comment)
- Dead code / unreachable branches

### Priority 6 — Test Quality
- Missing tests for public functions
- Tests coupled to implementation rather than behavior
- Flaky test patterns (non-determinism, shared state)
- Excessive mocking

For each finding, identify the **specific named refactoring** from the catalog that addresses it.

---

## Step 3: Write the Backlog

Write findings to `.refactoring-backlog.md` in the project root. Use this exact format:

```markdown
# Refactoring Backlog

Generated: {date}
Scope: {argument — e.g., "--changes", "src/services/", "src/order.py"}

## Summary

- **Total items**: {count}
- **Priority 1 (Correctness)**: {count}
- **Priority 2 (Structure)**: {count}
- **Priority 3 (Naming)**: {count}
- **Priority 4 (Duplication)**: {count}
- **Priority 5 (Comments)**: {count}
- **Priority 6 (Tests)**: {count}

## Backlog

### [{id}] {smell-name} — {one-line description}

- **File**: `{file-path}`
- **Lines**: {start}-{end}
- **Priority**: {1-6}
- **Smell**: {smell name from catalog}
- **Refactoring**: {named refactoring from catalog}
- **Rationale**: {why this matters — which coding standard is violated}
- **Status**: pending
```

Rules for the backlog:
- IDs are sequential: `R001`, `R002`, etc.
- Sort by priority (1 first), then by file path within priority
- Each item is a **single, atomic refactoring** — not a bundle
- The refactoring name must match a named refactoring from the catalog
- Rationale must cite the specific principle or rule violated

---

## Step 4: Report

After writing the backlog, report to the user:

1. Total findings by priority
2. Top 5 highest-priority items with brief descriptions
3. The path to the backlog file
4. Suggest: "Run `/phil:refactor` to work through this backlog."

---

## What NOT to Flag

- Style preferences already handled by formatters (indentation, spacing, trailing commas)
- Language idioms that are correct for the ecosystem
- Code that is clear and correct but could be written differently
- Hypothetical improvements for code you don't fully understand — when uncertain, skip

**Be precise, not exhaustive.** A backlog with 10 well-identified items beats one with 50 vague ones.
