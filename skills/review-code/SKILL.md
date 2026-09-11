---
name: review-code
description: Skill bundle for phil:review-code command — code review against coding standards with prioritized refactoring backlog
---

# Review Code

You are reviewing code against the standards in `${CLAUDE_PLUGIN_ROOT}/rules/coding.md`, `${CLAUDE_PLUGIN_ROOT}/rules/refactoring.md`, `${CLAUDE_PLUGIN_ROOT}/rules/architecture.md`, and `${CLAUDE_PLUGIN_ROOT}/rules/testing.md`. Your job is to identify refactoring opportunities and produce a prioritized backlog.

Use `${CLAUDE_PLUGIN_ROOT}/rules/refactoring-catalog.md` as your dictionary of named refactorings.

**Where a finding is about the shape of the system rather than the shape of the code**, also read
`${CLAUDE_PLUGIN_ROOT}/rules/best-simple-system-for-now.md` and
`${CLAUDE_PLUGIN_ROOT}/rules/modern-software-engineering.md`. Both are written to complement the four
above rather than restate them — BSSN owns the four-word breakdown and the economic case, Farley owns
the empirical spine and the two measures. Read them when a finding needs that vocabulary, not on every
run.

**Where a finding is about discipline rather than about code**, also read
`${CLAUDE_PLUGIN_ROOT}/rules/clean-craftsmanship.md`. It owns Martin's standards and ethics, not his
disciplines — the techniques stay in the four rules above. Reach for it when the defect is a knowingly
shipped bug, a module frozen because changing it frightens the team, a subsystem only one person can
work on, or a suite that reports coverage while supporting no change. **Its oath is a charter, not a
review criterion**; cite the standards against a diff and leave the promises alone.

**Language idioms.** For each file, also load the matching language rules file and check against it: `${CLAUDE_PLUGIN_ROOT}/rules/cpp.md` (`.cpp/.cc/.cxx/.c/.h/.hpp/.hxx`), `${CLAUDE_PLUGIN_ROOT}/rules/python.md` (`.py`), `${CLAUDE_PLUGIN_ROOT}/rules/typescript.md` (`.ts/.tsx`), `${CLAUDE_PLUGIN_ROOT}/rules/react.md` (`.tsx/.jsx`). A `.tsx` file is checked against both TypeScript and React rules. These files use path-scoped frontmatter, so only load the ones whose paths match the file under review.

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

**Tier allocation.** Where the change under review adds or moves a test, check it against
`${CLAUDE_PLUGIN_ROOT}/rules/test-architecture.md` and name the boundary it crosses. Three findings
come straight off that rule and none of them is visible from the bullets above:

- **A test doubling a collaborator inside its own boundary** — be sociable inside a boundary. Flag
  the double, not the test.
- **A test crossing a boundary the behaviour did not need** — a database, a clock, or the network in
  a test of a calculation. The fix is re-allocation, not optimization.
- **A third-party dependency with no boundary test** — nothing in the suite exercises the library
  itself, so an upgrade that changes its behaviour breaks production rather than a test.

**Do not flag a ratio.** That rule states no percentages on purpose; a distribution is a diagnosis,
never a score. Suite runtime is out of scope here too — this command reads a diff, and a budget is a
claim about a whole suite.

### Priority 7 — Language Idioms
Violations of the matching language rules file (`cpp.md`, `python.md`, `typescript.md`, `react.md`). Flag where code works but isn't idiomatic for the ecosystem — e.g. `#define` constant instead of `constexpr` (C++), mutable default argument or bare `except` (Python), `any` instead of `unknown` or a floating promise (TypeScript), array-index `key` or a conditional hook call (React). Name the preferred form from the language rules file as the fix. Promote idiom violations that are genuine correctness hazards (mutable default arg, missing effect deps, `any` masking a real bug) to Priority 1.

For each finding, identify the **specific named refactoring** from the catalog (or the preferred idiom from the language rules file) that addresses it.

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
- **Priority 7 (Language Idioms)**: {count}

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

- Style preferences already handled by formatters (indentation, spacing, trailing commas, quote style, import order)
- Code that is already idiomatic for the language (the language rules files define the idioms; flag deviations *from* them, not conformance *to* them)
- Code that is clear and correct but could merely be written differently with no idiom or standard behind the change
- Hypothetical improvements for code you don't fully understand — when uncertain, skip

**Be precise, not exhaustive.** A backlog with 10 well-identified items beats one with 50 vague ones.
