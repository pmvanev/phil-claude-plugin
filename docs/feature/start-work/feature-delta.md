# Feature Delta — start-work (`/phil:start`)

> Single narrative file for the feature. DISCUSS findings live here as
> `## Wave: DISCUSS / [REF|WHY|HOW]` sections. Machine artifacts: `slices/slice-NN-*.md`.
> SSOT updates: `docs/product/jobs.yaml` (new job), `docs/product/journeys/start-work.yaml` (new
> journey), `docs/product/personas/kai-session-relay.yaml` (facet added).
> Board: issue 80 (slices 01–03, closed); issue 98 (slice 04, GitLab), In Progress.
> Build path: DISCUSS only — the deliverable is prose (CLAUDE.md, edd-loop DDD8).

---

## Wave: DISCUSS / [REF] Source

Issue 80 asks for the command that picks a card up, as `/phil:done` puts one down. Starting a card
takes four steps by hand before any work begins: find the card, set Status to In Progress, assign it,
and cut a branch and a worktree. Then the agent picks how to work it by habit rather than from the card.

Measured on this repo, 2026-11-02, by starting issue 80 itself by hand in one session:

- **Five forge and git calls before the first line of work**: a whole-board GraphQL read to find the
  card's project item id, a Status mutation carrying three ids copied from CLAUDE.md, an assign, a
  read-back of both, and a worktree.
- **The ids live only in CLAUDE.md's board block.** A consumer repo without that block, or a
  `phil:board-setup` run, has no way to write Status without probing first.
- **The route came from CLAUDE.md, not from habit, only because the session read it.** CLAUDE.md sends
  a new command through `nw-discuss`; nothing in the plugin would have said so.

Three facts shape the design:

- **`/phil:done` names the developer by the signed-in forge account** (`viewer { login }`), never by
  git's `user.name`, which holds a display name.
- **`/phil:done` finds a card's worktrees by branch, never by folder.** It lists the worktrees checked
  out on the head branches of the card's merged pull requests. Where the worktree lives does not change
  what `/phil:done` finds.
- **Claude Code's worktree tool branches from a fresh default branch and moves the session in.**
  This session started issue 80 that way. The branch it cut is `worktree-issue-80-phil-start`: the tool prefixes
  every branch with `worktree-`.

## Wave: DISCUSS / [REF] Persona & Job

- **Persona:** `kai-session-relay`, with a pick-up facet. Kai owns the session boundary; this is the
  boundary at the start of the work, where `/phil:done` crosses it at the end.
- **JTBD one-liner:** *When I choose the next card, claim it on the board and land in a clean worktree
  with the card explained and a route recommended — without taking someone else's card or restarting
  finished work — so the first minute goes to the work, not the ceremony.*
- **Job ID:** `pick-up-the-next-card` (new).

## Wave: DISCUSS / [REF] Feature type & framing

- **Feature type:** developer tool, user-facing — the developer invokes `/phil:start` and reads its
  report.
- **Greenfield command** in a brownfield plugin: a new `commands/start.md` and `skills/start/`. It
  composes `phil:issue-board` (board write order), the repo's board block or a `phil:board-setup` run
  (the Status ids), and Claude Code's worktree tool.
- **Research depth:** lightweight — happy path plus the error paths in the journey.

## Wave: DISCUSS / [REF] Locked decisions

The developer answered D1 and D2 on 2026-11-02; the rest follow from those answers, the card and the
plugin's existing rules.

- **[D1] Claude Code's worktree; the session moves in.** *(Developer's answer.)* `/phil:start` creates
  the worktree with Claude Code's own worktree tool, named `issue-<n>-<slug>`, so its branch is
  `worktree-issue-<n>-<slug>`. The tool branches from the remote default branch, and `/phil:start`
  fetches first. The session works in the worktree from then on; quitting asks whether to keep it.

- **[D2] A card already underway is handed to `/phil:resume`.** *(Developer's answer.)* A card is
  underway when it has a worktree, an open pull request by the developer naming it, or a handoff
  snapshot in its worktree. `/phil:start` still claims it (D5, D6) and enters its existing worktree,
  then says the card is underway, names `/phil:resume` as the next step, and launches nothing. It never
  cuts a second worktree for a card that has one.

- **[D3] A worktree is the card's when `/phil:start` named it, or when it holds the card's branch.**
  A worktree under `.claude/worktrees/` whose name starts `issue-<n>-` is the card's, and so is one
  checked out on the head branch of the developer's open pull request that names the card. `/phil:start`
  lists several candidates with their branches, and the developer picks one. Reuse destroys nothing, so a
  name match suffices here, where `/phil:done` (D8) refuses it for deletion.

- **[D4] The argument resolves to exactly one open card, or the developer chooses.** A number names a
  card directly. `/phil:start` searches open cards for a title or description, and lists several
  matches by number and title for the developer to pick. With no match it says so and offers to file a
  card in the developer's words, filing it only on a yes (slice 02). It never picks among matches.

- **[D5] The developer is the signed-in forge account, named in the report.** `/phil:start` assigns
  the issue to `viewer { login }`, as `/phil:done` identifies the developer. It reports a missing
  signed-in account, or one the forge will not assign, and assigns nothing. It never matches git's
  `user.name` against a login.

- **[D6] Someone else's card stays theirs.** For a card assigned to another account, `/phil:start`
  names that login and asks before adding the developer. It never removes an assignee.

- **[D7] Finished work is never restarted silently.** `/phil:start` refuses a closed card and names
  `gh issue reopen` for the developer to run. An open card in Done is the defect CLAUDE.md names; the
  report states it and asks before moving the card to In Progress.

- **[D8] Claim in the order `phil:issue-board` requires, and read both back.** Add the card to the
  board if it is missing, write Status=In Progress, assign it, then read Status and assignees back. The
  Status field and option ids come from the repo's board block; with no block, `/phil:start` names
  `phil:board-setup` and writes no Status.

- **[D9] It recommends a route and launches none.** The recommendation names one route — an nWave
  wave, `phil:edd`, `phil:work` or inline — with its reason and the command that owns it. The
  repo's recorded build path comes first (here, CLAUDE.md sends a new command through `nw-discuss`).
  Then the card's `wave:` label and the nWave artifacts on disk, then whether users would see the
  change (`phil:edd`) or not (`phil:work`), then size: a card that fits one sitting goes inline.

- **[D10] The description states the card; it does not invent one.** In plain English: what the card
  asks for, how anyone will know it is done, and what it leaves open — each drawn from the card. A card
  with no way to tell when it is done says so and names `phil:groom-ask`; `/phil:start` never supplies
  the missing criterion. The description and the report follow `rules/writing.md`; the skill names the
  standard, and a test fails without the citation.

- **[D11] `commands/start.md` declares `mutates: true`** — it writes to the forge and git
  (`scripts/check-readonly-commands.py`).

## Wave: DISCUSS / [REF] User stories

### Story 1 — Name the card, get the right one *(slice 01)*
`job_id: pick-up-the-next-card`

As **Kai**, I want to name a card by number, title or a few words and have `/phil:start` settle on
exactly one open card or ask me, so I never start the wrong card or one that is already finished.

### Elevator Pitch
Before: I scroll the board for the card's number, and nothing stops me starting a closed card or a teammate's.
After: run `/phil:start worktree` → sees `3 open cards match: 80 /phil:start — …, 76 /phil:autopilot — …, 75 /phil:done — … Which one?`
Decision enabled: I pick the card I meant, or learn that the one I meant is closed or someone else's.

**Acceptance criteria**
- AC1.1 — Given an argument matching several open cards, then `/phil:start` lists each with number
  and title, asks, and writes nothing until the developer picks.
- AC1.2 — Given an argument matching no open card, then it says so and offers to file one, filing
  nothing without a yes.
- AC1.3 — Given a closed card, then it refuses and names `gh issue reopen`; given an open card in
  Done, then it reports the defect and asks.
- AC1.4 — Given a card assigned to another account, then it names that login and asks before adding
  the developer.

### Story 2 — Know what the card asks and how to work it *(slice 01)*
`job_id: pick-up-the-next-card`

As **Kai**, I want the card restated in plain English with a route recommended and its reason, so the
session works the card the way this repo works cards, not by habit.

### Elevator Pitch
Before: the agent reads the card and starts coding inline, and the repo's build path is skipped unless someone remembers it.
After: run `/phil:start 80` → sees `ASKS: a command that claims a card … DONE WHEN: six behaviours pinned by fixtures … OPEN: 5 questions` then `ROUTE: nw-discuss — CLAUDE.md sends a new command through it. Run /nw-discuss? yes / no`.
Decision enabled: I take the recommended route, pick another, or fix a card that says too little.

**Acceptance criteria**
- AC2.1 — Given any card, then the report names one route, its reason and its owning command, and
  launches nothing without a yes.
- AC2.2 — Given a repo whose CLAUDE.md records a build path for the card's kind of work, then the
  recommendation follows it and cites it.
- AC2.3 — Given a card with no way to tell when it is done, then the description says so and names
  `phil:groom-ask`, and supplies no criterion of its own.
- AC2.4 — Given `skills/start/SKILL.md` without its `rules/writing.md` citation, then a test fails.

### Story 3 — Claim the card on the board *(slice 02)*
`job_id: pick-up-the-next-card`

As **Kai**, I want the card moved to In Progress and assigned to me, both read back, so the board
tells a teammate the card is taken.

### Elevator Pitch
Before: I copy three ids out of CLAUDE.md into a GraphQL mutation, assign the card, and hope both stuck.
After: run `/phil:start 80` → sees `CLAIMED: Status In Progress, assigned to pmvanev — read back`.
Decision enabled: I start work knowing nobody else will pick this card up.

**Acceptance criteria**
- AC3.1 — Given a card not on the board, then it is added before its Status is written.
- AC3.2 — Given a claim, then Status and assignees are read back, and a mismatch is reported.
- AC3.3 — Given no signed-in forge account, or one the forge will not assign, then the report says so
  and assigns nothing.
- AC3.4 — Given a repo with no board block, then `/phil:start` names `phil:board-setup` and writes no
  Status.
- AC3.5 — Given the developer said yes to filing a card (AC1.2), then the card is filed in the
  developer's words and claimed.

### Story 4 — Land in a worktree ready to work *(slice 03)*
`job_id: pick-up-the-next-card`

As **Kai**, I want the session moved into a worktree cut from a fresh default branch — or into the
card's existing one, handed to `/phil:resume` — so the work starts isolated and nothing is cut twice.

### Elevator Pitch
Before: I cut a branch and a worktree by hand, from whatever main I last pulled, and may cut a second for a card I already started.
After: run `/phil:start 80` → sees `WORKTREE: .claude/worktrees/issue-80-phil-start on worktree-issue-80-phil-start, from origin/main at 86100a7 — session moved in`, or `UNDERWAY: worktree issue-80-phil-start has a handoff snapshot — next: /phil:resume`.
Decision enabled: I start the recommended route here, or resume where I left off.

**Acceptance criteria**
- AC4.1 — Given a card with no worktree, then the session moves into a new one cut from the freshly
  fetched default branch, and the report names its path, branch and base commit.
- AC4.2 — Given a card with a worktree, then the session enters it and no second worktree is cut.
- AC4.3 — Given a card underway (D2), then the report names `/phil:resume` as the next step and
  recommends no other route.
- AC4.4 — Given a session already inside another worktree, then `/phil:start` reports it and moves
  the session only on a yes.

## Wave: DISCUSS / [REF] Outcome KPIs

| KPI | Target | Measurement |
|---|---|---|
| Never the wrong card | 0 starts on a card the developer did not pick, when the argument matched several | fixture |
| Never finished work | 0 closed cards restarted; 0 cards in Done moved without a yes | fixture per kind |
| Never someone else's | 0 assignees added over another's without a yes; 0 removed | fixture |
| No second worktree | 0 worktrees cut for a card that has one | fixture; dogfood |
| Route launched only on a yes | 0 routes launched unasked | fixture |
| One command to the first line of work | a clean start runs from `/phil:start <n>` to working in the worktree with one question: the route | dogfood transcript |
| Applied, not cited | removing the `rules/writing.md` citation fails a test | pytest, watched red first |

## Wave: DISCUSS / [REF] Out of scope

- GitLab, in slices 01–03. `phil:issue-board` covers it, but v1's fixtures and dogfood are GitHub
  only. Slice 04 adds it (issue 98).
- Choosing which card to start. `phil:board-snapshot` and `phil:rank-issues` own the order;
  `/phil:start` takes the card it is given.
- Changing `/phil:resume`. A card underway is handed to it as it stands.
- Issue 76's autopilot, which will call `/phil:start`; its open questions stay on its card.
- Moving a card to a plain git worktree outside Claude Code (D1).

## Wave: DISCUSS / [REF] Driving ports & prerequisites

- **Driving port:** `/phil:start <number, title or description>`. Later, issue 76's autopilot.
- **Driven ports:** `gh` (search, the issue, assignees, the project's Status field, `viewer`), `git`
  (fetch, worktree list), Claude Code's worktree tool, the repo's CLAUDE.md (build path, board block).
- **Prerequisites:** `phil:issue-board`'s board write order, and the repo's board block or a
  `phil:board-setup` run for the Status field and option ids.

## Wave: DISCUSS / [REF] Walking-skeleton strategy

Slice 01 is the skeleton: `/phil:start` runs end to end — resolves the card, applies the refusals,
describes it and recommends a route — writing nothing. Slices 02 and 03 add the writes behind it.

## Wave: DISCUSS / [REF] Scope Assessment

**PASS (right-sized).** Four stories across three slices; one new command and skill; no change to an
existing skill; no new script.

## Wave: DISCUSS / [REF] Definition of Done

1. `commands/start.md` and `skills/start/SKILL.md` exist, authored after reading
   `plugin-dev:command-development` and `plugin-dev:skill-development`.
2. Every story traces to `pick-up-the-next-card`.
3. Every story has an Elevator Pitch with a real entry point and observable output.
4. Fixtures pin issue 80's six behaviours: an ambiguous argument lists candidates; another's card
   stays theirs; a closed or Done card is never restarted silently; a missing or unassignable account
   is reported, never guessed; a card with a worktree reuses it; the recommendation launches nothing.
5. Every new citation and gate has a test, watched red first.
6. `python3 -m pytest -q` and `scripts/check-invariants.py` pass.
7. `/phil:harden-instructions` over the command, the skill and its references; `phil:eos` over this
   file, its slice briefs and the SSOT entries; `plugin-dev:skill-reviewer` and
   `plugin-dev:plugin-validator` over the command and skill — then the tests again.
8. Dogfood: `/phil:start` starts the next card on this board.
9. `/phil:done` finds and lists the worktree `/phil:start` cut, by its branch.

## Wave: DISCUSS / [REF] Definition of Ready — validation

| # | DoR item | Status | Evidence |
|---|---|---|---|
| 1 | Job traceable | ✅ | `pick-up-the-next-card` in `jobs.yaml`; all 4 stories carry it |
| 2 | Persona defined | ✅ | `personas/kai-session-relay.yaml`, pick-up facet |
| 3 | Journey mapped | ✅ | `journeys/start-work.yaml`, with error paths |
| 4 | Elevator pitches | ✅ | all 4 stories, `/phil:start` entry point, observable output |
| 5 | ACs testable | ✅ | Given-When-Then, fixture- or pytest-checkable |
| 6 | Slices ≤1 day with a learning hypothesis | ✅ | `slices/slice-01` … `slice-03` |
| 7 | Walking skeleton | ✅ | slice 01, read-only |
| 8 | Outcome KPIs with targets | ✅ | table above |
| 9 | Scope right-sized | ✅ | Scope Assessment above |

Requirements completeness: each of issue 80's six steps, six fixture behaviours and five open
questions maps to a decision and an AC.

## Wave: DISCUSS / [REF] Changed Assumptions

DISCOVER and DIVERGE never ran; the changed assumptions are issue 80's own, as written on 2026-11-02.

- Step 3: "Assigns the issue to the forge account of the current git user".

  **New:** the signed-in forge account (D5). **Why:** git's `user.name` holds a display name that no
  forge resolves to a login, and `/phil:done` already names the developer by the signed-in account.

- Fixture behaviour 4: "a git user with no matching forge account is reported, never guessed".

  **New:** no signed-in account, or one the forge will not assign, is reported (AC3.3). **Why:** with
  D5 there is no git user to match.

- Step 4: "Creates a branch and a worktree for the issue, named from its number and title".

  **New:** the worktree is named from them; the branch carries Claude Code's `worktree-` prefix (D1).
  **Why:** the developer chose Claude Code's worktree, and the tool sets the prefix.

## Wave: DISCUSS / [REF] Decisions summary (for authoring)

- **Key decisions:** D1 Claude Code's worktree, session moves in · D2 underway goes to `/phil:resume`
  · D3 a worktree is the card's by its name or its branch · D4 one card or the developer chooses · D5
  the signed-in account · D6 another's card stays theirs · D7 finished work never restarted silently ·
  D8 board order, read back · D9 one route, launched only on a yes · D10 describe the card, invent
  nothing · D11 `mutates: true`.
- **Requirements summary:** `/phil:start` resolves its argument to one open card, refuses finished or
  someone else's work unasked, claims the card and reads the claim back, moves the session into a fresh
  or existing worktree, restates the card and recommends how to work it.
- **Constraints:** never picks among matches; never removes an assignee; never restarts a closed
  card; never cuts a second worktree; never launches a route unasked.
- **Settled at slice 01 authoring (2026-11-03):**
  - One GraphQL query reads the card and `viewer` through `issueOrPullRequest`. A pull request's
    number, or a number that names nothing (`NOT_FOUND`), is no match.
  - A search that matches more than 20 open cards asks for narrower words rather than offering part of
    the list.
  - Authoring refined D9's rules: a build path is a rule that names a command or skill to run, and a step that has
    already run gives way to the rule's next step. A `wave:` label routes by `phil:nwave-issue-board`'s
    table, and a card with no label goes on to rule 3. Inline needs exactly one done-when item the card
    states and nothing open.
  - The run prints its outcome, then launches through the `Skill` tool. Inline ends the skill, and the
    session works the card outside the command's grant. A route the developer names under Other
    launches with `ROUTE-OVERRIDDEN`, the evidence the learning hypothesis needs.
  - A run that cannot begin — no forge line, GitLab, a failed read — reports `CANNOT-RUN`.
  - Slice 01 does not detect a card already underway; slice 03 adds that check (D2).
- **Settled at slice 02 authoring (2026-11-03):**
  - Running `/phil:start` is the developer's yes to the claim; the route asks its own. A go-on answer
    at CHECK is the yes to moving a card out of Done or adding the developer beside another assignee.
  - Run live on issue 80, whose claim was already in place: `gh project item-add --format json` prints
    the item, `item-edit` prints nothing, and an unknown login makes `gh issue edit --add-assignee`
    exit 1 with `Could not resolve to a user or bot`. The read-back stays the evidence.
  - A write that would change nothing is skipped, so a card already claimed reports `CLAIMED` and
    `WROTE-NOTHING` together.
  - The claim stops at the first failed board write — the item add or the Status — and reads the card
    back once before reporting it; the run still describes and routes the card. The assign is no board
    write: one that fails, or exits 0 and does not hold, is `NOT-ASSIGNED`.
  - The read-back checks only the writes that ran, plus every assignee the card already had, so a
    removed assignee reads back as `READ-BACK-MISMATCH`.
  - A card in Blocked asks before the claim moves it, as a card in Done does.
  - With no signed-in account every read fails, so AC3.3's first half is `CANNOT-RUN`, naming
    `gh auth login`.
  - A filed card carries the developer's title and an empty body, so the skill composes no prose on the
    board; DESCRIBE then reports `NO-DONE-WHEN`. Once a card is filed, no failure reads as `CANNOT-RUN`.
  - The claim's procedure lives in `skills/start/references/claim.md`, which keeps the skill under
    3,000 words.
- **Settled at slice 03 authoring (2026-11-03)**, by a headless probe on Claude Code 2.1.317 against a
  throwaway repo one commit behind its remote:
  - A command drives `EnterWorktree`: the call ran in the default permission mode with no denial, and
    ran again with the grant removed. The grant declares the tool rather than enables it.
  - **Corrected the same day:** the probe showed the tool fetching, and the conclusion drawn — that
    `/phil:start` needs no fetch — was wrong. The probe's clone had never fetched. Claude Code
    2.1.317's source, read after plugin-validator flagged it, fetches only when the last fetch is a day
    old (`P$r=86400000`, a 5-second timeout), and otherwise branches from the local
    `origin/<default>`. So D1 holds as written: `/phil:start` runs `git fetch origin <default>` before
    the cut, then checks the base against the remote's head as GitHub reports it, and reads
    `worktree.baseRef` from the settings where the two differ.
  - The tool cannot create a worktree from inside another worktree session; a move out of one leaves it
    with `ExitWorktree` and `keep` first. A worktree another live session holds reads
    `locked claude session <name> (pid …)`, and `/phil:start` asks before entering it.
  - A card underway still gets its claim, then enters its worktree and ends `UNDERWAY`, naming
    `/phil:resume`. An open pull request with no worktree on this machine cuts nothing.
  - A card underway is one with a worktree, the developer's open pull request naming it, or a surviving
    `worktree-issue-<n>-*` branch; a `prunable` entry is not the card's. A session already in the card's
    worktree moves nowhere. Any `locked` worktree asks before entering.
  - The worktree procedure lives in `skills/start/references/worktree.md`, read whole at CHECK's step 4,
    and ROUTE's rules moved to `references/route.md`; the skill body is 2,541 words.

---

## Wave: DISCUSS / [REF] Slice 04 — GitLab (issue 98)

### Source

Issue 98 asks for `/phil:start` on GitLab. Today a GitLab forge line ends the run with `CANNOT-RUN`,
and on 2026-11-03 CLAUDE.md started asking every surface that drives issues, boards, branches or
worktrees to support both forges. `/phil:done` already does, through `skills/done/references/gitlab.md`.

Four facts shape the slice, read on 2026-11-03 with `glab` 1.112.0 unless the fact names its source:

- **A bare `--assignee` replaces the card's assignees.** `glab issue update --help`: "Prefix with '!'
  or '-' to remove from existing assignees, or '+' to add new. Otherwise, replace existing assignees".
  Ported as written, the GitHub assign would remove a teammate and exit 0, breaking D6.
- **A GitLab column is a label, and its name is its only id.** modive's hand-written block lists
  `status::to-do / status::in-progress / status::blocked` and says to close a finished issue rather
  than label it. `phil:board-setup`'s GitLab block records the status family, not which label is
  which column.
- **GitLab has no board item to add.** A GitLab board is a view over labels, so the label write alone
  moves the card into its column (`phil:issue-board`).
- **Issue and merge-request numbers are separate.** `projects/<p>/issues/99999` answers
  `404 Not found`, and a number names an issue or nothing, never a merge request. Read live against
  modive as `pvanevery`: an issue carries `state`, `labels` and `assignees[].username`, and
  `merge_requests?state=opened&author_username=<login>` lists the developer's open merge requests.

### Locked decisions

The developer answered D12 on 2026-11-03. The others follow from that answer, the facts above and
`/phil:done`'s GitLab reference.

- **[D12] Match the status label by name; ask when the match is unclear.** *(Developer's answer.)*
  Within the status family the board block lists, In Progress is the label whose value reads
  `in-progress`, `in progress` or `doing`. Blocked reads `blocked`, and Done reads `done`. Where none
  or several labels match In Progress, ask which label to use, and write no status label until the
  developer answers. Nothing records the answer, so the next run asks again.
- **[D13] The claim is one label swap.** Add the In Progress label and remove every other status
  label the card carries, in one `glab issue update --label … --unlabel …`, on every tier: Premium
  drops a scoped sibling server-side, and Free drops nothing (`phil:issue-board`). The claim runs no
  `item-add`. A block that lists no status family is `NO-BOARD-BLOCK`; the run still assigns.
- **[D14] Assign with `--assignee +<login>`, never a bare login.** The read-back checks every login the
  card already had, so a replaced assignee reads back as `READ-BACK-MISMATCH`.
- **[D15] On GitLab, Done is the closed list.** A closed card is `REFUSED-CLOSED`, naming
  `glab issue reopen <n> -R <repo>`. An open card carrying a status label that reads done is
  `OPEN-IN-DONE`. A family with no done label never fires that check. A label that reads blocked asks,
  as Blocked does on GitHub.
- **[D16] Every call names its target, and `glab api` sends GETs only.** Pass
  `-R https://<host>/<group/project>` to `glab issue` and `--hostname <host>` to `glab api`, and write
  the project URL-encoded in each path, as `skills/done/references/gitlab.md` does. The developer is
  `user`'s `username`. With no signed-in account, name `glab auth login --hostname <host>`.
- **[D17] A number names an issue.** A 404 is `NO-MATCH`. Fixture 10's pull-request case has no
  GitLab counterpart.
- **[D18] Underway reads merge requests.** Search the developer's open merge requests for the card
  pattern `/phil:done` uses, and report each as `!<n>`. Read the remote's head from
  `projects/<p>/repository/branches/<default>`. The fetch, the cut, the entry and the lock ask stay
  as they are.
- **[D19] Filing passes only the developer's title and an empty body**, through `glab issue create`
  with `-R`, `--title`, `--description ''` and `--yes`. The empty description is unverified; settle
  it at authoring.
- **[D20] The GitLab calls live in `skills/start/references/gitlab.md`**, read whole before RESOLVE
  wherever the forge line names GitLab. `SKILL.md` governs it, and the reference adds no outcome
  token. `commands/start.md` adds `glab api`, `jq`, `glab issue create` and `glab issue update` to its
  grant, and limits `glab issue update` to the status labels and `--assignee +<login>`.
- **[D21] The report keeps its lines and names labels in place of Status.** For example:
  `CLAIMED: status::in-progress set, status::to-do removed, assigned to pvanevery — read back`.

### Story 5 — Start a card on GitLab *(slice 04)*
`job_id: pick-up-the-next-card`

As **Kai** on a GitLab repo, I want `/phil:start` to claim the card, land me in its worktree and
recommend a route, so the first minute goes to the work on either forge.

### Elevator Pitch
Before: on modive, `/phil:start 58` stops with `CANNOT-RUN`, and I swap labels, assign the card and cut a worktree by hand.
After: run `/phil:start 58` in modive → sees `CLAIMED: status::in-progress set, status::to-do removed, assigned to pvanevery — read back`, then the WORKTREE, ASKS, DONE WHEN, OPEN and ROUTE lines.
Decision enabled: I take the recommended route, pick another, or fix a card that says too little, as on GitHub.

**Acceptance criteria**
- AC5.1 — Given a GitLab forge line and an open card in `status::to-do`, then the run swaps the card to
  `status::in-progress`, assigns the developer, reads both back, cuts a worktree and recommends a
  route, ending in a terminal the GitHub skill defines.
- AC5.2 — Given a card assigned to another account and a go-on answer, then the developer is added
  with `+<login>`, and the read-back finds both logins.
- AC5.3 — Given a status family where no label, or several labels, read in-progress, then the run asks
  which label to use before the claim, and writes no status label without an answer.
- AC5.4 — Given a closed card, then the run refuses it and names `glab issue reopen`. Given a blocked
  label, then it asks before the claim. Given an open card with a done label, then it reports
  `OPEN-IN-DONE` and asks.
- AC5.5 — Given the developer's open merge request naming the card, then the run ends `UNDERWAY`,
  names `!<n>` and cuts nothing.
- AC5.6 — Given a block that lists no status family, then the run reports `NO-BOARD-BLOCK`, writes no
  label and still assigns.
- AC5.7 — Given no match and a yes to filing, then the run files the card with the developer's title
  and an empty body, and claims it.
- AC5.8 — Given any GitLab path, then no run ends `CANNOT-RUN` because the forge is GitLab.
- AC5.9 — Given any GitLab fixture, then it forbids a bare `-R <group/project>`, a field or method on
  `glab api`, a bare `--assignee` and a board list.

**Fixtures** (`skills/start/self-test/`): 48 `gitlab-claim-cut-fresh` (AC5.1) · 49
`gitlab-another-assignee-kept` (AC5.2) · 50 `gitlab-no-in-progress-label` (AC5.3) · 51
`gitlab-closed-card` (AC5.4) · 52 `gitlab-blocked-label` (AC5.4) · 53
`gitlab-merge-request-underway` (AC5.5) · 54 `gitlab-no-status-family` (AC5.6) · 55
`gitlab-filed-on-a-yes` (AC5.7). Each forbids AC5.9's four.

### Outcome KPIs

| KPI | Target | Measurement |
|---|---|---|
| GitLab is no reason to stop | 0 GitLab runs end `CANNOT-RUN` because of the forge | fixtures 48–55 |
| Another's card stays theirs on GitLab | 0 assignees replaced by a bare `--assignee` | fixture 49; dogfood read-back |
| No guessed column | 0 status labels written when none or several match | fixture 50 |
| Same report on both forges | 0 outcome tokens added by `references/gitlab.md` | review of the diff |
| One command to the first line of work | modive's top to-do card starts with one question: the route | dogfood transcript |

### Scope assessment

**PASS (right-sized).** One story and one slice. The slice adds one reference file and eight fixtures,
and changes the command's grant and the skill's two GitLab lines. It adds no script and changes no other
skill.

### Definition of Done (slice 04)

1. `skills/start/references/gitlab.md` exists, written after reading `plugin-dev:skill-development`
   and `plugin-dev:command-development`; `SKILL.md` and `commands/start.md` name it.
2. Fixtures 48–55 exist, and `tests/test_start_fixtures.py` passes over them.
3. `python3 -m pytest -q` and `scripts/check-invariants.py` pass.
4. `/phil:harden-instructions` over the command, the skill and the new reference; `phil:eos` over this
   section and the slice brief; `plugin-dev:skill-reviewer` and `plugin-dev:plugin-validator` over the
   command and the skill. Then run the tests again.
5. Dogfood on modive, naming the plugin version it ran against.
6. Bump the plugin version.

### Definition of Ready — validation

| # | DoR item | Status | Evidence |
|---|---|---|---|
| 1 | Job traceable | ✅ | Story 5 carries `pick-up-the-next-card`; the job is unchanged |
| 2 | Persona defined | ✅ | `kai-session-relay`, pick-up facet |
| 3 | Journey mapped | ✅ | `journeys/start-work.yaml`; slice 04 adds a GitLab error path to `claim` |
| 4 | Elevator pitch | ✅ | Story 5: `/phil:start 58` in modive, the claim line |
| 5 | ACs testable | ✅ | AC5.1–AC5.9, each pinned by a fixture or the suite |
| 6 | Slice ≤1 day with a learning hypothesis | ✅ | `slices/slice-04-gitlab.md` |
| 7 | Walking skeleton | ✅ | slices 01–03 shipped; slice 04 extends a running command |
| 8 | Outcome KPIs with targets | ✅ | table above |
| 9 | Scope right-sized | ✅ | Scope assessment above |

Requirements completeness: each of issue 98's five *What changes* items and three *Done when* items
maps to a decision and an AC. Resolve maps to D16, D17 and D19; Check to D15 and D18; Claim to D12,
D13 and D14; Worktree to D18; the fixtures to AC5.9.
