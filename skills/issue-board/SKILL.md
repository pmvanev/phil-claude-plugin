---
name: issue-board
description: Use when driving a GitLab or GitHub issue tracker or board from the command line with `glab` or `gh` — moving a card between board columns, setting a status label or a Projects v2 Status field, deciding whether a piece of work is one issue or several, hyperlinking or cross-linking references in an issue body to a file, an ADR, or another issue, marking an issue blocked by another and recording why, weighing whether to sync a local task file with a board, or connecting to a self-hosted GitLab instance. Covers the semantics `--help` does not, where a wrong guess reports success.
---

# Driving GitLab and GitHub Issue Boards

Both forges are driven from the command line: `glab` for GitLab, `gh` for GitHub. Prefer the CLI
over an MCP server — the commands are auditable in the transcript, credentials stay in each tool's
own store, and no extra configuration is needed.

In an **nWave** repo, `phil:nwave-issue-board` maps features, slices, and steps onto the objects
below. This skill stays generic; that one holds the mapping.

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

## GitHub does not work the same way

GitHub has **no scoped labels and no label-based mutual exclusion**. Do not port the `status::`
convention across.

- **Issues** carry labels, assignees, and milestones, and are open or closed.
- A **board** is a Projects v2 board, where status is a project *field*, not a label — a separate
  API from Issues.

A card move on GitHub is three steps, not one:

1. `gh project item-add` — once, to make the issue a project item. An issue that was never added
   has no field to set, so editing it does nothing.
2. `gh project item-list` and `gh project field-list` — to resolve the item and field IDs.
3. `gh project item-edit` — which in practice wants node IDs (`--id`, `--field-id`,
   `--project-id`).

`gh auth login`'s default scopes **omit** `project`. Add it only if a board is actually needed:
`gh auth refresh -s project`. If `gh` is authenticated from `GH_TOKEN` or `GITHUB_TOKEN`, `refresh`
is unavailable — reissue the token with the scope instead. Check with `gh auth status`.

If a project needs a list rather than a board, plain issues plus open/closed is enough, and it works
with a repository-scoped token — which a Projects v2 board cannot, because projects are
owner-scoped.

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
  ```

  Each flag takes an issue number or a URL, so links cross repositories. It is one edge read from
  both ends — `blockedBy` and `blocking` are both fields on `Issue` in GraphQL — so the reverse side
  needs no second write.

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
- Docs root for links: `https://<host>/<project>/-/blob/<default-branch>/docs/` — `ADR-016` → `<docs root>adr/ADR-016.md`
- (nWave) see `phil:nwave-issue-board` for the artifact → issue mapping
- (optional) <local task system> owns in-flight work; issues own the outward-facing tier
```
