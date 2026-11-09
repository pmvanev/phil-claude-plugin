# CLEAR — what the work left behind

Part of the `done` skill. Read it whole before composing the plan. Its `SKILL.md` governs this file too.

CLEAR retires the work's handoff snapshots and deletes its branches, local and remote, under the plan's
one yes. **The guard is this skill's own tip check, not git.** `git push --delete` checks nothing, and
`git branch -d` accepts a branch merged only into its own remote copy. Git's refusals stand behind the
check as a second line. **Never pass `--force` or `-f`**: each removes that second line. Pass `-D` only
for a branch the developer chose to force-delete at its own question (FORCE, below); use `git branch -d`
for everything else. The one force-family flag allowed is `--force-with-lease=<ref>:<oid>` on a remote
delete, which makes the delete refuse a tip that moved.

**Remove a worktree only where all three hold:** it has a candidate's `headRefName` checked out at that
candidate's merged `headRefOid`; `worktree-state.py` reads it `CLEAN`; and `git worktree list
--porcelain` does not mark it `locked`, unless the lock is the one Claude Code holds for this session on
a worktree `EnterWorktree` made in this session. A lock means another session may work there, and git
refuses to remove a locked worktree without `--force`. **Who made it does not matter**: a session that
resumes in a worktree an earlier one cut, as `/phil:start` then `/phil:resume` does, holds the same work
(the developer's answer, 2026-11-05).

A clean-looking worktree can hold work nothing else has — a repository nested in an ignored folder,
edits git was told to ignore, submodules, commits only its own history remembers — and `git worktree
remove` deletes them without objecting (adversarial run, 2026-11-02); `worktree-state.py` reads each of
those `HIDDEN`. What no check reads, such as an editor's unsaved buffer, goes unseen; the plan names
each worktree it removes, so the developer's yes covers it.

Never pass `--force` to `git worktree remove`. List every other worktree with the commands to remove it
and its branch; the developer runs them. List a `HIDDEN` worktree with its findings and no remove
command: that command deletes what the findings name.

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
  the merged tip, which reads `CLEAN` and which no other session locks, read with
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
- In a worktree another session locks, keep the snapshot: that session may still need it.
- In a worktree that reads `DIRTY`, `HIDDEN` or `UNREADABLE`, keep the snapshot: it describes unfinished
  work.
- A branch any worktree has checked out, locally and on the remote, until that worktree is removed — by
  this run or by the developer. Git refuses to delete a checked-out branch, and work in that worktree may
  still need the remote.

The snapshot in the checkout this session runs in records no branch, so it may belong to other work. A
plain yes keeps it; it goes only on the third answer. Removing the worktree this session runs in deletes
that snapshot with it, so where the worktree holds one, remove it only on the third answer.

**Judge that snapshot stale or current, as `/phil:resume` does,** so the developer answers knowing
which. Read it with `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py head --file
<root>/.session-handoff.md`, where `<root>` is `git rev-parse --show-toplevel`, and keep the `SHA <h>`
for the third answer's retire. Take `commit:` and `dirty:` from its header. Read the tree's state with
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/worktree-state.py <root>`, without `--expect-head`: `DIRTY` reads
dirty, `CLEAN` or `HIDDEN` clean.

- **`STALE`** where the recorded commit is not `HEAD` — compare `git rev-parse --verify --quiet
  <recorded>^{commit}` with `git rev-parse HEAD`, full hashes both — or where `dirty:` disagrees with
  the tree.
- **`CURRENT`** otherwise. Where both read dirty, add that uncommitted work may have moved beneath it.
- **Unjudged** where `worktree-state.py` prints `UNREADABLE`: say the tree's state could not be read,
  and never print `CURRENT`.

Measure the distance only where `git merge-base --is-ancestor <recorded> HEAD` exits 0, with
`git rev-list --count <recorded>..HEAD`. A recorded commit off `HEAD`'s history — written on another
branch, or rebased away — gets no count: a snapshot written on a feature branch, then squash-merged,
still resolves, and counting from it measures nothing. Put the verdict on the snapshot's plan line
before its next action, with both short commits and the tree's state, in one of these shapes, never as
"may be out of date":

```
STALE — snapshot at 4a91c02, HEAD is now e17bd55 (6 commits); tree clean
STALE — snapshot at 4a91c02, not in HEAD's history (another branch, or rebased); HEAD is now e17bd55
STALE — snapshot at 4a91c02 recorded a clean tree; the tree is now dirty
CURRENT — snapshot at e17bd55, HEAD; tree clean
```

Stale proves only that the tree moved: a note about other work in flight turns stale once anything
merges. So a stale snapshot still survives a plain yes (the developer's answer, 2026-11-09).

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
  remove worktree  .claude/worktrees/fix-07 — clean, at PR 95's merged tip, locked only by this session;
                   deletes ignored: .venv, tests/__pycache__
  delete branch    finish-work/slice-01 (local and remote)
  FORCE-DELETE     finish-work/spike (local and remote) — 2 unmerged commits, at your answer
FOR YOU TO RUN — a worktree that is locked, not clean, or off the merged tip
  ../fw-04 is locked: claude session fw-04 (pid 4242) — once that session ends:
  git worktree remove ../fw-04 && git branch -d finish-work/slice-04 &&
    git push --delete origin refs/heads/finish-work/slice-04
  ../fw-03 has uncommitted changes:  M src/a.py  ?? notes.md
SURVIVES
  finish-work/spike and ../fw-spike — PR 86 closed unmerged
  ./.session-handoff.md — STALE — snapshot at 4a91c02, HEAD is now e17bd55 (6 commits); tree clean;
                          next: "verify the wave table"; may be other work; the third answer retires it
```

Ask with three answers: **yes**, **yes, and retire the snapshot here too** — offered where the
checkout this session runs in holds one — and **stop**.

## Run them in this order

1. **Snapshots** in worktrees the run keeps —
   `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py retire --file <path> --expect-sha <h>`,
   with the hash `head` printed. Anything but `RETIRED` keeps the snapshot.
2. **Other worktrees the run removes**, but not the one it runs in, each in turn: run `worktree-state.py
   --expect-head <headRefOid> <path>` again, and read the path's entry in `git worktree list
   --porcelain` for a lock; retire its snapshot only after that read comes back `CLEAN` and the entry
   shows no lock, as step 1 does; then, on `RETIRED` or where it holds none, run `git worktree remove
   <path>`. Anything else — `MOVED` or a new lock included — keeps the worktree, its snapshot and its
   branch, locally and on the remote.
3. **Local branches** — `git branch -d <branch>`, skipping the branch step 6's worktree holds: step 6
   deletes it. A squash or rebase merge leaves the branch unmerged in git's eyes, so git refuses it; that
   is a `LEFT`, not an error to work around.
4. **Remote branches** — `git push --delete --force-with-lease=refs/heads/<branch>:<headRefOid> <remote>
   refs/heads/<branch>`, skipping the branch step 6's worktree holds. The lease refuses the delete if the
   tip moved after the check; the qualified ref keeps a tag of the same name from matching.
5. **Force-deletes** — the developer's chosen branches, as FORCE gives them.
6. **The worktree this session runs in**, last, where it is a linked worktree; `<path>` is `git
   rev-parse --show-toplevel`. Run `worktree-state.py --expect-head <headRefOid> <path>` again, and act
   only on `CLEAN`. On the third answer, retire its snapshot as step 1 does, and go on only on
   `RETIRED`; a plain yes keeps a worktree that holds one.

   Where `EnterWorktree` made it in this session, call `ExitWorktree` with `action: "remove"`, which
   removes the worktree and its local branch and returns the session to the checkout it started from. It
   counts as unmerged any commit missing from that checkout's branch, not from `<default>`, so it may
   refuse a merged tip. Pass `discard_changes: true` only where `worktree-state.py` read `CLEAN` and
   `HEAD` is the merged `headRefOid`: then no file is uncommitted, and every commit it names is in
   `<default>` or, after a squash or rebase merge, in the pull request's own ref on the forge. Then
   delete the branch's remote copy as step 4 does.

   Where `EnterWorktree` did not make it in this session, `ExitWorktree` does nothing, so run
   `git worktree remove <path>`, never with `--force`. For a session that started in the worktree, git
   removed the directory the shell stood in, exited 0, and the next call ran from the main checkout
   (observed 2026-11-05, git 2.53.0); a worktree entered by `path` was not tried. Then delete the local
   branch as step 3 does, and its remote copy as step 4 does. A refusal, or a read other than `CLEAN`,
   keeps the worktree and its branch, locally and on the remote: report it `LEFT`, with its commands. A
   lock on it at plan time puts it under FOR YOU TO RUN, never in the plan's removals: git refuses a
   locked worktree without `--force`.

Any refusal or error in CLEAR leaves that item and goes on with the rest: report the refusal and leave
the item.

## Report

Count each branch once, saying where it went:

```
CLEARED: 1 snapshot, 1 worktree, 1 branch (local and remote)
FOR YOU: ../fw-02 — git worktree remove ../fw-02, then git branch -d and git push --delete for finish-work/slice-02
LEFT: finish-work/spike and ../fw-spike — PR 86 closed unmerged
LEFT: ./.session-handoff.md — kept: may be other work (STALE)
```
