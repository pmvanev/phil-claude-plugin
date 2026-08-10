---
name: issue-board
description: Use when driving a GitLab or GitHub issue tracker or board from the command line with `glab` or `gh` — creating or updating issues, moving a card between board columns, setting a status label or a Projects v2 Status field, grooming a forge backlog, cross-linking an issue to a file, an ADR, or another issue, recording a dependency chain when work pivots to a blocker, or connecting to a self-hosted GitLab instance. Covers the forge semantics `glab --help` and `gh --help` do not explain, where a wrong guess reports success.
---

# Driving GitLab and GitHub Issue Boards

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
glab api "groups/<group>/epics"   # 200 → Premium+ · 403 → Free · 404 → wrong group path · 401 → not authenticated
```

Epics need a real group; a project in a personal namespace has none, so the probe is unavailable
there. Do not substitute `/api/v4/version` — `"enterprise": true` reports the EE *package*, not a
paid subscription, and reading it as a tier signal is wrong.

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
renders as an ordinary link with none of that, and adds a URL to maintain. Leave bare: `#12` and
`owner/repo#12` on GitHub; `#12`, `group/project#12`, `!34` (MR), `%2` (milestone), `~label`,
`@user` on GitLab; commit SHAs on both.

Both forges autolink an issue reference **only when the issue exists**. A `#12` still rendering as
plain text after you post is the forge telling you the number is wrong — read the body back and use
it as a free correctness check. GitHub shares one number space between issues and pull requests, so
`#12` may resolve to a PR.

**Write an absolute URL for everything else.** Relative paths are the trap, because the two forges
disagree and both render a link either way:

| `[adr](docs/adr/016.md)` in an issue body | Result |
|---|---|
| GitLab | expands to `<host>/<project>/-/blob/<default-branch>/docs/adr/016.md` ✅ |
| GitHub | emitted verbatim, resolved against the *issue* URL → **404** |

Verified by rendering the same body through both forges' markdown APIs (`POST /markdown`). A
leading slash does not save it: GitLab resolves `/docs/…` identically, GitHub emits it verbatim and
it resolves to `github.com/docs/…`. Absolute URLs work on both — write those and the question never
comes up.

- **Docs and ADRs** — link at the default branch, so the reader gets current content:
  `https://<host>/<owner>/<repo>/blob/main/docs/adr/ADR-016.md` on GitHub,
  `https://<host>/<project>/-/blob/main/…` on GitLab. Note the `/-/` — GitLab needs it, GitHub has
  no such segment.
- **A specific line of code** — use a commit-SHA permalink, never a branch. A line anchor against a
  moving branch drifts onto unrelated code and stays plausible while doing it. Anchor syntax
  differs: GitHub `#L40-L52`, GitLab `#L40-52` *(GitLab form unverified — confirm on your
  instance)*.
- **Confirm the path is pushed** before linking it. A file that exists only in your working tree
  produces a link that renders correctly, passes your read-back, and 404s for every other reader.
  Resolve the path in the repo first, then check it is on the default branch.

On GitHub only, `gh api repos/<owner>/<repo>/autolinks` maps a prefix to a URL template, so every
bare `ADR-016` becomes a link — including ones a human types, with no markdown. It needs admin, is
configured per repository, and has no GitLab equivalent, so treat it as a bonus on top of writing
real links, never as the mechanism you rely on.

## Dependencies depend on the tier

- **GitLab Premium and above**: real link types — `blocks`, `is_blocked_by` — enforced by GitLab
  and rendered with backlinks on both sides. Prefer these. Created via
  `glab api --method POST "projects/<id>/issues/<iid>/links" -f target_project_id=<id> -f target_issue_iid=<iid> -f link_type=blocks`
  *(command form unverified — check whether your `glab` exposes a subcommand for this).*
- **GitLab Free**: only `relates_to` is available; `blocks` and `is_blocked_by` are Premium and
  above. Use `relates_to` and carry the direction in a `Blocked by #N` line in the description.
- **GitHub**: no native dependency links. Task lists and issue references in the body are the
  practical equivalent.

## Leave a chain when you pivot

Recognizing a blocker mid-work and switching to it — whether the blocker already existed or you
just created it — is the moment the reasoning exists only in your head. Write both ends **before**
starting work on the blocker, not after you finish it.

Under a fixed `## Chain` heading in each issue's **description**. Descriptions are what a reader
sees on landing; a comment scrolls away and has to be hunted for.

```
On #12:  Blocked by #47 — token refresh must land first or the retry test can't be written
On #47:  Blocks #12 — split out of it on 2026-08-10
```

The forge records the edge; the clause after the dash records why you stopped. Six issues deep, the
edge alone tells you what blocked but not what you were in the middle of.

Write both directions by hand unless GitLab Premium is writing them for you:

| Forge | Backlink written for you |
|---|---|
| GitLab Premium+ | Yes — `blocks` / `is_blocked_by` render on both issues. Add the prose line anyway; the link carries no reason. |
| GitLab Free | No — only `relates_to`, which carries no direction. |
| GitHub | No — a mention creates a cross-reference event on the target, but nothing states which way the dependency runs. |

Do not hand-maintain the chain as blockers close. The linked issue is authoritative about its own
state and is one click away, so editing #12 to say #47 closed just creates a second copy that can
go stale. This is the second reason to leave the reference bare: a live reference exposes that
state at the link, a hand-written markdown link does not.

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
- Docs root for links: `https://<host>/<project>/-/blob/main/docs/` — `ADR-016` → `<docs root>adr/ADR-016.md`
- (optional) <local task system> owns in-flight work; issues own the outward-facing tier
```
