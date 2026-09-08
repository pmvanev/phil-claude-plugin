# Why these rules

Rationale and measurement for `../SKILL.md`. Nothing here is normative. Written from the start, on the
precedent that a skill shipping without one becomes the 8,744-word outlier this repo has an open card
about.

## The numbers, and why they were re-taken

The card that asked for this measured on 2026-09-04. DISCUSS re-measured four days later, because a
four-day-old number was the whole evidence base.

| | Card | 2026-09-08 |
|---|---|---|
| Feature deltas | 12 | **15**, and 16 once this feature's own landed |
| Total words | 59,544 | **81,942** |
| Median | ~4,600 | **5,539** |
| Largest | 7,080 | **9,447** |

**The corpus grew 22,000 words in four days.** That is the strongest argument for this command and the
card could not make it.

**157 `ADR-NNN` references point at a record this repo does not contain.** There is no `docs/adrs/`. So
the most common handle in the corpus resolves nowhere at all, which is the sharpest possible case for
stating decisions rather than naming them.

## Why this surface forbids more than any other

Three surfaces now share a bounded word count and a plain-English rule, and they permit different things:

| Surface | Card numbers | Why |
|---|---|---|
| An interrupting question | forbidden | The reader was doing something else a second ago |
| A board read | **permitted** | The number has its own column, and forbidding it only launders it into *card 34* |
| A summary | forbidden | **No column.** Every identifier sits mid-sentence |

**The laundering argument does not transfer, and that is the whole reason the lists differ — but the
reason is not that laundering is impossible here.** It plainly is possible: fixture 04 supplies
*"the eleventh locked decision"*, the driver asserts it passes the checker, and the skill forbids it in
prose.

The difference is what the laundered form is worth. **On a board read, `card 34` means exactly what `#34`
means** — the reader is equally served, so forbidding the class buys nothing and the class is permitted.
**In a summary, the laundered form is still a lookup** — *the eleventh locked decision* sends the reader
to the artifact just as `D11` does. So the class is forbidden, and the prose adds the rule the pattern
cannot reach: state the decision rather than pointing at it, in any spelling.

*An earlier version of this section said there was "nothing to launder into", which this skill's own
fixture refutes. Corrected 2026-09-08.*

This is the fourth consumer of `scripts/plain_language.py`, and the first to want the strictest list. The
module takes its forbidden classes as an argument for exactly this reason.

## "Most recently completed" is not a thing that is recorded

The card asks for the *prior* stage, read as the most recently completed one. **No artifact carries a
completion marker.** The closest honest signal is the newest commit touching a feature directory, and it
is not the same thing — a feature whose DISCUSS landed an hour ago sorts above one finished last week.

Two ways to handle that: infer completion from artifact contents, or say what the default actually is.
**The second, because the first is a status derivation** and `phil:nwave-slice-status` owns every one of
those over these files. A second derivation drifts against the first, which is a rule this skill inherits
rather than invents.

So the default is *most recently touched*, the output says so, and it names the artifact and its date —
which makes a wrong pick visible immediately rather than inferred from a summary that reads plausibly.

## Why the read-only guarantee is mechanical here, and is not elsewhere

`board-snapshot` and `resume` both declare `mutates: true` while writing nothing, because a
`gh api graphql` grant accepts a mutation document and the honest declaration is about the grant rather
than the intent.

**This command touches no forge.** It grants one verb, `git log`, which is on
`scripts/check-readonly-commands.py`'s allowlist, so `mutates: false` is *checked* rather than merely
declared.

**Two corrections to what this section first claimed**, both made 2026-09-08 and both the same defect this
repo keeps recording — a rationale that reads well and is false.

**It is not the first.** `nwave-slice-status` has declared `mutates: false` with the identical
`Bash(git log:*)` grant since before this feature existed; `ai-eos` and `spirit-walk` do the same. The
true statement is narrower: it is the first in the **board and session** family, whose other members carry
forge grants.

**And "checked" is not "mechanical".** `CLAUDE.md` states that an allowlist entry is a promise that a verb
has no writing mode. `git log -p --ext-diff` runs a diff driver the target repo configures, and
`--textconv` runs a configured filter — arbitrary code reachable from a grant whose prefix is `git log`.
The guarantee is a verified grant over a human-maintained allowlist, which is worth having and is not
proof.

**It costs one thing, and the trade was taken deliberately.** No interpreter is granted, so nothing counts
the rendered output's words at run time. The ceiling is enforced by fixtures at build time and by this
skill's prose at run time. Granting `python3` would make the count mechanical and would make the
read-only guarantee promissory again — trading an enforced guarantee for an enforced check, on a command
whose whole distinction is the enforced guarantee.

## Cut the argument, never the decisions

Forty-fold compression means most of the source is discarded by design. The ordering rule exists because
the tempting cut is the opposite one: decisions are short and quotable, arguments are long, and a summary
under pressure tends to keep the interesting reasoning and lose the boundaries.

**A decision named without its reasoning is still useful. Reasoning without its decision is not.** The
command names the artifact it read, so the discarded part is one command away rather than reconstructed.

## Saying nothing is a result

An absent, empty or heading-only artifact gets a sentence, not a summary. This is the failure the feature
would otherwise introduce: before it existed, nobody could produce a confident 200 words about a stage
that decided nothing, and afterwards such an output is indistinguishable from a real one.

The same shape appears twice already in this family — a blocked card whose reason is unrecorded, and a
board card whose body says nothing. In all three the honest answer is the finding.
