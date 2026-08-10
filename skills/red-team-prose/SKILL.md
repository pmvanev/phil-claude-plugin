---
name: red-team-prose
description: Skill bundle for phil:red-team-prose command — red-teams a document from both prose angles in one pass, AI-generated tells (ai-eos) plus Elements of Style clarity (eos), as a single ranked report with an approval gate before any edit
---

# Red-Team Prose

You are red-teaming a document against **both** prose standards this plugin owns, in one pass:

| Pass | Skill | Asks |
|------|-------|------|
| **Tells** | `skills/ai-eos/SKILL.md` | Does this read as AI-generated? |
| **Clarity** | `skills/eos/SKILL.md` | Is this clear, concise, and active? |

The two passes catch different things and the overlap is small. `ai-eos` finds prose that is *hollow* — grand claims carrying no fact, participle clauses padding cadence. `eos` finds prose that is *slack* — passive voice, needless words, weak endings. A document can fail either independently.

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

Pass the argument through to both passes unchanged, so they review exactly the same span.

---

## Step 1: Read Once

Read the target **once** and hold it for both passes. Do not read the file twice.

Resolve the argument as `ai-eos` Step 1 specifies (`--changes` → `git diff HEAD~1 --name-only` filtered to `**/*.{md,txt,rst}`; line range → read with surrounding context; directory → glob recursively). Review prose only — skip code blocks, frontmatter, config, link URLs, and generated output.

---

## Step 2: Run the Tells Pass

Load `skills/ai-eos/SKILL.md` and apply its catalog and tiers to the text. Honor its `What NOT to Flag` section in full — especially the em-dash rule and the single-vocabulary-hit rule. Compute its density verdict.

---

## Step 3: Run the Clarity Pass

Load `skills/eos/SKILL.md` and apply its ten editing rules to the same text — but **diagnostically**. Identify each violation and its rewrite; do not edit the file yet. Honor `eos`'s Safety section: preserve meaning, formatting, tone, and domain terminology.

### Resolving overlap between the passes

The two catalogs collide in a few places. Assign each finding to exactly one pass so nothing is reported twice:

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

When a span genuinely violates both, report it once under `ai-eos` and note the `eos` rule in the same line. Never list one span twice.

---

## Step 4: Report Both, Ranked Together

Report inline. Write no files. Lead with both verdicts, then merge the findings into one worst-first list.

```
RED-TEAM: {file}

TELLS:   {verdict} — {N} tells / {M} words, {K} mechanisms
CLARITY: {n} rewrites, {m} cuts across {j} of eos's 10 rules

FINDINGS ({total}) worst-first

  L{line}  [tells] {mechanism name}
           "{exact quoted span}"
           Mechanism: {why an LLM produces this}
           Fix: {cut | plain form}                        [auto-applicable]

  L{line}  [clarity] {eos rule name}
           "{exact quoted span}"
           -> "{the rewrite}"                             [auto-applicable]

  L{line}  [tells] phantom attribution
           "Experts argue that..."
           Fix: name the source, or cut the claim.        [NEEDS YOU — I can't know this]

COPULATIVE RATIO: {n} avoidances vs {m} plain is/has     (omit if no pattern)

{X} of {total} are auto-applicable. {Y} need a fact only you have.
```

Ranking rules:
- **Worst-first across both passes**, interleaved. Not tells-then-clarity, and not file order.
- Rank by cost to the reader: hollow claims and phantom attribution above passive voice above fancy words.
- Tag every finding `[tells]` or `[clarity]` so the source pass is always visible.
- Mark each finding `[auto-applicable]` or `[NEEDS YOU]`.
- Quote the **exact span**. A finding you can't quote isn't a finding.
- If both passes come back clean, say so plainly and stop.

---

## Step 5: Offer to Apply — Approval Gate

After reporting, ask once:

> "Apply the {X} auto-applicable fixes? The {Y} marked NEEDS YOU require a fact I don't have."

Then:

- **On approval** — apply only the `[auto-applicable]` fixes, using `eos`'s editing discipline for clarity fixes and plain deletion for tells fixes. Report what you changed, per line.
- **On refusal, or no answer** — change nothing. The report is the deliverable.
- **Never** apply a `[NEEDS YOU]` finding. Not on approval, not on a follow-up "fix everything." Those need information the document does not contain.

Applying is opt-in every time. Do not offer to apply before the full report, and do not bundle the two.

---

## Safety

- **Never invent a fact** to replace vagueness. This is the single hardest rule here, because `eos`'s habit is to rewrite and `ai-eos` findings often *look* rewritable. "Plays a crucial role in validation" cannot become "validates the request schema" unless you verified that it does. Flag it and stop.
- **Never accuse the author.** Report tells in the text, not conclusions about provenance. Detection is unreliable and humans perform near chance — you are reporting style, not authorship.
- **Respect both `What NOT to Flag` sections.** `ai-eos` protects the em dash as a mark, single vocabulary hits, correct technical terms, and this project's deliberate house style. `eos` protects meaning, formatting, tone, and domain terminology. A composite is not a licence to flag more than either pass would alone.
- **No double-reporting.** One span, one finding. Use the overlap table.
- **When uncertain, skip.** A false flag on deliberate prose costs more than a missed one.

---

## Scope

This skill owns **prose review across both standards**. It does not own:

- **Comment and docstring quality** → `clean-comments`
- **CLAUDE.md structure** → `claude-md`
- **Independent adversarial critique** → `adversarial-review` (a different tool with a different contract: fresh-context reviewer, separate judge, honesty label)
