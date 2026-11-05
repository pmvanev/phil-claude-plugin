---
name: humanize-technical-prose
description: Skill bundle for phil:humanize-technical-prose command — edits a committed draft so it reads as its author's, by stripping the AI tells phil:ai-eos finds, rewording toward a voice profile built from documents the author wrote, and adding an exact number of slips, each reported by line. Use when asked to humanize, de-AI or make a draft sound like its author.
---

# Humanize Technical Prose

Edit a committed draft that Claude helped write so it reads as its author's. The run makes up to four
passes, always in this order:

| Pass | Runs when | Changes |
|------|-----------|---------|
| 1. Tells | always | rewrites each tell `phil:ai-eos` finds into the plain form its catalogue names |
| 2. Voice | `--profile <name>` names a profile that exists | rewords toward the profile's measured voice |
| 3. Tells again | the voice pass changed a sentence | keeps the plain form wherever a rewording brought a tell back |
| 4. Slips | `--slips N` with N above zero | adds exactly N slips of the kinds the profile's samples hold |

A second mode, `--build-profile`, measures documents the author names and stores the counts as a
named profile. It edits no draft.

Three rules hold in every pass:

- **The detector wins over the profile.** A rewording that brings back a tell is undone, even where
  the author's own samples hold that construction.
- **Reword; add nothing.** No pass adds a claim, a fact, a figure of speech, a hook, an analogy or a
  joke the draft did not hold.
- **Protected spans stay byte-for-byte** (Step 2).

---

## Parse the Argument

Read `$ARGUMENTS` as one of two forms:

| Form | Mode |
|------|------|
| `--build-profile <name> <sample paths…>` | Build a profile (Step B) |
| `<file> [--profile <name>] [--slips N] [--misspellings]` | Edit the draft (Steps 1–7) |

Report `REFUSED-ARGUMENT`, with the usage line from the command's `argument-hint`, and write nothing
when any of these holds:

- no file is named, or more than one;
- the file's extension is not `.md`, `.txt` or `.tex`;
- `N` is not a whole number of zero or more;
- a profile name holds anything but lowercase letters, digits and hyphens;
- a flag is not one of the four above.

`--slips 0`, or no `--slips`, adds no slips. `--misspellings` without `--slips` changes nothing; say so
in the report.

---

## Outcomes

Print exactly one terminal outcome on every run, and each report line that fires.

| Terminal | When |
|----------|------|
| `WROTE` | a pass changed the draft |
| `NOTHING-CHANGED` | the draft holds no tell, and no voice or slip pass changed it |
| `REFUSED-UNCOMMITTED` | git does not have the draft committed as it stands |
| `REFUSED-ARGUMENT` | the argument does not parse |
| `PROFILE-BUILT` | `--build-profile` wrote the profile |
| `PROFILE-NOT-BUILT` | no named sample held enough of the author's own prose to measure |

| Report line | When |
|-------------|------|
| `TELLS-LEFT` | a tell remains after the re-check, with its line and why |
| `VOICE-SKIPPED` | no profile was named, or the named one does not exist; lists the profiles that do |
| `SAMPLE-THIN` | a sample held too little own prose to measure and was left out, with its word count |
| `TRANSCRIPT-REFUSED` | a named sample is a Claude Code transcript and was not read |

---

## Step 1: Check the Draft Is Committed

The run edits the draft in place, so git must hold the version it starts from. Then `git diff` shows
the run and `git checkout` undoes it.

Run both, from the draft's directory:

```
git ls-files --error-unmatch -- {file}
git status --porcelain -- {file}
```

The first fails for a file git does not track; the second prints a line for a file with uncommitted
changes. On either, report `REFUSED-UNCOMMITTED`, name the file, and write nothing. Pass neither
`--output` nor `--ext-diff` to git: the first writes to any path and the second runs a diff driver the
repository configures.

---

## Step 2: Mark the Protected Spans

Read the whole draft, then list every span no pass may change. Each stays byte-for-byte:

- **code** — fenced blocks, indented blocks, inline code, and LaTeX `verbatim`, `lstlisting` and
  `minted`;
- **commands** — anything a reader would type, quoted or not;
- **identifiers** — file paths, function and variable names, flags, environment variables, keys;
- **links** — URLs, link targets, and LaTeX `\cite`, `\ref` and `\label` arguments;
- **numbers** — every figure with its unit, version and date;
- **quotations** — quoted words and blockquotes, which belong to whoever said them;
- **names** — people, organisations, products and places;
- **technical terms** — the domain's own vocabulary; when unsure whether a word is one, treat it as
  one;
- **headings**, **frontmatter**, **tables of data**, and LaTeX math.

A pass may change the words around a protected span, never inside it. After each pass, compare every
protected span with the original; restore any that differs, and drop the change that touched it.

---

## Step 3: Strip the Tells

Load `${CLAUDE_PLUGIN_ROOT}/skills/ai-eos/SKILL.md` and apply its Steps 1–3 to the draft: gather the
prose, hunt the tells, and judge the density. Honour its `What NOT to Flag` section in full. `ai-eos`'s
report template is suppressed; its findings feed Step 7. Its **Never edit** is lifted here, for
tell-tier findings only.

Rewrite each tell with the fix its catalogue names: cut it, or use the plain form. Then:

- **A fix that needs a fact the draft does not hold** — phantom attribution is the usual one — is left
  as it stands and listed under `TELLS-LEFT`. Never invent the source or the fact.
- **A formatting tell** is left and listed: its fix rewrites headings or markup, which Step 2 protects.
- **Whiffs** change only where `ai-eos` reports a cluster, and then each word becomes the plain word the
  sentence means.

Then re-run the hunt over every sentence this pass changed. Where a rewrite brought in a new tell,
rewrite it again in plain form; if that still trips the detector, restore the original sentence and
list it under `TELLS-LEFT`.

---

## Step 4: Reword Toward the Profile

Run this step only when `--profile {name}` names a profile that exists at
`~/.claude/humanize-technical-prose/profiles/{name}.json`. Otherwise report `VOICE-SKIPPED`, list the
profiles that exist in that directory (or say there are none, and name `--build-profile`), and skip
Steps 4 to 6: the slips draw on a profile too.

### 4a. Measure

Measure the draft as Step 3 left it, with the script that built the profile:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/humanize-technical-prose/scripts/measure_voice.py --draft {file}
```

Compare each feature with the profile's `measures`: the sentence median and 90th percentile, short
sentences, contractions, questions, openers and connectives. A feature is close enough when the
median is within two words of the profile's, or a rate is within a quarter of the profile's rate.
Leave a feature that is close enough alone.

### 4b. Reword

Move each remaining feature toward the profile's value, and stop there rather than overshoot. These
moves are allowed, and only these:

- split a long sentence where a clause ends, or join two short ones that share a subject;
- swap a connective for one the profile uses, where it means the same, such as *Also* for
  *Additionally*;
- contract or expand a verb, *do not* to *don't* or back, toward the profile's rate;
- replace a phrase with one of the profile's favoured phrases that means the same;
- reorder clauses within a sentence.

Never add a claim, a fact, a figure of speech, a hook, an analogy, a joke or a question the draft did
not hold, even where the author's samples are full of them. A question may become a statement, never
the reverse. Never change who acts, so leave first person as the draft has it. Never change a
sentence's modality: *must*, *should* and *may* keep their strength. Never touch a protected span
(Step 2).

### 4c. Check the direction

Measure the draft again. Where a feature is now farther from the profile than before, undo the
rewordings that moved it until it is not. Every feature the report names must end closer to the
profile, or unchanged.

---

## Step 5: Check the Tells Again

Re-run `ai-eos`'s hunt over every sentence the voice pass changed. Where a rewording brought in a
tell, restore the sentence as Step 3 left it. The detector wins over the profile, even where the
author's samples hold that construction: a writer's own pre-AI prose can carry a trailing participle,
and the profile cannot tell the difference.

---

## Step 7: Report

Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing the report. The standard applies to the
words the report composes, never to the document: the document follows its author's voice, and a span
the report quotes from it stays as written.

```
{terminal outcome} {file}
TELLS: {n} found, {r} rewritten; re-check: {k} left
  L{line}  {mechanism}: "{before}" → "{after}"
TELLS-LEFT
  L{line}  {mechanism}: "{span}" — {why: needs a fact the draft does not hold | formatting | rewrite still trips the detector}
VOICE {profile}: median sentence {before} → {after} (profile {target}); {feature} {before} → {after} (profile {target}); {n} rewordings; tells after: {k}
  L{line}  "{before}" → "{after}"
VOICE-SKIPPED: {no profile named | no profile named {name}}; profiles: {names | none — build one with --build-profile}
UNDO: git checkout -- {file}
```

Omit an empty section. The report says what each pass did and claims nothing about who wrote the
document. Whether to disclose AI assistance, where a venue asks, is the author's call.

---

## Step B: Build a Profile

`--build-profile <name> <sample paths…>` measures documents the author wrote and stores the counts as
a profile named for their register, such as `formal` or `essay`. A path may name a file or a
directory; a directory is one sample. The profile lives at
`~/.claude/humanize-technical-prose/profiles/{name}.json`, outside every repository, and holds counts,
never a sentence.

### B1. Gather the samples

Read only the paths the author named. Never read a transcript, the conversation, or the author's typed
prompts as a sample: prompts show how the author gives instructions, not how they write. The script
refuses a `.jsonl` file and any path under `~/.claude/projects/`; report each refused path under
`TRANSCRIPT-REFUSED`.

If the profile already exists, read its `samples` list and rebuild it from every sample, old and new.
A path named twice counts once. To drop a sample, delete the profile file and build it again.

### B2. Measure

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/humanize-technical-prose/scripts/measure_voice.py --measure {paths…}
```

The script measures only the author's own prose: it skips code, quotations, headings, tables, lists,
figures and math, and LaTeX's bookkeeping commands. It reports sentence lengths, short sentences,
questions, contractions, first person, openers, connectives and favoured phrases. A phrase is kept
only when it recurs, in two samples or three times in one, and never when it holds a name.

A sample under 500 words of own prose is left out and listed under `SAMPLE-THIN` with its count. If
every sample is thin, report `PROFILE-NOT-BUILT` and write nothing.

### B3. Tally the slips

Read each sample that was measured, whole, skipping what the script skips. Find each slip the author
made, and classify it in this vocabulary, which is the one the script accepts:

| Class | Kind |
|-------|------|
| misspelling | dropped letter |
| misspelling | added letter |
| misspelling | swapped letters |
| misspelling | wrong vowel |
| misspelling | wrong doubling |
| misspelling | other |
| revision residue | doubled word |
| revision residue | stray word |
| revision residue | words out of order |
| omission | dropped article |
| omission | dropped word |
| substitution | wrong word |
| substitution | wrong form |
| substitution | number agreement |
| substitution | wrong article |
| substitution | punctuation or case |

A **misspelling** is classed by its mechanism, what went wrong in the word. A **grammar slip** is
classed by its cause. Revision residue is a word left behind when a sentence was reworded, an omission
is a word that went missing, and a substitution is the wrong word, form or mark in the right place.
Count separately, as `on_name_or_term`, how many slips sit on a name or a technical term.

These are not slips: a spelling the author's variety of English uses, such as *travelling*; a choice
the document makes every time, such as its comma style; a term spelled the way its field spells it;
and an error inside a quotation. When unsure, it is not a slip.

Count, and never write a slipped word: not in the profile, the tally or the report. The profile needs
the kinds and their counts, and a slipped word quoted anywhere is a sentence fragment of the sample
leaving the machine.

### B4. Write the profile

Pass the tally to the script on standard input, with the same paths:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/humanize-technical-prose/scripts/measure_voice.py --build {name} --slips - {paths…} <<'TALLY'
{"misspelling": {"dropped letter": 0, …}, "grammar": {"revision residue": {…}, "omission": {…}, "substitution": {…}}, "on_name_or_term": 0}
TALLY
```

The script refuses a tally holding anything but whole numbers under the vocabulary above, and a
profile name holding anything but lowercase letters, digits and hyphens. It prints the profile's path.

### B5. Report

Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing the report, as Step 7 does.

```
PROFILE-BUILT {name}: {k} samples, {words} words — sentences {median}/{p90}, contractions {c} per 1,000 words, questions {q} per 100 sentences, slips {total} (grammar {g}, spelling {s}; {t} on names or terms)
  {path}
SAMPLE-THIN
  {sample} — {words} words
TRANSCRIPT-REFUSED
  {sample}
```

Name the samples by path, and quote nothing from them.
