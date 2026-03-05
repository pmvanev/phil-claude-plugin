---
paths:
  - "**/*.test.{ts,tsx,js,jsx}"
  - "**/*.spec.{ts,tsx,js,jsx}"
  - "**/test_*.py"
  - "**/*_test.{go,py,rs}"
  - "**/tests/**"
  - "**/__tests__/**"
  - "**/test/**"
  - "**/*.test.py"
  - "**/*Test.java"
  - "**/*_test.rb"
---

# Testing Guide

Guidelines for software testing, extracted from Robert C. Martin's *Clean Code* and *Clean Craftsmanship*, Kent Beck's *Tidy First?*, Dave Farley's *Modern Software Engineering*, and MinimumCD.org.

---

### Core Philosophy

> **"Test code is as important as production code. Dirty tests are worse than no tests."**

---

### Development Methodologies

#### TDD — Test-Driven Development
Write tests before production code. Three laws govern the practice:

1. Write no production code until you have a failing test
2. Write no more test code than is sufficient to fail
3. Write no more production code than is sufficient to pass

The cycle: Red → Green → Refactor. Repeat in seconds, not minutes.

#### BDD — Behavior-Driven Development
Express tests in terms of behavior, not implementation. Tests read as specifications. Use language the business understands: *Given* preconditions, *When* actions occur, *Then* outcomes follow. BDD bridges the gap between developers and stakeholders.

#### ATDD — Acceptance Test-Driven Development
Write acceptance tests before development begins. Stakeholders, testers, and developers collaborate to define acceptance criteria. The acceptance test is the contract. Development is complete when the test passes.

#### DDD — Domain-Driven Design
Model software around the business domain. Use ubiquitous language—the same terms in code, tests, and conversation. Entities and use cases reflect domain concepts. Tests verify domain behavior, not technical implementation.

---

### Test Types

| Type | Scope | Speed | Purpose |
|------|-------|-------|---------|
| **Unit tests** | Single function or class | Milliseconds | Verify isolated logic |
| **Integration tests** | Multiple components together | Seconds | Verify collaboration |
| **Acceptance tests** | Entire system from user perspective | Seconds to minutes | Verify requirements |

#### The Testing Pyramid
Many unit tests at the base; fewer integration tests in the middle; fewest acceptance tests at the top. Invert the pyramid and your build slows to a crawl.

#### The Testing Trophy (Alternative Model)
Prioritize sociable unit tests (~80%) over solitary unit tests. Sociable tests use real dependencies where possible; solitary tests mock everything. Testing behavior with real collaborators catches integration issues earlier.

---

### Test Doubles

Test doubles replace real dependencies during testing. Each type serves a different purpose.

| Double | Definition | Use When |
|--------|------------|----------|
| **Dummy** | Passed but never used | Filling parameter lists |
| **Stub** | Returns predetermined responses | Controlling indirect inputs |
| **Spy** | Records calls for later verification | Verifying indirect outputs |
| **Mock** | Verifies expected interactions occurred | Testing collaboration |
| **Fake** | Working implementation with shortcuts | Replacing slow dependencies (e.g., in-memory database) |

**Overuse of mocks signals design problems.** If you need many mocks, your code has too many dependencies.

---

### F.I.R.S.T. Principles

Good tests follow five principles:

- **Fast** — Run in milliseconds; slow tests don't get run
- **Independent** — No test depends on another; run in any order
- **Repeatable** — Same result every time, any environment
- **Self-validating** — Pass or fail; no manual inspection required
- **Timely** — Written before or with the production code

---

### Test Code Quality

Test code is production code. Apply the same standards:

- **Name well** — Test names are documentation
- **Keep functions small** — Extract helpers; avoid duplication
- **Refactor relentlessly** — Dirty tests become liabilities
- **Delete dead tests** — Obsolete tests mislead and slow the build
- **Tidy often** — Guard clauses, explaining variables, cohesion order—all apply

Neglected test code rots. When tests become hard to maintain, developers stop writing them. When developers stop writing tests, defects multiply. Treat test code with the same respect as the code it verifies.

---

### Test Design Guidelines

#### Structure
- One assert per test—or one concept per test at minimum
- **Arrange** — Set up preconditions
- **Act** — Execute the behavior under test
- **Assert** — Verify the outcome

#### Naming
Name tests to describe the behavior they verify:
- `shouldRejectInvalidEmail`
- `calculatesCompoundInterestCorrectly`
- `returnsEmptyListWhenNoMatchesFound`

#### Coverage
- Test behavior, not implementation
- Test edge cases: nulls, empty collections, boundaries
- Test error paths, not just happy paths
- QA should find nothing; your tests should find everything first

---

### Design for Testability

Testability is a design property, not an afterthought. Code that resists testing signals design problems. Four properties make code testable:

| Property | Meaning | How to Achieve |
|----------|---------|----------------|
| **Controllability** | Set up any state needed for a test | Inject dependencies; avoid hidden state; use constructor parameters |
| **Observability** | Verify any outcome | Return values over side effects; expose state through getters; emit events |
| **Determinism** | Same inputs produce same outputs | Isolate randomness; inject clocks; avoid global state |
| **Isolation** | Test units independently | Dependency injection; interfaces over concrete types; avoid singletons |

#### Achieving Determinism

Non-deterministic tests are flaky tests. Common sources of non-determinism and their solutions:

| Source | Problem | Solution |
|--------|---------|----------|
| **Current time** | `datetime.now()` returns different values each run | Use static timestamps; inject a clock |
| **Random values** | `random.random()` varies each run | Seed the generator; inject randomness |
| **UUIDs** | `uuid.uuid4()` varies each run | Use static IDs in tests, or use unique IDs to isolate test data |
| **Shared databases** | Prior test runs leave data behind | Use unique identifiers; clean up; use transactions |
| **Network calls** | External services are unreliable | Use fakes or stubs; record/replay |
| **File system** | Files may exist from prior runs | Use temp directories; clean up |
| **Concurrency** | Race conditions cause intermittent failures | Avoid shared mutable state; use synchronization |

**Static timestamps** are preferred over `datetime.now()` in tests:

```python
# Good: deterministic, repeatable
TEST_TIMESTAMP = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
client.write_reading(reading, TEST_TIMESTAMP)

# Bad: different every run, makes debugging harder
client.write_reading(reading, datetime.now(timezone.utc))
```

**If code is hard to test, redesign the code—not the test.** Testability and good design reinforce each other.

---

### Lock-In Tests Before Refactoring

When a component has only smoke tests (renders without error) but no behavioral assertions, refactoring it is unsafe — the tests cannot detect regressions. The correct order is:

1. **Write behavioral tests first** — assert the specific outputs, states, and rendered content the component is expected to produce. These tests describe the contract.
2. **Confirm tests pass** on the current implementation.
3. **Refactor the structure** — the behavioral tests now serve as a safety net.
4. **Confirm tests still pass** — the contract is preserved.

This is the test-side complement of *"make the change easy, then make the easy change."* Writing the behavioral tests *is* making the refactor safe.

---

### Anti-Patterns to Avoid

- **Fragile tests** — Coupled to implementation; break when code changes
- **Slow tests** — Discourage frequent execution
- **Test interdependence** — Tests that must run in order
- **Testing private methods** — Test through the public interface
- **Excessive mocking** — Mocking everything obscures real behavior
- **Ignoring failures** — A failing test demands immediate attention
- **Manual verification** — Tests should be self-validating
- **Untestable design** — Blaming the test when the code resists testing
- **Flaky tests** — Non-deterministic tests destroy pipeline trust; fix immediately

---

### The Mantra

**Test first. Test fast. Test behavior. Let the tests prove the code works.**
