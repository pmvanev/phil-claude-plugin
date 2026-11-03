# WORKTREE — the card's worktree, or a card already underway

Part of the `start` skill; `../SKILL.md` governs this step as much as this file does. Read this file
whole before CHECK's step 4: that step needs *Find the card's worktrees*, and the rest follows CLAIM.

The session works the card in a worktree of its own, cut by Claude Code's worktree tool, `EnterWorktree`.
The developer typed `/phil:start`, which asks for that worktree: say so in the call's reasoning, because
the tool runs only when a worktree was asked for. **Never cut a second worktree for a card that has
one**: enter the one it has.

## Find the card's worktrees

Run `git worktree list --porcelain` and read each entry's path, branch, and any `locked` or `prunable`
line. A worktree is the card's when either holds:

- its folder under `.claude/worktrees/` has a name starting `issue-<n>-`, the name this step gives it;
- it is checked out on the head branch of the developer's open pull request naming the card.

An entry marked `prunable` has lost its folder: it is not the card's, and the report names
`git worktree prune` for the developer.

Find the developer's open pull requests naming the card on every page, keeping a hit only where its title
or body holds `#<n>` or `issue <n>` with `<n>` not followed by a digit, as `/phil:done` does:

```bash
gh api graphql --paginate -f query='
query($q:String!,$endCursor:String){
  search(query:$q, type:ISSUE, first:50, after:$endCursor){ pageInfo{ hasNextPage endCursor }
    nodes{ ... on PullRequest{ number title body headRefName } } } }' \
  -f q='repo:<owner>/<repo> is:pr is:open author:<viewer.login> <n> in:title,body' \
  --jq '.data.search.nodes[] | select((.title+" "+.body) | test("(#|issue )<n>([^0-9]|$)"; "i"))'
```

Then look for a branch the tool would collide with: `git rev-parse --symbolic --branches='worktree-issue-<n>-*'`.

These reads run in CHECK, before any write, so a failed one is `CANNOT-RUN`.

## A card already underway

The card is **underway** when it has a worktree, the developer has an open pull request naming it, or a
`worktree-issue-<n>-*` branch survives with no worktree. For a card underway, name `/phil:resume` as the
next step, recommend no other route, and launch nothing: `UNDERWAY`.

**Ask before entering any candidate whose entry has a `locked` line**, quoting its reason: a reason of
`claude session <name> (pid <pid> …)` may be another live session, and two sessions in one worktree
overwrite each other's work. A no leaves the session where it is.

- **The session is already in it** — `git rev-parse --show-toplevel` is the card's worktree. Call no
  tool and skip the lock ask, because the lock is this session's: `WORKTREE-ENTERED`.
- **One worktree** — enter it with `EnterWorktree` and its `path`: `WORKTREE-ENTERED`. Where it holds a
  `.session-handoff.md`, say so: `/phil:resume` reads it. From inside another worktree session the tool
  enters only a path under `.claude/worktrees/`.
- **Several** — list each with its branch and its lock, and ask which to enter. No pick leaves the
  session where it is.
- **An open pull request, or a surviving branch, and no worktree here** — name it and its branch, and cut
  nothing: a fresh worktree would start that branch's work again from the default branch.

## A card with no worktree

1. **Fetch the default branch**: `git fetch origin <default>`, where `<default>` is the
   `defaultBranchRef.name` the query below returns. The tool fetches only when the last fetch is a day
   old (Claude Code 2.1.317, read from its source on 2026-11-03), so a repo fetched today would branch
   from a stale ref without this.
2. **Cut it** with `EnterWorktree` and a `name` of `issue-<n>-<slug>`. Build the slug from the title:
   lowercase it, turn every run of characters other than `a`–`z` and `0`–`9` into one `-`, trim the
   ends, and keep the leading words up to 40 characters, cutting at a `-`. An empty slug names the
   worktree `issue-<n>`. The tool prefixes the branch with `worktree-`.
3. **Check the base.** Read `git rev-parse HEAD` inside the new worktree, and the remote's head:

   ```bash
   gh api graphql -f query='query($o:String!,$r:String!){ repository(owner:$o,name:$r){
     defaultBranchRef{ name target{ oid } } } }' -f o=<owner> -f r=<repo>
   ```

   Name the path, the branch and the base commit: `WORKTREE-CUT`. Where the base differs from the
   remote's head, read `worktree.baseRef` from `.claude/settings.local.json`, `.claude/settings.json`
   and `~/.claude/settings.json`, first found wins, and say why: `head` branches from local HEAD; with
   `fresh` or no setting, the base is behind the remote and the fetch may have failed.

**From inside another worktree**, where the developer said yes to moving (`../SKILL.md`, CHECK), leave it
first with `ExitWorktree` and `action: "keep"`. That tool acts only on a worktree this session entered
with `EnterWorktree`; afterwards read `git rev-parse --show-toplevel`, and where it is not the main
checkout, cut nothing and report `WORKTREE-FAILED`. Use `ExitWorktree` only with `keep`: a worktree
holds work, and removing one is `/phil:done`'s call once the card is finished.

## When the tool refuses

Where `EnterWorktree` refuses, quote the refusal, leave the session where it is, and report
`WORKTREE-FAILED`. A card underway still ends `UNDERWAY`; any other card goes on to DESCRIBE and ROUTE.
Cut no worktree by any other means — not `git worktree add`, which this command does not grant.

## The worktree line

```
WORKTREE: .claude/worktrees/issue-95-retry-flaky-uploads on worktree-issue-95-retry-flaky-uploads, from 8562216 = origin/main — session moved in
WORKTREE: .claude/worktrees/issue-95-retry-flaky-uploads on worktree-issue-95-retry-flaky-uploads, from a448a36 — the remote is at 55640cd (worktree.baseRef: head)
WORKTREE: left .claude/worktrees/done-gitlab-no-card, kept; cut .claude/worktrees/issue-95-retry-flaky-uploads on worktree-issue-95-retry-flaky-uploads, from 8562216 = origin/main — session moved in
UNDERWAY: .claude/worktrees/issue-80-phil-start — session moved in; next: /phil:resume
UNDERWAY: .claude/worktrees/issue-80-phil-start holds a handoff snapshot — session moved in; next: /phil:resume
UNDERWAY: already in .claude/worktrees/issue-80-phil-start; next: /phil:resume
UNDERWAY: 2 worktrees — issue-80-phil-start, issue-80-retry; entered issue-80-retry; next: /phil:resume
UNDERWAY: .claude/worktrees/issue-80-phil-start is locked by claude session issue-80-phil-start — not entered; next: /phil:resume
UNDERWAY: PR 94 is open on worktree-issue-80-phil-start, with no worktree here — nothing cut; next: /phil:resume
UNDERWAY: branch worktree-issue-80-phil-start survives with no worktree — nothing cut; next: /phil:resume
WORKTREE FAILED: <the refusal> — the session is in <git rev-parse --show-toplevel after the refusal>
```
