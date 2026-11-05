---
name: humanize-technical-prose
description: Skill bundle for phil:humanize-technical-prose command — edits a committed draft in place so it reads as its author's, by stripping the AI tells phil:ai-eos finds, rewording toward a voice profile built from documents the author wrote, and adding an exact number of slips, each reported by line; or builds that named profile. Use only when the author asks for a draft to be edited in place to sound like them; for a review that edits nothing, use phil:red-team-prose.
---

# Humanize Technical Prose

Edit a committed draft that Claude helped write so it reads as its author's. The run makes up to four
passes, always in this order:

| Pass | Runs when | Changes |
|------|-----------|---------|
| 1. Tells | always | rewrites each tell `phil:ai-eos` finds into the plain form its catalogue names |
| 2. Voice | `--profile <name>` names a profile that exists | rewords toward the profile's measured voice |
| 3. Tells again | the voice pass changed a sentence | keeps the plain form wherever a rewording brought a tell back |
| 4. Slips | `--slips N` with N above zero, and the profile exists | adds exactly N slips of the kinds the profile's samples hold |

A second mode, `--build-profile`, measures documents the author names and stores the counts as a
named profile. It edits no draft.

Three rules hold in every pass:

- **The detector wins over the profile.** A rewording that brings back a tell is undone, even where
  the author's own samples hold that construction.
- **Reword; add nothing.** No pass adds a claim, a fact, a figure of speech, a hook, an analogy or a
  joke the draft did not hold.
- **Protected spans stay byte-for-byte** (Step 2).

The script `${CLAUDE_PLUGIN_ROOT}/skills/humanize-technical-prose/scripts/measure_voice.py` does every
count, and owns where profiles live. Ask it with `--list`; never build a profile path by hand.

---

## Parse the Argument

Read `$ARGUMENTS` as one of two forms:

| Form | Mode |
|------|------|
| `--build-profile <name> <sample paths…>` | Build a profile (Step B) |
| `<file> [--profile <name>] [--slips N] [--misspellings]` | Edit the draft (Steps 1–7) |

Every condition below must hold. When any fails, report `REFUSED-ARGUMENT`, name each one that fails,
print the usage line
`<file> [--profile <name>] [--slips N] [--misspellings] | --build-profile <name> <sample paths…>`, and
write nothing:

- edit mode names exactly one file, ending `.md`, `.markdown`, `.txt` or `.tex`;
- `N` is a whole number of zero or more, written in digits;
- every profile name holds only lowercase letters, digits and hyphens;
- every flag is `--profile`, `--slips`, `--misspellings` or `--build-profile`;
- build mode names a profile and at least one sample path, and takes no other flag.

---

## Outcomes

Print exactly one terminal outcome on every run, and each report line that fires.

| Terminal | When |
|----------|------|
| `WROTE` | a pass changed the draft |
| `NOTHING-CHANGED` | no pass changed the draft |
| `REFUSED-UNCOMMITTED` | git does not have the draft committed as it stands |
| `REFUSED-ARGUMENT` | the argument does not parse |
| `PROFILE-BUILT` | `--build-profile` wrote the profile |
| `PROFILE-NOT-BUILT` | no profile was written: every sample was thin, or the script refused a named path |

| Report line | When |
|-------------|------|
| `TELLS-LEFT` | a tell remains after the re-check, with its line and why |
| `VOICE-SKIPPED` | no profile was named, or the named one does not exist; lists the profiles that do |
| `SLIPS-SKIPPED` | slips were asked for with no profile to draw from, or `--misspellings` came without `--slips` |
| `SLIPS-NONE-OF-KIND` | the profile holds none of the kinds the run may add; names the kinds it holds |
| `SLIPS-SHORT` | the draft had fewer open positions than the count; says how many were added |
| `SLIPS-UNMIRRORED` | slips were added, and the samples put some of theirs on names or technical terms, where the run places none |
| `SLIPS-WARNING` | on every run that adds a slip: a later cleanup pass will fix them |
| `SAMPLE-THIN` | a sample held too little own prose to measure and was left out, with its word count |
| `SAMPLE-REFUSED` | the script refused a named sample — a transcript, a missing path, a wrong extension — with its reason |

---

## Step 1: Check the Draft Is Committed

The run edits the draft in place, so git must hold the version it starts from. Then `git diff` shows
the run and `git checkout` undoes it.

Run both from the current directory, with the path as given:

```
git ls-files --error-unmatch -- {file}
git status --porcelain -- {file}
```

The first fails for a file git does not track, or one outside the current repository; the second
prints a line for a file with uncommitted changes. On either, report `REFUSED-UNCOMMITTED`, name the
file and the reason, and write nothing. Pass neither `--output` nor `--ext-diff` to git: the first
writes to any path and the second runs a diff driver the repository configures.

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
report template is suppressed; its findings and its density verdict feed Step 7. Its **Never edit** is
lifted here for tell-tier findings and clustered whiffs.

Rewrite each tell with the fix its catalogue names: cut it, or use the plain form. Where `ai-eos`
reports a copulative-avoidance ratio, rewrite each avoidance in that passage to *is* or *has*. Leave a
finding as it stands, and list it under `TELLS-LEFT` with its reason, when:

- **its fix needs a fact the draft does not hold** — phantom attribution is the usual one. Never invent
  the source or the fact;
- **its fix would remove or rename a protected span** — a formulaic closer holding a number, or
  elegant variation across technical terms. Cut only the words around the span when that clears the
  tell;
- **it is a formatting tell** — its fix rewrites markup the author chose.

A clustered whiff takes the plain word the sentence means, one word at a time.

Then re-run the hunt over every sentence this pass changed. Where a rewrite brought in a new tell,
rewrite it again in plain form; if that still trips the detector, restore the original sentence and
list it under `TELLS-LEFT`.

---

## Step 4: Reword Toward the Profile

Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/humanize-technical-prose/scripts/measure_voice.py --list`.
It prints the profile directory and each profile's name. Run this step only when `--profile {name}`
names one of them, and read the profile at `{dir}/{name}.json`. Otherwise report `VOICE-SKIPPED`, list
the profiles that exist (or say there are none, and name `--build-profile`), and leave the draft as
Step 3 left it.

### 4a. Measure

Measure the draft as Step 3 left it, with the script that built the profile:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/humanize-technical-prose/scripts/measure_voice.py --draft {file}
```

Compare each feature with the profile's `measures`, and leave alone each one inside its band:

| Feature | Band |
|---------|------|
| sentence median | within 2 words of the profile's |
| sentence 90th percentile | within 3 words of the profile's |
| short sentences, contractions, questions | within a quarter of the profile's rate; exactly 0 where the profile's is 0 |
| each opener and each connective, entry by entry | within a quarter of the profile's rate; exactly 0 where the profile has none |

### 4b. Reword

Move each feature outside its band toward the profile's value. Stop at the band's edge, and where a
short draft cannot land inside the band, stop at the nearest value short of it. These moves are
allowed, and only these:

- split a long sentence where a clause ends, or join two short ones that share a subject;
- swap a connective for one the profile uses, where it means the same, such as *Also* for
  *Additionally*;
- contract or expand a verb, *do not* to *don't* or back, toward the profile's rate;
- replace a phrase with one of the profile's favoured phrases that means the same;
- reorder clauses within a sentence.

Never add a claim, a fact, a figure of speech, a hook, an analogy, a joke or a question the draft did
not hold, even where the author's samples are full of them. A question may become a statement, never
the reverse. Keep who acts: leave first person as the draft has it. Keep each sentence's modality:
*must*, *should* and *may* keep their strength. Keep every protected span (Step 2).

### 4c. Check the direction

Measure the draft again. Where a feature is now farther from the profile than before, undo the
rewordings that moved it until it is not.

---

## Step 5: Check the Tells Again

Re-run `ai-eos`'s hunt over every sentence the voice pass changed. Where a rewording brought in a
tell, restore the sentence as Step 3 left it. The detector wins over the profile, even where the
author's samples hold that construction: a writer's own pre-AI prose can carry a trailing participle,
and the profile cannot tell the difference.

Then measure the draft once more. These numbers are the `{after}` values Step 7 reports, and every
feature the report names must end closer to the profile than it began, or unchanged.

---

## Step 6: Add the Slips

`--slips 0`, or no `--slips`, adds none. With `--slips N` above zero and no profile from Step 4, add
none and report `SLIPS-SKIPPED`; do the same for `--misspellings` without `--slips`. The slips come
last, so no later pass of this run fixes them.

### 6a. Draw the kinds

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/humanize-technical-prose/scripts/measure_voice.py --allocate {name} {N} [--misspellings]
```

The script divides N among the kinds the profile's samples hold, in their proportions: grammar kinds
always, misspellings only with `--misspellings`. It never draws a misspelling whose mechanism the
samples left unrecorded. Add exactly the slips it returns, no more and no other kinds. When it returns
`none_of_kind`, add none and report `SLIPS-NONE-OF-KIND` with the kinds from `held`.

### 6b. Place each slip

Place each slip in ordinary prose, outside every protected span, and never on a name or a technical
term. One sentence takes one slip at most, and the slips spread through the document rather than
cluster. A revision-residue slip goes only in a sentence the voice pass reworded and Step 5 kept,
which is where a writer leaves one; when there is none, any open sentence will do.

A slip must never change what a sentence claims. Leave alone a negation, a number, a unit, a
quantifier, a comparative and a modal, and any word whose loss or change would reverse or weaken the
sentence. A misspelling goes on an ordinary word of five letters or more, and must not spell another
real word.

Make each slip the way its kind's row in the Slip Vocabulary describes, as the author's own samples
show it.

When the draft has fewer open positions than the count, add as many as fit and report `SLIPS-SHORT`
with the number added. When the run added a slip and the script's `unmirrored` count is above zero,
report `SLIPS-UNMIRRORED`: the samples put that many of their slips on names or technical terms, and
the run placed none there. On every run that adds a slip, report `SLIPS-WARNING`.

---

## Step 7: Report

Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing the report. The standard applies to the
words the report composes, never to the document: the document follows its author's voice, and a span
the report quotes from it stays as written.

```
{terminal outcome} {file}
TELLS: {ai-eos verdict} — {n} found, {r} rewritten; re-check: {k} left
  L{line}  {mechanism}: "{before}" → "{after}"
TELLS-LEFT
  L{line}  {mechanism}: "{span}" — {needs a fact the draft does not hold | would remove or rename a protected span | formatting | rewrite still trips the detector}
VOICE {profile}: median sentence {before} → {after} (profile {target}); {feature} {before} → {after} (profile {target}); {n} rewordings; tells after: {k}
  L{line}  "{before}" → "{after}"
VOICE-SKIPPED: {no profile named | no profile named {name}}; profiles: {names | none — build one with --build-profile}
SLIPS {n}: L{line} {kind} ({class}) · L{line} {kind} ({class})
SLIPS-SKIPPED: {N slips asked for, with no profile to draw from | --misspellings without --slips adds nothing}
SLIPS-NONE-OF-KIND: profile {name} holds {held | no kind the run can draw}; none may be added{ without --misspellings}
SLIPS-SHORT: {added} of {N} added; the draft has no more open positions
SLIPS-UNMIRRORED: the samples put {unmirrored} of {profile_total} slips on names or technical terms; none placed there
SLIPS-WARNING: a later phil:eos, phil:red-team-prose or spell-check pass will fix these slips; run this command last
UNDO: git checkout -- {file}
```

Omit an empty section. The report says what each pass did and claims nothing about who wrote the
document. Whether to disclose AI assistance, where a venue asks, is the author's call.

---

## Step B: Build a Profile

`--build-profile <name> <sample paths…>` measures documents the author wrote and stores the counts as
a profile named for their register, such as `formal` or `essay`. A path may name a file or a
directory; a directory is one sample. The profile lives in the directory `--list` prints, outside
every repository, and holds counts, never a sentence.

Read `${CLAUDE_PLUGIN_ROOT}/skills/humanize-technical-prose/references/build-profile.md` and follow it.
It classifies slips in the Slip Vocabulary below.

---

## Slip Vocabulary

Step 6 makes slips, and the profile build tallies them, in this vocabulary, which is the one the
script accepts:

| Class | Kind | Made, in Step 6, by |
|-------|------|---------------------|
| misspelling | dropped letter | dropping one letter |
| misspelling | added letter | adding one letter |
| misspelling | swapped letters | swapping two adjacent letters |
| misspelling | wrong vowel | changing one vowel |
| misspelling | wrong doubling | doubling a single letter, or undoubling a double |
| misspelling | other | never drawn: its mechanism went unrecorded |
| revision residue | doubled word | repeating a short function word, *the the* |
| revision residue | stray word | leaving a word an earlier wording needed, *is as it did* |
| revision residue | words out of order | swapping two short neighbouring words, *all the of* |
| omission | dropped article | dropping *a*, *an* or *the* |
| omission | dropped word | dropping a short function word, never a content word |
| substitution | wrong word | a near-homophone a careful writer types, *affects* for *effects* |
| substitution | wrong form | the wrong verb form, *it happen* |
| substitution | number agreement | a noun or verb in the wrong number, *one processes is* |
| substitution | wrong article | *a* for *an*, or the reverse |
| substitution | punctuation or case | a mark or capital the document's own style would not have |

A **misspelling** is classed by its mechanism, what went wrong in the word. A **grammar slip** is
classed by its cause. Revision residue is a word left behind when a sentence was reworded, an omission
is a word that went missing, and a substitution is the wrong word, form or mark in the right place.
Count separately, as `on_name_or_term`, how many slips sit on a name or a technical term.
