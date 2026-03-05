# Definitions

Terms and acronyms used in the development guides.

---

## Methodologies

| Term | Definition |
|------|------------|
| **TDD** | Test-Driven Development. Write a failing test, make it pass, refactor. Red-Green-Refactor. |
| **BDD** | Behavior-Driven Development. Express tests as specifications using Given-When-Then. |
| **ATDD** | Acceptance Test-Driven Development. Define acceptance criteria before development. |
| **DDD** | Domain-Driven Design. Model software around business concepts using ubiquitous language. |
| **CI** | Continuous Integration. Integrate code to trunk at least daily; verify with automated tests. |
| **CD** | Continuous Delivery. Software is always releasable. Pipeline certifies every commit. |
| **TBD** | Trunk-Based Development. Short-lived branches (< 1 day) that integrate to trunk. |

---

## Principles

| Term | Definition |
|------|------------|
| **SOLID** | Five design principles: SRP, OCP, LSP, ISP, DIP. |
| **SRP** | Single Responsibility Principle. A module has one reason to change. |
| **OCP** | Open-Closed Principle. Open for extension, closed for modification. |
| **LSP** | Liskov Substitution Principle. Subtypes must be substitutable for base types. |
| **ISP** | Interface Segregation Principle. Clients should not depend on methods they don't use. |
| **DIP** | Dependency Inversion Principle. Depend on abstractions, not concretions. |
| **CUPID** | Five properties of joyful code: Composable, Unix philosophy, Predictable, Idiomatic, Domain-based. |
| **F.I.R.S.T.** | Test principles: Fast, Independent, Repeatable, Self-validating, Timely. |

---

## Architecture

| Term | Definition |
|------|------------|
| **Ports and Adapters** | Hexagonal Architecture. Business logic at center; external systems at edges via interfaces. |
| **Port** | Interface the business logic defines for its needs. |
| **Adapter** | Implementation that connects a port to a real system. |
| **DAO** | Data Access Object. Humble object pattern for database access. |
| **Humble Object** | Separates testable logic from hard-to-test infrastructure. |
| **Boundary** | Separation between components that change for different reasons. |
| **Entity** | Enterprise-wide business rules; innermost layer, changes least often. |
| **Use Case** | Application-specific business rules; orchestrates entities. |
| **Interface Adapter** | Converts data between use cases and external systems. |

---

## Configuration

| Term | Definition |
|------|------------|
| **Application Config** | Internal behavior settings bundled with artifact. Does not vary by environment. |
| **Environment Config** | External settings (secrets, URLs, feature flags) injected at runtime via env vars. |
| **Twelve-Factor App** | Methodology for building SaaS apps. Code and config are separate concerns. |
| **Immutable Artifact** | Built once, deployed to all environments. No rebuilding per environment. |

---

## Testing

| Term | Definition |
|------|------------|
| **Unit Test** | Tests isolated logic. Runs in milliseconds. |
| **Integration Test** | Tests component collaboration. Runs in seconds. |
| **Acceptance Test** | Tests system from user perspective. Verifies requirements. |
| **Sociable Unit Test** | Unit test that uses real collaborators where possible. Tests behavior with real dependencies. |
| **Solitary Unit Test** | Unit test that mocks all dependencies. Tests in complete isolation. |
| **Testing Pyramid** | Many unit tests, fewer integration tests, fewest acceptance tests. |
| **Testing Trophy** | Alternative model prioritizing sociable unit tests (~80%) over solitary tests. |
| **Flaky Test** | Non-deterministic test that sometimes passes, sometimes fails. Destroys pipeline trust. |

---

## Test Doubles

| Term | Definition |
|------|------------|
| **Dummy** | Passed but never used. Fills parameter lists. |
| **Stub** | Returns predetermined responses. Controls indirect inputs. |
| **Spy** | Records calls for later verification. |
| **Mock** | Verifies expected interactions occurred. |
| **Fake** | Working implementation with shortcuts (e.g., in-memory database). |

---

## Delivery

| Term | Definition |
|------|------------|
| **Deployment** | Copying software to a host environment. Technical act. |
| **Release** | Making a feature available to users. Business decision. |
| **Pipeline** | Automated path from commit to production. Build → Test → Deploy. |
| **Deterministic Pipeline** | Same inputs produce same outputs. Repeatable and trustworthy. |
| **Blue-Green Deployment** | Two identical environments; switch traffic instantly. |
| **Canary Release** | Route small percentage of traffic to new version first. |
| **Feature Flag** | Toggle that controls feature visibility without deployment. |
| **Rollback** | Revert to previous version. Should take < 5 minutes. |

---

## Evolutionary Practices

| Term | Definition |
|------|------------|
| **Branch by Abstraction** | Introduce abstraction, implement new behavior behind it, migrate clients, remove old. |
| **Connect Last** | Build complete features in isolation, wire up in final commit. |
| **Refactoring** | Changing code structure without changing behavior. |
| **Tidying** | Small structural changes that ease behavior changes. Guard clauses, dead code removal, etc. |

---

## Code Smells

| Term | Definition |
|------|------------|
| **Feature Envy** | Code that uses another module's data more than its own. |
| **Shotgun Surgery** | One change requires touching many modules. |
| **Divergent Change** | One module changes for multiple unrelated reasons. |
| **Primitive Obsession** | Using primitives instead of small domain objects. |
| **Data Clump** | Data items that travel together but aren't encapsulated. |

---

## Design

| Term | Definition |
|------|------------|
| **Coupling** | Degree to which modules depend on each other. Lower is better. |
| **Cohesion** | Degree to which elements within a module belong together. Higher is better. |
| **Testability** | Design property enabling effective testing: controllability, observability, determinism, isolation. |
| **Deployability** | Design property enabling frequent, safe deployments. |
| **Optionality** | Tidy code creates future options; messy code forecloses them. |

---

## Resource Management

| Term | Definition |
|------|------------|
| **RAII** | Resource Acquisition Is Initialization. Tie resource lifetime to object lifetime—acquire in constructor, release in destructor. |
| **SBRM** | Scope-Bound Resource Management. Synonym for RAII emphasizing that cleanup occurs when scope exits. |
| **Context Manager** | Python protocol (`__enter__`/`__exit__`) implementing RAII. Enables `with` statements for deterministic cleanup. |

---

## Organizational

| Term | Definition |
|------|------------|
| **BAPO** | Business → Architecture → Process → Organization. High-performing sequence. |
| **OBAP** | Organization → ... → Business. Inverted, dysfunctional sequence. |
| **Conway's Law** | System design mirrors organizational communication structure. |
| **Stop-the-Line** | All feature work stops when the build is red. |
