---
name: red-team-prose
description: Skill bundle for phil:red-team-prose command — red-teams a document from all three prose angles in one pass, AI-generated tells (ai-eos) plus Elements of Style clarity (eos) plus document fitness for audience and purpose (rules/technical-communication.md), as a single ranked report with an approval gate before any edit
---

# Red-Team Prose

You are red-teaming a document against **all three** prose standards this plugin owns, in one pass:

| Pass | Tag | Source | Asks |
|------|-----|--------|------|
| **Tells** | `[tells]` | `skills/ai-eos/SKILL.md` | Does this read as AI-generated? |
| **Clarity** | `[clarity]` | `skills/eos/SKILL.md` | Is this clear, concise, and active? |
| **Fitness** | `[fitness]` | `rules/technical-communication.md` | Is this fit for its reader and purpose? |

The three catch different failures at different altitudes, so the overlap is small:

- `ai-eos` finds prose that is **hollow** — grand claims carrying no fact, participle clauses padding cadence. *Register.*
- `eos` finds prose that is **slack** — passive voice, needless words, weak endings. *Sentence.*
- `technical-communication` finds prose that is **unfit** — no named reader, missing prerequisites, unnavigable structure, a true-sentences-false-whole document. *Document.*

A document can fail any one independently. The third is the one the other two structurally cannot catch: every sentence can be tight, active, and free of tells while the document still omits what the reader needed.

**Note the asymmetry.** Two passes load skills; the fitness pass loads a **rule** directly, as `ux-review` does with `rules/ux.md`. There is no `technical-communication` skill — do not look for one.

**You review first and edit second, never both at once.** Report everything, get approval, then apply only what is safe to apply.

---

## Parse the Argument

Determine what `$ARGUMENTS` refers to:

| Pattern | Type | Example |
|---------|------|---------|
| `--changes` | Latest git changes | `--changes` |
| Digits separated by `-` or `:` | Line range | `42-67`, `42:67` |
| Has a file extension | File path | `README.md`, `docs/setup.md` |
| Ends with `/` or a directory with no extension | Directory path | `docs/`, `skills/` |
| No argument | Prose in the current context | — |

Pass the argument through to all three passes unchanged, so they review exactly the same span.

**One exception.** The fitness pass judges the document as a whole — audience, completeness, structure. A line range cannot be judged for comprehensiveness or navigability. When the argument is a line range, read the whole file for the fitness pass, scope the other two to the range, and say so in the report.

---

## Step 1: Read Once

Read the target **once** and hold it for all three passes. Do not read the file three times.

Resolve the argument as `ai-eos` Step 1 specifies (`--changes` → `git diff HEAD~1 --name-only` filtered to `**/*.{md,txt,rst}`; line range → read with surrounding context; directory → glob recursively). Review prose only — skip code blocks, frontmatter, config, link URLs, and generated output.

---

## Step 2: Run the Tells Pass

Load `skills/ai-eos/SKILL.md` and apply its catalog and tiers to the text. Honor its `What NOT to Flag` section in full — especially the em-dash rule and the single-vocabulary-hit rule. Compute its density verdict.

---

## Step 3: Run the Clarity Pass

Load `skills/eos/SKILL.md` and apply its ten editing rules to the same text — but **diagnostically**. Identify each violation and its rewrite; do not edit the file yet. Honor `eos`'s Safety section: preserve meaning, formatting, tone, and domain terminology.

---

## Step 4: Run the Fitness Pass

Load `rules/technical-communication.md` and apply it to the document **as a whole**. This pass is not span-by-span like the other two — it walks the measures of excellence and the checklist, asking whether the document serves its reader.

Check, in this order:

1. **Audience and purpose** — is the primary reader identifiable, and can you state "after reading this, the reader will be able to ___"? If not, that is the first finding and usually the root of the others.
2. **Comprehensiveness** — what does the reader need that is not here? Missing prerequisites, unstated assumptions, absent success criteria.
3. **Accessibility and structure** — can a reader find one part without reading all of it? Do headings describe or merely label? Is nesting real?
4. **Honesty of the whole** — do true sentences add up to a true impression? Are limitations where the reader meets them?
5. **Instructions**, where present — imperative mood, prerequisites first, warnings before their step, no alarm inflation, success stated.

**Expect most fitness findings to be `[NEEDS YOU]`.** "The audience is never named" and "this omits the prerequisite" cannot be auto-fixed — the missing thing is information you do not have. That is a property of the altitude, not a defect in the pass. Never fabricate the missing content.

Report fitness findings even when they have no span. A missing section has no line number; anchor it to the nearest heading and say what is absent. This is the **one exception** to the quote-the-span rule below, and it applies to absence only — never to a vague impression.

---

## Resolving overlap between the passes

The three catalogs collide in a few places. Assign each finding to exactly one pass so nothing is reported twice:

| Finding | Owner | Why |
|---------|-------|-----|
| "utilize" → "use", "facilitate" → "help" | `eos` (fancy words) | A plain-word substitution, not a tell |
| "seamless", "robust", "cutting-edge" | `ai-eos` (promotional register) | Marketing register, not verbosity |
| "it is important to note that" | `eos` (needless words) | Deletable filler with no AI signature |
| "highlighting its importance in..." | `ai-eos` (participle padding) | The signature construction |
| "absolutely essential", "completely unique" | `eos` (do not overstate) | Intensifier misuse |
| "stands as a testament to" | `ai-eos` (unearned significance) | Inflation of a mundane fact |
| Three near-synonym adjectives | `ai-eos` (rule-of-three padding) | Cadence padding |
| Passive voice, weak endings, parallelism | `eos` | No AI-tell equivalent |
| Conciseness, correctness, sentence-level clarity | `eos` | `technical-communication` names these measures but defers to `writing.md` for them |
| Overstated *register* ("powerful", "seamless") | `ai-eos` | Tone inflation |
| Misleading or missing *content* | `[fitness]` (honesty, comprehensiveness) | A content defect, not a word choice |
| Headings, nesting, navigability, prerequisites | `[fitness]` | No sentence-level equivalent |
| Audience mismatch, undefined purpose | `[fitness]` | Only this pass asks the question |

The honesty split is the one worth getting right: **`ai-eos` owns register, `[fitness]` owns content.** "A powerful, seamless solution" is a tells finding. "Claims 40% faster without saying faster than what" is a fitness finding. When a span genuinely violates two passes, report it once under the more severe and note the other rule on the same line. Never list one span twice.

---

## Step 5: Report All Three, Ranked Together

Report inline. Write no files. Lead with three verdicts, then merge the findings into one worst-first list.

```
RED-TEAM: {file}

TELLS:   {verdict} — {N} tells / {M} words, {K} mechanisms
CLARITY: {n} rewrites, {m} cuts across {j} of eos's 10 rules
FITNESS: {verdict} — {which measures fail}; audience {named | never named}

FINDINGS ({total}) worst-first

  §{heading}  [fitness] comprehensiveness
              Missing: prerequisites for step 1 (required access, tool versions)
              Measure: a reader cannot start from what is here.  [NEEDS YOU]

  L{line}  [tells] {mechanism name}
           "{exact quoted span}"
           Mechanism: {why an LLM produces this}
           Fix: {cut | plain form}                        [auto-applicable]

  L{line}  [clarity] {eos rule name}
           "{exact quoted span}"
           -> "{the rewrite}"                             [auto-applicable]

COPULATIVE RATIO: {n} avoidances vs {m} plain is/has     (omit if no pattern)

{X} of {total} are auto-applicable. {Y} need a fact only you have.
```

Ranking rules:
- **Worst-first across all three passes**, interleaved. Not grouped by pass, and not file order.
- Rank by cost to the reader: **a document the reader cannot use outranks any sentence-level defect.** Missing prerequisites and unnamed audience go first; then hollow claims and phantom attribution; then passive voice; then fancy words.
- Tag every finding `[tells]`, `[clarity]`, or `[fitness]` so the source pass is always visible.
- Mark each finding `[auto-applicable]` or `[NEEDS YOU]`.
- Quote the **exact span** — except for fitness findings about absence, which anchor to a heading (`§`) and name what is missing.
- If all three come back clean, say so plainly and stop.

---

## Step 6: Offer to Apply — Approval Gate

After reporting, ask once:

> "Apply the {X} auto-applicable fixes? The {Y} marked NEEDS YOU require a fact I don't have."

Then:

- **On approval** — apply only the `[auto-applicable]` fixes, using `eos`'s editing discipline for clarity fixes and plain deletion for tells fixes. Report what you changed, per line.
- **On refusal, or no answer** — change nothing. The report is the deliverable.
- **Never** apply a `[NEEDS YOU]` finding. Not on approval, not on a follow-up "fix everything." Those need information the document does not contain.

Applying is opt-in every time. Do not offer to apply before the full report, and do not bundle the two.

---

## Safety

- **Never invent a fact** to replace vagueness, and **never write the missing section.** This is the single hardest rule here, and the fitness pass raises the stakes: `eos`'s habit is to rewrite, `ai-eos` findings often *look* rewritable, and a missing-prerequisites finding is a standing invitation to invent prerequisites. "Plays a crucial role in validation" cannot become "validates the request schema" unless you verified that it does. Flag the gap and stop.
- **Never accuse the author.** Report tells in the text, not conclusions about provenance. Detection is unreliable and humans perform near chance — you are reporting style, not authorship.
- **Respect every `What NOT to Flag` boundary.** `ai-eos` protects the em dash as a mark, single vocabulary hits, correct technical terms, and this project's deliberate house style. `eos` protects meaning, formatting, tone, and domain terminology. A three-pass composite is not a licence to flag more than any pass would alone — it is three lenses, not a lower bar.
- **Fitness findings need a named measure.** "This could be clearer" is not a finding. "Comprehensiveness: a reader cannot start without the tool versions" is. No measure, no finding — this is the fitness pass's equivalent of the quote-the-span rule, and it is what stops the pass becoming vague editorializing.
- **Judge the document it is, not the document you'd write.** A terse reference page is not failing comprehensiveness for lacking a tutorial. Fitness is measured against the document's own purpose and audience.
- **No double-reporting.** One span, one finding. Use the overlap table.
- **When uncertain, skip.** A false flag on deliberate prose costs more than a missed one.

---

## Scope

This skill owns **prose review across all three standards**. It does not own:

- **Comment and docstring quality** → `clean-comments`
- **CLAUDE.md structure** → `claude-md`
- **Independent adversarial critique** → `adversarial-review` (a different tool with a different contract: fresh-context reviewer, separate judge, honesty label)
