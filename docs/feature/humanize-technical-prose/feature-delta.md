# Feature Delta — humanize-technical-prose (`/phil:humanize-technical-prose`)

> Single narrative file for the feature. DISCUSS findings live here as
> `## Wave: DISCUSS / [REF] <Section>` headings. Machine artifacts: `slices/slice-NN-*.md`.
> SSOT updates: `docs/product/jobs.yaml` (new job), `docs/product/personas/blair-named-author.yaml`
> (new persona), `docs/product/journeys/humanize-technical-prose.yaml` (new journey).
> Board: issue 88, In Progress.
> Build path: DISCUSS only — the deliverable is prose (CLAUDE.md, edd-loop DDD8).

---

## Wave: DISCUSS / [REF] Source

Issue 88 asks for a command that makes a document Claude helped draft read as its author's. It runs
three passes, in order: strip the tells, match the developer's voice, then add a set number of
plausible slips.

Measured on 2026-11-05:

- **Typed prompts are no voice sample.** Every transcript on the developer's machine holds 2,950
  typed prompts across 30 projects, 56,230 words in all. They have a 13-word median, 86% start
  lowercase and 41% end with a stop. They show how the developer gives instructions, not how they
  write. `scripts/session-exchanges.py`'s `_prompt()` separated typed prompts from tool results and
  command expansions unchanged; a paste carrying no marker still passes as typed.
- **Three documents written without AI help carry the voice.** *Following the Morris Worm* is a 2017
  course essay of 4,920 words of the developer's own prose. *Multicore Xinu* is a master's thesis of
  8,522 words. *Force Convergence in Stopping Power from Molecular Dynamics* is a 2014 summer-research
  paper of 2,730 words, written with Andrew Baczewski and Rudolph Magyar; nothing in it marks whose
  sentences are whose. Each count excludes quotations, code, figures, tables, captions and
  references. The paper's text came out of a PDF, the others' out of LaTeX source.

| | Essay | Thesis | Paper (co-written) |
|---|---|---|---|
| Sentence length, median / 90th percentile | 19 / 34 | 17 / 31 | 22 / 37 |
| Sentences of 6 words or fewer | 4 | 8 | 1 |
| Contractions | 16 | 0 | 0 |
| Questions | 4 | 0 | 0 |
| *Thus* / *Therefore* / *However* | 1 / 0 / 2 | 11 / 12 / 13 | 0 / 0 / 1 |
| *Perhaps* / *Unfortunately* | 3 / 4 | 0 / 0 | 0 / 0 |
| *Fortunately* / *Ultimately* / *Finally* | 1 / 2 / 5 | 4 / 2 / 2 | 0 / 0 / 0 |
| Slips | 33 | 29 | 21 |
| Misspellings / grammar slips | 29 / 4 | 5 / 24 | 14 / 7 |

Each slip was also classified by how it happened, from one reading of each document; the counts are
minimums. A misspelling's *mechanism* is what went wrong in the word. A grammar slip's *cause* is
*revision residue* (a doubled, stray or misordered word left by rewording a sentence: *will will*,
*Relative the to*, *is as it did*), *omission* (a dropped article or word: *It clear that*) or
*substitution* (a wrong word, form, agreement, article, punctuation or case: *probe the affects*).

| | Essay | Thesis | Paper |
|---|---|---|---|
| Misspellings: dropped / added / swapped letter | 5 / 6 / 2 | 2 / 3 / 0 | 6 / 4 / 2 |
| Misspellings: wrong vowel / wrong doubling / other | 9 / 2 / 5 | 0 / 0 / 0 | 1 / 1 / 0 |
| Misspellings on a name or technical term | 4 of 29 | 1 of 5 | 6 of 14 |
| Grammar: residue / omission / substitution | 2 / 1 / 1 | 5 / 5 / 14 | 3 / 2 / 2 |

The essay's *other* is one dropped silent *e* and four misspelled names whose mechanism went
unrecorded.

The slips quoted in this file, and the three examples in the skill's slip vocabulary, are the
developer's own, from all three samples, the private thesis and paper included. The developer
approved them being public in this repository on 2026-11-05.

Five facts shape the design:

- **Rhythm holds across the developer's own documents; register does not.** One profile cannot be
  both the thesis and the essay. The co-written paper runs five words longer at the median than the
  thesis, and nothing in the measurements separates co-authorship from the paper's field.
- **The editor probably decides which slips survive.** The essay was moved out of Overleaf into an
  editor with no spell-check, and its slips are misspellings: *devoloped*, *secruity*, *suddently*.
  The thesis's slips are the kind a spell-checker misses: a dropped article (*a mutex is binary
  semaphore*), number agreement (*only one processes is*), a doubled word (*will will*, *a an*), a
  wrong word (*complimentary*, *my spin*). The paper holds both kinds (*occuring*, *siginificant*;
  *the the*, *It clear that*), and its editor is unknown, so it neither supports nor refutes this.
- **A slip's mechanism and cause make it plausible; its kind alone does not.** Misspellings mostly
  drop or add a letter, or take the wrong vowel. Revision residue, which lands where a sentence was
  reworded, makes up 2 of the essay's 4 grammar slips, 3 of the paper's 7 and 5 of the thesis's 24.
  And slips land where a protected span forbids them: 6 of the paper's 14 misspellings sit on a name
  or technical term (*Beryillium*, *dyanmics*, *Monhorst*).
- **The card's sample slips mostly do not fit this writer.** Only the paper holds a homophone
  (*probe the affects*), and the essay uses the Oxford comma every time, so a missing one would read
  as a stranger's slip.
- **The detector flags some of the writer's own pre-AI prose.** The essay's abstract holds
  *"elicited both immediate and long term responses spanning multiple disciplines"*, a trailing
  participle `phil:ai-eos` lists as a tell. A voice pass that imitates the writer can bring back what
  the tells pass removed.

## Wave: DISCUSS / [REF] Persona & Job

- **Persona:** `blair-named-author` (new). The position is authorship: the document leaves under one
  person's name. No existing persona holds it. Robin curates a board, Kai crosses a session boundary,
  and Ari answers a question.
- **JTBD one-liner:** *When a document Claude helped draft is about to go out under my name, I want it
  to read as I write — without the model's tells, in my word choice and rhythm for that register, with
  the slips a careful writer still makes — so the document is mine.*
- **Job ID:** `ship-a-document-in-my-own-voice` (new).

## Wave: DISCUSS / [REF] Feature type & framing

- **Feature type:** developer tool, user-facing. The developer runs the command and reads its report.
- **Greenfield command** in a brownfield plugin: a new `commands/humanize-technical-prose.md` and
  `skills/humanize-technical-prose/`. It composes `phil:ai-eos` (the tells catalogue) and changes no
  existing skill.
- **Research depth:** lightweight. Happy path plus the error paths in the journey.

## Wave: DISCUSS / [REF] Locked decisions

The developer answered D1–D9 on 2026-11-05. D10–D15 follow from those answers, the card and the
measurements above. D16 and D17 are the developer's yes, the same day, to a proposal made after the
slips were classified.

- **[D1] Pass 1 runs `phil:ai-eos` directly.** *(Developer's answer.)* The command loads `phil:ai-eos`'s
  catalogue, takes its findings and rewrites each in the plain form the catalogue names.
  `phil:red-team-prose` does not change. Two surfaces now rewrite tells, so their fixes can drift;
  both take the fix from `phil:ai-eos`'s catalogue.
- **[D2] The profile reads only samples the developer names.** *(Developer's answer.)* It never reads
  a transcript. With no profile named, the run skips the voice pass and the report says so.
- **[D3] The profile stores counts, never sentences.** *(Developer's answer.)* It stores sentence-length
  distribution, opener and connective frequencies, contraction, question and first-person rates,
  favoured phrases of two to four words, and slips by kind, mechanism and cause with their rate, but
  never a slipped word. A phrase is kept only if it occurs in two or more samples, or several times
  in one, so a one-off secret or client detail never lands in the file. The file lives outside every repo, under `~/.claude/`, and is
  machine-local, as `.session-handoff.md` is.
- **[D4] Profiles are named, one per register.** *(Developer's answer.)* The developer groups samples
  into a named profile, such as `formal` or `essay`, and names one per run.
- **[D5] The voice pass rewords; it adds nothing.** *(Developer's answer.)* It changes word choice,
  sentence rhythm, openers and contractions toward the profile. It adds no claim, figure of speech,
  hook into the next section, analogy or joke the draft did not hold.
- **[D6] No slips unless counted.** *(Developer's answer.)* `--slips N` asks for exactly N. Without it
  the run adds none, and `--slips 0` adds none either.
- **[D7] Slip kinds come from the samples.** *(Developer's answer.)* The run draws from the kinds the
  chosen profile's samples hold, in their proportions. It has no built-in catalogue.
- **[D8] Grammar kinds by default.** *(Developer's answer.)* The run adds the kinds a spell-checker
  misses — a dropped or wrong article, number agreement, a doubled word, a wrong word, a dropped word —
  and adds misspellings only with `--misspellings`. A document written today in an editor that
  spell-checks probably carries the thesis's kinds, not the essay's.
- **[D9] Fixtures may quote short passages from the samples, each approved by the developer.**
  *(Developer's answer.)* Each passage is a few sentences, credited, and approved one by one before
  it is committed. These sentences ship to every consumer of the plugin.
- **[D10] Order: tells, voice, tells again, slips.** The voice pass may not bring back a tell. After
  rewording, the run re-runs `phil:ai-eos` over the changed sentences and keeps the plain form wherever
  a rewording tripped it. The detector wins over the profile.
- **[D11] Protected spans stay byte-for-byte.** Neither the voice pass nor the slips touch code,
  commands, identifiers, links, numbers, quotations, names or technical terms. A heading, frontmatter
  or a table of data is protected too.
- **[D12] The command edits the file in place, and only when git has it committed.** It refuses a
  file with uncommitted changes, so `git diff` shows the run and `git checkout` undoes it.
- **[D13] The profile governs the document; `rules/writing.md` governs the report.** The voice pass
  writes to the developer's profile, not to Strunk and White. The report follows `rules/writing.md`, and
  the skill names it. The report warns that a later `phil:eos` or `phil:red-team-prose` run will fix the
  slips, so this command runs last.
- **[D14] The report says what each pass did, not who wrote the document.** It claims nothing about
  authorship. Whether to disclose AI assistance, where a venue requires it, stays the writer's call.
- **[D15] `commands/humanize-technical-prose.md` declares `mutates: true`.** It edits the document and
  writes the profile (`scripts/check-readonly-commands.py`).
- **[D16] Slips follow the samples' mechanisms and causes, not only their kinds.** *(Developer's yes.)*
  The profile records each misspelling's mechanism (a dropped, added or swapped letter, a wrong vowel,
  a wrong doubling) and each grammar slip's cause (revision residue, omission, substitution). The run
  draws from both in their proportions. A residue slip lands only in a sentence the voice pass
  reworded, where a writer leaves one; with no voice pass, it lands in any sentence the run may touch.
- **[D17] A slip the protected spans forbid is counted, never silently dropped.** *(Developer's yes.)*
  The profile records how many of its slips sit on a name or technical term. The run places none
  there (D11), and the report says how many of the profile's slips it could not mirror.

## Wave: DISCUSS / [REF] User stories

### Story 1 — Strip the tells *(slice 01)*
`job_id: ship-a-document-in-my-own-voice`

As **Blair**, I want every tell `phil:ai-eos` finds rewritten in its plain form, with nothing new
introduced, so the draft stops reading as a model's.

### Elevator Pitch
Before: `/phil:ai-eos draft.md` lists nine tells, and I rewrite each by hand.
After: run `/phil:humanize-technical-prose draft.md` → sees `TELLS: 9 found, 9 rewritten; re-run: 0` and the file's diff.
Decision enabled: I ship the draft, or go on to the voice pass.

**Acceptance criteria**
- AC1.1 — Given a committed draft with tells, then each tell `phil:ai-eos` reports is gone after the
  run, and a re-run of `phil:ai-eos` reports none of them. A tell whose fix needs a fact the draft
  does not hold, such as phantom attribution, stays as written and the report lists it.
- AC1.2 — Given a draft with uncommitted changes, then the run refuses, names the file and writes
  nothing.
- AC1.3 — Given any run, then no protected span (D11) differs from the draft.
- AC1.4 — Given `skills/humanize-technical-prose/SKILL.md` without its `rules/writing.md` citation,
  then a test fails.

### Story 2 — Build a named profile from my own documents *(slice 02)*
`job_id: ship-a-document-in-my-own-voice`

As **Blair**, I want to name documents I wrote as one register's samples and see what they measure,
so the voice pass works from how I write, not from how I give instructions.

### Elevator Pitch
Before: nothing in the plugin knows how I write, and my prompts are no sample of it.
After: run `/phil:humanize-technical-prose --build-profile formal ~/Git/github/pmvanev/multicore-xinu` → sees `PROFILE formal: 1 sample, 8,522 words — sentences 17/31, contractions 0, questions 0, slips 29 (grammar 24, spelling 5)`.
Decision enabled: I keep the profile, add samples to it, or split them into another register.

**Acceptance criteria**
- AC2.1 — Given named samples, then the run builds the profile from those files alone and reads no
  transcript.
- AC2.2 — Given a sample, then its counts exclude quotations, code, figures and tables, and the report
  gives the words measured.
- AC2.3 — Given a phrase that occurs once in one sample, then the profile does not store it; given any
  profile, then it stores no sentence.
- AC2.4 — Given a profile, then it lives outside every repo, and the report names its path.
- AC2.5 — Given a sample with slips, then the profile records each misspelling's mechanism, each
  grammar slip's cause, and how many slips sit on a name or technical term, and stores no slipped
  word (D3, D16, D17).

### Story 3 — Sound like me in the register at hand *(slice 03)*
`job_id: ship-a-document-in-my-own-voice`

As **Blair**, I want the draft reworded toward the profile I name, adding nothing and bringing back no
tell, so the document reads as mine.

### Elevator Pitch
Before: the tells are gone, and the draft still reads in Claude's rhythm and word choice.
After: run `/phil:humanize-technical-prose draft.md --profile formal` → sees `VOICE formal: median sentence 24 → 18 (profile 17); contractions 3 → 0; 31 rewordings; tells after: 0`.
Decision enabled: I accept the rewording, or revert it with git and try another profile.

**Acceptance criteria**
- AC3.1 — Given a draft and a profile, then word choice moves toward the profile: the measured
  features the report names are closer to the profile's after the run than before.
- AC3.2 — Given any run, then technical terms, code and quotations are untouched (D11).
- AC3.3 — Given any run, then the document holds no claim, figure of speech, hook or analogy the draft
  did not (D5).
- AC3.4 — Given a rewording that brings back a tell, then the run keeps the plain form, and the
  re-run of `phil:ai-eos` reports no tell (D10).
- AC3.5 — Given no profile, or one that does not exist, then the voice pass is skipped, and the report
  says so and lists the profiles that exist.

### Story 4 — Add exactly the slips I asked for *(slice 04)*
`job_id: ship-a-document-in-my-own-voice`

As **Blair**, I want an exact number of slips of the kinds my own documents carry, each reported by
location, so the document reads as typed by a careful person, and I know every error and where it is.

### Elevator Pitch
Before: a cleaned draft has no error a careful person makes, and adding some by hand risks one in a command.
After: run `/phil:humanize-technical-prose draft.md --profile formal --slips 2` → sees `SLIPS 2: L14 dropped article · L37 doubled word — run no cleanup pass after this one`.
Decision enabled: I ship it, or fix a slip I would rather not keep.

**Acceptance criteria**
- AC4.1 — Given `--slips N`, then the run adds exactly N slips and reports each one's line and kind.
- AC4.2 — Given any slip, then it lies outside every protected span (D11).
- AC4.3 — Given `--slips 0`, or no `--slips`, then the document holds no new slip.
- AC4.4 — Given no `--misspellings`, then every slip is a grammar kind the profile holds (D8); given a
  profile with none of the asked-for kinds, then the run adds no slips and names the kinds it holds.
- AC4.5 — Given a run that adds slips, then the report warns that a later cleanup pass will fix them.
- AC4.6 — Given `--misspellings`, then each misspelling's mechanism is one the profile holds; given a
  residue slip and a voice pass that ran, then the slip lies in a sentence the voice pass reworded
  (D16).
- AC4.7 — Given a profile whose samples put slips on names or technical terms, then the run places
  none there, and the report says how many of the profile's slips it could not mirror (D17).

## Wave: DISCUSS / [REF] Outcome KPIs

| KPI | Target | Measurement |
|---|---|---|
| No tell survives, none comes back | 0 tell-tier findings when `phil:ai-eos` re-runs over the output | fixture; dogfood re-run |
| Protected spans untouched | 0 bytes changed inside code, commands, identifiers, links, numbers, quotations or names | fixture diff |
| Nothing added | 0 claims, figures of speech, hooks or analogies the draft lacked | fixture; developer's read |
| Exact slips | slips added = N for every N, 0 included | fixture per count |
| Voice moves toward the profile | every feature the report names is closer to the profile after the run | fixture on an approved passage |
| Recognised as mine | the developer, shown the tells-only and the voiced output of one real draft unlabelled, picks the voiced one as closer to theirs | dogfood, slice 03 |
| Applied, not cited | removing the `rules/writing.md` citation fails a test | pytest, watched red first |

## Wave: DISCUSS / [REF] Out of scope

- Changing `phil:red-team-prose` or `phil:ai-eos` (D1).
- Reading transcripts for the profile (D2).
- Adding metaphors, hooks, analogies or jokes, even in the profile's style (D5).
- A built-in slip catalogue (D7).
- Judging whether a document needs an AI-use disclosure (D14).
- Formats other than Markdown, plain text and LaTeX prose, for the draft. A sample may be LaTeX or
  Markdown.

## Wave: DISCUSS / [REF] Driving ports & prerequisites

- **Driving port:** `/phil:humanize-technical-prose <file> [--profile <name>] [--slips N] [--misspellings]`,
  and `/phil:humanize-technical-prose --build-profile <name> <sample paths…>`.
- **Driven ports:** `phil:ai-eos`'s catalogue, the file system (the draft, the samples, the profile),
  `git` (the draft is committed; the diff).
- **Prerequisites:** `phil:ai-eos` as it stands, and at least one sample for slices 02–04.

## Wave: DISCUSS / [REF] Walking-skeleton strategy

Strategy A, the thinnest end to end. Slice 01 is the skeleton: the command runs on a real draft,
rewrites its tells, re-checks and reports. It needs no profile. Slices 02–04 add the profile, the
voice pass and the slips behind it.

## Wave: DISCUSS / [REF] Scope Assessment

**PASS (right-sized).** Four stories across four slices; one new command and skill; no change to an
existing skill; the profile measurement may need one small script.

## Wave: DISCUSS / [REF] Definition of Done

1. `commands/humanize-technical-prose.md` and `skills/humanize-technical-prose/SKILL.md` exist,
   authored after reading `plugin-dev:command-development` and `plugin-dev:skill-development`.
2. Every story traces to `ship-a-document-in-my-own-voice`.
3. Every story has an Elevator Pitch with a real entry point and observable output.
4. Fixtures pin the card's six behaviours, as amended in *Changed Assumptions*: a reported tell is
   gone; the voice pass moves word choice toward the profile and leaves technical terms, code and
   quotations untouched; the profile draws only on named samples; exactly the configured number of
   slips, each located; no slip in a protected span; a count of zero adds none.
5. Every passage quoted from a sample was approved by the developer before its commit (D9).
6. Every new citation and gate has a test, watched red first.
7. `python3 -m pytest -q` and `scripts/check-invariants.py` pass.
8. `/phil:harden-instructions` over the command, the skill and its references; `phil:eos` over this
   file, its slice briefs and the SSOT entries; `plugin-dev:skill-reviewer` and
   `plugin-dev:plugin-validator` over the command and skill — then the tests again.
9. Dogfood: the command takes a real draft of the developer's through all four passes, naming the
   plugin version it ran against.

## Wave: DISCUSS / [REF] Definition of Ready — validation

| # | DoR item | Status | Evidence |
|---|---|---|---|
| 1 | Job traceable | ✅ | `ship-a-document-in-my-own-voice` in `jobs.yaml`; all 4 stories carry it |
| 2 | Persona defined | ✅ | `personas/blair-named-author.yaml` |
| 3 | Journey mapped | ✅ | `journeys/humanize-technical-prose.yaml`, with error paths |
| 4 | Elevator pitches | ✅ | all 4 stories, `/phil:humanize-technical-prose` entry point, observable output |
| 5 | ACs testable | ✅ | Given-then form, each checkable by a fixture or pytest |
| 6 | Slices ≤1 day with a learning hypothesis | ✅ | `slices/slice-01` … `slice-04` |
| 7 | Walking skeleton | ✅ | slice 01, no profile needed |
| 8 | Outcome KPIs with targets | ✅ | table above |
| 9 | Scope right-sized | ✅ | Scope Assessment above |

Requirements completeness: each of issue 88's three passes, six fixture behaviours and six open
questions maps to a decision and an AC. The open questions map to D1, D2, D3, D5, D6–D8 and D13.

## Wave: DISCUSS / [REF] Changed Assumptions

DISCOVER and DIVERGE never ran; the changed assumptions are issue 88's own, as written.

- Pass 2: "Reads the prompts the developer typed across several Claude Code sessions, builds a profile
  of their vocabulary, sentence length and phrasing".

  **New:** the profile reads documents the developer names, grouped into named profiles by register
  (D2, D4). **Why:** the developer chose samples. The prompts measure as instructions (13-word
  median, 86% lowercase), while the developer's pre-AI documents measure as prose and disagree by
  register.

- Fixture behaviour 3: "the profile draws only on what the developer typed, never on pasted text, tool
  output or a command's expanded prompt".

  **New:** the profile draws only on the samples the developer names, and reads no transcript (AC2.1).
  **Why:** D2 removes transcripts as a source, so the paste-versus-typed question no longer arises.

- Open question: "A homophone, a doubled word, a dropped article, a missing Oxford comma?"

  **New:** the kinds come from the samples, grammar kinds by default (D7, D8). **Why:** the essay
  uses the Oxford comma every time, and only the co-written paper holds a homophone; the slips a
  spell-checker leaves are the thesis's.

## Wave: DISCUSS / [REF] Decisions summary (for authoring)

- **Key decisions:** D1 `phil:ai-eos` directly · D2 named samples only · D3 counts, never sentences,
  outside every repo · D4 named profiles by register · D5 reword only · D6 no slips unless counted ·
  D7 slip kinds from the samples · D8 grammar by default · D9 approved passages in fixtures · D10
  tells, voice, tells again, slips · D11 protected spans · D12 in place, committed files only · D13
  the profile governs the document, `rules/writing.md` the report · D14 no authorship claim · D15
  `mutates: true` · D16 slips follow mechanism and cause · D17 forbidden slips counted, never dropped.
- **Requirements summary:** the command strips a draft's tells, rewords it toward a named profile
  built from the developer's own documents, adds exactly the slips asked for, and reports every
  change by line.
- **Constraints:** reads no transcript; stores no sentence; adds nothing the draft lacked; never
  touches a protected span; never brings back a tell; edits only a committed file.
