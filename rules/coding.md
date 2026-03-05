---
paths:
  - "**/*.{ts,tsx,js,jsx,py,go,rs,java,cs,rb,kt,swift,cpp,c,h,hpp,scala,clj,ex,exs,hs,ml,fs,fsx}"
---

# Coding Guide

Guidelines for writing clean code, extracted from Robert C. Martin's *Clean Code* and *Clean Craftsmanship*, Kent Beck's *Tidy First?*, Dan North's *Best Simple System for Now*, and MinimumCD.org.

---

### Core Philosophy

> **"Code is read far more often than it is written. Write for the reader."**

---

### Key Principles

#### 1. Test-Driven Development
- Write a failing test before writing production code
- Write only enough test code to fail
- Write only enough production code to pass
- Red, Green, Refactor—the cycle runs in seconds
- Tests are specifications; treat them as first-class citizens

#### 2. Naming
| Guideline | Example |
|-----------|---------|
| **Names reveal intent** | `isEligible` over `flag` |
| **Names are pronounceable** | `customerAddress` over `custAddr` |
| **Names are searchable** | `MAXIMUM_RETRY_COUNT` over `3` |
| **Class names are nouns** | `Customer`, `Account`, `Parser` |
| **Method names are verbs** | `save()`, `calculate()`, `send()` |
| **Avoid encodings** | `name` over `strName` |

#### 3. Functions
- Small. Then smaller. Twenty lines is long.
- Do one thing, do it well, do it only
- One level of abstraction per function
- Minimize arguments: zero is ideal, three requires justification
- Avoid flag arguments—they signal multiple responsibilities
- Prefer exceptions to error codes

#### 4. Reading Order
- **Stepdown rule** — Each function calls the next at a lower level of abstraction; read top to bottom like a narrative
- **Newspaper metaphor** — Headline at the top, details below; high-level functions first, helpers after
- **Definitions before usages** — Readers should not encounter a call before understanding what it does
- **Group by cohesion** — Code that changes together lives together

#### 5. Tidying
Small structural changes that ease behavior changes:

- **Guard clauses** — Replace nested conditionals with early returns
- **Dead code** — Delete it; version control remembers
- **Explaining variables** — Extract expressions into named variables
- **Explaining constants** — Replace magic numbers with named constants
- **Cohesion order** — Group code that changes together
- **Extract helper** — Name the block; enable reuse

*Tidy first when it makes the next change easier. Tidy after when you understand better. Never tidy code that doesn't matter.*

This is **empirical design**—structural decisions based on evidence, not speculation. You observe the change you need, assess the structure as it is, and decide if tidying would reduce the cost of the change.

#### 6. Comments
- The best comment is code that needs no comment
- If you must comment, explain *why*, not *what*
- Delete commented-out code
- Delete redundant comments

#### 7. Error Handling
- Use exceptions, not return codes
- Provide context: what operation failed and why
- Don't return null—return empty collections or throw
- Don't pass null—forbid it

#### 8. Resource Management (RAII / SBRM)
Use **RAII** (Resource Acquisition Is Initialization) or equivalently **SBRM** (Scope-Bound Resource Management) to tie resource lifetimes to object lifetimes. Resources are acquired in constructors and released in destructors—or in Python, using context managers.

#### 9. Testing Principles
| Principle | Meaning |
|-----------|---------|
| **Fast** | Tests run in milliseconds |
| **Independent** | Tests don't depend on each other |
| **Repeatable** | Same result every time, any environment |
| **Self-validating** | Pass or fail, no manual inspection |
| **Timely** | Written before or with the code |

The Testing Pyramid: many unit tests, fewer integration tests, fewest end-to-end tests.

#### 10. Simple Design
Kent Beck's four rules, in priority order:

1. **Pass all tests** — Non-negotiable
2. **Reveal intent** — Clear beats clever
3. **Remove duplication** — The root of maintenance nightmares
4. **Minimize elements** — After satisfying the first three

#### 11. The Best Simple System for Now
- **See what is really there** — Solve today's problem, not the imagined general case
- **Do not anticipate the future** — Speculative code ages unused and harbors bugs
- **Simple enables flexible** — Code so simple it can flex in any direction
- **Sketch, don't hack** — Just enough quality to sustain momentum
- **Context sets the bar** — Core logic demands rigor; experiments need less

#### 12. Refactoring
- Change structure without changing behavior
- Tests make refactoring safe; without tests, refactoring is gambling
- Refactor continuously, not in scheduled sprints
- Small improvements compound
- Each refactoring is reversible

#### 13. Evolutionary Coding
Practices that enable continuous integration while making large changes:

- **Branch by Abstraction** — Introduce an abstraction, implement new behavior behind it, migrate clients, remove old implementation
- **Connect Last** — Build complete features in isolation, wire up in final commit
- **Feature Flags** — Control visibility without blocking integration (use sparingly; remove within 2-4 weeks)

#### 14. SOLID Principles
| Principle | Guideline |
|-----------|-----------|
| **SRP — Single Responsibility** | A module has one reason to change—one stakeholder |
| **OCP — Open-Closed** | Open for extension, closed for modification |
| **LSP — Liskov Substitution** | Subtypes must be substitutable for their base types |
| **ISP — Interface Segregation** | Clients should not depend on methods they do not use |
| **DIP — Dependency Inversion** | Depend on abstractions, not concretions |

#### 15. The Humble Object Pattern
Separate testable logic from hard-to-test infrastructure. Push complexity into objects you can test; leave infrastructure objects "humble"—so simple they need no tests.

- **Presenters** contain formatting logic; **views** just render
- **Interactors** contain business logic; **database gateways** just fetch and store
- **Controllers** contain routing logic; **HTTP handlers** just parse requests

When a class is hard to test, extract the logic into a testable collaborator.

**The DAO Pattern** is a humble object for data access. The DAO handles SQL, connections, and transactions—mechanics that resist testing. Business logic calls an abstract interface; tests substitute a fake. Keep DAOs thin: fetch, store, delete. If a DAO contains conditionals or calculations, extract that logic into a testable service.

#### 16. CUPID Properties
Joyful code exhibits these qualities:

| Property | Meaning |
|----------|---------|
| **Composable** | Plays well with other code; minimal dependencies |
| **Unix philosophy** | Does one thing, obviously and comprehensively |
| **Predictable** | Consistent behavior, observability, and failure modes |
| **Idiomatic** | Uses patterns familiar to experienced developers |
| **Domain-based** | Intention-revealing in naming and structure |

You can write joyful code as fast as—faster than—hacky code. It requires habits, not heroics.

---

### The Essential and the Arbitrary

Every discipline has essential and arbitrary parts. The essential delivers value—tests proving correctness, refactoring preserving behavior, clear naming revealing intent. The arbitrary is convention—brace placement, file organization, spacing preferences.

Techniques like TDD or pair-programming are tools—neither necessary nor sufficient, but often helpful. The "four laws" of TDD are not set in stone. You *can* design code first, then test it. The essential part of TDD is confidence: confidence changing code, confidence cleaning code, confidence extending code.

**The essential is non-negotiable. The arbitrary adapts to context.**

---

### Development Rhythm

**Complete before continuing.** Write one test, make it pass, then tidy—code and test alike—before writing the next test. Extract helpers. Name constants. Delete duplication. Polish until the code teaches the next reader.

At a larger scale, develop and polish one module before starting the next. This discipline compounds:

- Reusable functions emerge from refactoring
- Test fixtures become shared infrastructure
- Patterns crystallize into conventions
- Each module builds faster than the last

> **"The kinds of projects that juice me are ones where building the project creates infrastructure for continuing to build the project."** — Kent Beck

The goal is not just working software. The goal is working software *and* the tools to build more of it. Red-Green-Refactor is not just a testing discipline—it is an investment strategy.

---

### Code Quality Checklist

- [ ] Does every public function have a test?
- [ ] Can I explain what this function does in one sentence?
- [ ] Are there any magic numbers without names?
- [ ] Is there any dead code?
- [ ] Are similar things expressed similarly?
- [ ] Would a new team member understand this code?

---

### Anti-Patterns to Avoid

- **Comments as deodorant** — Commenting bad code instead of rewriting it
- **Flag arguments** — Boolean parameters that fork behavior
- **Train wrecks** — `a.getB().getC().doSomething()`
- **Hybrids** — Half object, half data structure
- **Mixed commits** — Tidying and behavior changes in the same commit
- **Premature optimization** — Clever code that obscures intent
- **Test neglect** — Production code without corresponding tests

---

### The Mantra

**Test first. Name well. Keep it small. Tidy often. Make every line tell.**
