---
name: eos
description: Edit prose for clarity using Elements of Style principles — active voice, no needless words, positive form, parallel structure, strong endings. Use when tightening documentation, commit messages, comments, READMEs, or any written text.
argument-hint: <lines:N-M | file-path | directory-path>
allowed-tools: Read, Edit, Glob, Grep
---

# Elements of Style

You are editing prose using the principles from `~/.claude/rules/writing.md` — Strunk & White's *The Elements of Style*. Every edit tightens without changing meaning.

## Parse the Argument

Determine what `$ARGUMENTS` refers to:

| Pattern | Type | Example |
|---------|------|---------|
| Digits separated by `-` or `:` | Line range | `42-67`, `42:67` |
| Has a file extension | File path | `docs/setup.md`, `README.md` |
| Ends with `/` or has no extension and is a directory | Directory path | `docs/`, `src/services` |
| Otherwise | File path (assume current context) | — |

If the argument contains both a file and a line range (e.g., `docs/setup.md:12-30`), split them.

---

## Line Range

1. Read the file with surrounding context.
2. Apply the **editing rules** below to the selected block only.

---

## File Path

1. Read the entire file.
2. Apply the editing rules to all prose content (skip code blocks, frontmatter, and tables unless the table contains prose).
3. Report a summary: how many sentences rewritten, how many cut, how many left unchanged.

---

## Directory Path

1. Glob recursively for prose files (`**/*.{md,txt,rst}`).
2. Apply the **File Path** analysis to each file.
3. Summarize changes per file.

---

## Editing Rules

Apply these in order. Each pass tightens the prose.

### 1. Active Voice

Replace passive constructions with active voice. The subject acts.

| Before | After |
|--------|-------|
| The file is read by the parser | The parser reads the file |
| Tests were written for the module | We wrote tests for the module |
| The request will be handled by the server | The server handles the request |

Keep passive voice only when the actor is unknown or irrelevant.

### 2. Positive Form

State what is, not what is not. Positive statements are stronger and shorter.

| Before | After |
|--------|-------|
| He was not punctual | He was late |
| Did not remember | Forgot |
| Does not support | Lacks |
| Not unlike | Like |
| Not important | Trivial |

### 3. Omit Needless Words

Cut every word that carries no meaning. Vigorous writing is concise.

| Cut | Replace with |
|-----|-------------|
| in order to | to |
| the fact that | (rephrase) |
| at this point in time | now |
| due to the fact that | because |
| in the event that | if |
| it is important to note that | (delete or rephrase) |
| basically, actually, really | (delete) |
| very, quite, rather, pretty | (delete) |
| there is / there are | (rephrase with real subject) |
| who is, which was | (often deletable) |
| case, character, nature | (vague fillers — cut) |

### 4. Definite, Specific, Concrete

Replace vague language with precise language. Prefer facts to generalities.

| Before | After |
|--------|-------|
| A period of time | Three days |
| Caches for a while | Caches for 5 minutes |
| Several components | Four components |
| Some kind of error | A timeout error |

### 5. Parallel Structure

Express coordinate ideas in similar form. Parallel content demands parallel structure.

**Before:**
> The system validates input, is performing calculations, and the results are stored.

**After:**
> The system validates input, performs calculations, and stores results.

### 6. Strong Endings

Place the emphatic word or phrase at the end of the sentence. The final position carries weight.

| Before | After |
|--------|-------|
| Performance is what this feature improves | This feature improves performance |
| It is clarity that we should aim for | Aim for clarity |

### 7. Nouns and Verbs

Write with nouns and verbs, not adjectives and adverbs. Strong subjects and strong verbs carry prose.

| Before | After |
|--------|-------|
| The process runs extremely slowly | The process crawls |
| A very important configuration step | A critical configuration step |
| Quickly and efficiently processes | Processes |

### 8. Do Not Overstate

Understatement persuades. Exaggeration weakens.

| Before | After |
|--------|-------|
| This is absolutely essential | This is essential |
| A completely unique approach | A unique approach |
| Literally impossible | Impossible |

### 9. Fancy Words

Prefer plain words. Anglo-Saxon over Latinate.

| Before | After |
|--------|-------|
| Utilize | Use |
| Facilitate | Help |
| Implement | Build |
| Commence | Start |
| Terminate | End |
| Aggregate | Collect |
| Subsequent | Next |

### 10. Usage

Fix common misuse:

| Wrong | Right |
|-------|-------|
| less items | fewer items |
| data is | data are |
| nauseous (meaning sick) | nauseated |
| presently (meaning now) | currently |
| which (restrictive clause) | that |
| alright | all right |

---

## Safety

- **Preserve meaning.** Every edit must say the same thing, tighter. If tightening changes the meaning, leave the original.
- **Preserve formatting.** Do not change markdown structure, headings, lists, links, or code blocks.
- **Preserve tone.** Match the document's voice. Technical docs stay technical. Casual docs stay casual.
- **Preserve terminology.** Do not replace domain-specific terms with simpler synonyms. "Deployment" stays "deployment" even if "release" is shorter.
- When uncertain whether an edit improves clarity, leave the original. False edits cost more than false keeps.
