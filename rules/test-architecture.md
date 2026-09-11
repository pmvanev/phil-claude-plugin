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

# Test Architecture

Guidelines extracted from Robert C. Martin's *Clean Code*, *Clean Craftsmanship* and *Clean Architecture*, Jez Humble and David Farley's *Continuous Delivery*, and Dave Farley's *Modern Software Engineering*.

This rule owns two questions the other testing rules name and never answer: **which tier a given behaviour belongs in**, and **what a whole suite may cost before it is too slow to run**. It is the single owner of the pyramid, the trophy, and their settlement. The techniques stay where they are: the three laws, doubles, F.I.R.S.T. and determinism in `testing.md`; test-code quality in `coding.md`; architectural boundaries and the dependency rule in `architecture.md`; pipeline stages and release mechanics in `continuous-delivery.md`. Complement those — do not restate them.

---

### Core Philosophy

> **"Tests are part of the system."** — *Clean Architecture*

Tests are not a commentary on the system; they are its outermost ring. They depend inward, nothing depends on them, and they obey the same design rules as everything else. That single fact answers both questions below.

---

### The Allocation Rule

**A test's tier is decided by the outermost boundary it crosses.** Not by how many lines it touches, not by how many doubles it uses, and not by a ratio somebody set.

Start from the behaviour, name the boundary, and the tier follows:

| The behaviour | Outermost boundary crossed | Tier | Speed |
|---|---|---|---|
| A calculation, a policy, a state transition — no I/O | none | **Unit** | microseconds |
| Objects collaborating inside one boundary | none | **Unit, sociable** | milliseconds |
| Your code against a port you own — repository, gateway, queue | one you control | **Integration** | seconds |
| How a third-party library or service actually behaves | one you do not control | **Boundary test** | seconds, and on every upgrade |
| A user-visible behaviour of the whole system, driven through its ports | all of them | **Acceptance** | seconds to minutes |
| Capacity, resilience, and the deployment itself | the deployment | **Later pipeline stages** | minutes to hours |

**Why the boundary and not the shape.** The dependency rule says a test is an ordinary client of the thing it tests. So the real question is how far in you can reach and still land on a stable surface. Reach past a boundary and you inherit its cost and its instability; stop short of one and you have tested less than the behaviour. **Test against the innermost stable abstraction that expresses the behaviour** — that abstraction names your tier.

**Corollary: "hard to place" means "badly bounded."** A behaviour that fits no row is telling you the code has no boundary where one belongs. Fix the design, then place the test.

---

### Pyramid or Trophy — Settled

They are not rivals. They answer different questions, and each is right about its own.

| | Claims | About | Status |
|---|---|---|---|
| **The pyramid** | Tests crossing more boundaries cost more to write, run and diagnose, so you can afford fewer | **Cost** | Arithmetic — not a preference |
| **The trophy** | A test that doubles its own collaborators is coupled to structure, not behaviour | **Coupling** | Also true — and about a different axis |

They appear to conflict only because both get stated as ratios. State them as rules and they compose into one:

> **Be sociable inside a boundary. Be solitary across one.**

Inside a boundary, use the real collaborators. They are yours, they are fast, and replacing them buys the fragile test that breaks on every refactoring. Across a boundary, substitute. The real thing is slow, shared, or not yours, and the commit stage cannot afford it.

**The shape is an output, never a target.** Follow the rule and the result is broad at the base, because behaviours outnumber boundaries — and sociable at the base, which was the trophy's point all along. Set a ratio as a goal instead and you will hit it, by writing the tests that move the number.

**So this project states no percentages.** A suite whose distribution looks wrong is reporting one of two design findings: behaviours tested at the wrong tier, or boundaries drawn in the wrong places. Read the shape as a diagnosis and never as a score.

---

### The Speed Budget

"Fast" describes one test. A suite needs a number, and the number is the feedback loop it sits in.

| Stage | What runs | Budget | Act when |
|---|---|---|---|
| **Local, per change** | the tests over the code you are touching | **under 10 seconds** | you stop running it between edits |
| **Commit stage** | every unit and boundary test | **under 5 minutes; never past 10** | you batch changes to avoid the wait |
| **Acceptance stage** | the whole system through its ports | **under an hour** | it stops running on every commit |
| **Later stages** | capacity, resilience, deployment | as slow as the feedback allows | a result arrives too late to act on |

**The threshold is behavioural, not numeric.** "The suite feels slow" is not a signal — people tolerate almost anything gradually. The signal is the moment someone **changes what they do** to avoid the wait: skipping the run, batching commits, pushing and hoping. Watch for that, because it arrives before the number does.

**A slow suite is a design finding.** Farley's forcing function applies to the suite itself: tests are slow because they cross boundaries they did not need to cross, and that is a statement about coupling. Treat the clock as a diagnostic instrument.

**Which of these numbers is published.** Only the commit stage — *Continuous Delivery* puts it under five minutes and never past ten, and that is the single suite budget any of this rule's five sources states. The local and acceptance figures are this project's, scaled from that one to the loops they sit in; treat them as defaults to argue with rather than as findings. The allocation rule and the pyramid-trophy settlement below are likewise derived from the five sources, not quoted from any of them: **"be sociable inside a boundary, solitary across one" is this rule's synthesis.** Said plainly so nobody cites it back to a book that does not contain it.

---

### Getting Back Under Budget

In order. The first three are the only ones that fix anything.

1. **Measure before touching anything.** Attribute the time per test. A slow suite is almost never uniformly slow — a handful of tests usually own most of the clock, and they are rarely the ones people suspect.
2. **Re-allocate rather than optimize.** A slow test is usually a correctly written test at the wrong tier. Name the boundary it crosses and ask what it bought.
3. **Substitute at the boundary.** Replace a port you own with a fast in-memory implementation, and keep one integration test on the real thing. This is the commit stage's central trade.
4. **Split the stages.** The commit stage runs on every commit; acceptance runs on every commit too, but without making anyone wait for it.
5. **Parallelize.** Real, and last, because it hides the design signal the clock was giving you. Parallelize a suite you have already diagnosed.
6. **Delete.** A test that duplicates another's coverage costs time forever and proves nothing new.

**Quarantine is not on the list.** Quarantining a flaky test converts a failing test into a passing suite and changes nothing else. If it is worth keeping, fix it today; otherwise delete it, and say so.

---

### Boundary Tests

The third-party seam gets its own tier because the usual reasoning breaks there: you cannot refactor the other side, and you cannot trust its documentation.

**Write a test that exercises the dependency itself — not your use of it.** Call the library, assert what it really does, and discover the gap between the documented behaviour and the actual one before production does.

- **They cost nothing.** You had to learn the API regardless. Writing the exploration as tests is the same work with a durable artifact at the end.
- **Keep them, and run them on every upgrade.** This is the whole return: a changed dependency breaks a test you own instead of production code you do not.
- **Then wrap it.** Depend on an interface you define, with the third party behind an adapter. Your code stays testable with a fake; the boundary test holds the adapter honest.
- **Where the dependency does not exist yet, define the interface you wish you had** and write against that. The adapter comes later, and the design does not wait for someone else's release.

---

### Fragile Tests Are a Coupling Defect

A suite that breaks every time you refactor is not thorough. It is coupled.

- **The cause is one-to-one correspondence** — a test file per production file, a test method per method. The structure of the tests mirrors the structure of the code, so every structural change is a test change, and refactoring stops being free.
- **The fix is a testing API.** Give the tests a vocabulary of their own, expressed in the domain, and let it absorb the structural churn. Acceptance tests should speak that vocabulary through the system's ports — never through the UI, which is the most volatile surface in the system and the worst place to anchor anything.
- **Then apply the design rule to the tests themselves.** Tests depend on the system; the system never depends on the tests. A production type that exists only to satisfy a test has inverted the ring.

---

### Allocation Checklist

- [ ] What boundary does this behaviour cross? Is the test at that tier?
- [ ] Am I reaching past a boundary I did not need to cross?
- [ ] Inside this boundary, am I using the real collaborators?
- [ ] Across it, am I substituting?
- [ ] Does every third-party dependency have one test that exercises it directly?
- [ ] Does the commit stage still finish inside five minutes?
- [ ] Has anyone started skipping, batching, or working around the suite?
- [ ] If I refactor without changing behaviour, how many tests break? (The answer should be none.)

---

### Anti-Patterns to Avoid

| Anti-pattern | Fix |
|---|---|
| **Ratio as a target** — "we need 80% unit tests" | Allocate by boundary; read the resulting shape as a diagnosis |
| **Doubling your own collaborators** — mocks inside a single boundary | Be sociable inside a boundary; the real objects are fast and yours |
| **Crossing a boundary out of habit** — a database in a test of a calculation | Name the boundary the behaviour actually needs |
| **One-to-one test structure** — a test file per production file | Give the tests their own domain vocabulary and let structure move underneath |
| **Acceptance tests through the UI** | Drive the system through its ports |
| **Trusting the documentation** — no test against the real dependency | One boundary test per dependency, re-run on every upgrade |
| **Parallelizing first** | Measure, re-allocate, substitute; then parallelize |
| **Permanent quarantine** — a flaky test parked indefinitely | Fix it today or delete it and say so |
| **"Fast" with no number** | Budget the stage, and watch for the behaviour that says act |

---

### The Mantra

> **The boundary decides the tier. Be sociable inside one and solitary across one. Budget the stage, not the test — and when someone starts working around the suite, the suite is the defect.**
