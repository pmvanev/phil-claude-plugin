---
name: nwave-wave-summary
description: >-
  Use when asked what finished work decided, rather than where it stands or what you were doing —
  "what did DISCUSS decide", "what did that stage settle", "catch me up on what this feature
  decided", "what did that slice actually land", "what did that slice ship as against its brief",
  "summarise the decisions" — in a repo holding `docs/feature/`. Two modes: a finished stage's
  decisions, and with --slice a finished slice's brief reconciled against what shipped. 200 words
  each, plain English, with no file paths, handles, card numbers or decision numbers — the decision
  itself, never the label pointing at it. Reads and prints; writes nothing and derives no status.
  For where a slice STANDS use phil:nwave-slice-status; for what you personally were doing,
  phil:resume; for what is on the board, phil:board-snapshot.
---

# Wave summary — what the thinking decided, not where the work stands

A finished artifact is written for the wave that produced it. Measured 2026-09-08 across this repo: **16
feature deltas, a median of 5,539 words and a largest of 9,447** — carrying 157 `ADR-NNN`
references pointing at a record this repo does not contain, and 54 `DDD-N` handles numbering a decision
inside one file.

So the answer to *what did this settle* is an afternoon's read whose load-bearing sentences are keyed on
identifiers the reader must resolve first. **A record nobody opens is not meaningfully different from one
nobody wrote.**

## What this answers, and what it does not

| Question | Command |
|---|---|
| What did this stage decide? | **this one** |
| Where does the work stand? | `phil:nwave-slice-status` |
| What was *I* doing? | `phil:resume` |
| What is on the board? | `phil:board-snapshot` |
| What is wrong with the cards? | `phil:groom-issues` |

**Never derive a status.** `phil:nwave-slice-status` owns every derivation over these files, and two
derivations over one source drift. Where the reader wants position, name that skill and stop.

## Resolving the target

**With a name, read `docs/feature/<name>/feature-delta.md`.**

**With no name, take the most recently touched feature** — and say that is what was taken:

```sh
git log -1 --format=%cI -- docs/feature/<id>/
```

**"Most recently completed" is not recorded anywhere, so it is not what this resolves.** No artifact
carries a completion marker; the newest commit touching a feature directory is the closest honest
signal, and it is not the same thing. A feature whose DISCUSS landed an hour ago sorts above one finished
last week — which is usually right and is sometimes not. **Name the artifact and its date in the output**
so a wrong pick is visible immediately rather than inferred from a summary that reads plausibly.

**Where two features tie, say so and stop.** Do not pick. Where no `docs/feature/` exists at all, or a
named feature does not, that is a different answer — see *Decision outcomes*.

## The summary

**200 words or fewer, counted over the whole rendered output** — the summary, the provenance line, the
outcome names, and any `ARGUMENT-DROPPED` or `ATTRIBUTION-INCOMPLETE` clause. Everything printed counts; a line outside the budget is
the budget leaking.

**Nothing counts it at run time**, and that is a deliberate trade rather than an oversight — see
*Half enforced, half promised* below.

**State what was decided and what it rules out.** A stage's value to a later reader is the decisions and
their boundaries — not the argument that produced them, which is what the artifact is for.

**Where the summary will not fit, cut the argument and never the decisions.** A decision named without
its reasoning is still useful; reasoning without its decision is not. Say what was left out, and report
`ARGUMENT-DROPPED`.

**Name the feature read, and the date of the artifact** — *"the board-snapshot feature record, last
changed 2026-09-08"*. The discarded 98% is then one command away and never has to be reconstructed from
the summary.

**Name the feature, never the path.** A path is a file-path identifier and the vocabulary rule below
forbids one everywhere, this line included — there is no exemption, because a reader who knows the
feature can find its record and a reader who cannot is not helped by a path either. An earlier draft
required the artifact's name and would have made every run breach its own rule.

### State the decision, never its number

**No identifier of any kind reaches the output** — no file path, no bracketed identifier, no bare handle
like `D11` or `ADR-013`, and **no card number either**.

**This is the strictest vocabulary rule in the plugin, and the reason is positional.** A board read
prints `#34` because the number has a column of its own; forbidding it there would only launder it into
*card 34*. **A summary has no column.** Every identifier in it sits mid-sentence, where it is precisely
the lookup this command exists to spare the reader.

**A slice's own number is the one exemption, and nothing else gained one.** A slice summary must say
which slice it read, exactly as the stage summary names its feature — an identifier naming *what this
output is about* is not the lookup the rule exists to remove. Commit shas stay forbidden: a sha points
into history and is never the subject of a sentence.

So *"per the fourth locked decision"* is not the fix, and neither is *"as recorded in the delta"*. The fix
is to **say the thing**: *"the board's order is consumed and never recomputed, because a second producer
would make neither answer trustworthy."*

**Half enforced, half promised, and which is which matters — including inside the enforced half.**
`scripts/plain_language.py` holds both the counter and the forbidden list. **The fixtures apply the
forbidden list and do not apply the counter**: no fixture here can fail because something was too long,
and the counter appears in the suite only to prove a counterexample is *short* enough to fail for the
right reason. So the word ceiling is prose at run time and prose at build time; only the vocabulary is
checked.

Nothing counts the rendered output at run time either: this command holds no interpreter, deliberately,
because that is what keeps the read-only grant narrow. At run time both rules are this section.

### When the stage recorded nothing

**Say so. Do not summarise.** An absent or empty artifact, or one that records only a heading, gets
`NOTHING-RECORDED` and one sentence naming what was looked for and what was found.

A confident 200 words about a stage that decided nothing is the worst output this command can produce,
because it is indistinguishable afterwards from a real summary — and it is the failure this feature would
otherwise introduce, having never existed before.

## The slice mode — `--slice`

The stage summary reads one artifact. **The slice summary reads a brief and reconciles it against what
shipped**, because a brief states what a slice *intended* and the useful question is what it *landed*.

**200 words per slice**, same vocabulary rule.

**With a number, read that slice. With none, read the most recently touched brief** — resolved as the
stage mode resolves a feature, and named in the output for the same reason. **Never summarise every slice
at once:** a per-slice bound leaves the whole output unbounded, on a command whose one promise is a
bounded read. Where briefs tie, that is `TARGET-AMBIGUOUS`; where a number names no brief,
`TARGET-NOT-FOUND`.

### Attributing commits to a slice

```sh
git log --oneline -- docs/feature/<id>/slices/<brief>          # the brief's own history
git log --oneline --grep "slice NN"                            # the naming convention
git show --stat <sha>                                          # what each commit touched
```

**The naming convention is a habit, not a guarantee, and it fails on the case that matters most.**
Measured 2026-09-08 over this repo's last nine commits: **four name no slice at all**, and one of those
four is a *precursor commit* belonging to a slice whose sibling commit does name it. So attribution by
subject silently drops exactly the work a slice did before its headline change.

**The range is defined, because the count means nothing without it.** It runs from the commit that
created the slice's brief to the commit that last touched the feature's directory — `git log --reverse --
<brief>` for the first, `git log -1 -- docs/feature/<id>/` for the last. Commits outside it are not this
slice's and are not counted; commits inside it naming no slice are the gap.

**Report what could not be attributed.** Where commits in that range cannot be tied to the slice, say how
many and stop guessing — a landed view built on a partial commit set is confidently wrong about the one
thing it exists to establish. Report `ATTRIBUTION-INCOMPLETE` alongside.

### What the fold must produce

**Name what landed that the brief did not describe**, and **what the brief promised that did not land**.
Those two are the whole value; everything else the brief already said.

**Compare meaning, never paths — and never count files.** A file count is a path diff wearing a sentence.

**Compare meaning, never paths.** A brief describes work in prose — *"two fixtures in the existing
suite"* — so a file the brief never names is usually a file the brief plainly anticipated. Measured
2026-09-08 against three real slices: a naive path comparison produced 48 differences of which roughly
five were real. **A mechanical version of this check is worse than none**, and that is why the vocabulary
is fixtured here while this is not. The ceiling is fixtured in neither mode — see *Half enforced, half
promised*.

**Where brief and outcome agree, say they agree, briefly.** Do not pad to prove effort.

**Where the fold finds nothing the brief does not already say, say that.** The card that asked for this
doubted the whole mode on those grounds. Producing a shorter brief instead of a landed view is exactly
the failure it feared, and reporting the absence is how that stays visible.

**Never judge what landed.** This reports; `phil:adversarial-review` judges. And never derive whether the
slice is done — `phil:nwave-slice-status` owns that.

## Decision outcomes

Report exactly one terminal outcome, every run:

`SUMMARY-RENDERED` · `NOTHING-RECORDED` · `TARGET-NOT-FOUND` · `TARGET-AMBIGUOUS`

**`READ-ONLY` is reported on every run.** Unlike the rest of this family it is a claim the tool list
already guarantees — no `Write`, no `Edit`, and a `Bash` scoped to read-only git verbs — so here it
restates the frontmatter rather than making a promise. Kept for consistency, and its weaker meaning is
stated rather than left to be assumed.

These are reported **alongside** `SUMMARY-RENDERED`: `ARGUMENT-DROPPED` whenever reasoning was cut to
fit, naming what went; and `ATTRIBUTION-INCOMPLETE` in `--slice` mode whenever commits in the range could
not be tied to the slice, naming how many.

- **`TARGET-NOT-FOUND`** — a name was given and no such feature exists. **Never report `NOTHING-RECORDED`
  for this.** That outcome is a claim about the work — *this stage decided nothing* — and deriving it from
  a typo is fixture 02's own failure arriving through the front door. Say the feature was not found, and
  where it was looked for.
- **`TARGET-AMBIGUOUS`** — no name was given and the default cannot be resolved because two or more
  features tie on their newest commit. Name the candidates and stop; picking one silently is how a summary
  of the wrong feature reads as correct. **Where there is no `docs/feature/` at all, that is
  `TARGET-NOT-FOUND`** — zero candidates is not the same as too many, and one outcome covering both tells
  the reader nothing about which happened.

## What this skill must never do

- **Write anything.** No `Write`, no `Edit`, and a `Bash` holding two read-only git verbs. **The grant is
  checked rather than merely declared** — `scripts/check-readonly-commands.py` verifies every verb against
  its allowlist. That is one level short of mechanical, and `CLAUDE.md` says why: an allowlist entry is a
  promise that a verb has no writing mode. `git log -p --ext-diff` runs a diff driver the target repo
  configures — conditional on their config. **Worse, and unconditional: `git log` and `git show` both
  accept `--output=<file>`, which writes, and clobbers an arbitrary absolute path outside the repo.**
  Verified on git 2.53.0, 2026-09-08. So the declaration asserts more than the grant delivers — here and
  for the three other commands on that allowlist. Checked, not proven, and the gap is named rather than
  implied.
- **Derive a status.** Not done, not in progress, not a percentage. That belongs to
  `phil:nwave-slice-status`.
- **Summarise a stage that recorded nothing.**
- **Put any identifier in the output** — path, handle, bracketed id or card number.
- **Name a decision instead of stating it.** *"See the sixth decision"* is the defect, not the citation
  style.
- **Cut a decision to fit.** The argument goes first, and what went is named.
- **Pick between tied targets**, or infer a target from the current branch, the open editor, or the most
  recently mentioned feature in conversation.
- **Edit or shorten the artifact it read.** A summary is not a licence to rewrite its source.
- **Claim the default is the most recently *completed* stage.** It is the most recently touched, and the
  output says so.

## The standard for everything here

**This surface quotes nothing.** Every other board-family surface mixes composed text with a filer's own
words, and the discriminator does real work separating them. Here there is no quoted half, so
`${CLAUDE_PLUGIN_ROOT}/rules/writing.md` governs the entire output.

Read it as **compose well, never compose short** — the ceiling already bounds length, and the standard
bears on active voice, positive form, concrete language and the emphatic word last, in a read whose whole
value is being finishable in one pass. *State the decision, never its number* is that standard's
*definite, specific, concrete language* applied where no pattern reaches; fixture 06 is what would fail
without it.

## Acceptance

`self-test/` holds the fixtures and its `README.md` carries the fixture table and the counterexample
rule; the driver is `tests/test_wave_summary_fixtures.py`. Run them whenever this
file, the command loader, or `scripts/plain_language.py` changes.

Rationale and measurements: `references/why-these-rules.md`.
