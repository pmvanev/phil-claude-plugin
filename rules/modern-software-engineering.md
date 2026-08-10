---
paths:
  - "**/*.{ts,tsx,js,jsx,py,go,rs,java,cs,rb,kt,swift,cpp,c,h,hpp,scala,clj,ex,exs,hs,ml,fs,fsx}"
---

# Modern Software Engineering

Guidelines extracted from Dave Farley's *Modern Software Engineering: Doing What Works to Build Better Software Faster*.

This rule owns Farley's **spine** — engineering as an empirical discipline, the two problems all software work reduces to, and the two measures that tell you whether you are improving. The details live in the rules that already own them: empirical design in `architecture.md`, the four testability properties in `testing.md`, pipeline and release mechanics in `continuous-delivery.md`, evolutionary coding practices in `coding.md`. Complement those — do not restate them.

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

### Engineering Checklist

- [ ] Does this change make the code easier or harder to test?
- [ ] Does it make the system easier or harder to release?
- [ ] Am I taking one small step, or a large one I cannot revert?
- [ ] What feedback tells me this worked, and how long until I get it?
- [ ] Is this decision grounded in an observation, or in a prediction?
- [ ] Which of the two problems does this practice serve — learning, or complexity?
- [ ] If this is an experiment, which variables did I control?

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

---

### The Mantra

> **Everything is design. Optimize for learning and for managing complexity. Force good design through testability and deployability. Measure throughput and stability, and take smaller steps.**
