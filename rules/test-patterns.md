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

# Test Patterns

Guidelines extracted from Gerard Meszaros's *xUnit Test Patterns*, Vladimir Khorikov's *Unit Testing Principles, Practices, and Patterns*, Steve Freeman and Nat Pryce's *Growing Object-Oriented Software, Guided by Tests*, Kent Beck's *Test-Driven Development: By Example*, Michael Feathers's *Working Effectively with Legacy Code*, and Winters, Manshreck and Wright's *Software Engineering at Google*. Martin Fowler's bliki, Scott Wlaschin's property-based testing series, Llewellyn Falco's ApprovalTests and Ian Robinson's consumer-driven contracts are named where each applies.

This rule owns **how a test is written**: how it builds its fixture, how it verifies a result, how it chooses its cases, and the names for what goes wrong. `testing.md` owns the methods, the double taxonomy and F.I.R.S.T.; `test-architecture.md` owns which tier a test belongs in. A finding about a test names a smell from the catalogue below and the pattern that fixes it, as a finding about production code names a refactoring from `refactoring-catalog.md`.

---

### Core Philosophy

**A test earns its place on four counts** — Khorikov's four pillars: it catches regressions, it survives refactoring, it runs fast, and it costs little to read and keep. The first, third and fourth trade against one another. **Resistance to refactoring does not trade.** A test that fails on a correct refactoring is a false alarm, and a team that learns to expect false alarms stops reading red.

Every pattern below serves one of the four. Every smell costs one of them.

---

### The Stance: Classical, Not London

Two schools disagree on what a unit is. Khorikov sets them out:

| School | A unit is | Doubles replace |
|---|---|---|
| **London** (*GOOS*) | a class | every collaborator |
| **Classical** (Beck, Khorikov) | a behaviour | only dependencies shared between tests or outside the process |

**This project takes the classical side.** `test-architecture.md`'s rule — be sociable inside a boundary, solitary across one — is the classical school stated as an allocation rule. *GOOS* is cited here for Test Data Builders, for "only mock types you own", and for listening to tests that resist being written. This rule rejects its practice of mocking collaborators inside a boundary.

**Across a boundary, the kind of dependency decides the double.** Khorikov splits out-of-process dependencies in two:

- **Managed** — only your application touches it, like your own database. Its state is an implementation detail. Substitute a fake at the commit stage and keep one integration test on the real thing.
- **Unmanaged** — other systems observe it: an email gateway, a message bus another team reads, a third-party API. **The messages you send it are observable behaviour.** A mock that asserts them verifies an outcome, not an implementation, and is the right test. Double a port you own that wraps the gateway, not the third-party type itself — that is Mocked Foreign Type.

---

### Verifying a Result

Prefer these in order. Each step down couples the test more tightly to the code.

1. **Output-based** — assert on the return value. No state, no doubles.
2. **State-based** — act, then read the resulting state through the public interface.
3. **Communication-based** — assert on the messages sent to a double. **Use it only at an unmanaged dependency.** Anywhere else it is Overspecified Software.

Meszaros's verification patterns make the assertions themselves readable:

| Pattern | Use when |
|---|---|
| **Expected Object** | the outcome is an object; build the expected one and compare it whole |
| **Custom Assertion** | several tests verify the same thing; name the check and give it a failure message |
| **Delta Assertion** | the starting state is not yours to fix; assert the change, not the total |
| **Guard Assertion** | a later assertion is meaningless unless a precondition holds; assert the precondition first instead of branching |

---

### Building the Fixture

The fixture is everything a test sets up before it acts. Meszaros's **Four-Phase Test** — setup, exercise, verify, teardown — is Arrange-Act-Assert with teardown made explicit. Use the language's scoped cleanup for the fourth phase, never a manual call a failure can skip.

| Pattern | Use when | Watch for |
|---|---|---|
| **Fresh Fixture** | always, by default — each test builds its own | — |
| **Immutable Shared Fixture** | setup is expensive and nothing a test does can change it | a mutable shared fixture produces Interacting Tests |
| **Minimal Fixture** | always — build only what this test reads | General Fixture |
| **Creation Method** | an object needs construction the test does not care about; a named function builds it | hiding the values the assertion depends on |
| **Test Data Builder** (Pryce) | an object has many fields or variants; defaults for every field, an override for each one the test is about | changing a default breaks distant tests without warning |
| **Object Mother** (Fowler's bliki) | a handful of canonical examples recur across the suite | it grows into one module every test depends on — switch to builders when variants multiply |

**DAMP, not DRY** — *Software Engineering at Google*. Test code tolerates duplication that production code would not, because a test must explain itself without a reader leaving it. Extract a helper for detail the outcome does not depend on. **Keep the values the assertion depends on in the test body**, so the reader sees the cause and the effect together: pass them to the helper as arguments, and prefer the duplication to a helper that hides them.

---

### Doubles in Practice

`testing.md` defines dummy, stub, spy, mock and fake. Choosing among them:

- **Prefer a fake for a port you own.** It supports state-based verification where a mock forces communication-based verification.
- **Hold the fake honest with a contract test** — Fowler's term. Run the same tests against the fake and the real implementation, so the fake cannot drift from what it stands in for.
- **Only mock types you own** — *GOOS*. Wrap a third-party API behind an interface you define, double the interface, and let `test-architecture.md`'s boundary test hold the wrapper honest.
- **Self Shunt** — Beck. The test class implements the collaborator's interface itself. Use it for a one-off double too small to deserve a class.

---

### Designing for the Test

When code resists testing, change the code, not the test.

- **Humble Object** — Meszaros. Move the logic out of the hard-to-test thing — a UI, a thread, a framework callback — into an object you can test directly. Leave a shell too simple to break.
- **Seam** — Feathers. A place where behaviour changes without editing the code at that place: an object seam (a constructor parameter), a link seam, a preprocessor seam. In legacy code, find the seam before writing the test.
- **No test logic in production.** A flag, branch or hook that exists only for tests has inverted the ring `test-architecture.md` describes. Replace it with a seam.

---

### Choosing the Cases

- **Triangulate** — Beck. Generalise the code only when a second example forces it. One example justifies only a constant.
- **Parameterized Test** — Meszaros; table-driven tests in Go. One behaviour, many inputs: one row per case, and each row named. **Never parameterize different behaviours into one table** — they need different names, and the table hides that.
- **Property-based tests** assert a rule over generated inputs and shrink a failure to its smallest case. Wlaschin's shapes name the properties worth asserting:

  | Shape | Property |
  |---|---|
  | *There and back again* | decode(encode(x)) == x |
  | *Some things never change* | an invariant holds after every operation — the length after a sort |
  | *The more things change, the more they stay the same* | idempotence: f(f(x)) == f(x) |
  | *Different paths, same destination* | two orders of operations give the same result |
  | *Hard to prove, easy to verify* | check the answer without recomputing it — a sorted list is ordered |
  | *The test oracle* | compare against a slow, obviously correct implementation |

  **Pair properties with examples.** A property states the general rule; an example shows a reader one case they can check by hand.

- **No logic in tests** — *Software Engineering at Google*. No loops, no conditionals, and no expected value computed by the algorithm under test. Expected values are literals. A loop belongs in a Parameterized Test; a branch belongs in a Guard Assertion.

---

### Pinning Behaviour Nobody Specified

- **Characterization Test** — Feathers. Assert what the code does now, not what it should do, so a change cannot alter it unnoticed. `testing.md`'s lock-in tests are this pattern.
- **Approval test / golden master** — Falco's ApprovalTests. Serialize a large output, approve it once by reading it, and diff every later run against the approved copy. Scrub every field that varies between runs — timestamps, ids, ordering — or the test is erratic. **An approval nobody read is a characterization of a bug.** For a small value, write a plain assertion.

---

### Testing Across Services

**Consumer-driven contract** — Robinson; Pact implements it. The consumer records the requests it sends and the responses it relies on. The provider replays that record in its own build. Each side learns of a breaking change at its commit stage, and neither side needs a shared end-to-end environment to learn it. It is the boundary test from `test-architecture.md`, applied to a service whose team you can talk to.

---

### Smell Catalogue

Meszaros names most of the smells; the fix column names the pattern above or the move the route's command applies. **The route says which command applies the fix.** A structural route never changes what a test asserts, and a behavioural route always does — `refactor-tests` and `redesign-tests` exist on either side of that line. `report only` means no command applies the fix; the reviewer reports it and a human applies it.

| Smell | Signal | Fix | Changes the assertion? | Route |
|---|---|---|---|---|
| **Test Code Duplication** | the same arrange repeated across tests | Extract Fixture/Helper — a Creation Method, or a fixture when nothing it holds decides the outcome | No | `/phil:refactor-tests` |
| **Obscure Test** | a long body buries why the outcome follows | Extract Test Helper for the irrelevant detail — a Creation Method for a build block, a Custom Assertion for an assert block; keep the values the outcome depends on in the body | No | `/phil:refactor-tests` |
| **Vague Name** | the name states no behaviour | Rename to the behaviour verified | No | `/phil:refactor-tests` |
| **Interleaved Phases** | assertions between several acts | Reorder into Arrange-Act-Assert | No | `/phil:refactor-tests` |
| **Mystery Guest** | the outcome depends on data the test never shows — a file, a seeded row, a global | Inline the data, or a Creation Method that names it | No | report only |
| **General Fixture** | shared setup builds more than any one test reads | Minimal Fixture | No | report only |
| **Irrelevant Information** | literals that cannot affect the outcome crowd the ones that do | Test Data Builder with defaults | No | report only |
| **Assertion Roulette** | several unlabelled assertions, and a failure does not say which | Custom Assertion with a failure message, or one concept per test | No | report only |
| **Eager Test** | one test verifies several behaviours | Split into one named test per behaviour | No — every assertion survives, in a different test | report only |
| **Conditional Test Logic** | `if`, loops, or an expected value computed in the test | Parameterized Test for the loop, literal expected values, Guard Assertion for the branch | Yes | report only |
| **Overspecified Software** | asserts calls to an in-process collaborator instead of the outcome | Assert on observable outcome | Yes | `/phil:redesign-tests` |
| **Sensitive Equality** | compares a `str()`, `repr()` or serialized form | Assert on observable outcome: an Expected Object, or the fields that matter | Yes | `/phil:redesign-tests` |
| **Private Access** | reads private state or calls a private method | Assert on observable outcome through the public interface | Yes | `/phil:redesign-tests` |
| **Mock Inside a Boundary** | doubles an owned, in-process collaborator | Replace mock with real collaborator, or Replace mock with fake | Yes | `/phil:redesign-tests` |
| **Erratic Test** | passes and fails with no code change — clock, randomness, ordering, Interacting Tests | Inject clock / static timestamp, Seed RNG, or Isolate shared state as a Fresh Fixture | Yes | `/phil:redesign-tests` |
| **Mocked Foreign Type** | doubles a third-party API directly | Wrap it behind an interface you own and add a boundary test | Yes | report only |
| **Test Logic in Production** | production code exists only for tests | Humble Object, or a Seam | No — the production code changes | report only |
| **Wrong Tier** | crosses a boundary the behaviour does not need | Re-allocate to the tier `test-architecture.md` names | Yes | report only |
| **Missing Boundary Test** | nothing exercises a third-party dependency itself | Add a boundary test per `test-architecture.md` | Yes — adds one | report only |
| **Missing Test** | a public behaviour no test exercises | Write a failing test for the behaviour, then make it pass | Yes — adds one | report only |

**Two smells live in `test-architecture.md` and are not repeated here:** Slow Tests and Fragile Test. Both are coupling findings, and that rule owns coupling.

**A mock at an unmanaged dependency is not Overspecified Software and not Mock Inside a Boundary.** It is the communication-based verification the stance above calls for, and a reviewer that flags it pushes a correct test toward a wrong one. **Judge by what the double stands in for, not by who owns its type:** your own `EmailSender` port wrapping a gateway is still the gateway. Two smells still apply there — doubling the third-party type directly is Mocked Foreign Type, and a message asserted with a wall-clock or random value is an Erratic Test.

---

### Pattern Checklist

- [ ] Can a reader see the cause and the effect without leaving the test?
- [ ] Does each test build only what it reads?
- [ ] Is the verification output-based or state-based wherever that is possible?
- [ ] Is every mock at an unmanaged dependency, and every other double a fake or the real thing?
- [ ] Does a contract test hold each fake to the real implementation?
- [ ] Are the expected values literals, with no loop or branch in the test?
- [ ] Does each parameterized table hold one behaviour?
- [ ] Does each approved output carry a scrubber for every field that varies?

---

### Anti-Patterns to Avoid

| Anti-pattern | Fix |
|---|---|
| **DRY test code** — the asserted values hidden in a helper | DAMP: pass them as arguments, or keep the duplication |
| **Mocking everything** — the London school inside a boundary | Real collaborators inside; doubles across |
| **Flagging every mock** — including the email the system must send | Mock unmanaged dependencies and assert the message |
| **A fake nobody checks** | One contract test, run against fake and real |
| **A table of different behaviours** | One table per behaviour, one name per row |
| **Properties with no examples** | Pair each property with a case a reader can check by hand |
| **Approving unread output** | Read it once; scrub what varies |
| **Test hooks in production** | A seam, or a Humble Object |

---

### Sources and Synthesis

The pattern and smell names are quoted from their sources: Meszaros for the fixture, verification and smell vocabulary; Khorikov for the four pillars, the two schools, the three verification styles and the managed/unmanaged split; Pryce for the Test Data Builder; Beck for Triangulate and Self Shunt; Feathers for seams and characterization tests; Google for DAMP and no logic in tests; Wlaschin for the property shapes. **Three things are this rule's own:** the Route and Changes-the-assertion columns, which map each smell onto this plugin's commands; the names Vague Name, Interleaved Phases, Private Access, Mock Inside a Boundary, Mocked Foreign Type, Wrong Tier, Missing Boundary Test and Missing Test, which label findings the sources describe without naming; and the choice of the classical school, which the sources argue for and against. Lasse Koskela's *Effective Unit Testing* catalogues an overlapping set of smells under other names; this rule uses Meszaros's. Citations are to books and named articles, not to pages. Said plainly so nobody cites this table back to Meszaros.

---

### The Mantra

> **Show the cause and the effect in the test. Verify the outcome, not the conversation — unless the conversation is the outcome. Name the smell, then route it to the command that may fix it.**
