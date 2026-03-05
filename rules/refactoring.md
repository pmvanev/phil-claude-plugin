---
paths:
  - "**/*.{ts,tsx,js,jsx,py,go,rs,java,cs,rb,kt,swift,cpp,c,h,hpp,scala,clj,ex,exs,hs,ml,fs,fsx}"
---

# Refactoring Guide

Guidelines for refactoring, extracted from Martin Fowler's *Refactoring*, Kent Beck's *Tidy First?*, and Robert C. Martin's *Clean Craftsmanship*.

---

### Core Philosophy

> **"Make the change easy, then make the easy change."** — Kent Beck

---

### Definition

**Refactoring:** Changing code structure without changing behavior. Tests pass before; tests pass after.

---

### When to Refactor

- **First** — Before adding a feature; make the change easy
- **After** — After a change; you understand the code better now
- **Comprehension** — As you read; clarify for the next reader
- **Litter-pickup** — Leave code better than you found it

**When not to refactor:** Code you don't need to touch. Code easier to rewrite.

---

### The Cycle

1. Tests pass
2. Small structural change
3. Tests pass
4. Repeat or commit

If tests fail, undo. Try a smaller step. Never break the build.

---

### Separate Structure from Behavior

Keep refactoring commits separate from behavior-change commits. Mixed commits obscure intent and complicate review.

---

### Code Smells

Smells indicate where refactoring may help. Context determines action.

| Smell | Signal |
|-------|--------|
| **Duplicated Code** | Same structure in multiple places |
| **Long Function** | Does too much |
| **Long Parameter List** | Too many arguments |
| **Feature Envy** | Uses another module's data more than its own |
| **Data Clumps** | Data that travels together |
| **Primitive Obsession** | Primitives instead of small objects |
| **Shotgun Surgery** | One change touches many modules |
| **Divergent Change** | One module changes for multiple reasons |
| **Message Chains** | `a.getB().getC().getD()` |
| **Speculative Generality** | Hooks for futures that never arrive |
| **Comments** | Compensating for unclear code |

#### JSX Stanza Header Comments

A `{/* Section Label */}` comment preceding a block of JSX is the **Comments** smell in a React-specific form: the comment exists because the block has no name of its own. The fix is extraction — the name becomes the documentation, and the comment disappears.

Scan for `{/* ... */}` comments in JSX and ask: *could this block be a named function or component?*

**Extract when the stanza:**
- Has a single clear responsibility (the comment name already reveals it)
- Contains more than ~5 lines of JSX
- Would read naturally as a component name (`EnergySection`, `RowDeleteCell`, etc.)

**Skip extraction when:**
- The stanza is a single expression — the comment is a label, not a name for a block
- The stanza is a positional marker (e.g. `{/* Row */}` on a layout wrapper)
- Extraction would require threading so many props that the gain is lost

The comment is the symptom. Naming — through extraction — is the cure.

---

### Tidyings

Small, reversible structural changes. Low risk, high readability.

| Tidying | Action |
|---------|--------|
| **Guard Clauses** | Replace nested conditionals with early returns |
| **Dead Code** | Delete it; version control remembers |
| **Normalize Symmetries** | Similar code should look similar |
| **Reading Order** | Arrange for the reader; definitions before usages; stepdown rule |
| **Cohesion Order** | Group code that changes together |
| **Explaining Variables** | Name expressions |
| **Explaining Constants** | Name magic numbers |
| **Chunk Statements** | Separate logical groups with blank lines |
| **Extract Helper** | Name blocks; enable reuse |
| **One Pile** | Inline scattered code, then re-extract better |

---

### Key Refactorings

**Composing Methods**
- **Extract Function** — Name what a fragment does
- **Inline Function** — Replace call with body
- **Extract Variable** — Name an expression
- **Inline Variable** — Replace variable with expression

**Moving Features**
- **Move Function** — To the module that uses it most
- **Move Field** — To the class that uses it most
- **Slide Statements** — Group related code

**Simplifying Conditionals**
- **Decompose Conditional** — Extract condition and branches
- **Replace Nested Conditional with Guard Clauses** — Early returns
- **Replace Conditional with Polymorphism** — Branch per subclass

**Organizing Data**
- **Replace Primitive with Object** — Wrap in a class
- **Replace Temp with Query** — Method instead of variable

**Refactoring APIs**
- **Separate Query from Modifier** — Return or mutate, not both
- **Remove Flag Argument** — Separate functions per case
- **Preserve Whole Object** — Pass the object, not extracted values

---

### Economics

- **Coupling** — Cost of change propagation; reduce it
- **Cohesion** — Elements that change together live together
- **Constantine's Equivalence** — Software cost = change cost; change cost = coupling cost
- **Optionality** — Tidy code creates options; messy code forecloses them
- **Reversibility** — Refactorings are reversible; behavior changes may not be

---

### Safety

Refactoring without tests is gambling. Tests make refactoring safe.

- Run tests after every small change
- If a test fails, the bug is in the last change
- Small steps reduce risk
- Commit often

---

### The Mantra

**Structure and behavior are separate concerns. Change structure freely; preserve behavior absolutely. Small steps. Tests always pass.**
