---
paths:
  - "**/*.{ts,tsx,js,jsx,py,go,rs,java,cs,rb,kt,swift,cpp,c,h,hpp,scala,clj,ex,exs,hs,ml,fs,fsx}"
---

# Clean Craftsmanship

Guidelines extracted from Robert C. Martin's *Clean Craftsmanship: Disciplines, Standards, and Ethics*.

This rule owns the book's **standards and ethics** — what a programmer owes the people who depend on the code, and the promises that follow. The disciplines live in the rules that already own them: the three laws, test doubles and F.I.R.S.T. in `testing.md`; simple design and the humble object in `coding.md`; the refactoring cycle and the tidyings in `refactoring.md`. Complement those — do not restate them.

**The two halves divide on checkability, not on subject.** A reviewer can apply the standards to a diff: a knowingly shipped defect, a test suite that cannot support change, a module only one person can touch. Nobody can grade the oath from code — it is a charter a team adopts, and adopting it is the only enforcement it has. Both halves are here, labeled, so neither borrows the other's authority.

---

### Core Philosophy

> **"The only way to go fast is to go well."**

Speed and quality are not a trade. The mess that buys a week costs a month, and it charges interest for as long as the code lives.

---

### Why Standards Exist

Software runs the world. It moves money, dispatches ambulances, flies aircraft, and decides who gets a loan. Almost nothing in modern life happens without a programmer having written something first.

That power arrived faster than the discipline to hold it. Programmers set their own bar today because no one else has set one — and because the day a catastrophe forces legislators to set one, they will set it badly. **A profession that will not govern itself gets governed.**

So these standards are not aspirations. They are the terms on which the rest of the world should be willing to depend on us.

---

### The Standards

Martin groups them three ways. Read each as a commitment you make to the business, not a favor you do for the code.

#### Productivity

| Standard | The commitment | What it rules out |
|---|---|---|
| **We ship no defects** | Every release works as specified | "Known issues" as a shipping category |
| **Continuous readiness** | The system is deployable at the end of every day | A stabilization phase before release |
| **Stable productivity** | The tenth month runs as fast as the first | Velocity that decays and gets blamed on scale |
| **Inexpensive adaptability** | A small requirement change costs a small change | "The architecture won't allow that" |

**Decaying productivity is the diagnosis, not the weather.** Software is called soft because it was meant to be easy to change. When a change that sounds small turns out expensive, the estimate is reporting a design defect.

#### Quality

| Standard | The commitment | What it rules out |
|---|---|---|
| **Continuous improvement** | The code is better this month than last | Freezing a module because touching it is risky |
| **Fearless competence** | Any programmer may change any code | Territory nobody dares refactor |
| **Extreme quality** | Good enough is not the bar | Shipping what you would not sign |
| **QA finds nothing** | QA confirms; it does not discover | Handing testers a defect-detection job |
| **Automate the repeatable** | Machines do what machines can do | Manual regression passes |
| **We cover for each other** | Two people can work on any part | A module with one owner and no second reader |

**Fearless competence is a loop, and it runs in one direction.** You fear the code, so you leave it alone; left alone, it rots; rotted, it deserves more fear. Tests are the only thing that breaks the loop, which is why a suite you do not trust is worse than none — it charges the cost and pays no dividend.

#### Courage

| Standard | The commitment | What it rules out |
|---|---|---|
| **Honest estimates** | Say what you know, with its uncertainty | A date presented as a fact |
| **You must say no** | Refuse what you cannot deliver | "Yes" bought by hoping |
| **Continuous aggressive learning** | Keep your skills current on your own time | Waiting for an employer to schedule it |
| **Mentoring** | Teach the next programmer deliberately | Leaving juniors to absorb it by osmosis |

---

### Estimates Are Not Promises

An estimate is a probability distribution. A promise is a commitment. Confusing the two is how teams end up dishonest without anyone lying.

- **Give three numbers, not one** — best case, nominal, worst case. A single number hides everything the reader needs.
- **"I don't know" is an honest estimate.** It is often the only honest one, and it invites the question that produces a better one.
- **Aggregate the distributions, not the optimism.** Summing best cases across ten tasks yields a schedule that no combination of outcomes will meet.
- **Never let an estimate become a date by being repeated.** State the uncertainty every time, in the same breath.

---

### Saying No

The hardest standard, and the one that protects every other standard.

- **Say no to the schedule, never to the quality.** Scope and dates negotiate; the tests, the design and the discipline do not. A team that trades quality for a date has traded away next quarter as well.
- **"Yes" you cannot deliver is a lie with a delay on it.** It buys peace in the meeting and spends it, with a penalty, in the one after.
- **"I'll try" is worse than either.** It promises a reserve of effort you do not have, and it converts a disagreement into a commitment without anyone noticing.
- **Give the real number and let the business decide.** Your job is an accurate picture, not a comfortable one; deciding what to do about it is theirs.

---

### The Programmer's Oath

The charter half. It binds nobody who has not agreed to it, which is the point — a team adopts it out loud or does not hold it at all.

> In order to defend and preserve the honor of the profession of computer programmers, I promise that, to the best of my ability and judgement:
>
> 1. I will not produce harmful code.
> 2. The code that I produce will always be my best work. I will not knowingly allow code that is defective either in behavior or structure to accumulate.
> 3. I will produce, with each release, a quick, sure, and repeatable proof that every element of the code works as it should.
> 4. I will make frequent, small, releases so that I do not impede the progress of others.
> 5. I will fearlessly and relentlessly improve my creations at every opportunity. I will never degrade them.
> 6. I will do all that I can to keep the productivity of myself and others as high as possible. I will do nothing that decreases that productivity.
> 7. I will continuously ensure that others can cover for me, and that I can cover for them.
> 8. I will produce estimates that are honest both in magnitude and precision. I will not make promises without certainty.
> 9. I will never stop learning and improving my craft.

Promises 2, 3, 5 and 7 restate standards a reviewer can check. Promises 1, 4, 6, 8 and 9 describe conduct over a career, and no diff will ever show them.

---

### Conduct Checklist

- [ ] Am I about to ship something I know is defective?
- [ ] Could this system deploy today, or does it need a stabilization pass first?
- [ ] Is there code here I am avoiding because changing it frightens me?
- [ ] Do the tests let me change this fearlessly, or do they only report coverage?
- [ ] Can anyone but me work on this module?
- [ ] Did I give an estimate, or did I give a date?
- [ ] Did I say yes to something I cannot deliver — or "I'll try"?
- [ ] What did I learn this month, and who did I teach?

---

### Anti-Patterns to Avoid

| Anti-pattern | Fix |
|---|---|
| **Known issues as a release category** | Fix it or cut it; a shipped defect is a shipped decision |
| **The stabilization phase** — a sprint spent making the build releasable | Stay releasable daily; the phase is the symptom |
| **Quality traded for a date** | Negotiate scope; the schedule is the only thing that was ever negotiable |
| **The frozen module** — code nobody will touch | Write the characterization tests, then refactor it; fear is the finding |
| **Single-owner code** — one person who understands a subsystem | Pair on it until a second person does |
| **The single-number estimate** | Three numbers and the uncertainty, every time |
| **"I'll try"** | Say yes, or say no, and say which |
| **Dumping on QA** — shipping to testers to find the defects | Your tests find them first; QA confirms |
| **Learning on the employer's schedule** | The craft is yours; keep it current yourself |

---

### The Mantra

> **Ship no defects, stay always ready, keep the code changeable by anyone, estimate honestly, and say no when no is the truth — because the only way to go fast is to go well.**
