---
name: issue-board
description: Use when driving a GitLab or GitHub issue tracker or board from the command line with `glab` or `gh` — moving a card between board columns, reordering a column or prioritizing a backlog so the top card is what to work on next, ordering sub-issues under a parent, reading which issues are sub-issues of which, setting a status label or a Projects v2 Status field, reading a parent issue's completed-children count or progress bar, deciding whether a piece of work is one issue or several, hyperlinking or cross-linking references in an issue body to a file, an ADR, or another issue, marking an issue blocked by another and recording why, weighing whether to sync a local task file with a board, reading a forge's GraphQL schema to confirm a mutation's signature, or connecting to a self-hosted GitLab instance. Covers the semantics `--help` does not, where a wrong guess reports success.
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
*A column is a queue, so its order is a claim*, in `references/ordering.md`, for the position, which is a separate write.

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
   item, so it has no Status and is **invisible in any kanban grouped by Status**, and a grooming scan
   reports the board clean while the card sits outside it. Wound: two hand-made cards, found only when a
   ranking run counted ten issues against eight board items (2026-08-14).

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

## Position, sub-issue order and milestones

**Before reordering a column, ranking a backlog, reading which card is next, or setting a sub-issue
order or a milestone, read `references/ordering.md` whole.** It holds both forges' position calls, whose anchor parameters point
in opposite directions, and why a milestone is a goal.

## Links and dependencies

**Before writing a link into an issue body, read `references/links.md` whole.** A relative path renders
on both forges and 404s on GitHub.

**Before writing or reading a blocking link or a sub-issue edge, reading a parent's completion count,
or closing an issue that has a parent — setting Done included — read `references/hierarchy.md`
whole.** Each forge offers different link types per tier and counts a parent's children differently,
and a closed child counts as completed whatever the reason it closed.

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

**Compose the clause against `${CLAUDE_PLUGIN_ROOT}/rules/writing.md`.** The forge renders the edge;
the clause is the only part a person writes, and the only part a reader six issues deep depends on.
Facts first, active voice, no expletive construction, the emphatic word last — *compose it well*, never
*compose it short*.

**A clause that restates the edge fails.** `Blocked by #47 — blocked by issue 47` satisfies the shape and
carries nothing the link did not. Pinned by `self-test/01-chain-clause-composed/`.

**Judging is taste; generating is not.** This licenses nothing about chain lines somebody else wrote —
it governs the one you are about to write.

Where the forge writes the reverse edge for you — GitHub, and GitLab Premium — it writes only the
edge, never the reason, so the prose line goes on both issues either way. See *Dependencies depend
on the tier*, in `references/hierarchy.md`, for what each forge gives you.

Do not hand-maintain the chain as blockers close. The linked issue is authoritative about its own
state and is one click away, so editing #12 to say #47 closed just creates a second copy that can
go stale. Bare references carry title and state, as `references/links.md` shows; this is the second reason to leave them
bare — a live reference exposes a closed issue at the link, a hand-written markdown link does not.

## Bulk seeding needs two passes

Issue numbers are assigned **at creation**, so a set of issues that reference each other cannot be
written correctly in one pass. Create every issue first, record the resulting numbers, then write
the cross-references in a second pass. Assuming "the third issue will be #3" breaks the moment the
project already has issues.

This matters only for one-time seeding. Day-to-day work touches one issue at a time.

## `glab` and self-hosted instances

**Before asking any `glab` command for JSON, reporting a `glab` error, reading a GitLab schema, or
connecting to a self-hosted instance — and on any certificate error from either CLI — read
`references/gitlab-cli.md` whole.** Its JSON flag differs per subcommand, introspection returns the whole
schema, and a certificate failure has two causes with different fixes.

## A status write can close the issue underneath you

GitHub Projects v2 ships built-in workflows, and one of them — commonly enabled — **closes the issue
when Status is set to Done**. So `gh project item-edit --single-select-option-id <Done>` is not only a
field write; on such a board it is also `gh issue close`, with no output saying so.

The damage is to whatever you queued next. Observed 2026-08-12: setting an item to Done, then running
`gh issue close <n> -c "<closing note>"`, produced `! Issue #<n> is already closed` — and **the
comment was silently discarded**. The exit path reports the state you wanted, so nothing
looks wrong.

Two consequences worth holding:

- **Order the two operations comment-first.** Post the closing comment, *then* set Status. The reverse
  loses the comment on any board with the workflow enabled, and you cannot tell from the board which
  kind you are on until it bites.
- **A status write is not reversible by another status write.** Moving Done → Todo does not reopen the
  issue. Reopen it explicitly with `gh issue reopen`.

The same class applies to the mirror workflow (*item closed → Status: Done*), which makes
`gh issue close` a board write. Neither is discoverable from `--help`, and neither is visible in the
project's field schema — check the project's workflow settings, or infer it the way this was found.

**Reopening restores the issue and not the field.** `gh issue reopen` puts an issue back to OPEN and leaves
Status wherever the close left it — so a card reopened out of Done sits **OPEN inside Done**, and no board view
groups on that combination or flags it. Setting the field back is a separate `gh project item-edit`, and a
command that holds no such verb can only hand the call over. The asymmetry is the same one this section
describes from the other direction: **the two facts are coupled on the way in and independent on the way out.**

Check for it after any reopen — an open issue sitting in Done, or a closed one outside it, is always a defect,
and the single board read that lists items with their Status already returns both halves.

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

`skills/issue-board/self-test/` holds the suite. Fixture 01 pins the chain clause: both ends written, under the fixed heading, in the description, before
work starts on the blocker, with the clause carrying what the edge cannot. It supplies **no candidate
text** — composing the clause is the act under test, and a fixture offering two variants would test
selection instead.

**Add an outcome only with the fixture that exercises it.** One fixture so far, so one outcome:
`CHAIN-COMPOSED`.

`tests/test_issue_board_fixtures.py` checks what is automatable — every fixture well-formed, every
`expected_decision` naming exactly one defined outcome, every defined outcome carrying a fixture. It does
not judge whether a run reached the right decision, and says so. Drive the fixtures by hand per
`self-test/README.md` whenever this file or its `references/` change, and whenever `phil:nwave-issue-board` or
`phil:nwave-slice-status` changes, since both build on these mechanics.
