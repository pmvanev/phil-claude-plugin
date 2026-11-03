---
paths:
  - "**/*.{ts,tsx,js,jsx,py,go,rs,java,cs,rb,kt,swift,cpp,c,h,hpp,scala,clj,ex,exs,hs,ml,fs,fsx}"
---

# Modern Software Engineering

Guidelines extracted from Dave Farley's *Modern Software Engineering: Doing What Works to Build Better Software Faster*.

This rule owns Farley's **spine** — engineering as an empirical discipline, the two problems all software work reduces to, the two measures that tell you whether you are improving, and — from his interviews rather than the book — his claim that concurrency is complexity and clear code is usually fast code. The details live in the rules that already own them: empirical design in `architecture.md`, the four testability properties in `testing.md`, pipeline and release mechanics in `continuous-delivery.md`, evolutionary coding practices in `coding.md`, test-suite speed in `test-architecture.md`, a Lambda web app's load time in `lambda-web-app-speed.md`. Complement those — do not restate them.

---

### Core Philosophy

> **"Engineering is the application of an empirical, scientific approach to finding efficient, economic solutions to practical problems."**

Engineering is not the tools. It is not the ceremony. It is a way of working that produces reliable results under uncertainty.

---

### What Software Engineering Is Not

Reject the metaphors that mislead:

| Wrong metaphor | Why it fails |
|---|---|
| **Software as construction** | Bridges are built once to a fixed spec. Software changes continuously; the design is never finished. |
| **Software as manufacturing** | Manufacturing optimizes repeated production of an identical thing. Every line of software is written once. Our cost is *design*, not production. |
| **Software as pure craft** | Craft explains individual skill but offers no way to tell whether a practice works. It cannot be measured, so it cannot be improved systematically. |

Software has no production phase. Compilation and deployment are effectively free. **Everything we do is design** — so optimize the design process, not the output.

---

### The Two Problems

All software engineering reduces to two problems. Every practice worth keeping serves one of them.

#### 1. Optimize for Learning

You do not know what you are building until you have built some of it. Structure the work to learn fast and cheaply.

| Idea | Practice |
|------|----------|
| **Iteration** | Take many small passes at a problem, not one large one. Each pass may revise the last. |
| **Feedback** | Build channels that tell you when you are wrong, and shorten them relentlessly. Feedback you receive too late is not feedback. |
| **Incrementalism** | Build in pieces that stand alone and add value. Design so a piece can be replaced without a rewrite. |
| **Empiricism** | Ground decisions in observation of the real system, not in argument about what should be true. |
| **Being experimental** | Form a hypothesis, control the variables, run the test, accept the result. Prefer falsifiable claims to confident ones. |

Nothing here permits sloppiness. Iterating means taking small steps toward a goal — not skipping the thinking.

#### 2. Optimize for Managing Complexity

Complexity is the constraint that eventually stops all progress. Fight it structurally.

| Idea | Practice |
|------|----------|
| **Modularity** | Build from parts with boundaries you can reason about one at a time. |
| **Cohesion** | Keep things that change together in the same place; separate things that change for different reasons. |
| **Separation of concerns** | One module, one concern. Concerns that leak across boundaries multiply the cost of every change. |
| **Information hiding & abstraction** | Expose what a caller needs; hide how it works. An abstraction that leaks its implementation buys nothing. |
| **Coupling** | Coupling is the dominant cost driver. Prefer loose coupling everywhere, and treat any tightening as a debt you chose. |

These are the classical ideas. Farley's contribution is not the list but the claim that follows.

---

### The Forcing Functions: Testability and Deployability

**This is the load-bearing argument of the book.** You do not get modularity, cohesion, separation of concerns, information hiding, and loose coupling by exhorting people to want them. You get them by insisting on two properties that *cannot be faked*:

- **Testability** — code that is hard to test is badly designed. The difficulty is the diagnostic. Fixing testability forces you to fix coupling and cohesion, because there is no other way to fix it.
- **Deployability** — a system that is hard to release is badly designed. Optimizing for release forces modular boundaries, controlled dependencies, and honest interfaces.

So when design quality is the goal, do not argue about design quality. **Make the code testable and the system deployable, and the design follows.** Treat "this is hard to test" as a design finding, never as a reason to skip the test.

---

### Measure Two Things

Farley adopts the DORA measures as the only feedback that says whether your engineering is improving:

| Measure | Composed of | Question it answers |
|---|---|---|
| **Throughput** | Lead time (commit → production) + deployment frequency | How fast can we deliver a change? |
| **Stability** | Change failure rate + time to restore service | How reliably does a change land? |

Two properties make these useful. They are **not a tradeoff** — high performers improve both together, so a proposal that sacrifices one for the other is usually a proposal to do worse work. And they are **outcome measures**, not activity measures: they say nothing about how busy anyone is.

Prefer them over velocity, story points, lines of code, and test count — all of which measure activity and can be improved without improving anything.

---

### Control the Variables

An experiment with uncontrolled variables tells you nothing. Most "we tried that and it didn't work" claims are uncontrolled experiments.

- Change one thing at a time when you want to know what caused a result.
- Make the environment deterministic before you draw conclusions from it — same inputs, same outputs.
- Distinguish a *deterministic* failure from a *flaky* one; a flaky test controls nothing and teaches nothing.
- Keep the feedback loop fast enough that you can afford to run the experiment again.

---

### Work in Small Steps

Small steps are how every idea above is actually implemented.

- Smaller changes are easier to reason about, review, test, and revert.
- Smaller changes fail smaller. Recovery time drops with batch size.
- If a step is too big to take safely, the answer is a smaller step, not more care.
- **If it hurts, do it more often.** Pain at integration, release, or test time is a signal to increase frequency until the pain forces the fix.

---

### Performance: Concurrency Is Complexity

Farley treats speed as a product of good design, not a trade against it. The claims below come from his interviews and his LMAX blog post, not from the book's text. Its table of contents shows the book taking up the subject under Empiricism (ch. 7), Cohesion (ch. 10) and Managing Coupling (ch. 13); cite none of those chapters for a claim here.

This section governs threads that share mutable state in production code. Threads that share nothing until one merge at the end, and threads that overlap independent network waits, need no measurement and raise no item; in a Lambda web app, `lambda-web-app-speed.md`'s LWS-3 flags network waits left serial. A slow test suite belongs to `test-architecture.md`.

- **Concurrency and coupling are the hardest problems in software.** Threads that share state bring both. Add them only when a measurement shows that nothing simpler meets the need.
- **Shared state costs more than threads save.** In Farley's example, the cheapest safe way for several threads to update one counter ran about 300 times slower than one thread doing all the work. Split work across threads only where the parts share nothing until the end.
- **Keep shared state out of the business logic.** LMAX's exchange gave each core one job — network intake, journaling to disk, business logic — shared nothing between them, and fed data to a single-threaded business core. The domain code stayed sequential and testable, and coordination lived at the edges, where ports and adapters (`architecture.md`) put it.
- **Clear code is usually the fast code.** LMAX found that simple code leaves waste fewer places to hide and that compilers optimize it better — the reason `coding.md` lists premature optimization as a smell. Write clear code first.
- **Know the machine at the hot path.** Farley defines high performance as the most effect for the fewest instructions. When a measurement names a hot path, fix it with knowledge of the hardware — allocation, cache lines, false sharing — before adding threads. Martin Thompson, Farley's colleague at LMAX, calls that knowledge mechanical sympathy.

**A file shows the thread but never the measurement.** In a review, ask the author for the measurement; never flag the thread itself as a defect. A write the threads race on with no guard is a defect all the same.

The throughput in *Measure Two Things* measures delivery, not runtime; never read it as requests per second.

*Sources: Tech Lead Journal episode 100 (Farley, on the book); Thoughtworks Technology Podcast, "Software engineering with Dave Farley"; Farley's blog post on the LMAX Disruptor; the book's table of contents.*

---

### Engineering Checklist

- [ ] Does this change make the code easier or harder to test?
- [ ] Does it make the system easier or harder to release?
- [ ] Am I taking one small step, or a large one I cannot revert?
- [ ] What feedback tells me this worked, and how long until I get it?
- [ ] Is this decision grounded in an observation, or in a prediction?
- [ ] Which of the two problems does this practice serve — learning, or complexity?
- [ ] If this is an experiment, which variables did I control?
- [ ] If this adds threads that share state, which measurement showed that nothing simpler would do, and does the business logic stay free of that state?

---

### Anti-Patterns to Avoid

| Anti-pattern | Fix |
|---|---|
| **Tools as engineering** — adopting a platform and calling it a practice | Tools serve a way of working; choose the practice first |
| **Uncontrolled experiment** — changing several things, then attributing the outcome to one | Change one variable; make the environment deterministic |
| **Activity measures** — tracking velocity, points, or commit counts as progress | Measure throughput and stability |
| **Deferring testability** — "we'll add tests once the design settles" | Testability *is* the design signal; deferring it defers the design |
| **Big-batch delivery** — long-lived branches, large releases, staged integration | Smaller batches, integrated continuously |
| **Argument over evidence** — deciding by seniority or confidence | Form a falsifiable claim and test it |
| **Craft as an excuse** — treating design quality as taste beyond measurement | Route it through testability and deployability, which are measurable |
| **Threads as a default speed-up** — parallelizing production code before measuring | Measure first; keep shared mutable state out of the business logic, and push coordination to the edges |

---

### The Mantra

> **Everything is design. Optimize for learning and for managing complexity. Force good design through testability and deployability. Measure throughput and stability, and take smaller steps.**
