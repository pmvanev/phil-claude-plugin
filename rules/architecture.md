---
paths:
  - "**/*.{ts,tsx,js,jsx,py,go,rs,java,cs,rb,kt,swift,cpp,c,h,hpp,scala,clj,ex,exs,hs,ml,fs,fsx}"
---

# Architecture Guide

Guidelines for software architecture, extracted from Robert C. Martin's *Clean Architecture*, Kent Beck's *Tidy First?*, Dave Farley's *Modern Software Engineering*, Dan North's *Best Simple System for Now*, and MinimumCD.org.

---

### Core Philosophy

> **"The goal of software architecture is to minimize the human resources required to build and maintain the required system."**

---

### Key Principles

#### 1. Dependency Direction
- Point dependencies inward—toward higher-level policy
- High-level modules define interfaces; low-level modules implement them
- Source code dependencies oppose the flow of control when crossing boundaries
- Never let a concrete detail appear in a policy declaration

#### 2. Boundaries
| Guideline | Rationale |
|-----------|-----------|
| **Draw boundaries between things that change for different reasons** | Isolates volatility |
| **Separate business rules from infrastructure** | Policy outlives mechanism |
| **Treat the database as a plugin** | Storage is a detail |
| **Treat the UI as a plugin** | Delivery is a detail |
| **Treat the framework as a plugin** | Frameworks change; business rules endure |

**The DAO Pattern** enforces the database boundary. Business rules depend on an abstract repository interface; the DAO implements it. Swap PostgreSQL for MongoDB—business rules never know. The database becomes a deployment decision, not an architectural commitment.

#### 3. The Four Layers
From innermost to outermost:

1. **Entities** — Enterprise-wide business rules; change least often
2. **Use Cases** — Application-specific business rules; orchestrate entities
3. **Interface Adapters** — Convert data between use cases and external agencies
4. **Frameworks & Drivers** — Web, database, UI; the outermost, most volatile layer

*Dependencies point inward. Inner layers know nothing about outer layers.*

#### 4. Ports and Adapters
Also called Hexagonal Architecture. Business logic at the center; external systems at the edges.

- **Ports** — Interfaces the business logic defines for its needs
- **Adapters** — Implementations that connect ports to real systems
- **Business logic never imports infrastructure** — Adapters import business logic, not the reverse

#### 5. Component Cohesion
- **Group classes that change together** — Minimizes release frequency
- **Group classes that are reused together** — Consumers get what they need
- **Exclude classes not reused together** — Avoid forcing unnecessary dependencies

#### 6. Component Coupling
- **Eliminate cycles in the dependency graph** — Cycles create monoliths
- **Depend in the direction of stability** — Volatile components depend on stable ones
- **Make stable components abstract** — Abstractions accommodate extension
- **Make volatile components concrete** — Concrete implementations change freely

#### 7. Configuration Separation
- **Application config** (internal behavior) bundles with the artifact—does not vary by environment
- **Environment config** (secrets, URLs, feature flags) injected at runtime via env vars
- Follow Twelve-Factor App: code and config are separate concerns

#### 8. Deferral
- Defer decisions about frameworks, databases, and delivery mechanisms
- A good architecture makes these decisions easy to change
- Commit to abstractions, not implementations

#### 9. Empirical Design Over Speculation
Design timing falls on a spectrum:

- **Speculative design** — Design done too soon, before actual need. Predictions are often wrong; speculative code goes unused or becomes an obstacle.
- **Reactive design** — Design done too late, after coupling costs have already accumulated. The pain of poor structure is paid repeatedly.
- **Empirical design** — Design done at the right moment, based on evidence. Observe the change you need, assess the structure, decide if restructuring would reduce the cost of change.

Prefer empirical design:

- **Do not anticipate the future** — Predictions are close-but-wrong; solve for what is really there
- **Simple enables flexible** — Architecture so simple it can flex in any direction
- **Gall's Law** — Complex systems that work evolved from simple systems that worked
- **Avoid speculative interfaces** — Generic solutions arc toward failure

#### 10. Screaming Architecture
Architecture should scream its intent. A healthcare system's folder structure should reveal healthcare—not that it uses FastAPI or Django. A banking application should look like a banking application at first glance.

- **Top-level directories name use cases**, not technical layers
- **File organization reveals domain concepts**, not frameworks
- **A new developer should grasp the domain** before noticing the technology

Frameworks are tools, not architecture. When the framework dominates the structure, the system screams "I'm a Rails app" instead of "I manage patient records."

#### 11. BAPO: Align Organization to Architecture
Most organizations follow **OBAP**: Organization dictates Process, Process dictates Architecture, Architecture dictates Business outcomes. This inversion lets org charts and team boundaries constrain technical decisions.

High-performing organizations follow **BAPO**:

1. **Business** vision drives
2. **Architecture**, which drives
3. **Process**, which drives
4. **Organization**

Design the architecture first. Then organize teams around it. Conway's Law cuts both ways—use it deliberately.

---

### Boundaries Checklist

- [ ] Can the business rules run without the database?
- [ ] Can the business rules run without the UI?
- [ ] Can the business rules run without any framework?
- [ ] Do all source dependencies point toward higher-level policy?
- [ ] Are infrastructure concerns implemented as plugins?

---

### Anti-Patterns to Avoid

- **Framework marriage** — Letting framework types invade business logic
- **Database worship** — Building the system around the data model
- **Leaky abstractions** — Exposing implementation details through interfaces
- **Dependency cycles** — Components that depend on each other in loops
- **Mixed levels** — High-level policy depending on low-level detail
- **Speculative generalization** — Building for imagined futures that never arrive
- **Over-broad data types** — Generic structures where specific types would suffice
- **Premature abstraction** — Interfaces with only one implementation

---

### The Mantra

**Separate policy from detail. Defer decisions. Keep options open.**
