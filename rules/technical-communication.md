---
paths:
  - "**/*.md"
  - "**/*.txt"
  - "**/*.rst"
  - "**/docs/**"
  - "**/README*"
  - "**/CHANGELOG*"
  - "**/CONTRIBUTING*"
---

# Technical Communication

Guidelines extracted from Mike Markel and Stuart A. Selber's *Technical Communication* (Bedford/St. Martin's — Macmillan Learning; 14th ed. as of this writing).

This rule works at a **different altitude** from the plugin's other prose standards, and that difference is the whole point of having it:

| Rule | Altitude | Asks |
|---|---|---|
| `writing.md` (Strunk & White) | Sentence | Is this sentence clear and tight? |
| **this rule** | **Document** | **Is this document fit for its reader and its purpose?** |

Sentence-level clarity and concision stay in `writing.md` — do not restate them here. This rule owns audience analysis, comprehensiveness, accessibility, and honesty of content: the failures a perfectly-written sentence cannot fix.

---

### Core Philosophy

> **"Your goal is to produce a document that conveys a single meaning the reader can understand easily."**

A technical document is a tool someone uses to do something. It succeeds when that person succeeds. Elegance that leaves the reader unable to act is failure.

---

### The Measures of Excellence

Markel's central framework. Editions group these differently — seven to nine, with usability added in later editions — but the substance is stable. Treat it as a review rubric: walk the list, ask each question of the document in front of you.

| Measure | The question | Failure looks like |
|---|---|---|
| **Honesty** | Is every claim true, and does the whole leave a true impression? | Technically-accurate statements arranged to mislead; buried caveats |
| **Clarity** | Does the *document* convey one meaning, easily? (sentence-level clarity: see `writing.md`) | Ambiguity a reader must resolve by guessing |
| **Accuracy** | Are the facts, figures, and names right? | Wrong version numbers, stale commands, transposed values |
| **Comprehensiveness** | Is everything the reader needs here, in enough detail to follow? | Missing prerequisites; a step that assumes unstated knowledge |
| **Accessibility** | Can a reader find the part they need without reading it all? | One undifferentiated wall of text; no headings |
| **Usability** | Can the reader actually *do* the task with this? | Instructions that are correct and unfollowable |
| **Conciseness** | Is it short enough for a busy reader? (see `writing.md`) | Padding that dilutes the signal |
| **Professional appearance** | Does it meet the conventions of its format? | Inconsistent formatting that costs credibility |
| **Correctness** | Grammar, punctuation, spelling, usage (see `writing.md`) | Errors that make the reader doubt the content |

Honesty and comprehensiveness are the two most often missed, because neither is visible in the prose. A document can read beautifully and still omit the thing the reader needed.

---

### Start With Audience and Purpose

This is the first move, not a preliminary. Nearly every document-level failure traces back to skipping it.

**Ask about the reader:**

- What do they already know? What do they *need* to learn here?
- What will they do with this document — read it once, follow it step by step, consult it under pressure?
- What do they expect from a document of this kind?
- What is their attitude toward the subject, and toward you?

**Name the audiences, plural.** Most technical documents have more than one:

| Audience | Wants |
|---|---|
| **Primary** | To act — the person the document is for |
| **Secondary** | To decide, approve, or be informed |
| **Expert / technician** | Precision, mechanism, edge cases |
| **Manager** | Implications, cost, risk, the decision |
| **General reader** | Orientation and plain terms first |

When audiences differ this much, serve them in separate sections rather than averaging them into prose that fits nobody. An executive summary exists for exactly this reason.

**State the purpose in a sentence** before drafting: *after reading this, the reader will be able to ___.* If that sentence is hard to write, the document is not ready to write.

**Across cultures**, do not assume your conventions travel: directness, humor, idiom, date and number formats, and expectations about hierarchy all vary.

---

### Design for Access, Not Decoration

Readers of technical documents scan, jump, and consult. Structure is a usability feature.

**Three functions structure performs:**

- **Chunking** — break content into pieces a reader can take in at once
- **Queuing** — signal relative importance through visual hierarchy (heading levels, weight, size)
- **Filtering** — let a reader distinguish *kinds* of information at a glance (a warning looks unlike a step, which looks unlike an example)

**Four design principles:**

| Principle | Means |
|---|---|
| **Proximity** | Related things sit together; unrelated things sit apart |
| **Alignment** | A visual structure that shows relationship and reading order |
| **Repetition** (consistency) | The same kind of element looks the same throughout |
| **Contrast** | Real visual difference marks real difference in importance |

Applied to the documents this repo produces: headings that describe content rather than label it, a heading level per real level of nesting, tables for comparison and prose for argument, and one consistent treatment per element type.

---

### Instructions and Safety

For any document that tells someone how to do something:

- **Imperative mood, one action per step.** "Run `make build`" — not "the build should then be run."
- **Number sequential steps**; bullet non-sequential ones. The numbering is a claim about order.
- **State prerequisites before step one** — required access, tools, versions, state.
- **Put the warning before the step it applies to.** A caution discovered after the damage is not a caution.
- Respect the severity hierarchy: **DANGER** (will cause injury) → **WARNING** (may cause injury) → **CAUTION** (may cause damage) → **NOTE** (useful information). Do not inflate; a document where everything is a warning has no warnings.
- **Say what success looks like** so the reader can tell whether the step worked.

---

### Honesty in Content and Graphics

Honesty is a content property, not a tone.

- Do not mislead by selection, omission, or emphasis. A set of true sentences can add up to a false impression.
- Present limitations where the reader will encounter them, not in a footnote after the decision.
- **Graphics carry the same obligation** as prose: label axes, start value axes at zero unless you say otherwise and why, keep scales honest, and never let visual design imply a difference the data does not support.
- Every graphic needs a purpose, a reference from the text, and enough caption to stand alone.
- Attribute borrowed material. Cite sources for data you did not produce.

---

### Checklist

- [ ] Who is the primary reader, and what will they do with this?
- [ ] Can I write "after reading this, the reader will be able to ___"?
- [ ] Is there a second audience being served badly by an averaged document?
- [ ] What does the reader need that is not here? (comprehensiveness — the most-missed measure)
- [ ] Are the prerequisites stated before the first step?
- [ ] Can a reader find one section without reading all of it?
- [ ] Do headings describe content, or merely label it?
- [ ] Does every warning precede the thing it warns about?
- [ ] Does the whole document leave a true impression, not just true sentences?
- [ ] Is every graphic referenced, labeled, and honestly scaled?

---

### Anti-Patterns to Avoid

| Anti-pattern | Fix |
|---|---|
| **No named audience** — written for whoever shows up | Name the primary reader and their task first |
| **Averaged audience** — one register serving expert and novice equally poorly | Separate sections; add a summary for deciders |
| **Missing prerequisites** — step one assumes unstated setup | State access, tools, versions, and starting state up front |
| **Wall of text** — correct content, unnavigable | Chunk, add descriptive headings, queue by real importance |
| **Label headings** — "Overview", "Details", "Miscellaneous" | Headings that say what is in the section |
| **Warning after the step** | Move it before; a late caution is decoration |
| **Alarm inflation** — everything marked important or WARNING | Reserve severity for real severity |
| **True but misleading** — accurate parts, false whole | Check the impression, not just the assertions |
| **Undefended graphic** — unlabeled, unreferenced, or truncated axis | Label, reference from the text, scale honestly |
| **Curse of knowledge** — writing for who you are, not who reads | Ask what the reader knows, then write from there |

---

### The Mantra

> **Name the reader and the task. Give them everything they need and nothing they don't. Make it findable, make it followable, and make the whole thing true — not just the sentences.**
