---
name: groom-issues
description: Skill bundle for the phil:groom-issues command — reads a whole issue board in one call per forge and reports what is wrong with it, against a stated standard for what a well-formed issue contains. Derives the defect table fresh every run, stores no grooming marker, surfaces cross-issue candidates without acting on them, and changes nothing.
---

# Groom issues — say what is wrong with a board

A board accumulates cards that someone filed half-finished. Reading them one at a time finds the
sloppy ones and misses the expensive ones, because the costly defects live *between* issues.

**Slice 01 scope: this reads and reports. It changes nothing.** Fixing within a scope is slice 02;
merging, splitting, closing and grouping are slice 03 and are never applied unasked. Do not
improvise either.

**REQUIRED BACKGROUND: `phil:issue-board`.** Every forge mechanic — `-R` targeting, label semantics,
absolute-URL rules, dependency links, generated blocks — lives there. Do not guess any of it here.

## The standard — what a well-formed issue contains

Without this, "appropriate description" is not checkable and grooming is taste. This is the house
default. **A project may override it in its own `CLAUDE.md`**, beside the per-project setup block
`phil:issue-board` already prescribes; where it does, that override wins and this section is ignored.

A well-formed issue has:

1. **A purpose readable without context** — what and why, in the body. A title is not a purpose, and
   the next reader is a stranger or a forgetful you.
2. **A way to tell when it is done** — acceptance criteria, or an outcome concrete enough to check.
3. **Links that resolve.** Absolute URLs for files, because GitHub emits relative paths verbatim and
   they 404. Bare `#N` for issues, because a bare reference renders live title and state where a
   markdown link freezes both. **This rule is about the form, and the form is fully checkable here** —
   a relative path is a finding whether or not its target exists, because the form 404s either way.
   Whether a correctly-formed link *reaches* something is a different question, and it belongs to the
   cross-reference row of the defect table below, which is where it goes dark.
4. **Correct labels**, with single-valued families carrying exactly one value — **checkable only where
   the project declares which families are single-valued.** Nothing in a label's name says whether it
   excludes a sibling; GitHub has no scoped labels at all. `documentation` + `enhancement` on one issue
   is a defect or two orthogonal facts depending on a convention no forge records. Absent a declaration
   in the project's `CLAUDE.md`, report this rule **unevaluated**. Do not infer the family from the
   labels in use — that makes the most common pairing the rule, and then the board's habits audit
   themselves.
5. **A `## Chain` section when blocked or related** — the edge *and* the reason it exists, **on both
   ends**. `phil:issue-board` puts the prose line on both issues even where the forge writes the
   reverse edge itself, because the forge records the edge and never the reason. A chain naming an
   issue that does not name back is therefore half-written, and it is the half a reader lands on that
   decides whether they learn why. Cheap to check: the reciprocal is derivable from the same payload.

And it does **not** contain:

- **Session scratch or working state.** It belongs in the git-ignored local surface (ADR-013); a
  board is world-readable.
- **Hand-written content inside a generated region** — anything between `nwave:status` markers is
  regenerated, so a hand edit is destroyed on the next refresh and disagrees with its source until
  then.
- **A second copy of something the forge already keeps** — a roster where sub-issues exist, an order
  where position holds it. The copy is the one that goes stale.

  **A dated observation is not a copy.** The defect is a body asserting the forge's *present* state —
  "this board currently shows two cards In Progress" — which is wrong the moment the board moves and
  says nothing about when it was true. An observation stamped with its date, and pointing at the forge
  for the live answer, is history: it stays true, and a reader knows what to distrust. Prefer the
  observation where the state is the argument and deleting it would remove the argument.

## Scan once, derive fresh

**One call per forge**, bodies included:

```sh
gh issue list -R <owner/repo> --state open --json number,title,body,labels,milestone --limit 200
glab issue list -R <group/project> --output json --per-page 100
```

On `glab`, the JSON flag is **`-O`/`--output`**. `-F` is `--output-format` and takes
`details|ids|urls` — hand it `json` and it silently returns the human-readable table. Both commands
return bodies populated, so there is no N+1 and no reason to fetch issues individually.

**Never read or write a grooming marker.** No `groomed` label, no timestamp block, no state file. The
defect table is re-derived on every run. A stored marker becomes a second authority the moment
somebody edits a groomed issue — the exact failure `phil:issue-board` forbids under *One system of
record per scope* — and re-deriving costs one call.

The visible consequence, which the report must own: **a candidate the user declined will be proposed
again next run.** That is the price of storing nothing. Say so plainly, or it reads as the tool
forgetting and the user starts asking for the marker this rule exists to refuse.

## The defect table

Every finding names the rule it violates and quotes the evidence. A finding without both is an
opinion, and this skill does not report opinions.

Classify each, because slice 02 acts only on the first column:

| Mechanical — one right answer | Semantic — needs a human |
|---|---|
| A relative file link (404s on GitHub) | No purpose stated |
| An issue reference wrapped in markdown that should be bare | No way to tell when it is done |
| A single-valued label family carrying two values, where the project declares the family | Session scratch in the body |
| A missing cross-reference whose target is unambiguous | A second copy of forge-kept state the body's argument leans on |
| A second copy of forge-kept state that only restates it | Deciding which of those two a copy is |
| A `## Chain` line naming an issue that does not name back | Which end of a one-sided chain is right |

**A one-sided chain is the cheapest finding here and the easiest to write.** Detection is pure
derivation: collect every `#N` inside a `## Chain` section, and flag any whose target is open and
carries no reciprocal line. It is mechanical because the missing half is *stated on the other issue* —
nothing has to be invented, only mirrored. What is **not** mechanical is which end is right when the
two disagree about the reason; that is a human's.

Weight it by who writes it. On a real run, three of four chains written that day by an author who had
just read this rule were one-sided — writing one end while the relationship is fresh, and never
returning for the other, is the normal way this defect is made, not a careless one.

**The cross-reference row needs two things, and only one of them is a command away.** First, a
discriminator, because "unambiguous" alone made this row a judgement call wearing a mechanical label:
a reference is a finding when it names **a specific file a reader would open to follow the argument**.
A repository-root file (`CLAUDE.md`), a bare directory (`rules/`, `agents/`), a glob (`commands/*.md`)
and an ambiguous basename (`SKILL.md`, where twenty exist) are **not** findings — the first two are one
click from any page, and the last two have no single target to link. Without that line, two references
in the same body get opposite treatment and the column stops meaning "one right answer".

Second, the check itself. "Unambiguous" also means the target exists and is pushed, which
`phil:issue-board` establishes with
`git ls-tree origin/<default-branch> -- <path>` — outside a `Bash` scoped to `gh issue list` /
`glab issue list`, and deliberately so. A bare file path in a body is therefore a **candidate**, not a
finding: report it as unverified and say what would settle it. Promoting it anyway produces the failure
`phil:issue-board` warns about from the other direction — a link that renders, passes a read-back, and
404s for everyone else.

**A stale copy of forge state is two defects wearing one name.** The row used to sit wholly in the
semantic column, and a real run split it. Where the copy only restates what the forge holds — a prose
roster beside real sub-issues — deleting it loses nothing and the forge answers instead. Where the
copy is load-bearing — a card justifying its own existence by describing the board's current shape —
deleting it removes the argument, and only a human can say what replaces it.

Detection costs nothing either way: one `--json` call returns the body and the fields it contradicts,
so the comparison is inside the payload already fetched. **Read the two sides against each other on
every run** — a body asserting a sibling shipped, a parent listing children, a card citing a column's
contents. The prose keeps its confident tone long after the forge has moved.

Note what that does to the row's own classification: **the judgement comes before the fix**, so a later
slice cannot delete a stale copy unasked even when deletion turns out to be mechanical. It has to
establish which kind it is holding first, and that question is the human's.

**Do not report a missing `Work this with:` line as a body defect.** That line is generated into the
delimited block by `phil:nwave-issue-board`; its absence is a publishing question, not a content one,
and hand-writing it would be typing into a generated region.

## Cross-issue candidates — surface, never act

These cannot be found by reading one issue, which is why the scan is whole-board. Report each with
its evidence and stop; every one is expensive to undo and belongs to slice 03.

- **Duplicates** — quote the overlapping content from both. Partial overlap is the real case and is
  not automatically a merge; it may be a split or a dependency.
- **Oversized** — a card carrying work that cannot be demonstrated on its own. Name the seam.
- **Overcome by events** — the work landed another way, or the decision behind it was reversed.
- **Ungrouped effort** — a card belonging to a larger effort that says so nowhere. A milestone is a
  goal (`phil:issue-board`); do not invent a second convention.

## Reporting

Lead with the shape of the board, not the findings:

```
57 issues read · 52 clean · 3 with body defects · 2 duplicate candidates · 1 oversized
```

Then the defects, grouped by issue, each citing its rule and evidence. Then the cross-issue
candidates. Then, if anything was declined on a previous run, the note that it will reappear.

**A clean board is reported clean.** Do not manufacture findings to justify the run — that is how a
grooming tool teaches people to stop running it.

**A partial read may never make a completeness claim.** If pagination failed, the forge was
unreachable, or the limit truncated the list, say the read was partial and report *only* what was
found. "52 clean" over a partial scan is the single most misleading thing this skill can emit,
because it is a claim about issues nobody looked at.

**A rule that could not be evaluated is not a rule that passed.** Two checks go dark routinely: rule 4
wherever the project declares no label family, and the cross-reference row wherever a target cannot be
confirmed pushed. Both then produce no findings, and no findings reads as compliance. Name them, with
the reason:

```
rules 1, 2, 3, 5 evaluated · rule 4 unevaluated (no label family declared in CLAUDE.md)
· 6 unlinked paths unverified (target check needs git, out of scope here)
```

This is the partial-read failure one rule narrower, and it hides better — the issue count is honest,
so nothing in the summary looks incomplete. A reader who is told the board is clean will not ask which
rules were awake.

**Say a check went dark only when it had something to decide.** A board where no issue carries two
labels does not need rule 4's oracle, and reporting it unevaluated there is boilerplate — which is how
a caveat stops being read by the run that needs it. The note is owed when a candidate existed and the
check could not settle it: two labels and no declared family, an unlinked path and no way to confirm
the target. No candidate, no note.

## What this skill must never do

- **Write anything.** No issue edits, no labels, no comments, no milestones. Read-only is the slice.
- Read or write a grooming marker, in any form.
- Report a finding without the rule it violates and the evidence for it.
- Claim completeness over a partial read.
- Let a rule that could not be evaluated pass for a rule that was satisfied.
- Report a missing generated line as a body defect.
- Merge, split, close, or group — slice 03, and never unasked even then.

## Acceptance

`self-test/` holds the fixtures. Run them whenever this file, the command loader, or
`phil:issue-board`'s body-relevant sections change.
