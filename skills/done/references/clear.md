# CLEAR — what the work left behind

Part of the `done` skill. Read it whole before composing the plan. Its `SKILL.md` governs this file too.

CLEAR retires the work's handoff snapshots and deletes its branches, local and remote, under the plan's
one yes. **The guard is this skill's own tip check, not git.** `git push --delete` checks nothing, and
`git branch -d` accepts a branch merged only into its own remote copy. Git's refusals stand behind the
check as a second line. **Never pass `--force` or `-f`**: each removes that second line. Pass `-D` only
for a branch the developer chose to force-delete at its own question (FORCE, below); use `git branch -d`
for everything else. The one force-family flag allowed is `--force-with-lease=<ref>:<oid>` on a remote
delete, which makes the delete refuse a tip that moved.

**Remove a worktree only where all three hold:** the conversation shows this session creating it — with
a successful `EnterWorktree` or `git worktree add`; `worktree-state.py` reads it `CLEAN`; and its `HEAD`
is the merged `headRefOid` of a candidate. A clean-looking worktree can hold work nothing else has — a
repository nested in an ignored folder, edits git was told to ignore, submodules, commits only its own
history remembers — and `git worktree remove` deletes them without objecting (adversarial run,
2026-11-02); `worktree-state.py` reads each of those `HIDDEN`. Hold a worktree `git worktree list
--porcelain` marks `locked`, except the one this session runs in, which Claude Code locks for the
session: a lock means another session may work there. Never pass `--force` to `git worktree remove`.
List every other worktree with the commands to remove it and its branch; the developer runs them. List
a `HIDDEN` worktree with its findings and no remove command: that command deletes what the findings
name.

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
  it prints `CLEAN`, `DIRTY`, `HIDDEN` or `UNREADABLE` for each, with a `DIRTY` worktree's changes or a
  `HIDDEN` one's findings indented under it, and writes nothing. Where the plan lists a `DIRTY` or
  `HIDDEN` worktree, show the changes `worktree-state.py` printed under it. For a worktree the run may
  remove, pass `--expect-head <headRefOid>`: it then prints `MOVED` where `HEAD` is not the merged tip.
  On the plan's line for a worktree the run removes, show the `ignored:` entries `CLEAN` printed: the
  removal deletes them.
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

These are listed as surviving, with the reason. Of them, only the developer's own unmerged branch
reaches FORCE; never offer the rest for deletion:

- `<default>` itself, a branch with a `branchProtectionRule`, a branch from a pull request from a fork
  or a pull request someone else opened, and any branch that is the head or the base of an open pull
  request.
- A branch whose pull request closed unmerged or merged into another base.
- A branch, local or remote, whose tip is not the merged `headRefOid` — it holds commits the merge did
  not.
- A worktree whose branch is held, and the snapshot inside it.
- In a worktree that reads `DIRTY`, `HIDDEN` or `UNREADABLE`, keep the snapshot: it describes unfinished
  work.
- A branch any worktree has checked out, locally and on the remote, until that worktree is removed — by
  this run or by the developer. Git refuses to delete a checked-out branch, and work in that worktree may
  still need the remote.

The snapshot in the checkout this session runs in records no branch, so it may belong to other work. A
plain yes keeps it; it goes only on the third answer. Removing the worktree this session runs in deletes
that snapshot with it, so where the worktree holds one, remove it only on the third answer.

## FORCE — an unmerged branch, one at a time

An unmerged branch survives unless the developer says otherwise, for that branch alone. Offer it only for
the developer's own branch: one whose pull request closed unmerged or merged into another base, or whose
tip is past the merged `headRefOid` — and which is not `<default>`, protected, from a fork, someone
else's, the head or base of an open pull request, or checked out in any worktree. Never offer to remove a
worktree.

A name is not ownership: a colleague can push a new branch under an old name. Offer it only where the
branch still descends from the pull request's `headRefOid` and every commit it would lose was authored by
`viewer.login`:

- local — `git merge-base --is-ancestor <headRefOid> refs/heads/<branch>` exits 0, and
  `git log --format='%h %an <%ae> %s' <remote>/<default>..refs/heads/<branch>` lists what it would lose,
  each with its author;
- remote — read the list, the tip and the ancestry in one query, so the shown tip is the tip the list
  came from:
  `ref(qualifiedName:"refs/heads/<default>"){ compare(headRef:"refs/heads/<branch>"){ aheadBy
  headTarget{ oid } commits(first:50){ nodes{ abbreviatedOid messageHeadline author{ name user{ login }
  } } } } }` and `ref(qualifiedName:"refs/heads/<branch>"){ compare(headRef:"<headRefOid>"){ status } }`,
  whose `status` must read `BEHIND` or `IDENTICAL`. Keep `headTarget.oid` as the shown tip.

Where `aheadBy` exceeds 50, do not offer it: the list shows the oldest commits first, so the newest,
the tip among them, would go unshown. Hold the branch and say how many commits it carries.

Ask about each branch that passes on its own, before the plan, showing every commit the delete would
lose with its author. Offer **keep** — the default — or **force-delete**, and stop. Any answer but
force-delete keeps both copies. A force-delete joins the plan as its own line, and the plan's one yes
runs it with the rest:

- local — `git branch -D <branch>`. Read the local tip again just before `-D`, and skip the delete where
  it moved from the tip the list came from.
- remote — `git push --delete --force-with-lease=refs/heads/<branch>:<shown tip> <remote>
  refs/heads/<branch>`, so a commit pushed after the question refuses the delete. Force-delete the remote
  copy only after the local delete succeeded, or where no local copy exists: where git refuses the local
  delete — a worktree mid-rebase hides its branch from `git worktree list` — the remote copy stays.

## The plan's cleanup lines

Add to the plan, after the close's writes:

```
CLEAR
  retire snapshot  ../fw-02/.session-handoff.md — next: "verify the wave table"; stack: 2 frames
  remove worktree  .claude/worktrees/fix-07 — this session made it; clean, at PR 95's merged tip;
                   deletes ignored: .venv, tests/__pycache__
  delete branch    finish-work/slice-01 (local and remote)
  FORCE-DELETE     finish-work/spike (local and remote) — 2 unmerged commits, at your answer
FOR YOU TO RUN — a worktree this session did not make, or one that is not clean
  git worktree remove ../fw-02 && git branch -d finish-work/slice-02 &&
    git push --delete origin refs/heads/finish-work/slice-02
  ../fw-03 has uncommitted changes:  M src/a.py  ?? notes.md
SURVIVES
  finish-work/spike and ../fw-spike — PR 86 closed unmerged
  ./.session-handoff.md — may be other work; the third answer retires it
```

Ask with three answers: **yes**, **yes, and retire the snapshot here too** — offered where the
checkout this session runs in holds one — and **stop**.

## Run them in this order

1. **Snapshots** in worktrees the run keeps —
   `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py retire --file <path> --expect-sha <h>`,
   with the hash `head` printed. Anything but `RETIRED` keeps the snapshot.
2. **Worktrees this session made**, but not the one it runs in, each in turn: run
   `worktree-state.py --expect-head <headRefOid> <path>` again; retire its snapshot only after that read
   comes back `CLEAN`, as step 1 does; then, on `RETIRED` or where it holds none, run
   `git worktree remove <path>`. Anything else — `MOVED` included, a commit made after the plan — keeps
   the worktree, its snapshot and its branch, locally and on the remote.
3. **Local branches** — `git branch -d <branch>`. A squash or rebase merge leaves the branch unmerged in
   git's eyes, so git refuses it; that is a `LEFT`, not an error to work around.
4. **Remote branches** — `git push --delete --force-with-lease=refs/heads/<branch>:<headRefOid> <remote>
   refs/heads/<branch>`. The lease refuses the delete if the tip moved after the check; the qualified ref
   keeps a tag of the same name from matching.
5. **Force-deletes** — the developer's chosen branches, as FORCE gives them.
6. **The worktree this session runs in**, last, and only where `EnterWorktree` made it: git cannot remove
   the directory a session works in. Run `worktree-state.py --expect-head <headRefOid> <path>` again,
   and on `CLEAN` call `ExitWorktree` with `action: "remove"`, which removes the worktree and its local
   branch and returns the session to the checkout it started from. It counts as unmerged any commit
   missing from that checkout's branch, not from `<default>`, so it may refuse a merged tip. Pass
   `discard_changes: true` only where `worktree-state.py` read `CLEAN` and `HEAD` is the merged
   `headRefOid`: then no file is uncommitted, and every commit it names is in `<default>` or, after a
   squash or rebase merge, in the pull request's own ref on the forge. Then delete the branch's remote
   copy as step 4 does. Where `git worktree add` made it, list it for the developer instead.

Any refusal or error in CLEAR leaves that item and goes on with the rest: report the refusal and leave
the item.

## Report

Count each branch once, saying where it went:

```
CLEARED: 1 snapshot, 1 worktree, 1 branch (local and remote)
FOR YOU: ../fw-02 — git worktree remove ../fw-02, then git branch -d and git push --delete for finish-work/slice-02
LEFT: finish-work/spike and ../fw-spike — PR 86 closed unmerged
LEFT: ./.session-handoff.md — kept: may be other work
```
