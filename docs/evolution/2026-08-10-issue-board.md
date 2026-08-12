# Evolution — issue-board (2026-08-10)

## What shipped

`skills/issue-board/SKILL.md` — a knowledge-only skill (no paired command) carrying the semantics
for driving GitLab and GitHub issue boards from the command line with `glab` and `gh`.

It is the residue of two research passes that both concluded **buy, don't build**:

- `docs/research/tooling/local-markdown-kanban-backlog-tooling-research.md` — local markdown kanban
  tooling. Outcome: adopt Backlog.md plus its VS Code extension.
- `docs/research/tooling/claude-driven-forge-issue-boards-research.md` — whether an agent can drive
  forge issue boards without custom code. Outcome: `gh` and `glab`, no MCP server, no plugin, no
  sync layer.

Both reports carry supersession blocks recording what execution overturned in them.

## Why

Nothing needed building except knowledge. The CLIs already do the work; what neither
`glab --help` nor `gh --help` explains is the handful of semantics where a wrong guess **reports
success**:

- GitLab boards are label views, so a card move is a label swap. Creating a board list instead
  reports success, adds a column, and leaves the card where it was.
- Scoped labels (`key::value`) are **Premium or Ultimate**. On Free they are labels with colons in
  them and nothing enforces exclusion — the failure appears only on someone else's instance.
- GitHub has no scoped labels at all. A board is a Projects v2 Status *field* on a separate API,
  and an issue must be `item-add`ed before it has a field to set.
- Both CLIs infer the project from the current directory's git remote, and issue #12 exists in
  every project.

## The design, in one idea

**Generic semantics ship; instance constants don't.** The skill carries what is true of any GitLab
or GitHub, and ends with a `CLAUDE.md` template each project fills in with its own host, IDs, and
tier. That split is why this is a distributable skill rather than a note in one repo's `CLAUDE.md`.

Knowledge-only, with no command, because there is no workflow, gate, artifact, or argument to
parse. Every command in `commands/` fronts a multi-step gated process; a `/phil:issue-board` would
be a lookup wrapper.

## Outcome (before → after)

| | Before | After |
|---|---|---|
| Driving a board | Hand-rolled API scripts per project | `glab` / `gh`, one command per operation |
| Tier awareness | None — a Premium-only mechanism assumed universal | Tier probe first, Free path documented |
| Target safety | `glab issue update 12` against whatever the cwd pointed at | `-R` on every invocation, stated as a rule |
| Certificate handling | Process-wide TLS disabling | CA import as the fix; host-scoped bypass as a warned, developer-authorized stopgap |

## Scope / accepted limitations

- **No sync.** The skill states the partition rule — one system of record per scope, joined by an
  issue reference — and explicitly declines bidirectional sync.
- **Two command forms ship marked unverified**: the `glab config set skip_tls_verify` flag and the
  `blocks`-link creation call. Both are labelled in the text rather than presented as settled.
- **Projects v2 remains owner-scoped**, so a GitHub board cannot be driven by a repository-scoped
  token. Noted, not solved.

## Amendment — cross-linking and dependency chains

Two sections added after first ship: `## Link what the forge cannot resolve` and `## Leave a chain
when you pivot`.

The motivating request was "hyperlink every reference." Rendering the same issue body through both
forges' `POST /markdown` endpoints showed the naive form is wrong twice over:

- **Relative paths split the forges silently.** GitLab expands `[adr](docs/adr/016.md)` to a blob
  URL on the default branch; GitHub emits the href verbatim, where it resolves against the *issue*
  URL and 404s. Both render a link, so the GitHub failure is invisible until clicked. A leading
  slash changes nothing. Absolute URLs are the only portable form.
- **Wrapping an issue reference downgrades it.** A bare `#12` is a live reference carrying title and
  state (GitHub delivers it as a hovercard); `[#12](…/issues/12)` is an ordinary link that drops all
  of it. So the rule is *not* "link everything" — it is link what the forge cannot resolve, and
  leave alone what it can.

A useful side effect: both forges autolink a reference only when the issue exists, so a `#12` still
rendered as plain text is a free wrong-number check on read-back.

The chain sections record why work stopped, not just that it did — the edge is what the forge
stores, the reason is what only the author has. Written on both issues before starting the blocker,
because that is when the reason exists. Not hand-maintained afterwards: the linked issue is
authoritative about its own state, and a copy in the blocked issue can only go stale.

One claim ships marked unverified — GitLab's `#L40-52` line-anchor form, since no project on the
available instance had issues to render against. GitHub's `#L40-L52` is confirmed.

## Correction — GitHub does have dependency links

A `plugin-dev:skill-reviewer` pass over the amendment doubted "GitHub: no native dependency links"
without being able to assert the alternative. Checking settled it: `gh issue edit` carries
`--add-blocked-by`, `--add-blocking`, `--add-sub-issue`, and `--parent`, and the GraphQL `Issue`
type exposes `blockedBy`, `blocking`, `parent`, and `subIssues`. The claim was not stale, it was
wrong — and it was wrong in a skill whose entire premise is that a wrong guess about forge semantics
reports success.

Two things follow. The **absolute negative is the dangerous shape**: "X has no Y" reads as settled
and gets no re-check, while "confirm against your version" invites one. The skill already opens by
telling the reader to check `gh --version` before trusting board behavior, and then failed to apply
that to itself. Capability claims about a moving forge now name the version they were verified on.

The same pass caught a check that could not fire: "a `#12` still rendering as plain text means the
number is wrong" is true of *rendered* output, but `gh issue view --json body` returns raw markdown,
where `#12` is literal text unconditionally. The section named a retrieval path that defeated its
own test. Replaced with a `POST /markdown` round-trip, verified — `#3` renders with an `href`,
`#999` stays plain text — plus the caveat that an unreadable target renders identically to a wrong
number.

## Amendment — issue granularity and the nWave mapping

Two sections added: `## Choosing what becomes an issue` and `## nWave features on a board`.

The question behind them was whether nWave already does something kanban-shaped. It does not. It
holds the data and renders it three ways, none of them persistent or visible to anyone else:

| Artifact | Role | Status? |
|---|---|---|
| `roadmap.json` | The plan — `phases[].steps[]` with `id`, `name`, `criteria`, `deps`, `agent` | **No.** 56 of 57 roadmaps on disk carry no `status` field on any step |
| `execution-log.json` | The ledger — `{sid, p: RED\|GREEN\|COMMIT, s, d, t}` | Yes; status is a fold over events per `sid` |

`/nw-continue` derives progress and then launches the next wave; `/nw-buddy` answers in prose;
`/phil:slice-status` already renders the table, read-only. No `nw-*` skill touches `gh` or `glab`
for issues. So the gap was never the table — it was persistence and visibility to other people.

Design decisions worth recording:

- **Slices are the cards, not features.** A feature card sits in one column for weeks; a slice moves.
  Steps stay rows, because one 22-phase feature would otherwise mint hundreds of issues.
- **Wave is a label, not a column** — reversed during the session. Wave-columned boards looked
  natural (waves are sequential, so the board reads left to right) until the owner pointed out that
  nWave is worked one feature at a time. Five columns holding one card between them is a progress
  readout wearing a board's clothes. The wave stays as a label, which still filters and still
  records how far a finished feature got. The board that earns its keep is the slice board.
- **The projection is generated, never typed** — otherwise the description becomes a second
  authority over facts `execution-log.json` owns, which this skill already forbids.
- **The log cannot say `blocked` or `awaiting input`.** No event exists for either. The render owns
  the three derivable states and must preserve human-set ones; a regeneration that overwrites
  "blocked — waiting on an answer" destroys the only record of why work stopped.
- **Delimited `nwave:status` block**, because both forges replace a description wholesale.

The `skill-reviewer` correction above changed this section before it shipped: since GitHub has real
sub-issues (`--add-sub-issue`, `--parent`, verified on `gh` 2.97.0), slices attach to the feature
natively and the roster table is redundant there. `glab issue update` 1.112.0 exposes no hierarchy
flag, so the roster table survives as the GitLab path only.

Dropping wave columns also retired the section's one unverified claim — that multiple issue boards
per project is GitLab Premium — which mattered only when a project needed a wave board *and* a slice
board. One board suffices.

`phil:slice-status` was renamed `phil:nwave-slice-status` in the same change: it was always
nWave-specific, and the pairing reads clearly now that a second nWave skill exists. The rename
covers the skill, its command, and its twelve self-test fixtures.

## Split — `nwave-issue-board` extracted

The mapping shipped inside `issue-board` and was extracted within the session. Size was the visible
reason (3403 words); the real one was a conflict that appeared immediately:

| | `phil:slice-status` | the new section, as first written |
|---|---|---|
| Vocabulary | `done`, `current`, `next`, `not started`, `blocked`, `deferred`, `unknown` | `done`, `in progress`, `not started` |
| `blocked` | derivable from `.develop-progress.json` | claimed not derivable at all |
| `unknown` | a distinct claim; reporting it as `not started` is "a lie the user will act on" | absent |

Two skills deriving status from the same files, disagreeing on the vocabulary and on whether
`blocked` exists. So the split is not primarily about length — **derivation already had an owner**,
and the extracted skill is a bridge rather than a second implementation. It names `phil:issue-board`
and `phil:slice-status` as REQUIRED BACKGROUND and states outright that it never derives a status.

The generic half stayed behind as `## Choosing what becomes an issue`, which applies to any tracker:
one issue per independently demonstrable thing, split when two halves would occupy different columns
at once, ask when the split is not obvious.

Named `nwave-issue-board`, not `nw-issue-board`: `nw-*` is the nwave plugin's own namespace
(`nw-buddy`, `nw-roadmap`, `nw-continue`), and a prefixed name would read as one of theirs.

`issue-board` ends at 2665 words; the bridge at 1297.

### What the reviewer pass caught in the bridge

Two independent `skill-reviewer` passes ran over both skills. The bridge shipped its first draft
reproducing, at birth, the exact fault the split was meant to cure:

- **It forbade what the owner permits.** "Never read a step's status from `roadmap.json`" contradicts
  `nwave-slice-status`, which takes done-ness from "the execution log, `progress.md`, or the per-step
  `status` field, whichever the project actually maintains" — and the 57th roadmap is precisely the
  one that maintains it. A precedence rule, invented by the skill that had just delegated precedence
  away.
- **It re-listed the status vocabulary verbatim** — the very table whose divergence justified the
  split.
- **It duplicated the `gh` sub-issue commands and their version pin**, which already live in
  `issue-board`, inside the skill whose charter says it does not own forge mechanics.
- **It dropped the `Notes` column.** `nwave-slice-status` renders four columns, and Notes is where
  drift (`⚠ no commit found`), named source disagreements, and missing artifacts go. Publishing
  three columns sends the cleanest-looking version of the table to the widest audience — inverting
  the honesty the neighbouring section spends two paragraphs defending.

All four are fixed. The lesson worth keeping: extracting a skill does not, by itself, stop
duplication. The bridge had to be rewritten to *reference* rather than *restate*, and the reviewer
found each restatement by reading the two owners side by side.

Also corrected in `issue-board`: the tier probe's non-200 rows are now marked inferred rather than
observed, and 404 is no longer read as "wrong path" when it equally means the token cannot see the
group; the personal-namespace case now has a fallback (assume Free, keep `--unlabel`) instead of a
dead end; the autolink-existence check is scoped to what was actually verified on each forge.

**Open, not fixed:** `## Verify the end state` asserts three GitHub Projects v2 behaviors as "learned
the hard way", and no run in this repo records that experience. The operational advice is sound
either way, but the experience claim is unsourced and unversioned while every neighbouring capability
claim names `gh` 2.97.0. Left standing pending the author's confirmation of what was actually run.

### Self-test suite added

Twelve fixtures under `skills/nwave-issue-board/self-test/`, mirroring the sibling's format. The
reviewer's argument for building them: this skill's failure modes are strictly worse than
`nwave-slice-status`'s, because a wrong table there is read by one person in a terminal and a wrong
table here is read by the team, in an issue, for as long as it stands.

Two fixtures pin faults the skill actually shipped in its first draft — the dropped `Notes` column
(02) and the invented rule forbidding a status source its owner permits (12) — which is the argument
for the suite in miniature: both got through design, review of the design, and writing, and were
caught only by reading the two owners side by side.

Fixtures 04 and 11 are deliberately adjacent and resolve opposite ways. In 04 a person recorded
something no artifact can hold (*waiting on Sam*) and it must survive a refresh. In 11 a person
overwrote something the artifacts own (a step's done-ness) and it must not. A rule that gets one right
by getting the other wrong is a gate failure — this is the pair that stops "preserve human edits" from
becoming "let the forge edit the ledger".

Fixture 08 is the suite's only actively harmful case, matching the sibling's 04: a card for deferred
work does not misinform someone, it assigns them.

`issue-board` still has no suite. Its content is reference rather than procedure, so the convention
there is genuinely unsettled — noted rather than resolved.

## Amendment — card ordering (2026-08-11)

Neither skill said anything about the order of the cards. Asked directly whether the nWave mapping
covered it, the answer was no: the only ordering rule anywhere was *row order is `phases[].steps[]`
array order*, governing rows inside one issue, and `issue-board` had no hit for order, sort, rank,
position, or priority at all. Both now cover it.

`issue-board` gains *A column is a queue, so its order is a claim*: known order gets written, unknown
order gets ranked anyway with the basis recorded where readers already look. The mechanics were
verified the same day against live schemas — `updateProjectV2ItemPosition` and `reprioritizeSubIssue`
on GitHub, `issueMoveList` on the 18.9.1-ee instance, and the negative claims (`glab issue` has no
reorder subcommand, `gh project item-edit` has no position flag) against `glab` 1.112.0 and `gh`
2.97.0. **None of the mutations was exercised**, and the section says so.

`nwave-issue-board` gains *The order of the cards is the order of the work*: slice cards sit in
`phases[]` array order, and before `/nw-roadmap` exists they sit in slice-number order carrying
`Order: slice number, provisional until /nw-roadmap`. The suite goes from twelve fixtures to
**fourteen** — `13-order-follows-roadmap` (array order beats the slice and issue numbers that agree
with each other) and `14-guessed-order-says-so` (a guess published as a guess). Both sit with `08`:
a position is an instruction to whoever reads the column next, whether or not anyone chose it.

### What the reviewer pass caught, again

The first draft repeated the mistake `12` exists to pin — asserting behavior beyond its evidence.
The ordering section was the least evidence-marked passage in a file whose identity is evidence
marking, and its highest-consequence claim (`afterId` null moves an item to the **top**, not nowhere)
was stated flatly while the same paragraph admitted the mutation was never run. Both quoted
behaviors are schema description fields now, attributed as such.

Three contradictions with the file's own content came out of the same pass: the intro said GitLab
board lists fall back to a timestamp while the table said position is `relative_position` ten lines
later; the prescribed `--label`/`--unlabel` move cannot set a position, which the file never said;
and the table's GitHub read-back pointed at `gh project item-list`, which *Verify the end state*
already warns under-reports. A fourth claim — that `--add-sub-issue` appends in call order — was
unverified inference, and `nwave-issue-board` had built a seeding strategy on it that would have left
the column in forge order while reporting the board ordered. That is fixture 13's failure mode,
licensed by the skill's own text. Claim dropped, strategy replaced.

## Amendment — progress rollups (2026-08-12)

Asked whether GitLab has GitHub's `0/3` sub-issue progress bar, neither skill had an answer, and the
honest one turned out to be forge-shaped rather than yes/no. `issue-board` gains *A parent's "N of M
done" counts different things on each forge*.

The asymmetry is the content: **GitHub's parent rollup counts sub-issues, which are cards; GitLab's
stable parent rollup counts markdown checkboxes, which are not.** So a GitLab feature whose children
must also cross board columns has no project-scoped, non-experimental count of them, and the remedy
is a milestone — the one GitLab rollup that is stable and counts real issues.

Evidence, all gathered the same day. `subIssuesSummary {total, completed, percentCompleted}` returned
`{3, 0, 0}` on a three-sub-issue parent with `trackedIssues.totalCount: 0` alongside it, confirming
the two GitHub counters are independent (`gh` 2.97.0). GitLab's `task_completion_status` was verified
by parsing checkboxes out of twelve raw descriptions on the 18.9.1-ee instance and comparing —
partials and completes matched. `rolledUpCountsByType` is marked Experiment in that instance's schema
and **was not run**. `WorkItemWidgetProgress` is recorded as the trap it is: the name fits and the
field is OKR start/current/end values, so it answers with something unrelated.

A second section came out of the tooling rather than the question. **`glab api graphql` 1.112.0
discards any query containing `__type` or `__schema` and answers with a 7.4 MB full-schema dump** —
valid JSON with a `data` key, so it reads as success until `data.__type` turns out to be missing.
Five query forms pinned the discriminator as introspection, not syntax; two neighbouring forms
(`--input` with a JSON body, `-f query=@file`) fail differently and are not workarounds. The remedy
is to keep one dump and query it locally, which is in fact how the previous amendment's GitLab
signatures were read — so the section documents a practice the file already depended on silently.

`nwave-issue-board` gains the mapping consequence: on GitHub the slices-done count is free and the
generated block must not restate it; on GitLab the roster stays bare references and **must not be
converted to checkboxes to manufacture a bar**, because a checkbox is ticked by hand while a slice
issue closes on its own. The suite goes from fourteen fixtures to **fifteen** —
`15-roster-not-checkboxes`, which sits with `08`, `13`, and `14`: correct on the day it is written,
authoritative long after.

### What the reviewer pass caught, again

Two self-contradictions, both introduced by compressing a four-mechanism answer into one sentence.
"GitLab's stable rollup counts checkboxes, not issues" was flatly contradicted by the milestone row of
its own table two lines below, and by the milestone remedy twenty lines below — fixed by scoping the
claim to the *parent-issue* rollup. On the nWave side, "there is no slices-done count" dropped the
*project-scoped* qualifier that the surrounding paragraph, the sibling skill, and fixture 10's fourth
assertion all carry; as written it would have failed that fixture.

The sharpest finding was self-inflicted. Fixture 15's own assertion 5 forbids restating GitLab rollup
field names in this skill, and the prose it shipped alongside named `MilestoneStats`. The fixture
caught the skill it was written for, in the same commit — which is the delegation boundary working,
one draft later than it should have.

### Driving the suite turned up two pre-existing gaps

All fifteen fixtures produce the correct decision. Two failed on a *checkable assertion* rather than
on the outcome, both predating this change, and both the same shape: a disclosure the skill implies
but never requires.

`07` asserts that a slice issue opened before `/nw-roadmap` says its step table arrives with the
roadmap. *Fill in two stages* forbade inventing rows and deferred the table, but never required the
line — so an issue reached the same false impression as invented rows would have, by omission.

`11` is the more interesting one, and it is a hole in the 04/11 pair the suite calls its sharpest.
The fixture asserts the forge-versus-artifacts disagreement is surfaced. *Generate into a delimited
block* does name `Notes` as where disagreeing sources go — but `nwave-slice-status` populates `Notes`
and never reads the forge, so the one disagreement only this skill can observe was the one nothing
instructed it to write down. `04` had its disclosure rule from the start; its deliberate opposite did
not. Both are now stated as one rule read in two directions, sharing the discriminator explicitly:
*awaiting input* adds what no artifact can hold, a hand-typed `done` overwrites what they do.

The gaps are evidence for the suite rather than against it — both sat under passing outcomes, and
neither surfaced until the assertions were read one at a time. The grader was also the author, which
is the standing weakness of driving this suite at all.

## Follow-ups

- `plugin-dev:skill-reviewer` raised ~30 medium/low findings across today's three skills that were
  not folded into this change; queue them as issues.
- The repo has **no `LICENSE`**. `ai-eos` summarizes a CC BY-SA source with attribution present, so
  the share-alike question is open until a license statement exists somewhere in the repo.
- `nw-skill-reviewer` approved all three of today's skills with zero actionable findings, including
  one verifiably false certification. Treat it as a structure check, not a quality gate.
- `issue-board` is well over the 3,000-word guideline (~4,000 after the 2026-08-12 amendment, up from
  ~3,400). The reviewer's split proposal — move the per-type link recipes and the self-hosted
  certificate section to `references/` — is sound and deliberately not taken here, because no skill in
  this repo uses `references/` yet and the write-path content must stay resident. Decide the
  convention before splitting.
- The 2026-08-12 reviewer pass argues the real defect is shape, not length: sixteen flat `##` sections
  in the order they were written, which is why the introspection section landed 200 lines from the
  advice that sends readers into it. Its proposal — group under *Before you write* / *Writing to a
  board* / *Reading back* / *Operating*, demoting today's sections to `###` — is zero content change
  and was not taken. Forward pointers were added instead. Revisit if a seventeenth section has nowhere
  obvious to go.
- Neither ordering mutation has been run against a real board. The first person to reorder a real
  column should confirm the `afterId`-null and `positionInList` semantics and upgrade the markers.
- `agents/adversarial-reviewer.md` frontmatter has an unquoted `description` containing
  `Pattern lineage: …`; a plain YAML scalar cannot contain `: `, and a strict parser drops the agent.
  Predates this work.
