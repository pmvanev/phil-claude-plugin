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

| Report line | When |
|-------------|------|
| `TELLS-LEFT` | a tell remains after the re-check, with its line and why |

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
UNDO: git checkout -- {file}
```

Omit an empty section. The report says what each pass did and claims nothing about who wrote the
document. Whether to disclose AI assistance, where a venue asks, is the author's call.
