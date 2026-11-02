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
- GitLab. `phil:issue-board` covers it, but v1's fixtures and dogfood are GitHub only.
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
- **Upstream changes:** see Changed Assumptions.
