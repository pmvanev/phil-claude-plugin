---
name: issue-board
description: Use when driving a GitLab or GitHub issue tracker or board from the command line with `glab` or `gh` — moving a card between board columns, reordering a column or prioritizing a backlog so the top card is what to work on next, ordering sub-issues under a parent, setting a status label or a Projects v2 Status field, reading a parent issue's completed-children count or progress bar, deciding whether a piece of work is one issue or several, hyperlinking or cross-linking references in an issue body to a file, an ADR, or another issue, marking an issue blocked by another and recording why, weighing whether to sync a local task file with a board, reading a forge's GraphQL schema to confirm a mutation's signature, or connecting to a self-hosted GitLab instance. Covers the semantics `--help` does not, where a wrong guess reports success.
---

# Driving GitLab and GitHub Issue Boards

**Check the repo before touching the board.** If `.nwave/` or `docs/feature/` exists, load
`phil:nwave-issue-board` first — it owns what a feature, a slice, and a step each become, and it
sends you back here for the mechanics. Acting from this skill alone in an nWave repo mints the
wrong objects: an issue per step instead of per slice, and no feature parent to hang them on.

Both forges are driven from the command line: `glab` for GitLab, `gh` for GitHub. Prefer the CLI
over an MCP server — the commands are auditable in the transcript, credentials stay in each tool's
own store, and no extra configuration is needed.

Check `gh --version` and `glab --version` against the latest upstream release before trusting board
behavior. Some distribution channels lag badly — Ubuntu's universe repository shipped `gh` 2.46
against upstream 2.97 — while vendor channels (GitHub's own apt repo, Homebrew, winget, dnf) track
releases. An upstream release tarball drops a single binary into `~/.local/bin` with no sudo.

## Always name the target repository

```sh
glab issue update 12 -R group/project --label 'status::in-progress' --unlabel 'status::to-do'
gh issue edit 12 -R owner/repo --add-label needs-review
```

Both tools infer the project from the current directory's git remote. Issue #12 exists in every
project, so running from the wrong directory mutates a different project's issue — successfully,
with no error. Pass `-R` on every invocation.

## Find the tier before choosing a convention

Two of GitLab's board mechanisms are gated behind Premium, and both fail silently on Free rather
than erroring. Establish the tier first.

```sh
glab api "groups/<group>/epics"   # 200 → Premium+ · 403 → Free · 404 → path wrong OR invisible to the token · 401 → not authenticated
```

Only the 200 case is observed (against an 18.9.1-ee instance); the rest are inferred from GitLab's
documented tier gating. Treat 404 with care — GitLab returns it for a group the token cannot see as
well as for one that does not exist, so it is not proof the path is wrong.

Epics need a real group; a project in a personal namespace has none, so the probe is unavailable
there. **Assume Free in that case** and keep `--unlabel` mandatory — the cost of being wrong that
way is a redundant flag, and the cost of the other way is cards in two columns. Do not substitute
`/api/v4/version` — `"enterprise": true` reports the EE *package*, not a paid subscription, and
reading it as a tier signal is wrong.

## GitLab boards are label views, not a status field

A board column is backed by a label, so moving a card means *swapping the label*. Never create a
board list to move a card: that reports success, adds an unwanted column, and leaves the card
exactly where it was. Board lists are created once, at setup; day-to-day work only touches labels.

**Scoped labels (`key::value`) require Premium or Ultimate.** On Premium and above, adding
`status::in-progress` makes GitLab drop the sibling `status::to-do` server-side. On **Free**, colons
carry no meaning — nothing enforces exclusion, so every move must remove the old label explicitly
and a missed `--unlabel` leaves the card in two columns at once. Keep `--unlabel` in every command:
mandatory on Free, belt-and-braces on Premium.

Confirm `--label` / `--unlabel` against `glab issue update --help` on your version; flag names drift
across major releases.

A label swap moves the card between columns and says nothing about where it lands inside one. See
*A column is a queue, so its order is a claim* for the position, which is a separate write.

## GitHub does not work the same way

GitHub has **no scoped labels and no label-based mutual exclusion**. Do not port the `status::`
convention across.

- **Issues** carry labels, assignees, and milestones, and are open or closed.
- A **board** is a Projects v2 board, where status is a project *field*, not a label — a separate
  API from Issues.

A card move on GitHub is three steps, not one:

1. `gh project item-add` — once, to make the issue a project item. An issue that was never added
   has no field to set, so editing it does nothing.

   **Create and add in the same breath.** An issue created with `gh issue create` is *not* a project
   item, so it has no Status and is **invisible in any kanban grouped by Status** — present in the issue
   list, absent from the board. Nothing catches it: a board reader cannot see a card that is not on the
   board, so a grooming scan reports the board clean while the card sits outside it. Observed
   2026-08-14, on two cards created by hand and found only when a later ranking run counted ten issues
   against eight board items.

   Read Status back after adding rather than assuming it is empty. On a project with an
   add-to-project workflow enabled, `item-add` lands the card in the workflow's column — observed as
   `Todo` on `pmvanev/phil-claude-plugin` — so "newly added therefore unset" is not safe either way.
2. `gh project item-list` and `gh project field-list` — to resolve the item and field IDs.
3. `gh project item-edit` — which in practice wants node IDs (`--id`, `--field-id`,
   `--project-id`).

`gh auth login`'s default scopes **omit** `project`. Add it only if a board is actually needed:
`gh auth refresh -s project`. If `gh` is authenticated from `GH_TOKEN` or `GITHUB_TOKEN`, `refresh`
is unavailable — reissue the token with the scope instead. Check with `gh auth status`.

If a project needs a list rather than a board, plain issues plus open/closed is enough, and it works
with a repository-scoped token — which a Projects v2 board cannot, because projects are
owner-scoped.

## A column is a queue, so its order is a claim

Read top to bottom, a column says what to pick up next. Neither forge decides that for you, and the
two cases fail differently. A **plain issue list** is a reverse-chronological feed — `glab issue
list` defaults to `created_at` descending, per `--help` on 1.112.0 — which is a record of when work
was filed, not of when it will be done. A **board column** has a real position, and it stays unset
until someone writes one. Unset still renders in some order, and that order is indistinguishable
from one a person chose.

**Where the work has a known order — a plan, a dependency chain, a release — write that order into
the board.** Where it has none, rank it anyway, by what unblocks the most work, and record the basis
where the column's readers already look: the description of the parent or tracking issue, under a
fixed heading, as with `## Chain` below. A stated guess gets corrected; an unstated one gets
followed.

| | Position is | Set with | Read back with |
|---|---|---|---|
| GitLab board | the issue's `relative_position` | `issueMoveList` (GraphQL) | `glab issue list --order relative_position --sort asc --label <column>` |
| GitHub Projects v2 | the item's position in the project | `updateProjectV2ItemPosition` (GraphQL) | `gh api graphql`, per *Verify the end state* |
| A plain issue list, either forge | nothing | — | — |

**Neither CLI exposes a way to set position, and the label swap this skill prescribes cannot set
one either.** *(Correction, 2026-08-12: the "GraphQL-only" claim that used to close this paragraph was
wrong for GitLab — see* A column is a queue *below and* GitLab reorders over REST *for what replaced
it.)* A `glab
issue update --label/--unlabel` move changes the column and leaves the card wherever the default
drops it — so on GitLab a deliberate move is two operations, not one. `glab issue` has no reorder
subcommand and `gh project item-edit` has no position flag (checked on `glab` 1.112.0 and `gh`
2.97.0) — but that does **not** make position GraphQL-only. It is on GitHub; on GitLab there is a
REST endpoint that works. GitHub's mutation:

```sh
gh api graphql -f query='mutation($p:ID!,$i:ID!,$a:ID){
  updateProjectV2ItemPosition(input:{projectId:$p,itemId:$i,afterId:$a}){clientMutationId}}' \
  -f p=<project-node-id> -f i=<item-node-id> -f a=<the item this one should land below>
```

### GitLab reorders over REST

**Use this, not GraphQL.** Exercised 2026-08-12 against a self-hosted 18.x Premium instance:

```sh
glab api --method PUT "projects/<id>/issues/<iid>/reorder" -f move_after_id=<issue id>
# or -f move_before_id=<issue id>
```

Three things the run established, each of which will otherwise cost an hour:

- **`move_after_id` and `move_before_id` name the *other* issue's destination, not the subject's.**
  `move_after_id=X` means "place X **after** the issue in the path" — so the subject moves *ahead of*
  X. The natural reading is inverted, and the call succeeds either way.

  **This is the exact opposite of GitHub's convention.** In `updateProjectV2ItemPosition`, `afterId`
  is the item the subject lands *below*. Same word, opposite direction. Carrying a mental model
  across forges silently reverses your ordering.

  | | Parameter | Subject ends up |
  |---|---|---|
  | GitHub | `afterId: X` | **after** X |
  | GitLab | `move_after_id: X` | **before** X |

- **The IDs are global issue `id`s, not project `iid`s** — while the path takes the `iid`. Both
  numbers appear on the same object and mixing them yields `404 Issue Not Found`.
- **`relative_position` is not serialized in the REST response.** It read `null` on every issue
  before, during, and after a successful reorder, in both the single-issue GET and the list. A
  reorder that worked is indistinguishable from one that did nothing if you check that field — so
  **verify by reading the ordered list back**, never by reading `relative_position`.

An unset position also reads as `null`, which is the same warning as everywhere else in this
section: the order you see is indistinguishable from one somebody chose. On the instance tested, all
39 open issues had `null` — nothing had ever been positioned.

GitLab's GraphQL `issueMoveList` carries `moveBeforeId`, `moveAfterId`, and `positionInList` alongside
`fromListId` and `toListId`, so there a move between columns and a move within one are the same
mutation. It has no one-liner here because it needs a `boardId` and both list IDs resolved first.

Two behaviors come from the schemas' own description fields, and both are the kind that reads as a
no-op and is not: `afterId` **omitted or null moves the item to the top**, and `positionInList` is
0-based with `-1` meaning the end of the list. The `afterId`-omitted behavior is **confirmed by a run**
(GitHub, `gh` 2.97.0) — it moved a card from last to first. `positionInList` is still description-only.

**`afterId` set to an item id is also confirmed by a run** (GitHub, `gh` 2.97.0, 2026-08-14): it places
the subject *immediately after* the named item, and the read-back matched the intended sequence exactly.
Worth knowing what that buys under a two-level scheme, because it is more than it looks: **within-goal
order is board position restricted to that goal's members**, so a single well-chosen move can correct one
goal's internal order while leaving every other goal's untouched. Ranking ten issues across three goals
took one mutation.

**Sub-issue order is a separate order** from any column's. Repositioning it is a third mutation —
`reprioritizeSubIssue(issueId, subIssueId, afterId | beforeId)` — and setting a card's board
position leaves the parent's list untouched.

**Confirmed by a run**: `--add-sub-issue 11,10,12` produced the parent list `12, 10, 11` — not call
order, not creation order, not the column's order. Both `beforeId` and `afterId` anchoring then fixed
it on the first attempt. Set the sub-issue order explicitly whenever it matters; nothing you have
already done will have set it for you.

All three signatures here were read from live schemas — GitHub's, and an 18.9.1-ee instance, the
latter out of the schema dump described under *`glab api graphql` answers introspection with the whole
schema*. Exercise status, as of 2026-08-12:

| Mutation | Exercised? |
|---|---|
| `updateProjectV2ItemPosition`, `afterId` omitted → top | **yes** — `gh` 2.97.0 |
| `updateProjectV2ItemPosition`, `afterId` → a specific sibling | **yes** |
| `reprioritizeSubIssue`, `beforeId` and `afterId` | **yes**, both forms |
| GitLab REST `PUT …/issues/:iid/reorder` | **yes** — 18.x Premium, both directions, repeatable |
| GitLab GraphQL `issueMoveList` | **no** — still schema-only, and superseded by the REST call above |

Every form above landed correctly on the first attempt. Read the introspection section before running
a query of your own.

**Write the order top-down in one pass.** Each call anchors to a neighbor, so anchoring to a card
you have not placed yet shifts everything after it — successfully, and with no output that says so.
That failure mode is reasoned from the mutations' shape, not observed: read the column back and
compare it against the intended sequence, per *Verify the end state*.

A GitHub view with a sort configured orders by that field, which leaves a hand-set position
invisible on that view *(unverified — check the view's sort and the position it may be hiding before
trusting either)*. On GitLab, `glab issue list --order` also offers field-derived orders —
`priority`, `label_priority`, `weight`, `milestone_due`, `due_date`, among them — which keep working
as new issues arrive, where a hand-set position does not. Which of those fields your tier populates
is a tier question; see *Find the tier before choosing a convention*.

Without a board there is no position to set. Carry the order in a checklist in one tracking issue,
and say which one is authoritative.

### A milestone is a goal, and its due date is the only order that survives

**A goal is not a story, and the discriminator is what each can hold: a goal holds *cards*; a story
holds *feature directories*.** A goal is this milestone slot — a due date, unrelated work grouped by
design, an ordering that survives new cards arriving. A story is itself **a card** and can never hold
another; it groups several nWave features *inside* one issue (`phil:nwave-issue-board`). Positionally:
a list of issues is a goal, the inside of one issue is a story. Both group several features and they are
not alternatives — milestones do not nest, and neither replaces the other.

**One issue carries at most one milestone.** Verified on `glab` 1.112.0 (*"Set to `""` or 0 to
unassign"*) and `gh` 2.97.0 (`--milestone` singular, plus `--remove-milestone`). That slot is spent
once, so what it means is a real decision — and the decision is: **a milestone is a goal**, on both
forges alike.

That buys the one thing hand-set position cannot give: an order that **survives new issues arriving**.

| Level | Ordered by | Survives new arrivals? |
|---|---|---|
| Between goals | milestone **due date** (`--due-date`, ISO 8601, on both CLIs) | **yes** |
| Within a goal | hand-set position | no — needs a re-rank, but only inside one goal |

A new issue then needs a goal (coarse, cheap) and a position inside it, instead of a re-cut of one
flat total order across the whole backlog.

**Why a goal and not a feature.** Grouping issues by feature is the obvious alternative and it is the
wrong trade. On GitHub, native sub-issues already give a feature its roster and its rollup, so the
slot buys nothing. On GitLab it does buy a roster — but at the price of the only durable cross-issue
ordering the forge offers, and a stale roster is a smaller problem than an unrankable backlog.

**Same meaning on both forges.** A milestone that means "goal" on one and "feature" on the other is a
word that has to be re-explained at every boundary, in a skill already carrying two forges'
conventions. Accept the redundancy on GitHub rather than the divergence.

Three limits worth stating before anyone builds on it:

- **Milestones do not nest.** One level of goal, and no sub-goals.
- **A milestone gives no order *within* itself.** It groups; ranking inside a goal is still position.
- **Not Premium-gated** — verified against a self-hosted 18.x instance, which is what makes this
  usable on Free where epics are not.

## Link what the forge cannot resolve

An issue is read on its own page, away from the repo and away from you. Every reference a reader
might need to follow — a file, an ADR, a sibling issue — should be traversable by clicking. Two
rules, and they pull in opposite directions.

**Do not wrap what the forge already autolinks.** A bare `#12` becomes a live reference carrying the
issue's title and state — on GitHub, as a hovercard on the rendered link. `[#12](https://…/issues/12)`
renders as an ordinary link with none of that, and adds a URL to maintain. Leave these bare:

| | Autolinked without markdown |
|---|---|
| Both | `#12`, `@user`, commit SHAs |
| GitHub also | `owner/repo#12` |
| GitLab also | `group/project#12`, `!34` (MR), `%2` (milestone), `~label` |

A forge autolinks an issue reference **only when the issue exists**, which makes a read-back a
free wrong-number check — verified on GitHub (`#3` renders an href, `#999` stays plain text), and
on GitLab only in the negative direction, where a reference to a non-existent issue stayed plain.
It works only against *rendered* output. `gh issue view --json body` returns
the raw markdown, where `#12` is literal text whether or not it resolves, so checking there proves
nothing either way. Render it:

```sh
gh api -X POST /markdown -f mode=gfm -f context=<owner>/<repo> \
  -f text="$(gh issue view 12 -R <owner>/<repo> --json body -q .body)"
# GitLab: POST /api/v4/markdown with gfm=true and project=<group/project>
```

Plain text means the number is wrong **or** you cannot read the target — a confidential issue or a
private project renders identically. GitHub shares one number space between issues and pull
requests, so `#12` may resolve to a PR.

**Write an absolute URL for everything else.** Relative paths are the trap, because the two forges
disagree and both render a link either way:

| `[adr](docs/adr/016.md)` in an issue body | Result |
|---|---|
| GitLab | expands to `<host>/<project>/-/blob/<default-branch>/docs/adr/016.md` |
| GitHub | emitted verbatim, resolved against the *issue* URL → **404** |

Verified by rendering the same body through both forges' markdown APIs (`POST /markdown`). A
leading slash does not save it: GitLab resolves `/docs/…` identically, GitHub emits it verbatim and
it resolves to `github.com/docs/…`. Absolute URLs work on both — write those and the question never
comes up.

- **Docs and ADRs** — link at the default branch, so the reader gets current content:
  `https://<host>/<owner>/<repo>/blob/<default-branch>/docs/adr/ADR-016.md` on GitHub,
  `https://<host>/<project>/-/blob/<default-branch>/…` on GitLab. Note the `/-/` — GitLab needs it,
  GitHub has no such segment.
- **A specific line of code** — use a commit-SHA permalink, never a branch. A line anchor against a
  moving branch drifts onto unrelated code and stays plausible while doing it. Anchor syntax
  differs: GitHub `#L40-L52`, GitLab `#L40-52` *(GitLab form unverified — confirm by clicking a line
  number on any file in your instance; GitLab writes the anchor into the address bar)*.
- **Confirm the path is pushed** before linking it. A file that exists only in your working tree
  produces a link that renders correctly, passes your read-back, and 404s for every other reader.
  Resolve it against the branch you are linking, not your checkout:
  `git ls-tree origin/<default-branch> -- <path>` prints nothing if the file is not there.

On GitHub only, a repository can map a prefix to a URL template, so every bare `ADR-016` becomes a
link — including ones a human types, with no markdown:

```sh
gh api --method POST repos/<owner>/<repo>/autolinks \
  -f key_prefix='ADR-' -f url_template='https://…/docs/adr/ADR-<num>.md'
```

The same path without `--method POST` lists what is already configured. It needs admin, is
configured per repository, and has no GitLab equivalent, so treat it as a bonus on top of writing
real links, never as the mechanism you rely on.

## Dependencies depend on the tier

- **GitLab Premium and above**: real link types — `blocks`, `is_blocked_by` — enforced by GitLab
  and rendered with backlinks on both sides. Prefer these. Created via
  `glab api --method POST "projects/<id>/issues/<iid>/links" -f target_project_id=<id> -f target_issue_iid=<iid> -f link_type=blocks`
  *(command form unverified — check whether your `glab` exposes a subcommand for this).*
- **GitLab Free**: only `relates_to` is available; `blocks` and `is_blocked_by` are Premium and
  above. Use `relates_to` and carry the direction in a `Blocked by #N` line in the description.
- **GitHub**: native `blocked by` / `blocking` links and sub-issues, exposed as first-class flags.
  These are recent — older guidance says GitHub has none, so check `gh --version` before believing
  it. Verified on `gh` 2.97.0:

  ```sh
  gh issue edit 123 -R owner/repo --add-blocked-by 200 --add-blocking 300,301
  gh issue edit 100 -R owner/repo --add-sub-issue 123,124   # or: --parent 100 on the child
  gh issue edit 100 -R owner/repo --remove-sub-issue 123    # or: --remove-parent on the child
  ```

  **The edge can be removed as well as added** — `--remove-sub-issue` / `--remove-parent`, and GraphQL
  `removeSubIssue`. Verified on `gh` 2.97.0, 2026-08-14. This matters because *removing* the edge is the only
  way to stop a child counting toward its parent's completion; see the next section.

  Each flag takes an issue number or a URL, so links cross repositories. It is one edge read from
  both ends — `blockedBy` and `blocking` are both fields on `Issue` in GraphQL — so the reverse side
  needs no second write.

## A parent's "N of M done" counts different things on each forge

Both forges render a completion count on a parent issue, and the two are backed by unrelated
mechanisms. Reading the wrong field returns a real number that counts something else — the
characteristic failure of this whole area, since nothing errors.

**GitHub carries two independent rollups on one issue.** Sub-issues are real issues, so the children
are also cards; the parent's bar comes from `subIssuesSummary`. A markdown task list that references
issues is counted separately, by `trackedIssues`. The two do not fall back to each other.

```sh
gh api graphql -f query='query{ repository(owner:"<o>",name:"<r>"){ issue(number:9){
  subIssuesSummary{ total completed percentCompleted }
  trackedIssues(first:1){ totalCount } } } }'
```

Verified on `gh` 2.97.0, 2026-08-12: a parent with three open sub-issues and no checkboxes in its
body returned `{total: 3, completed: 0, percentCompleted: 0}` alongside `trackedIssues.totalCount: 0`.

**`completed` counts CLOSED children, and closing one is what increments it.** Measured 2026-08-14 on a live
parent: adding an open child gave `{1, 0, 0}`, **closing that child** gave `{1, 1, 100}`, and **removing the
edge** gave `{0, 0, 0}`. Two consequences worth having before you rely on the number:

- **A child closed for any reason counts as completed.** A won't-build close and a shipped close are the same
  value here. Observed on `pmvanev/phil-claude-plugin`: parent #9 reads `3/3 · 100%` while one of its three
  children was deliberately **not** built and closed anyway. The counter is doing what it documents; the
  difference survives only in prose elsewhere.
- **To stop a child counting, remove the edge — closing it does the opposite.** Anything that consolidates
  children into a parent must un-parent before closing, or it renders the parent complete while the work
  continues.
What the issue page renders when *both* counters are non-zero is unverified — check it before relying
on either to be the one displayed.

**GitLab's stable *parent-issue* rollup counts checkboxes, not issues.**

| Mechanism | Field | Children are | Status |
|---|---|---|---|
| Checklist | `taskCompletionStatus {count, completedCount}`; REST `task_completion_status {count, completed_count}` | markdown `- [ ]` in the description | Free, stable — **verified** |
| Child work items | `WorkItemWidgetHierarchy.rolledUpCountsByType` → `countsByState {all, opened, closed}` | real issues and tasks | **Experiment**, added 17.3 — 18.9.1-ee schema only, not run |
| Milestone | `MilestoneStats {closedIssuesCount, totalIssuesCount}` | real issues | Free, stable |

`task_completion_status` needs no widget and no tier, and appeared on every issue observed in the
REST payload — which makes it the one to reach for:

```sh
glab api "projects/<id>/issues/<iid>" | jq .task_completion_status   # {"count":6,"completed_count":1}
```

Verified against an 18.9.1-ee instance by parsing checkboxes out of raw descriptions and comparing:
counts matched on twelve issues, including partials (`1/6`, `2/6`) and complete (`5/5`).

**`WorkItemWidgetProgress` is not this.** Despite the name it carries
`startValue` / `currentValue` / `endValue` / `progress` for OKR key results — a manually set
percentage, not a count of finished children. It answers, and the answer is unrelated.

The asymmetry decides the design: **GitHub's parent rollup counts things that are cards; GitLab's
stable parent rollup counts things that are not.** A GitLab parent whose children must also cross
board columns has no project-scoped, non-experimental count of them.

A milestone is the one GitLab rollup that is both stable and counts real issues, so grouping those
children under one *would* buy the count — but **do not**. The milestone slot is singular and is
spent on the goal (see *A milestone is a goal*), and trading the backlog's only durable ordering for
a progress bar is a bad exchange. Accept that GitLab has no reliable feature-level count, and read
the children's live states instead of a summed one.

**Reopening restores the issue and not the field.** `gh issue reopen` puts an issue back to OPEN and leaves
Status wherever the close left it — so a card reopened out of Done sits **OPEN inside Done**, and no board view
groups on that combination or flags it. Setting the field back is a separate `gh project item-edit`, and a
command that holds no such verb can only hand the call over. The asymmetry is the same one the paragraph above
describes from the other direction: **the two facts are coupled on the way in and independent on the way out.**

Check for it after any reopen — an open issue sitting in Done, or a closed one outside it, is always a defect,
and the single board read that lists items with their Status already returns both halves.

## Leave a chain when you pivot

Recognizing a blocker mid-work and switching to it — whether the blocker already existed or you
just created it — is the moment the reasoning exists only in your head. Write both ends **before**
starting work on the blocker, not after you finish it.

Put it under a fixed `## Chain` heading in each issue's **description**. Descriptions are what a
reader sees on landing; a comment scrolls away and has to be hunted for.

In #12's description:

```markdown
## Chain

Blocked by #47 — token refresh must land first or the retry test can't be written
```

And the mirror, in #47's: `Blocks #12 — split out of it on 2026-08-10`.

The forge records the edge; the clause after the dash records why you stopped. Six issues deep, the
edge alone tells you what blocked but not what you were in the middle of.

**The clause is composed, so compose it against `${CLAUDE_PLUGIN_ROOT}/rules/writing.md`.** The edge is
rendered by the forge and there is nothing to compose in a link; the clause is the only part a person
writes, and it is the only part a reader six issues deep depends on. Facts first, active voice, no
expletive construction, the emphatic word last. **The standard is eleven principles of composition and concision is one
of them** — read this as *compose it well*, never as *compose it short*.

**A clause that restates the edge fails.** `Blocked by #47 — blocked by issue 47` satisfies the shape and
carries nothing the link did not. Pinned by `self-test/01-chain-clause-composed/`.

**Judging is taste; generating is not.** This licenses nothing about chain lines somebody else wrote —
it governs the one you are about to write.

Where the forge writes the reverse edge for you — GitHub, and GitLab Premium — it writes only the
edge, never the reason, so the prose line goes on both issues either way. See *Dependencies depend
on the tier* above for what each forge gives you.

Do not hand-maintain the chain as blockers close. The linked issue is authoritative about its own
state and is one click away, so editing #12 to say #47 closed just creates a second copy that can
go stale. Bare references carry title and state, as above; this is the second reason to leave them
bare — a live reference exposes a closed issue at the link, a hand-written markdown link does not.

## Bulk seeding needs two passes

Issue numbers are assigned **at creation**, so a set of issues that reference each other cannot be
written correctly in one pass. Create every issue first, record the resulting numbers, then write
the cross-references in a second pass. Assuming "the third issue will be #3" breaks the moment the
project already has issues.

This matters only for one-time seeding. Day-to-day work touches one issue at a time.

## Self-hosted certificates

Two failure modes look alike and are not:

- **Unknown certificate authority** — import the CA into the OS trust store. `glab` and `gh` are Go
  binaries and read it. This is the fix:
  `sudo cp ca.pem /usr/local/share/ca-certificates/gitlab.crt && sudo update-ca-certificates`
- **Expired certificate** — no CA import helps. Renew it. There is no safe workaround.

Disabling verification is not a fallback an agent may choose. It exposes an `api`-scope token to
anyone on the network path, and a private-IP instance on a shared or home network is exactly where
that matters. If the developer decides to accept that risk, it is scoped to the single host
(`glab config set skip_tls_verify true --host <host>` — confirm the flag against your `glab`
version), it is temporary, and it must be stated out loud in the transcript every time it is used.

An expired certificate is a defect to fix, not a setting to work around.

## `glab`'s JSON flag differs per subcommand — check before you type it

**There is no blanket rule.** This section asserted one until 2026-08-17 (*"the JSON flag is `-O`, and
`-F` fails silently"*), and it was right about exactly one of the three subcommands below.

| Subcommand | JSON flag | What the other flag does there |
|---|---|---|
| `glab issue list` | **`-O` / `--output`** `json` | `-F` is `--output-format`, taking `details\|ids\|urls` |
| `glab repo view` | **`-F` / `--output`** `json` | `-O` **does not exist** |
| `glab api` | **none** — prints JSON natively | `-O` is **rejected**: `Unknown shorthand flag: 'O' in -O` |

```sh
glab issue list -R <group/project> --output json --per-page 100   # correct
glab issue list -R <group/project> -F json                       # silently returns a table
glab repo view <group/project> -F json                           # correct — -O is not a flag here
glab api projects/<url-encoded-path>                             # correct — no output flag at all
```

**On `issue list`, `-F json` does not error**: it returns the human-readable table. A caller that
parses the result finds no JSON and concludes the issues have no bodies, or that the list is empty.
That is the characteristic shape of every trap in this file — a wrong guess that reports success.

**Verified against `glab --help`, not from memory**, which is how the blanket rule was caught. It was
found by `phil:board-setup`'s GitLab adapter, whose first call — `glab api … -O json` — failed
outright, and even then only became visible after the refusal message was made informative: the code
had been reporting `failed: ERROR`, because `glab` prints a bare `ERROR` banner before the real
message. **A refusal whose reason is uninformative hides the defect that caused it.**

The lesson generalises past `glab`: a flag verified on one subcommand is evidence about that
subcommand. This entry lived in `phil:groom-issues` until 2026-08-14 — a forge mechanic in a skill
whose charter says it owns none — and being moved here did not make it correct.

Checked by `tests/test_gitlab_probe.py::test_the_json_flag_is_correct_per_subcommand_not_blanket`,
which is the fixture this fold-back required: without it the next author re-derives the blanket rule
from the one subcommand where it holds.

## `glab api graphql` answers introspection with the whole schema

This skill sends readers to live schemas to confirm mutation signatures. On `glab` 1.112.0, that
route has a trap: **any query containing `__type` or `__schema` is discarded and answered with a full
schema dump** — 7.4 MB against an 18.9.1-ee instance. The response is valid JSON with a `data` key,
so it looks like a success; only `data.__type` is missing, and a naive parse raises a `KeyError`
rather than reporting what happened.

Verified on 1.112.0 — the discriminator is introspection, not syntax:

| Query | Result |
|---|---|
| `--raw-field query='{currentUser{username}}'` | correct response |
| `--raw-field query='query{currentUser{username}}'` | correct response |
| `--raw-field query='{__type(name:"Issue"){name}}'` | full schema dump |
| `--raw-field query='query{__type(name:"Issue"){name}}'` | full schema dump |
| `--raw-field query='query Foo{__type(name:"Issue"){name}}'` | full schema dump |

Ordinary queries pass through untouched, so this affects schema reading only. Two neighboring forms
fail differently and are not workarounds: `--input <file>` with a `{"query": "..."}` body arrives as
an empty document (`Unexpected end of document`), and `-f query=@<file>` sends the literal string
`@<file>` rather than reading it.

**Capture the dump once and query it locally** — `jq`, or a few lines of Python over
`data.__schema.types` — rather than fighting the flag. It contains every type, so one dump answers
every later question. Write it to a scratch path, never into the repository: it is megabytes of
generated content that dates the moment the instance is upgraded. Going around `glab` with `curl`
needs the instance's CA and its own token handling, and on an IP-addressed instance the certificate
may carry no matching SAN.

## A status write can close the issue underneath you

GitHub Projects v2 ships built-in workflows, and one of them — commonly enabled — **closes the issue
when Status is set to Done**. So `gh project item-edit --single-select-option-id <Done>` is not only a
field write; on such a board it is also `gh issue close`, with no output saying so.

The damage is to whatever you queued next. Observed 2026-08-12: setting an item to Done, then running
`gh issue close <n> -c "<closing note>"`, produced `! Issue #<n> is already closed` — and **the
comment was silently discarded**. The exit path reports the state you wanted, so nothing looks wrong;
the note simply never posted.

Two consequences worth holding:

- **Order the two operations comment-first.** Post the closing comment, *then* set Status. The reverse
  loses the comment on any board with the workflow enabled, and you cannot tell from the board which
  kind you are on until it bites.
- **A status write is not reversible by another status write.** Moving Done → Todo does not reopen the
  issue. Reopen it explicitly with `gh issue reopen`.

The same class applies to the mirror workflow (*item closed → Status: Done*), which makes
`gh issue close` a board write. Neither is discoverable from `--help`, and neither is visible in the
project's field schema — check the project's workflow settings, or infer it the way this was found.

## Verify the end state

If the instance is reachable only over a VPN or a home network, expect connection-level failures; a
single failed call is usually the network, not the tool, so retry before concluding anything is
broken. Regardless of link quality, a multi-step operation can fail partway and leave a board
half-updated.

Read back what was written. `glab issue list` and `gh issue list` are cheap, and a board operation
that reports success while placing a card in the wrong column is the characteristic failure here.

**GitHub Projects v2 reads lag writes.** Three consequences, learned the hard way:

- `gh project item-add` exits **0 with no output** whether or not the item landed. The exit code is
  not evidence.
- `gh project list` and `gh project item-list` can under-report — an empty result is not proof of an
  empty board. Treat `gh api graphql` as the source of truth, and **pause and re-read** before
  concluding a write failed. Adding the same issue twice is idempotent, so a retry is safe.
- **Check for an existing project before creating one**, and do not trust a single empty
  `gh project list` to tell you there isn't one. This is exactly how a duplicate board gets built
  alongside the real one.

## One system of record per scope

Do not sync a local task file and a forge board — two authorities over the same item generate
conflicts nobody has designed a resolution for. If both exist, partition by scope: local files own
in-flight detail, the forge owns what other people see, and the local task records the issue number
as the only join. Nothing duplicated means nothing can drift.

## Choosing what becomes an issue

Ask what moves. A board earns its keep when cards cross columns; an issue that sits in one column
for weeks is a status page with extra steps.

Default to **one issue per thing that can be demonstrated on its own**, and split further only when
two halves would sit in different columns at the same time. When the right split is not obvious,
ask rather than guess — the cost of asking is one question, and the cost of guessing is a backlog
someone has to re-cut by hand.

**Read the split clause as being about concurrency, because that is what it means.** Two halves sit in
different columns at the same time only when two people are working them at once. So a decomposition
nobody works in parallel — however cleanly it divides — is *one* issue with the parts written inside it,
and splitting it produces cards only their author can pick up. Ask who would hold each half; if the answer
is the same person, it is one card.

An **nWave** project answers this question for you, because its artifacts already name the units —
feature, slice, step. Use `phil:nwave-issue-board` for that mapping. Everywhere else, use the rule
above.

## Per-project setup

Instance-specific constants belong in the project's `CLAUDE.md`, not in this skill. Record only what
cannot be discovered:

```markdown
## Issue board

- Forge: GitLab at <host> (or GitHub) — use `glab -R <group/project>` (or `gh -R <owner/repo>`)
- Project ID <id>, board ID <id>
- Tier: Premium (scoped labels swap server-side; real `blocks` links) | Free (swap manually with
  `--unlabel`; `relates_to` only)
- Status lives in `status::` labels — swap, never add a board list
- Column families: `<name>` (e.g. the nWave waves) + `<name>` (e.g. to do · in progress · blocked ·
  done). **One board's status field holds one enum**, so two families share it and every card sorts
  against all of them. Record how many options the field has before adding any — a field going from 3 to
  11 re-sorts every existing card.
- Label families: `<name>` single-valued — swap, never add · `<a>` + `<b>` multi-valued by decision.
  Nothing on a forge records this, so grooming reports the rule **unevaluated** for any family not
  listed here. `wave: *` needs no entry — `phil:nwave-issue-board` declares it single-valued for
  every nWave repo.
- (Projects v2) Built-in workflows enabled: <none | auto-close on Done | auto-Done on close> —
  a status write is also an issue write when one is on; comment before setting Status
- Docs root for links: `https://<host>/<project>/-/blob/<default-branch>/docs/` — `ADR-016` → `<docs root>adr/ADR-016.md`
- (nWave) see `phil:nwave-issue-board` for the artifact → issue mapping
- (optional) <local task system> owns in-flight work; issues own the outward-facing tier
```

---

## Self-test

`skills/issue-board/self-test/` — **created 2026-09-04**; this was the only board-family skill without a
suite while five siblings carried 30, 43, 18, 13 and 10 fixtures.

Fixture 01 pins the chain clause: both ends written, under the fixed heading, in the description, before
work starts on the blocker, with the clause carrying what the edge cannot. It supplies **no candidate
text** — composing the clause is the act under test, and a fixture offering two variants would test
selection instead.

**The outcome vocabulary grows with the suite.** One outcome, `CHAIN-COMPOSED`, because there is one
fixture. Shipping a vocabulary ahead of its fixtures asserts coverage that does not exist.

`tests/test_issue_board_fixtures.py` checks what is automatable — every fixture well-formed, every
`expected_decision` naming exactly one defined outcome, every defined outcome carrying a fixture. It does
not judge whether a run reached the right decision, and says so. Drive the fixtures by hand per
`self-test/README.md` whenever this file changes, and whenever `phil:nwave-issue-board` or
`phil:nwave-slice-status` changes, since both build on these mechanics.
