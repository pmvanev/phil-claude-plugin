---
name: nwave-wave-summary
description: >-
  Use when asked what a finished stage of work decided, rather than where the work stands or what
  you were doing — "what did DISCUSS decide", "what did that wave settle", "catch me up on this
  feature", "what was decided here", "summarise the design decisions" — in a repo holding
  `docs/feature/`. Reads one finished feature artifact and states its decisions in 200 words or
  fewer of plain English, with no file paths, handles, card numbers or decision numbers: the
  decision itself, never the label pointing at it. Reads and prints; writes nothing and derives no
  status. For where a slice stands, use phil:nwave-slice-status; for what you personally were doing,
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
outcome names and any `ARGUMENT-DROPPED` clause. Everything printed counts; a line outside the budget is
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

## Decision outcomes

Report exactly one terminal outcome, every run:

`SUMMARY-RENDERED` · `NOTHING-RECORDED` · `TARGET-NOT-FOUND` · `TARGET-AMBIGUOUS`

**`READ-ONLY` is reported on every run.** Unlike the rest of this family it is a claim the tool list
already guarantees — no `Write`, no `Edit`, and a `Bash` scoped to read-only git verbs — so here it
restates the frontmatter rather than making a promise. Kept for consistency, and its weaker meaning is
stated rather than left to be assumed.

`ARGUMENT-DROPPED` is reported **alongside** `SUMMARY-RENDERED` whenever reasoning was cut to fit, and
names what went.

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

- **Write anything.** No `Write`, no `Edit`, and a `Bash` holding one read-only git verb. **The grant is
  checked rather than merely declared** — `scripts/check-readonly-commands.py` verifies every verb against
  its allowlist. That is one level short of mechanical, and `CLAUDE.md` says why: an allowlist entry is a
  promise that a verb has no writing mode. `git log -p --ext-diff` runs a diff driver the target repo
  configures, so even this verb reaches arbitrary code in principle. Checked, not proven.
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

## Acceptance

`self-test/` holds the fixtures and its `README.md` carries the fixture table and the counterexample
rule; the driver is `tests/test_wave_summary_fixtures.py`. Run them whenever this
file, the command loader, or `scripts/plain_language.py` changes.

Rationale and measurements: `references/why-these-rules.md`.
