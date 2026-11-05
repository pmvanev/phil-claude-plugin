# Feature Delta — finish-work (`/phil:done`)

> Single narrative file for the feature. DISCUSS findings live here as
> `## Wave: DISCUSS / [REF|WHY|HOW]` sections. Machine artifacts: `slices/slice-NN-*.md`.
> SSOT updates: `docs/product/jobs.yaml` (new job), `docs/product/journeys/finish-work.yaml` (new
> journey), `docs/product/personas/kai-session-relay.yaml` (facet added).
> Board: issue 75, In Progress, `wave: discuss`.
> Build path: DISCUSS only — the deliverable is prose (CLAUDE.md, edd-loop DDD8).

---

## Wave: DISCUSS / [REF] Source

Issue 75 asks for one command that puts a session down **finished**, as `/phil:handoff` puts one
down unfinished. Finishing a card takes five steps by hand: the closing comment, the Status write,
the merged branch, the worktree, and the side request nobody did. The developer added a sixth on
2026-11-02: the stale `.session-handoff.md` the work leaves behind.

Measured on this repo, 2026-11-02: no merged branch left on the remote, one worktree, no snapshot on
disk, every one of 40 closed cards carries a closing comment, and no card's Status disagrees with its
state. **The cost here is the labour, not the debris** — the developer runs all five steps by hand,
carefully, every time. A consumer repo without this CLAUDE.md's board rules pays the same labour with
no rules to guide it.

Three facts shape the design:

- **Nothing retires a snapshot.** The session-handoff journey's last step says the snapshot is
  "marked consumed" on resume; no skill implements it. A snapshot left in a finished checkout sends
  the next `/phil:resume` back to finished work, and a stale handoff is worse than none (Kai's
  mental model).
- **Nothing in the plugin touches a worktree.**
- **The forge cannot say which branches are the card's.** This repo's pull requests name their card
  in prose ("Tracked on issue 38") and never link it, because a closing keyword closes the card early
  (CLAUDE.md). `closingIssuesReferences` is empty on all eight merged pull requests sampled.

## Wave: DISCUSS / [REF] Persona & Job

- **Persona:** `kai-session-relay`, with a put-down-finished facet. Kai already owns the session
  boundary; this is the same boundary, crossed at the end of the work rather than the middle of it.
- **JTBD one-liner:** *When a card's work has merged, close it and clear everything it left behind —
  without dropping an ask or deleting anything unmerged — so done means done and the next session
  starts clean.*
- **Job ID:** `put-finished-work-down` (new).

## Wave: DISCUSS / [REF] Feature type & framing

- **Feature type:** developer tool, user-facing — the developer invokes `/phil:done` and reads its
  report.
- **Greenfield command** in a brownfield plugin: a new `commands/done.md` and `skills/done/`. It
  composes `phil:issue-board` (close order), `phil:nwave-issue-board` (the generated block) and
  `scripts/session-exchanges.py head` (reading a snapshot without its exchanges).
- **Research depth:** lightweight — happy path plus the error paths in the journey.

## Wave: DISCUSS / [REF] Locked decisions

The developer answered D1–D4 on 2026-11-02; the rest follow from those answers, the card and the
plugin's existing rules.

- **[D1] The asks come from the card and the current session.** *(Developer's answer.)* `/phil:done`
  reads the card's checklist and its *Done when* items, which survive across sessions, plus the
  requests and tasks in the current session. Each ask is marked **done** with its evidence — a merged
  pull request, a commit, a passing run, a file — or **open**. A sentence saying it was done is not
  evidence. Any open ask holds the close; the developer answers each one by doing it, or by dropping it
  with a reason the closing comment records.

- **[D2] `/phil:done` starts after the merge.** *(Developer's answer.)* It never merges and never
  opens a pull request; `superpowers:finishing-a-development-branch`, or the developer, does that. It
  refuses to close until every pull request it found for the card has merged and the default branch's
  pipeline is green at or after the last merge. A repo with no pipeline is reported as `no pipeline`,
  never as green. It needs no other plugin installed.

- **[D3] One plan, one yes.** *(Developer's answer.)* `/phil:done` lists every write it intends — the
  closing comment, the Status write, each branch local and remote, each worktree, each snapshot — and
  asks once. The plan holds out three things and asks about each on its own: an open ask (D1), a
  branch not merged into the default branch, and a worktree with uncommitted or unpushed changes. Each
  survives unless the developer says otherwise. Every ask offers `stop`; a stop writes nothing.

- **[D4] The card's generated summary becomes one dated finished line.** *(Developer's answer.)*
  Where the card carries `phil:nwave-issue-board`'s generated block, a dated finished line —
  `Finished 2026-11-02 — closed by /phil:done.` — replaces its projected why, next action and stack.
  The block has one writer
  (`phil:nwave-issue-board`, *Project the reasoning*), so `/phil:done` asks that writer to regenerate
  it; it never edits the block. The generator must learn a third reasoning state, **finished**, beside
  a snapshot and `unknown`: deleting the snapshot and regenerating as things stand would render
  `Stack: unknown — no snapshot projected`, a false claim about finished work.

- **[D5] Close in the order `phil:issue-board` requires, and read both back.** Post the closing
  comment, then write Status=Done, then read the card's state and Status back. Where the board's
  workflows do not close the issue on Done, close it explicitly after the comment. A closed card
  outside Done, or an open one in Done, is a defect the read-back reports.

- **[D6] The closing comment and the report follow `rules/writing.md`.** Both are prose `/phil:done`
  composes for the team, so the skill names the standard and ships a fixture that fails without the
  citation (CLAUDE.md, *Board surfaces that compose prose*). An ask in the developer's own words is
  quoted as written.

- **[D7] The snapshot is cleared before any worktree is removed.** Removing a worktree deletes the
  snapshot inside it unasked. For each checkout the work used, `/phil:done` shows the snapshot's next
  action and stack — read through `session-exchanges.py head`, so the recorded exchanges never enter
  the context — and lists its deletion in the plan. The file is git-ignored and has no undo; leaving it
  sends the next `/phil:resume` to finished work.

- **[D8] The work's branches and worktrees are confirmed, never guessed by name.** Where the forge
  links pull requests to the card, those pull requests' head branches are the work's. Where it does
  not — this repo — `/phil:done` lists as candidates the merged pull requests whose title or body names
  the card, and the worktrees checked out on their branches; the plan shows each with its pull request,
  and the developer's one yes confirms them. A branch matching only by name is never a candidate.

- **[D9] Deletion is never forced.** Local branches go with `git branch -d`, worktrees with
  `git worktree remove` without `--force`, remote branches only once merged. `/phil:done` reports a
  refusal from git and leaves the item.

- **[D10] `commands/done.md` declares `mutates: true`** — it writes to git and the forge
  (`scripts/check-readonly-commands.py`).

## Wave: DISCUSS / [REF] User stories

### Story 1 — Every ask accounted for *(slice 01)*
`job_id: put-finished-work-down`

As **Kai**, I want every ask the work received listed with its evidence before anything closes, so a
side request made three sessions ago cannot vanish with the card.

### Elevator Pitch
Before: I close a card from memory and learn a week later that a mid-session request was never done.
After: run `/phil:done 75` → sees `ASKS 6: 5 done, 1 open` with each done ask's evidence (`PR 81 merged`) and the open one quoted: `"make sure it cleans up a stale session-handoff.md" — no evidence`.
Decision enabled: I do the open ask or drop it with a reason before the card closes.

**Acceptance criteria**
- AC1.1 — Given a card checklist item with no evidence, when `/phil:done` runs, then it lists the item
  as open and closes nothing.
- AC1.2 — Given a request made in the current session and absent from the card, then `/phil:done`
  lists it beside the card's items.
- AC1.3 — Given an ask whose only support is a sentence saying it was done, then it is open.
- AC1.4 — Given the developer drops an open ask with a reason, then the closing comment records the
  ask and the reason.

### Story 2 — Refuse until the work has landed *(slice 01)*
`job_id: put-finished-work-down`

As **Kai**, I want `/phil:done` to refuse while a pull request is open or main is red, so "done" never
means "done on my branch".

### Elevator Pitch
Before: I close the card when the code feels finished, and the merge or the main pipeline is still pending.
After: run `/phil:done 75` → sees `LANDED: PR 81 merged 2026-11-03; main green at a1b2c3d` or `NOT LANDED: PR 82 open — nothing closed`.
Decision enabled: I close now, or go and merge first.

**Acceptance criteria**
- AC2.1 — Given an open pull request for the card, then `/phil:done` closes nothing and names it.
- AC2.2 — Given a red default-branch pipeline after the last merge, then it closes nothing and names
  the run.
- AC2.3 — Given a repo with no pipeline, then it reports `no pipeline`, never `green`.
- AC2.4 — Given a pull request still unmerged, then `/phil:done` offers no merge.

### Story 3 — Close the card in the safe order *(slice 02)*
`job_id: put-finished-work-down`

As **Kai**, I want the closing comment posted before Done and both read back, so the comment is never
silently dropped and the board never disagrees with the issue.

### Elevator Pitch
Before: I post the comment, set Done and close by hand, and on a closed issue `gh issue close -c` drops the comment without a word.
After: run `/phil:done 75` → sees `CLOSED: comment posted, Status Done, issue closed — read back` and, on a card with a generated block, `Finished 2026-11-03.` in place of its next action.
Decision enabled: I move to the next card, trusting the board says this one is finished.

**Acceptance criteria**
- AC3.1 — Given a close, then the comment is posted before Status=Done, and a fixture fails on the
  reverse order.
- AC3.2 — Given the read-back finds a closed card outside Done or an open one in Done, then the report
  names the defect.
- AC3.3 — Given a card with a generated block, then `phil:nwave-issue-board` regenerates it with the
  finished line, and `Stack: unknown` does not appear.
- AC3.4 — Given `skills/done/SKILL.md` without its `rules/writing.md` citation, then a test fails.

### Story 4 — Clear what the work left behind *(slice 03)*
`job_id: put-finished-work-down`

As **Kai**, I want the work's snapshot, worktrees and branches cleared in one approved plan, with
anything unmerged or uncommitted held back, so the next session starts clean and nothing is lost.

### Elevator Pitch
Before: I delete branches and worktrees by hand, and the stale snapshot stays until a resume trips on it.
After: run `/phil:done 75` → sees `PLAN: delete snapshot (next: "verify the wave table"), remove worktree ../finish-work, delete finish-work/slice-01 local and remote — yes / stop`, then `LEFT: finish-work/spike — not merged`.
Decision enabled: I approve the plan once, and choose separately what happens to the unmerged branch.

**Acceptance criteria**
- AC4.1 — Given a worktree with a snapshot inside it, then the plan shows the snapshot and lists its
  deletion before the worktree's removal.
- AC4.2 — Given a branch not merged into the default branch, then the plan holds it out, and it
  survives unless the developer says otherwise.
- AC4.3 — Given a worktree with uncommitted or unpushed changes, then the plan holds it out, and it
  survives unless the developer says otherwise.
- AC4.4 — Given a branch matching the card only by name, then it is not a candidate.
- AC4.5 — Given a clean finish — everything merged and clean, no open ask — then `/phil:done` asks
  exactly one question.
- AC4.6 — Given the run ends, then the report lists what it did and what it left, with the reason for
  each item left.

## Wave: DISCUSS / [REF] Outcome KPIs

| KPI | Target | Measurement |
|---|---|---|
| No close over an open ask | 0 closes while an ask stands open and unanswered | fixture |
| Comment before Done | 100% of closes post the comment first and read both back | fixture |
| Nothing unmerged lost | 0 unmerged branches or dirty worktrees deleted without their own yes | fixture per kind |
| No stale snapshot | 0 snapshots left in a finished checkout after an approved plan | fixture; dogfood on this repo |
| One question | a clean finish asks exactly one question | dogfood transcript |
| Applied, not cited | removing the `rules/writing.md` citation fails a test | pytest, watched red first |

## Wave: DISCUSS / [REF] Out of scope

- Merging, opening a pull request, or choosing between them (D2).
- ~~GitLab.~~ Brought in by slice 04 (2026-11-03); see *Decisions summary*.
- Retiring a snapshot on `/phil:resume` — the journey's unimplemented "marked consumed" step. This
  feature retires it at finish instead; resume is unchanged.
- Issue 76's autopilot, which will call `/phil:done`; its open questions stay on its card.
- Linking pull requests to their card on the forge. D8 works without the link.

## Wave: DISCUSS / [REF] Driving ports & prerequisites

- **Driving port:** `/phil:done <card>`. Later, issue 76's autopilot.
- **Driven ports:** `gh` (pull requests, checks, the issue, the project's Status field), `git`
  (branches, worktrees), `scripts/session-exchanges.py head`, `phil:nwave-issue-board`'s generator.
- **Prerequisites:** `phil:issue-board`'s close order and the repo's board block — or a `phil:board-setup`
  run — for the Status field and option ids. The generator change in D4 lands in slice 02.

## Wave: DISCUSS / [REF] Walking-skeleton strategy

Slice 01 is the skeleton: `/phil:done` runs end to end and reports whether the card is ready to
close, writing nothing. Slices 02 and 03 add the writes behind it.

## Wave: DISCUSS / [REF] Scope Assessment

**PASS (right-sized).** Four stories across three slices; one new command and skill; one change to an
existing skill (the generator's finished state); no new script.

## Wave: DISCUSS / [REF] Definition of Done

1. `commands/done.md` and `skills/done/SKILL.md` exist, authored after reading
   `plugin-dev:command-development` and `plugin-dev:skill-development`.
2. Every story traces to `put-finished-work-down`.
3. Every story has an Elevator Pitch with a real entry point and observable output.
4. Fixtures pin issue 75's refusals: an open ask holds the close; the comment precedes Done; an
   unmerged branch survives; a dirty worktree survives; a snapshot survives until the plan's yes.
5. `phil:nwave-issue-board` renders the finished state, with a fixture showing no `Stack: unknown` on
   a finished card.
6. Every new citation and gate has a test, watched red first.
7. `python3 -m pytest -q` and `scripts/check-invariants.py` pass.
8. `/phil:harden-instructions` over the command, the skill and its references; `phil:eos` over this
   file, its slice briefs and the SSOT entries; `plugin-dev:skill-reviewer` and
   `plugin-dev:plugin-validator` over the command and skill — then the tests again.
9. Dogfood: `/phil:done` closes issue 75 itself.

## Wave: DISCUSS / [REF] Definition of Ready — validation

| # | DoR item | Status | Evidence |
|---|---|---|---|
| 1 | Job traceable | ✅ | `put-finished-work-down` in `jobs.yaml`; all 4 stories carry it |
| 2 | Persona defined | ✅ | `personas/kai-session-relay.yaml`, put-down-finished facet |
| 3 | Journey mapped | ✅ | `journeys/finish-work.yaml`, with error paths |
| 4 | Elevator pitches | ✅ | all 4 stories, `/phil:done` entry point, observable output |
| 5 | ACs testable | ✅ | Given-When-Then, fixture- or pytest-checkable |
| 6 | Slices ≤1 day with a learning hypothesis | ✅ | `slices/slice-01` … `slice-03` |
| 7 | Walking skeleton | ✅ | slice 01, read-only |
| 8 | Outcome KPIs with targets | ✅ | table above |
| 9 | Scope right-sized | ✅ | Scope Assessment above |

Requirements completeness: each of issue 75's five steps, the snapshot step and the three open
questions maps to a decision and an AC.

## Wave: DISCUSS / [REF] Changed Assumptions

DISCOVER and DIVERGE never ran; the changed assumptions are the session-handoff journey's and issue
75's own.

- **Session-handoff journey**, `docs/product/journeys/session-handoff.yaml`, step `resume`:
  > "Work continues under the owning command. The snapshot is superseded rather than left standing as
  > a second account of where things are." — output: "prior snapshot marked consumed"

  **New:** nothing implements that step; `/phil:done` retires the snapshot when the work finishes
  (D7). The journey stays unedited. **Why:** a snapshot left after resume is still current work; one
  left after the work finished is the stale handoff Kai's job is built against.

- **Issue 75**, step 4 as written on 2026-11-02: "deletes the file on the developer's yes".

  **New:** the plan's one yes covers it (D3). **Why:** the developer chose one plan, one yes.

## Wave: DISCUSS / [REF] Decisions summary (for authoring)

- **Key decisions:** D1 asks from the card and the session, each with evidence · D2 starts after the
  merge · D3 one plan, one yes, exceptions held out · D4 a finished line, written by the block's one
  writer · D5 comment, Done, read back · D6 composed prose to `rules/writing.md` · D7 snapshot before
  worktree · D8 branches confirmed, never guessed · D9 nothing forced · D10 `mutates: true`.
- **Requirements summary:** `/phil:done` lists every ask with its evidence, refuses until the work
  has merged and main is green, closes the card comment-first and reads it back, and clears the
  snapshot, worktrees and branches in one approved plan, holding back anything unmerged or uncommitted.
- **Constraints:** never merges; never forces; never writes the generated block itself; never reads a
  snapshot's exchanges.
- **Settled at slice 01 authoring (2026-11-02):** `/phil:done` takes the card number as its argument
  and asks for it when absent, never inferring it from the branch. The current session's asks come from
  the conversation itself, with no script; a compacted session says its earlier asks come from the
  summary, and a fresh session says it holds none. A ticked or unnamed ask is searched for evidence
  among the card's pull requests and the files it names, never assumed.
- **Settled at slice 02 authoring (2026-11-02):** the generator detects the finished state from the
  issue's closed state and its `closedAt`, never from a marker a command leaves, so the line reads
  `Finished <YYYY-MM-DD>.` — the generator cannot know which command closed a card, and D4's "closed by
  /phil:done" would be a claim it cannot derive. The terminal outcomes became `NOT-READY`, `STOPPED` and
  `CLOSED`: slice 01's `READY` named a verdict, not what the run did. `/phil:done`'s closing comment
  joined CLAUDE.md's list of board surfaces that compose prose.
- **Settled at slice 03 authoring (2026-11-02):** D3 and D9 conflicted. Deleting an unmerged branch or
  a worktree with uncommitted changes needs `-D` or `--force`, which D9 forbids, so "survives unless the
  developer says otherwise" cannot be honoured. Such items are listed in the plan as surviving, with the
  reason, and never offered. **The guard is the skill's own tip check**: a branch, local or remote, or a
  worktree goes only when its tip is the `headRefOid` of a pull request merged into the default branch,
  and the branch is not the default, protected, from a fork, or used by an open pull request. Both
  slice 03 reviews disproved the first draft's premise that git's refusals were the guard:
  `git push --delete` checks nothing, `git branch -d` accepts a branch merged only into its own remote,
  `-f` forces either, and a dirty worktree's snapshot was retired before git refused the worktree. A
  dirty worktree is now found before the plan by `scripts/worktree-state.py`, and held with its
  snapshot. A branch held or left keeps its remote branch. The snapshot goes through a new
  `session-exchanges.py retire`, with the same compare-and-swap as every write, never a bare `rm`; and
  the plan gains a third answer, *yes, and retire the snapshot here too*: the snapshot in the checkout
  `/phil:done` runs in records no branch, so a plain yes keeps it. The two entries below overturn two
  rules here: worktrees are no longer removed at all, and an unmerged branch is offered after all.
- **Worktrees are listed, never removed (the developer's answer, 2026-11-02).** An adversarial run,
  verified in scratch repositories, showed `git worktree remove` deleting, with exit 0, a repository
  nested in an ignored folder, edits hidden by `--assume-unchanged` or `--skip-worktree`, and commits
  only the worktree's history held; and git refuses any worktree with a submodule. Each check closes one
  known way and leaves unknown ones open, so the plan lists each finished worktree with its commands and
  the developer runs them. This revises story 4 and issue 75's step 5. The same run moved three more
  rules into place: the remote is judged by every push URL, the remote delete carries the merged tip as
  `--force-with-lease`, and only the developer's own pull requests give candidates.
- **An unmerged branch survives unless the developer says otherwise (the developer's answer at the
  close of issue 75, 2026-11-02).** This reverses the slice 03 settlement for branches only. FORCE asks
  about each of the developer's own unmerged branches on its own, before the plan, listing every commit a
  delete would lose; keep is the default, and force-delete runs `git branch -D` and a remote delete
  leased on the tip shown. It offers only a branch that still descends from the pull request's head and
  whose lost commits the developer wrote; past 50 commits it offers nothing. Worktrees stay listed,
  never removed, with a dirty one's changes shown.
- **Slice 04: GitLab, and a run with no card (the developer's request, 2026-11-03).** `/phil:done 21`
  on modive, a GitLab repo, stopped at the forge check; the developer had closed the card, deleted the
  branches and removed the worktrees by hand, and only the stale snapshot remained. The developer
  asked for GitLab support, and for a run with no card that still checks every session task and
  clears the session's merged branches.
  - **GitLab runs the same steps through `glab`**, in `skills/done/references/gitlab.md`, and every
    rule stands. Every read ran against modive on 2026-11-03. The closing-link and search reads
    named the same 79 merge requests that `related_merge_requests` returns. `glab api` reads take no
    field, because a field turns the GET into a POST. A board column is a `status::` label, and the
    closed list is Done, so the Status write removes the card's status labels. Ownership compares
    commit emails, because GitLab's compare names no account.
  - **No argument runs without a card**, in `skills/done/references/no-card.md`. It closes no card,
    and never infers one. The work is the pull requests and branches the conversation shows this
    session opening, pushing or merging, and D8 carries over: a branch the conversation never names is
    no candidate. Every session ask counts. The plan holds only CLEAR's lines. It asks once, asks
    *retire it or keep it* where only the snapshot here remains, and asks nothing where nothing
    remains. The new terminal outcome is `FINISHED`.
  - **Reviews (2026-11-03).** The plugin validator found that a bare `-R <group/project>` sends a
    `glab issue` write to gitlab.com outside a checkout of the host, so every `glab issue` call now
    takes the full URL. It also found that `-X` went unbanned, and that the GitLab label default
    contradicted the skill's skip rule. The skill reviewer found that a reused branch name matched an
    old merged pull request, so a head-branch hit now counts only at the branch's tip (fixture 46). It
    also found that a no-card run needed its own query, and that the GitLab read-back could miss the
    note behind system notes. Its claim that GitLab's search misses one- and two-digit card numbers
    failed live: for cards 1, 7, 9, 18, 21 and 38, the search returned what a filter over every merge
    request returned. That run also showed `glab api --paginate` printing one array per page.
  - **Not yet run:** the three GitLab writes (note, unlabel, close), and a run without a card. Their
    flags come from `glab --help`. The note and the block refresh pass their body through
    `$(cat <<'EOF' …)`, and the command grants no `cat`, so either may stop for a permission prompt
    after the yes. Dogfood on the next GitLab finish.
- **Slice 05: a worktree this session made is removed (the developer's answer, 2026-11-03).** This
  partly reverses "worktrees are listed, never removed" (2026-11-02). The first run without a card,
  on 1.22.0, finished clean and left this session's own worktree and its branch standing, and the
  developer asked why. The slice 04 request had said "clean up sessions branches/worktrees", and the
  run had marked that ask done on its branch half alone.
  - **`scripts/worktree-state.py` reads the adversarial run's losses as `HIDDEN`**: a repository nested
    in an ignored folder, an `--assume-unchanged` or `--skip-worktree` edit, a submodule, and a commit
    only the worktree's own history holds. Each has a test that builds the case in a scratch
    repository. Ignored caches alone still read `CLEAN`.
  - **A worktree goes only where all three hold**: the conversation shows this session creating it,
    `worktree-state.py` reads it `CLEAN`, and its `HEAD` is the merged tip. Every other worktree is
    still listed with its commands. Another worktree goes through `git worktree remove`, never with
    `--force`. The one the session runs in goes last, through Claude Code's `ExitWorktree`, because git
    cannot remove a session's working directory.
  - **Run live, 2026-11-03:** `ExitWorktree` refused this session's merged worktree over "1 commit",
    PR 93's head, already in main, because it compares against the branch the session started from.
    The skill passes `discard_changes: true` only where the worktree read `CLEAN` at the merged tip.
  - A session worktree that holds the snapshot here goes only on the third answer, because removing
    the worktree deletes the snapshot.
  - **Reviews (2026-11-03).** The plugin validator found that a commit made in the worktree after the
    plan still read `CLEAN`, because its branch reaches it, and `discard_changes: true` would delete
    it. `worktree-state.py --expect-head <sha>` now reads `MOVED` for it, and both removal steps
    re-read with the merged tip just before acting. The skill's list of allowed git verbs also gained
    `worktree remove`. The skill reviewer found more:
    - `ls-files` without `-z` quoted a non-ASCII folder name and missed the repository nested inside.
    - `--all` counted the worktree's own `refs/worktree/*`, which the removal deletes.
    - A snapshot was retired before a removal that could still be refused.
    - An ignored `.env` went with the worktree unannounced.
    - A `HIDDEN` worktree was listed with the very command that deletes its findings.
    - A worktree another session holds, recreated at the same path, could be removed.

    Each is fixed with a test or fixture. A worktree `git worktree list` marks `locked` is held, except
    the one Claude Code locks for this session.
- **A clean worktree goes whoever made it (the developer's answer, 2026-11-05).** This widens slice
  05's "a worktree this session made". `/phil:done 98` listed the worktree its own session ran in,
  because an earlier session had cut it and this one resumed there, as `/phil:start` then
  `/phil:resume` does. The developer asked why it did not just remove it.
  - **A worktree goes where all three hold**: it has a candidate's branch checked out at the merged
    tip, `worktree-state.py` reads it `CLEAN`, and `git worktree list` marks it unlocked. Who made it
    no longer counts. The one lock that is no bar is the one Claude Code holds on a worktree
    `EnterWorktree` made in this session, because `ExitWorktree` releases it. Any other lock holds the
    worktree and its snapshot (fixtures 50 and 51), since git refuses a locked worktree without
    `--force`. A session that started in a worktree saw no lock on it: card 98's read unlocked, live.
  - **The worktree the session runs in** goes last: through `ExitWorktree` where `EnterWorktree` made
    it in this session, otherwise through `git worktree remove`. Run live 2026-11-05 with git
    2.53.0, git removed the directory the shell stood in, exit 0, and the next call ran from the main
    checkout; `ExitWorktree` does nothing for a worktree it did not make.
  - **What stays unchecked**: what no check reads, such as an editor's unsaved buffer or a terminal
    open in the directory. The plan names each worktree it removes, so the developer's one yes
    covers it. Fixtures 23 and 29 now expect the removal they once forbade.
  - **Reviews (2026-11-05).** The plugin validator found the command and `SKILL.md` saying "unlocked"
    while Claude Code locks the worktree `EnterWorktree` makes, a locked worktree's snapshot still
    retired, and a fixture guard that checked nothing. The skill reviewer found that step 6 removed the
    session's worktree with its snapshot unretired, and that step 2 retired a snapshot before checking
    for a new lock. Each is fixed, with a test or a fixture.
- **Upstream changes:** see Changed Assumptions.
