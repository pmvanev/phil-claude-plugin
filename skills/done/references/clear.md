# CLEAR — what the work left behind

Part of the `done` skill. Read it whole before composing the plan. Its `SKILL.md` governs this file too.

CLEAR retires the work's handoff snapshots and deletes its branches, local and remote, under the plan's
one yes. **The guard is this skill's own tip check, not git.** `git push --delete` checks nothing, and
`git branch -d` accepts a branch merged only into its own remote copy. Git's refusals stand behind the
check as a second line. **Never pass `--force`, `-f` or `-D`**: each removes that second line. Use
`git branch -d`, never `-D`. The one force-family flag allowed is `--force-with-lease=<ref>:<oid>` on a
remote delete, which makes the delete refuse a tip that moved.

**Never remove a worktree.** A clean-looking worktree can hold work nothing else has — a repository
nested in an ignored folder, edits git was told to ignore, submodules, commits only its own history
remembers — and `git worktree remove` deletes them without objecting (adversarial run, 2026-11-02). List
each finished worktree with the commands to remove it and its branch; the developer runs them.

## Find the candidates

A candidate comes only from a pull request FIND kept that merged into `<default>`, with
`isCrossRepository` false and `author.login` equal to `viewer.login`: its `headRefName` is the branch,
its `headRefOid` the merged tip — never a branch matched by name.

Delete a branch only when its tip is the `headRefOid` of a pull request merged into `<default>`:

- **Remote branch** — read `ref(qualifiedName:"refs/heads/<branch>"){ target{ oid }
  branchProtectionRule{ id } associatedPullRequests(states:OPEN, first:5){ nodes{ number } } }` and
  `pullRequests(baseRefName:"<branch>", states:OPEN, first:1){ totalCount }` on the repository. A null
  `ref` means the merge already deleted it; skip it.
- **Local branch** — `git rev-parse --verify --quiet refs/heads/<branch>` prints its tip, or nothing.
- **Worktrees** — `git worktree list --porcelain` gives each worktree's path, `HEAD` and `branch`. Run
  `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/worktree-state.py <path>...` over those on a candidate branch:
  it prints `CLEAN`, `DIRTY` or `UNREADABLE` for each, and writes nothing.
- **Snapshot** — `<worktree>/.session-handoff.md` in each worktree on a candidate branch whose `HEAD` is
  the merged tip and which reads `CLEAN`, read with
  `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py head --file <path>`: it prints the file
  above the recorded exchanges and `SHA <h>` on stderr, so the exchanges never enter the context. Keep
  `<h>`; the plan shows the snapshot's next action and stack.

**The remote** is the one `git rev-parse --abbrev-ref <default>@{upstream}` names before its first `/`,
and only when every URL `git remote get-url --push --all <remote>` prints names `<owner>/<repo>` on
GitHub, over HTTPS or SSH: the push URL, not the fetch URL, decides where a delete lands. Where no remote
resolves or any push URL names another repo, hold every remote delete and say why.

## Hold what must survive

These are listed as surviving, with the reason, and never offered for deletion:

- `<default>` itself, a branch with a `branchProtectionRule`, a branch from a pull request from a fork
  or a pull request someone else opened, and any branch that is the head or the base of an open pull
  request.
- A branch whose pull request closed unmerged or merged into another base.
- A branch, local or remote, whose tip is not the merged `headRefOid` — it holds commits the merge did
  not.
- A worktree whose branch is held, and the snapshot inside it.
- In a worktree that reads `DIRTY` or `UNREADABLE`, keep the snapshot: it describes unfinished work.
- A branch any worktree has checked out, locally and on the remote, until the developer removes the
  worktree. Git refuses to delete a checked-out branch, and work in that worktree may still need the
  remote.

The snapshot in the checkout this session runs in records no branch, so it may belong to other work. A
plain yes keeps it; it goes only on the third answer.

## The plan's cleanup lines

Add to the plan, after the close's writes:

```
CLEAR
  retire snapshot  ../fw-02/.session-handoff.md — next: "verify the wave table"; stack: 2 frames
  delete branch    finish-work/slice-01 (local and remote)
FOR YOU TO RUN — worktrees are never removed for you
  git worktree remove ../fw-02 && git branch -d finish-work/slice-02 &&
    git push --delete origin refs/heads/finish-work/slice-02
SURVIVES
  finish-work/spike and ../fw-spike — PR 86 closed unmerged
  ./.session-handoff.md — may be other work; the third answer retires it
```

Ask with three answers: **yes**, **yes, and retire the snapshot here too** — offered where the
checkout this session runs in holds one — and **stop**.

## Run them in this order

1. **Snapshots** — `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py retire --file <path>
   --expect-sha <h>`, with the hash `head` printed. Anything but `RETIRED` keeps the snapshot.
2. **Local branches** — `git branch -d <branch>`. A squash or rebase merge leaves the branch unmerged in
   git's eyes, so git refuses it; that is a `LEFT`, not an error to work around.
3. **Remote branches** — `git push --delete --force-with-lease=refs/heads/<branch>:<headRefOid> <remote>
   refs/heads/<branch>`. The lease refuses the delete if the tip moved after the check; the qualified ref
   keeps a tag of the same name from matching.

Any refusal or error in CLEAR leaves that item and goes on with the rest: report the refusal and leave
the item.

## Report

Count each branch once, saying where it went:

```
CLEARED: 1 snapshot, 1 branch (local and remote)
FOR YOU: ../fw-02 — git worktree remove ../fw-02, then git branch -d and git push --delete for finish-work/slice-02
LEFT: finish-work/spike and ../fw-spike — PR 86 closed unmerged
LEFT: ./.session-handoff.md — kept: may be other work
```
