# Slice 02 — A named profile from the developer's own documents

**Goal (one sentence):** `/phil:humanize-technical-prose --build-profile <name> <samples…>` measures the
developer's own prose in the named samples and stores the counts as a named profile outside every repo.

Story 2 · Decisions D2, D3, D4, D9, D16, D17.

## IN scope
- Read only the named samples: Markdown, plain text or LaTeX. Exclude quotations, code, figures and
  tables, and report the words measured (AC2.2).
- Measure sentence-length distribution; opener, connective, contraction, question and first-person
  rates; favoured phrases of two to four words; slips by kind and their rate, split into grammar and
  spelling, with each misspelling's mechanism, each grammar slip's cause, and how many slips sit on a
  name or technical term (D16, D17). Store no slipped word.
- Keep a phrase only if it occurs in two or more samples, or several times in one (D3). Store no
  sentence.
- Write the profile under `~/.claude/` and name its path. Adding samples to an existing profile
  rebuilds it from all of them.
- If counting needs code, add one small script with its own test, and keep the judgement calls, such
  as what counts as a slip, in the skill.
- Fixtures: a profile from two samples; a phrase that occurs once and must be dropped; a sample with
  too little prose to measure; quotations excluded from the counts; a sample whose misspellings,
  residue slips and slips on technical terms the profile records by mechanism, cause and count,
  with no slipped word in the file.

## OUT of scope
- Using the profile (slices 03 and 04).
- Reading any transcript (D2).

## Learning hypothesis
- **Disproves** "these counts are stable within a register" if the two halves of the thesis differ by
  more than three words in median sentence length, or disagree on whether contractions occur.
- **Confirms** it if both halves agree within those bounds, and the `formal` and `essay` profiles still
  differ on contractions, questions and connectives as measured on 2026-11-05.

## Acceptance criteria
AC2.1–AC2.5 in `feature-delta.md`.

## Dependencies
None; it can ship before or after slice 01.

## Effort estimate
≤1 day. Reference class: the measurement scripts run during this DISCUSS on 2026-11-05.

## Production data
The essay at `~/Git/github/pmvanev/MorrisWorm`, the thesis at `~/Git/github/pmvanev/multicore-xinu`,
and the co-written paper at `~/Git/github/pmvanev/stopping-power-force-convergence`, a PDF with its
extracted text. Their published counts are in `feature-delta.md` under *Source*.

## Dogfood moment
The same day, build `formal` from the thesis and `essay` from the essay, and compare the report with
the table in `feature-delta.md`. Then build `formal` again with the paper added, and decide whether a
co-written sample belongs in it: the paper's 22-word median sits five words above the thesis's.

## Dogfood result
The released plugin, phil 1.29.1, built four profiles on 2026-11-05:

| | `formal` | `essay` | `paper` | `all` |
|---|---|---|---|---|
| Samples measured (words) | 4 (10,338) | 6 (5,466) | 1 (2,664) | 11 (18,468) |
| Sentence length, median / 90th percentile | 17 / 28 | 17 / 32 | 22 / 36 | 17 / 30 |
| Contractions per 1,000 words | 0 | 3.3 | 0 | 1.0 |
| Questions per 100 sentences | 0 | 1.4 | 0 | 0.4 |
| *Therefore* / *Unfortunately* per 100 sentences | 2.2 / 0 | 0 / 1.4 | 0 / 0 | 1.3 / 0.4 |
| Misspellings / grammar slips | 5 / 24 | 26 / 9 | 14 / 9 | 45 / 42 |

- **The hypothesis holds.** The thesis's halves agree: Multicore_XINU has a median of 16 words and
  the other three parts 18, and neither half uses a contraction. `formal` and `essay` still differ
  on contractions, questions and connectives.
- **The build reads the essay differently from *Source*.** The script skips lists, quotations and
  the essay's 195-word abstract, all of which DISCUSS counted. So the essay's 29 misspellings become
  26, and its 19-word median becomes 17. A second reading of the paper found 9 grammar slips, not 7.
- **The paper gets its own profile, `paper`, and stays out of `formal`:** it is co-written, and its
  22-word median sits five words above the thesis's.
- **At the developer's request, `all` sets aside D4.** It mixes three registers, and the thesis,
  with 56% of the words, sets its rhythm. A voice pass with `all` would add the odd contraction to a
  draft that has none.
- **A PDF's extracted text needs cutting before it serves as a sample.** Measured raw, the paper's
  text gave 4,764 words, and the names in its running heads ranked among the commonest openers.
  `paper` measures `force-convergence-in-stopping-power-body.txt`: the abstract and section prose
  alone, every word as printed. The skill gives no warning of this.
- **Favoured phrases are mostly the subject's terms:** *stopping power*, *critical section*, *ready
  queue*. The voice pass swaps a phrase only for one that means the same, so they rarely apply.
