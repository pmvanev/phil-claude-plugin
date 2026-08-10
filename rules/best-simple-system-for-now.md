---
paths:
  - "**/*.{ts,tsx,js,jsx,py,go,rs,java,cs,rb,kt,swift,cpp,c,h,hpp,scala,clj,ex,exs,hs,ml,fs,fsx}"
---

# Best Simple System for Now

Guidelines extracted from Dan North's *Best Simple System for Now* (BSSN) — <https://dannorth.net/blog/best-simple-system-for-now/>.

This rule owns the **four-word breakdown**, the **economic case**, and the **reasons teams don't do it**. The parts already covered elsewhere stay there: the five working bullets in `coding.md` §11, the CUPID properties in `coding.md` §16, and the speculative/reactive/empirical design spectrum in `architecture.md` §9. Complement those — do not restate them.

---

### Core Philosophy

> **"The simplest system that meets the needs of the product right now, written to an appropriate standard."**

BSSN is the middle path between two failure modes that both feel like virtue: **perfectionism**, which over-engineers for a future that does not arrive, and **pragmatism**, which cuts corners and calls it speed. Neither is the deal. Every word in the phrase is doing work — read them one at a time.

---

### For Now

**Build for what is actually there. Not for what the pattern suggests will be there.**

The pull toward the general solution is not laziness; it is expertise misfiring. Recognizing a pattern is fast, unconscious, and usually the right instinct — which is exactly why it needs a deliberate check. Seeing what is really in front of you takes conscious effort, every time.

- Solve today's problem. The general case is a different, harder, unrequested problem.
- "We'll need this later" is a prediction. Predictions about software requirements are usually close, and close is wrong in a way that costs more than absence would have.
- Speculative code is not neutral. It must be read, maintained, and reasoned around, and it constrains the change you eventually do need.

### Simple

**Simple is a function of now.** When the requirements change, what counts as simple changes with them. There is no permanently simple design.

> *"Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away."* — Saint-Exupéry

- Minimum complexity **is** maximum adaptability. A simple system can flex in a direction you never predicted; a system built to flex in three predicted directions usually cannot flex in the fourth.
- Watch three specific traps: **premature abstraction**, **over-DRYing** (removing duplication that was coincidental, not conceptual), and **speculative interfaces**.
- Simple is not the same as few lines, and not the same as easy.

### Best

**Match quality to context.** "Best" is not gold-plating and it is not uniform.

- Core business logic earns rigor. An experiment earns much less.
- **Sketching is not hacking.** A sketch has enough quality to sustain progress and stays cheap to throw away. Hacking produces something you cannot throw away and cannot extend.
- The quality bar is a decision you make per component, deliberately — not a global setting, and not an accident.
- What "best" looks like in code is CUPID: Composable, Unix philosophy, Predictable, Idiomatic, Domain-based (see `coding.md` §16). Writing it is as fast as writing poor code — faster, usually. It takes habits, not heroics.

### System

**The whole thing, not the parts.** BSSN judges the system, and the system is more than the code — it includes the tests, the build, the deployment path, the operational story, and the people who work in it.

- A collection of individually tidy components is not a simple system if the whole is incoherent.
- Ask whether someone new can navigate it, not whether each file is clean.
- Local optimization that degrades the whole is a net loss, however good the part looks.

---

### The Economic Case

The objection to BSSN is always some version of "iterating is wasteful — we'll rework it." That argument counts the wrong costs. Following Reinertsen, **value costs dwarf effort costs**, and only effort costs appear on the burn-down:

| Cost | What it is | Why it dominates |
|---|---|---|
| **Cost of Delay** | Revenue not earned while you are still building | Accrues every day, invisibly, and usually exceeds team cost |
| **Opportunity Cost** | What the team could have built instead | Compounds with every week spent on the unrequested general case |
| **Value at Risk** | Exposure to being wrong about the whole bet | Shrinks the moment something real ships |
| **Effort Cost** | Burn rate, licenses, rework | The only one most plans actually track |

So iterative delivery can look worse on paper ROI and still be the better decision: on a **risk-adjusted** basis it wins, because it starts returns earlier and cuts the exposure of building the wrong thing at all. Rework you actually needed is cheaper than speculation you didn't.

---

### Rebuttals to Keep Handy

| Objection | Answer |
|---|---|
| **"Too simple for production — this is just a prototype"** | Successful prototypes are rarely rewritten; they are built upon. WhatsApp served hundreds of millions on a small Erlang codebase; SQLite is among the most-deployed software on earth, maintained by a tiny team. |
| **"It ships an incomplete product"** | Deliberate incompleteness is a feature. The original iPhone shipped on 2G with no copy-paste and won anyway. Google Docs never matched Office's feature list and did not need to. |
| **"Constant rework is inefficient"** | See the economics above. Delay and opportunity cost are the large numbers; rework is the small one. |

The shared move in all three: **look at the actual scope of the problem, not the general case.** North's team replaced a library debate with a nine-method interface for their nine entity types — zero dependencies, no transitive complexity, fully transparent behavior. XStream was rejected as "too simple" and is still in use two decades later, still simple.

---

### Why Teams Don't Do This

Knowing BSSN is not doing BSSN. Three things are required, and all three are hard:

1. **Good habits.** Resisting premature abstraction, extra dependencies, and over-specification is a daily practice, not a decision you make once. It is best learned by pairing with someone who already has it.
2. **Courage.** BSSN contradicts received wisdom and therefore feels reckless. The way in is "trust me once" — try it on one contained problem and look at the result.
3. **Humility.** It means trusting the part of you that knows it doesn't know, over the confident part making predictions. Be like water: flexible because it is simple, not because it anticipated the shape of the container.

---

### Checklist

- [ ] Am I solving the problem in front of me, or the general case I recognized?
- [ ] Which of these am I about to add — an abstraction, a dependency, an interface, a configuration point — and what present need requires it?
- [ ] Is this duplication conceptual, or coincidental? (Only the first should be removed.)
- [ ] Is this a sketch or a keeper, and does its quality match that answer?
- [ ] Is the *whole system* coherent, or just this component?
- [ ] What is the cost of delay on shipping this later than I could?
- [ ] If I am wrong about the future, is this cheap to delete?

---

### Anti-Patterns to Avoid

| Anti-pattern | Fix |
|---|---|
| **Speculative generality** — building the general case before a second case exists | Solve for one. Generalize when the second real case arrives |
| **Over-DRYing** — merging code that merely looks alike | Remove conceptual duplication only; coincidental duplication is not debt |
| **Gold-plating** — production rigor on an experiment | Set the quality bar per component, deliberately |
| **Hacking disguised as sketching** — throwaway quality on something you cannot throw away | A sketch stays cheap to discard; if you can't discard it, it needed the bar |
| **Component polish, system neglect** — clean files, incoherent whole | Judge the system: code, tests, build, deploy, operations, people |
| **Effort-cost-only planning** — tracking burn rate while ignoring delay | Price cost of delay and opportunity cost before choosing scope |
| **"We'll need it later"** — a prediction presented as a requirement | Name the present need, or leave it out |

---

### The Mantra

> **Solve what is really there, as simply as now allows, to a standard the context earns, judged across the whole system — and ship it before the cost of delay eats the value.**
