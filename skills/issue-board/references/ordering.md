# Ordering a column, a parent's sub-issues and the backlog

Part of the `issue-board` skill. Read it before reordering a column, ranking a backlog, reading which card is next, or setting a sub-issue order or a milestone. Its `SKILL.md` governs this file too.

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
fixed heading, as with `## Chain` in `SKILL.md`. A stated guess gets corrected; an unstated one gets
followed.

| | Position is | Set with | Read back with |
|---|---|---|---|
| GitLab board | the issue's `relative_position` | `PUT …/issues/:iid/reorder` (REST), per *GitLab reorders over REST* | `glab issue list --order relative_position --sort asc --label <column>` |
| GitHub Projects v2 | the item's position in the project | `updateProjectV2ItemPosition` (GraphQL) | `gh api graphql`, per *Verify the end state* in `SKILL.md` |
| A plain issue list, either forge | nothing | — | — |

**Neither CLI exposes a way to set position, and the label swap this skill prescribes cannot set
one either.** A `glab issue update --label/--unlabel` move changes the column and leaves the card
wherever the default drops it, so on GitLab a deliberate move is two operations. `glab issue` has no
reorder subcommand and `gh project item-edit` has no position flag (`glab` 1.112.0, `gh` 2.97.0).
Position is GraphQL on GitHub; on GitLab use the REST reorder endpoint, though GraphQL `issueMoveList`
also exists. GitHub's mutation:

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
the subject *immediately after* the named item. **Within-goal order is board position restricted to that
goal's members** (see *A milestone is a goal*), so one well-chosen move corrects one goal's order and leaves the others untouched.

**Sub-issue order is a separate order** from any column's. Repositioning it is a third mutation —
`reprioritizeSubIssue(issueId, subIssueId, afterId | beforeId)` — and setting a card's board
position leaves the parent's list untouched.

**Confirmed by a run**: `--add-sub-issue 11,10,12` produced the parent list `12, 10, 11` — not call
order, not creation order, not the column's order. Both `beforeId` and `afterId` anchoring then fixed
it on the first attempt. Set the sub-issue order explicitly whenever it matters; nothing you have
already done will have set it for you.

All three signatures here were read from live schemas — GitHub's, and an 18.9.1-ee instance, the
latter out of the schema dump described in `references/gitlab-cli.md` under *`glab api graphql` answers introspection with the whole
schema*. Exercise status, as of 2026-08-12:

| Mutation | Exercised? |
|---|---|
| `updateProjectV2ItemPosition`, `afterId` omitted → top | **yes** — `gh` 2.97.0 |
| `updateProjectV2ItemPosition`, `afterId` → a specific sibling | **yes** |
| `reprioritizeSubIssue`, `beforeId` and `afterId` | **yes**, both forms |
| GitLab REST `PUT …/issues/:iid/reorder` | **yes** — 18.x Premium, both directions, repeatable |
| GitLab GraphQL `issueMoveList` | **no** — still schema-only, and superseded by the REST call above |

Every form above landed correctly on the first attempt. Read that introspection section before running
a query of your own.

**Write the order top-down in one pass.** Each call anchors to a neighbor, so anchoring to a card
you have not placed yet shifts everything after it — successfully, and with no output that says so.
That failure mode is reasoned from the mutations' shape, not observed: read the column back and
compare it against the intended sequence, per *Verify the end state* in `SKILL.md`.

A GitHub view with a sort configured orders by that field, which leaves a hand-set position
invisible on that view *(unverified — check the view's sort and the position it may be hiding before
trusting either)*. On GitLab, `glab issue list --order` also offers field-derived orders —
`priority`, `label_priority`, `weight`, `milestone_due`, `due_date`, among them — which keep working
as new issues arrive, where a hand-set position does not. Which of those fields your tier populates
is a tier question; see *Find the tier before choosing a convention* in `SKILL.md`.

Without a board there is no position to set. Carry the order in a checklist in one tracking issue,
and say which one is authoritative.

### A milestone is a goal, and its due date is the only order that survives

**A goal holds *cards*; a story holds *feature directories*.** A goal is this milestone slot — a due
date, unrelated work grouped by design, an ordering that survives new cards arriving. A story is itself
**a card** and never holds another; it groups several nWave features inside one issue
(`phil:nwave-issue-board`). A goal and a story are not alternatives; neither replaces the other.

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

**A goal, not a feature, because** on GitHub sub-issues already give a feature its roster; on GitLab a feature milestone would buy a roster at the price of the only durable
cross-issue ordering. One meaning on both forges beats re-explaining the word at every boundary.

Three limits worth stating before anyone builds on it:

- **Milestones do not nest.** One level of goal, and no sub-goals.
- **A milestone gives no order *within* itself.** It groups; ranking inside a goal is still position.
- **Not Premium-gated** — verified against a self-hosted 18.x instance, which is what makes this
  usable on Free where epics are not.
