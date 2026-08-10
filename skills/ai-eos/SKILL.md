---
name: ai-eos
description: Skill bundle for phil:ai-eos command — detects the stylistic tells that mark technical prose as AI-generated, with a density verdict and ranked findings
---

# AI Elements of Style

You are hunting the stylistic tells that mark a piece of technical prose as AI-generated. Your job is to find them and report them. You do not edit.

The counterpart to `eos`: where `eos` holds prose to Strunk & White, this holds prose to the tells that a machine wrote it. Same target, different standard.

Invoked directly as `/phil:ai-eos`, or as one half of `/phil:red-team-prose` (which pairs this pass with an `eos` clarity pass over the same document).

Take an adversarial stance: assume the text is trying to pass as human-written and look for what gives it away. But hold the opposite discipline just as hard — **a tell is a specific span you can quote, name, and fix.** Vague suspicion is not a finding.

This skill owns **LLM tells only**. Clarity, concision, and voice belong to `eos`; comment quality belongs to `clean-comments`. Do not review against those here.

**Density beats any single token.** Every credible source on this says so. One "pivotal" proves nothing; four mechanisms clustered in one paragraph is damning. Lead with the density verdict, then the spans.

## Sources

The catalog below summarizes [Wikipedia's *Signs of AI writing*](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup, CC BY-SA), the excess-vocabulary measurements in Kobak et al., *Delving into LLM-assisted writing in biomedical publications through excess vocabulary* (Science Advances, 2025) and Liang et al., *Mapping the Increasing Use of LLMs in Scientific Papers* (COLM, 2024), and George Orwell's "Politics and the English Language" (1946) on the dying metaphor and the ready-made phrase.

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

If the argument contains both a file and a line range (`docs/setup.md:12-30`), split them.

---

## Step 1: Gather the Prose

Review prose only. Skip code blocks, frontmatter, config, link URLs, and generated output. Review table cells only when they contain sentences.

### `--changes`
Run `git diff HEAD~1 --name-only`, filter to prose files (`**/*.{md,txt,rst}`), and read each in full. Review only the added and modified lines — but read the whole file for context, since density is a property of the passage, not the diff.

### Line Range
Read the file with surrounding context. Review the selected block only.

### File Path
Read the entire file.

### Directory Path
Glob recursively for `**/*.{md,txt,rst}`. Review each. For large directories (>20 files), use an Explore agent to parallelize reading.

---

## Step 2: Hunt the Tells

Two tiers. **Tells** are over-the-top enough to flag on a single occurrence. **Whiffs** are weak signals — flag them only when they cluster with tells or with each other.

For every finding, name the **mechanism** (why an LLM produces it), not just the phrase. The mechanism is what makes the finding actionable and what keeps the catalog useful as models change.

### Tell tier — flag on sight

**1. Unearned significance**
Inflates a mundane fact into grand importance. The subject always "stands," "serves," or "plays a role" rather than simply doing something.

> "stands as a testament to" · "plays a crucial/pivotal/vital role in" · "underscores the importance of" · "marks a key turning point" · "reflects a broader shift toward" · "has become synonymous with"

*Fix:* cut, or replace the claim with the specific thing the subject actually does.

**2. Participle padding**
A trailing `-ing` clause bolted to a finished sentence, adding cadence and no information. The single most reliable tell in technical prose.

> "..., highlighting its importance in modern workflows" · "..., ensuring scalability and reliability" · "..., reflecting the team's commitment to quality" · "..., contributing to overall performance"

*Fix:* cut. If the clause carries a real claim, promote it to its own sentence with a subject.

**3. The formulaic closer**
A wrap-up that concedes a vague weakness and pivots to vague optimism. Often arrives unbidden at the end of a section that needed no conclusion.

> "Despite these challenges, [subject] remains well positioned to..." · "While not without limitations, ..." · "In conclusion," · "Overall," · "As the landscape continues to evolve, ..."

*Fix:* delete the paragraph. If a real limitation exists, state it plainly and stop.

**4. Phantom attribution**
Opinion attributed to an unnamed consensus, inflating one source — or zero — into a field.

> "Experts argue that" · "Observers have noted" · "Industry reports suggest" · "It is widely regarded as" · "Many developers find" · "Critics have pointed out"

*Fix:* name the source, or cut the claim. Flag this as **needs a fact you cannot supply** — never invent the citation.

**5. Copulative avoidance**
Systematic refusal of plain *is* and *has*. One instance is style; a pattern across a passage is a fingerprint.

| Tell | Plain form |
|------|-----------|
| serves as / functions as / acts as | is |
| represents / constitutes / embodies | is |
| marks / stands as | is |
| features / boasts / offers / maintains | has |
| enables / facilitates / allows for | lets, or the actual verb |

*Fix:* use *is* and *has*. Count occurrences and report the ratio — that's the evidence.

**6. Negative parallelism**
Defines by contrast with a strawman, for rhythm rather than meaning.

> "not just X, but Y" · "not only X but also Y" · "it isn't about X — it's about Y" · "not a X, but a Y" · "X rather than Y" (when nobody proposed X)

*Fix:* state Y. Drop the contrast unless a reader would genuinely have assumed X.

**7. Rule-of-three padding**
Three coordinate items where one carries the meaning and two pad the cadence. Especially adjectives.

> "fast, reliable, and scalable" · "clear, concise, and actionable" · "designing, building, and maintaining"

*Fix:* keep the item that does work; cut the rest. Legitimate triads name three distinct things — flag only when the members are near-synonyms or the third is filler.

**8. Promotional register**
Marketing warmth in documentation that asked for none. Reads like a launch post wearing a manual's clothes.

> "seamless" · "robust" · "powerful" · "cutting-edge" · "groundbreaking" · "state-of-the-art" · "effortlessly" · "a rich set of" · "a diverse array of" · "boasts" · "vibrant" · "nestled"

*Fix:* cut the adjective, or replace it with the measurement that justifies it.

### Whiff tier — flag only when clustered

**9. Era vocabulary** — *dated section; replace as models shift.*
Words measured as sharply over-represented in post-2022 text. This list is the most perishable part of this skill; treat it as evidence, not law.

> delve · tapestry · intricate · pivotal · realm · showcase · leverage (as a verb) · foster · align with · landscape · testament · myriad · nuanced · underscore · harness · elevate · streamline · robust

A single occurrence in correct technical use is **not** a finding. Three or more in a short passage is.

**10. Elegant variation**
Synonym churn for one referent across a passage — "the parser," then "the analyzer," then "the component," then "the module," all meaning the same thing. Caused by repetition penalties.

*Fix:* pick one term and repeat it. Technical prose wants consistent naming, not variety.

**11. Formatting tells**
Title Case In Headings · boldface on repeated phrases or scattered across a paragraph · emoji as structural markers · inline-header vertical lists (**Term** — definition, stacked) · thematic breaks (`---`) immediately before a heading · skipped heading levels.

*Fix:* match the surrounding document's conventions. Only flag deviation from the file's own established pattern.

**12. Assistant residue**
Conversational scaffolding that survived the copy-paste. Rare, but conclusive when present — promote to Tell tier on sight.

> "Certainly!" · "I hope this helps" · "Let me know if you'd like..." · "As an AI language model" · "As of my last update" · knowledge-cutoff disclaimers · unfilled placeholders like `[insert X]` or `[Your Name]`

*Fix:* delete.

---

## Step 3: Judge the Density

Compute the verdict before you write the findings. Count tells (not whiffs) per 100 words of prose, and count how many distinct mechanisms appear.

| Verdict | Signal |
|---------|--------|
| **reads as generated** | ≥3 tells per 100 words, **or** ≥4 distinct mechanisms clustered in one section |
| **has the habits** | 1–2 tells per 100 words across 2–3 mechanisms |
| **a few spots** | isolated tells, no mechanism repeating |
| **clean** | no tells; whiffs alone never escalate past this |

These thresholds are heuristics, not measurements. State the counts alongside the verdict so the reader can judge your judgment. If the counts and the verdict disagree with your read of the text, trust the text and say why.

---

## Step 4: Report

Report inline. Write no files.

```
VERDICT: {verdict} — {N} tells / {M} words, {K} mechanisms{, clustered in <where> if relevant}

TELLS ({count})
  L{line}  {mechanism name}
           "{the exact quoted span}"
           Mechanism: {why an LLM produces this}
           Fix: {cut | the plain form | "name the actual fact — I can't know it"}

WHIFFS ({count}) — flagged only because they cluster
  L{line}  {mechanism name}: "{span}", "{span}"

COPULATIVE RATIO: {n} avoidances vs {m} plain is/has   (omit if no pattern)
```

Rules for the report:
- **Rank worst-first** — highest-confidence, most-egregious tells at the top. Never file order.
- Quote the **exact span**, not a paraphrase. A finding you can't quote isn't a finding.
- One line per finding. No prose commentary between findings.
- If a fix needs a fact the text doesn't contain, say so explicitly and stop. Do not supply the fact.
- If you find nothing, say `VERDICT: clean` and stop. Do not manufacture findings to justify the run.

---

## What NOT to Flag

- **The em dash as a mark.** It is a legitimate tool and this project's house style uses it deliberately throughout. Flag em dashes only when sustained above roughly one per two sentences *and* co-occurring with other tells — and then flag the *density*, never the punctuation.
- **A single vocabulary hit.** "Delve," "robust," or "underscore" used once, correctly, is not evidence. Only clusters count.
- **Correct technical terms** that happen to appear on a list. "Robust" describing error handling, "leverage" in a financial context, "pivotal" about an actual pivot — all fine.
- **Deliberate house style.** This project's own rules and skills use em dashes, bold lead-ins, tables, and `---` separators heavily and on purpose. Deviation from a document's established pattern is a finding; the pattern itself is not.
- **Rhetorical structure that earns its keep.** A real triad of three distinct things. A genuine contrast a reader would otherwise get wrong. Emphasis on something that is in fact important.
- **Non-native-speaker patterns.** Several tells overlap with constructions taught in ESL instruction and academic English. Flag the span; never speculate about the author.
- **Anything in a code block, frontmatter, URL, or generated output.**

**Be precise, not exhaustive.** Eight quotable findings beat forty vague ones. The failure mode of this skill is a witch hunt — every flag you can't quote and name costs you the reader's trust in the ones you can.

---

## Safety

- **Never edit.** This skill reports. `eos` edits. If the user wants the fixes applied, say so and let them invoke an editing skill.
- **Never invent a fact** to replace vagueness. Flag the gap; the author fills it.
- **Never accuse the author.** Report tells in the text, not conclusions about who or what wrote it. Detection is unreliable — the sources are unanimous on this, and humans perform near chance. You are reporting *style*, not provenance.
- **When uncertain, skip.** A false flag on deliberate prose costs more than a missed tell.
