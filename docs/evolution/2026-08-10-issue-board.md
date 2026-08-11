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

## Follow-ups

- `plugin-dev:skill-reviewer` raised ~30 medium/low findings across today's three skills that were
  not folded into this change; queue them as issues.
- The repo has **no `LICENSE`**. `ai-eos` summarizes a CC BY-SA source with attribution present, so
  the share-alike question is open until a license statement exists somewhere in the repo.
- `nw-skill-reviewer` approved all three of today's skills with zero actionable findings, including
  one verifiably false certification. Treat it as a structure check, not a quality gate.
