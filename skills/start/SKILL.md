---
name: start
description: >-
  This skill should be used when the user asks to "start card N", "start issue N", "work on #N", "pick
  up the card about X", "what does this card ask and how should I work it", or runs /phil:start. It
  resolves the argument to one open GitHub card, refuses a closed one, asks before one in Done or someone
  else's, claims it, moves the session into its worktree, restates it, and recommends one route,
  launched only on a yes. A card underway goes to /phil:resume. Not for choosing which card to start.
---

# Start — pick a card up

`/phil:done` puts a card down finished. This skill picks one up: it settles on exactly one open card,
refuses finished work and asks before someone else's, claims the card on the board, moves the session into
the card's worktree, restates it in plain English, and recommends how to work it — the way the repo
records, not by habit. A card already underway goes to `/phil:resume` instead of a route.

**Running `/phil:start` is the developer's yes to the claim and the worktree; the route needs its own.**

## Inputs

- **The argument** — a number, an issue URL, a title, or a few words of description. With none, ask
  which card to start; never infer it from the branch. No answer is `CANNOT-RUN`.
- **The repo** — the forge line in the working tree's `CLAUDE.md`; `git rev-parse --show-toplevel` finds
  the root. Pass `-R <owner/repo>` on every `gh issue` call, and pass the owner and repo as variables to
  every `gh api graphql` query, which takes no `-R`: an inferred remote reads the wrong repo's issues
  successfully (`phil:issue-board`). With no forge line, name `/phil:board-setup`: `CANNOT-RUN`. On a
  GitLab forge line, say this skill covers GitHub only: `CANNOT-RUN`.
- **The board constants** — from the board lines `/phil:board-setup` writes into `CLAUDE.md`, its
  `Board:` and `Columns:` lines: the project's id and number, its owner from the board URL, the `Status`
  field id and the `In Progress` option id. Read them; never probe for them. With no board lines, or
  lines missing any of these, read Status from every project the card is on, and say no board block was
  found.
- **The developer** — the signed-in account, `viewer.login`, never git's `user.name`: a display name no
  forge resolves to a login. With no signed-in account, name `gh auth login`: `CANNOT-RUN`.

Run `git` only for `rev-parse`, `worktree list --porcelain` and `fetch origin <default>`. A `gh` call that fails for any reason but `NOT_FOUND` —
auth, network, rate limit — before CLAIM and before any filing is `CANNOT-RUN`, quoting the error. Where
any `gh` error names a missing `project` scope, name `gh auth refresh -s project`.

**This skill composes no prose on the board.** A filed card's title is the developer's words and its body
is empty; the claim writes a board item, a Status and an assignee, and no comment. It applies no writing
standard on the board for that reason.

## Asking

**Every ask this skill puts follows `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`.** Load it
before the first ask. Put card numbers, logins, commands and paths in the context block above the
question, and describe them in plain words in the question and its options: a strict repo's hook refuses
an issue number or a path there.

## RESOLVE — exactly one open card, or the developer chooses

A number, with or without `#`, names a card directly; so does an issue URL in this repo. A URL in another
repo is `NO-MATCH`, naming that repo. Read the card and the developer in one query:

```bash
gh api graphql -f query='
query($o:String!,$r:String!,$n:Int!){
  viewer{ login }
  repository(owner:$o,name:$r){
    issueOrPullRequest(number:$n){ __typename
      ... on Issue{ number title body state url
        assignees(first:10){ nodes{ login } } labels(first:20){ nodes{ name } }
        projectItems(first:10){ nodes{ id project{ id title } fieldValueByName(name:"Status"){
          ... on ProjectV2ItemFieldSingleSelectValue{ name } } } } } } } }' \
  -f o=<owner> -f r=<repo> -F n=<n>
```

A `PullRequest` is no card: say the number names a pull request: `NO-MATCH`. A number that names
nothing makes `gh` exit 1 with a `NOT_FOUND` error: `NO-MATCH`.

Search any other argument against the open cards' titles and bodies. Strip the qualifiers that would
change the search's scope — `is:`, `repo:`, `org:`, `user:`, `in:`, `state:` — and escape each `'`:

```bash
gh api graphql -f query='
query($q:String!){ search(query:$q, type:ISSUE, first:20){ issueCount
  nodes{ ... on Issue{ number title } } } }' \
  -f q='repo:<owner>/<repo> is:issue is:open <argument> in:title,body'
```

- **One match** — read it with the number query.
- **More than 20 matches** — `issueCount` over 20 means the query returned only the first 20: say how
  many matched and ask for narrower words. No answer is `STOPPED`.
- **Several matches** — list every one by number and title above the question, and ask which the
  developer meant; the run describes and routes nothing until the developer picks. **Never pick among
  matches**, not even the closest. Offer up to four as options, each described in plain words; the
  developer types any other number under Other. Read a pick with the number query and run CHECK on it.
  A pick reports `PICKED`; no pick is `STOPPED`.
- **No match** — say so, quoting the argument, and offer to file a card titled in the developer's words:
  the argument as typed, or the words typed under Other. File only on the developer's yes; no yes is
  `NO-MATCH`. With no board block, the offer and the report say the card will land on no board. File it
  as `${CLAUDE_PLUGIN_ROOT}/skills/start/references/claim.md` directs — `gh issue create`, then CLAIM
  adds it to the board in the same breath — and report `FILED`.

Offer filing only after a search: a number or URL that names no card is `NO-MATCH`, with no offer.

## CHECK — finished work and someone else's

Check in this order, and stop at the first stop.

1. **Refuse a closed card.** Say it is closed, name `gh issue reopen <n> -R <owner/repo>` for the
   developer to run, and stop: `REFUSED-CLOSED`. Never reopen it, and never describe or route it as
   though it were open.
2. **An open card in `Done` is a defect**: the board says finished and the forge says open. Read Status
   from the board's project item where the board block names a project; otherwise Done on any project
   counts, and the report names that project. State the defect and ask whether to go on — **go on** moves
   the card to In Progress at CLAIM, or, with no board block, leaves it in Done and says so; **stop** is
   `STOPPED`, with nothing written. Report `OPEN-IN-DONE` either way. A card in `Blocked` is no defect,
   but moving it hides the blocker: name it and ask the same way, with no outcome token of its own.
3. **Someone else's card stays theirs.** Where the card has assignees and `viewer.login` is not among
   them, name every assignee's login and ask whether to go on — **go on** adds the developer beside them
   at CLAIM; **stop** is `STOPPED`, with nothing written. Report `ANOTHERS-CARD` either way. **Never
   remove an assignee.** A card assigned to the developer, or to no one, needs no ask.
4. **A session in another worktree stays there unless the developer says otherwise.** Read
   `${CLAUDE_PLUGIN_ROOT}/skills/start/references/worktree.md` whole first, and find the card's worktrees
   as its *Find the card's worktrees* directs; a failed read there is `CANNOT-RUN`. Where
   `git rev-parse --show-toplevel` is neither the main checkout — the first entry of
   `git worktree list --porcelain` — nor one of the card's worktrees, name where the session is and ask
   whether to move it; move the session only on the developer's yes. **stop** is `STOPPED`, with nothing
   written.

## CLAIM — In Progress, assigned, read back

**Read `${CLAUDE_PLUGIN_ROOT}/skills/start/references/claim.md` whole before the first claim write.** It
holds the writes, the read-back and the claim line. In outline: add the card to the board where it is
missing, write Status = In Progress, assign `viewer.login`, then read back every write that ran — and
every assignee the card already had. It skips a write that would change nothing, stops at the first
board write that fails, and repairs nothing it reads back wrong.

## WORKTREE — the card's worktree, or a card underway

Follow `${CLAUDE_PLUGIN_ROOT}/skills/start/references/worktree.md`, read whole at CHECK's step 4. It
enters the card's worktree or cuts a fresh one with Claude Code's worktree tool, and names
`/phil:resume` for a card already underway. In outline: a card with a worktree, the developer's open pull
request or a surviving branch is underway and gets no second worktree; any other card gets the default
branch fetched, a worktree cut from it, and the session moved in.

## DESCRIBE — what the card asks, in plain English

Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing the description and the report, and apply
it to every word this run composed: active voice, no needless words, the concrete thing named. A quoted
line from the card or from `CLAUDE.md` keeps its own words.

Draw three lines from the card's title and body, and from nothing else:

- **ASKS** — the change the card asks for, in a sentence or two. Where the body has a heading containing
  *What it does*, *Scope* or *Requirements*, summarize its items.
- **DONE WHEN** — how anyone will know the card is done: its checklist items and the items under a
  heading containing *Done when* or *Acceptance criteria*, counted, each in a short phrase. Merge none
  and drop none: `/phil:done` checks these later. Where the card holds none, write
  `DONE WHEN: the card does not say`, name `/phil:groom-ask` to add it, and report `NO-DONE-WHEN`.
  Restate what the card holds, and never supply a criterion the card does not hold — not one inferred
  from the title, nor one this session would write.
- **OPEN** — what the card leaves open: the items under a heading containing *Open questions* or
  *Unknowns*, counted, each in a few words. With none, `OPEN: nothing the card names`.

Skip the generated block between `<!-- nwave:status:begin -->` and `<!-- nwave:status:end -->`: it
describes progress, not the ask.

## ROUTE — one route, its reason and its owner

A card underway takes no route: the report names `/phil:resume` and the run ends `UNDERWAY`, launching
nothing.

**Read `${CLAUDE_PLUGIN_ROOT}/skills/start/references/route.md` whole before naming a route.** It holds
the four rules, the question and the launch. In outline: the repo's recorded build path decides first,
then the card's `wave:` label, then whether a user would see the change — `phil:edd` or `phil:work` — and
a card that fits one sitting goes inline. Name one route, its reason and its owner, ask once, print the
outcome tokens, and launch only then. **Launch nothing without the developer's yes.**

## REPORT

Print the report before the route question:

```
CARD 76 · New command: /phil:autopilot — carry a card through its repo's build path, and stop only for a blocker that needs the developer · open · Todo · unassigned
CLAIMED: Status In Progress, assigned to pmvanev — read back
WORKTREE: .claude/worktrees/issue-76-new-command-phil-autopilot-carry-a-card on worktree-issue-76-new-command-phil-autopilot-carry-a-card, from 8562216 = origin/main — session moved in
ASKS: a command that carries a card through its repo's build path, stopping only for a blocker the developer must clear.
DONE WHEN: 6 items — the command and its skill exist, through nw-discuss and plugin-dev; fixtures pin that a taken recommendation is recorded on the card, a developer's decision stops the run, a blocker leaves a comment and a snapshot, a declared build path beats nWave directories, and a missing credential declaration blocks.
OPEN: 4 questions — what counts as a blocker, what marks a declared build path, where test credentials live, which recorded rules it cannot override.
ROUTE: nw-discuss — CLAUDE.md: "Run `nw-discuss` before authoring a new feature, skill or command."
```

The CARD line carries the title as the forge holds it and the state RESOLVE read, with `on no board`
where the card is on none. The claim line, then the worktree line, follow it, in shapes
`references/claim.md` and `references/worktree.md` list; the ROUTE line, a shape `references/route.md`
lists.

## Decision outcomes

Report exactly one terminal outcome, every run: `LAUNCHED` · `NOT-LAUNCHED` · `UNDERWAY` · `STOPPED` ·
`NO-MATCH` · `REFUSED-CLOSED` · `CANNOT-RUN`.

- **`LAUNCHED`** — the developer said yes, or named another route, and the route was launched.
- **`NOT-LAUNCHED`** — the report and its route printed; the developer said not now, or gave no clear
  answer.
- **`UNDERWAY`** — the card already had a worktree or the developer's open pull request; the report
  names `/phil:resume`, and no route was recommended.
- **`STOPPED`** — the developer stopped before the claim: picked no card, gave no narrower words, or
  declined a card in Done or Blocked, someone else's, or a move out of another worktree.
- **`NO-MATCH`** — the argument named no open card in this repo, or named a pull request, and nothing
  was filed.
- **`REFUSED-CLOSED`** — the card is closed.
- **`CANNOT-RUN`** — the run could not begin: no argument and no answer, no forge line, a GitLab forge, no
  signed-in account, a failed read before CLAIM, or a filing that failed and filed nothing.

Report these alongside, each only when it fires: `PICKED` (several matched and the developer picked) ·
`FILED` (a card was filed in the developer's words) · `ANOTHERS-CARD` (assigned to someone else) ·
`OPEN-IN-DONE` (open, but in Done) · `CLAIMED` (read back In Progress and assigned to the developer) ·
`NO-BOARD-BLOCK` (no Status written) · `NOT-ASSIGNED` (the assign failed or did not hold) ·
`CLAIM-FAILED` (a board write failed, or a read failed after filing, and the claim stopped) ·
`READ-BACK-MISMATCH` (the claim did not read back as written, or could not be read) · `WORKTREE-CUT` (a
new worktree, the session moved in) · `WORKTREE-ENTERED` (the card's existing worktree) ·
`WORKTREE-FAILED` (the tool refused; the session stayed) ·
`NO-DONE-WHEN` (the card says no way to tell when it is done) · `BUILD-PATH` (the repo's recorded build
path chose the route) · `ROUTE-OVERRIDDEN` (the developer launched another route).

Report `WROTE-NOTHING` on every run that made no write call before the launch: a stop before CLAIM, or a
claim that found every write already made, for a card that needed no worktree cut. A failed write is still
a write call, and a fetch or a cut worktree is a write. It asserts that every forge and git call the run
made was a read: the `gh api graphql` grant accepts a mutation document, and only the
invariants below forbid one.

## Invariants

- **Write only the claim and the worktree before the launch**: a filed card, its board item, the Status,
  an assignee, a fetch of the default branch, and a worktree the tool cuts. No label, comment or file. A launched route, inline
  included, writes under its own rules.
- **Use `ExitWorktree` only with `keep`, and never cut a second worktree for a card that has one.**
- **Send only `query` documents through `gh api graphql`, never `mutation`.** Writes go through
  `gh issue create`, `gh project item-add`, `gh project item-edit` and `gh issue edit`.
- **Use `gh issue create` only with `-R`, `--title` and `--body ''`.**
- **Use `gh issue edit` only with `--add-assignee`, and `gh project item-edit` only to set the Status
  option.** Pass none of `--remove-assignee`, `--clear` or any flag the steps above do not name. No tool
  boundary backs this.
- **Let the developer pick among several matches.**
- **Leave a closed card for the developer to reopen, and every assignee in place.**
- **Launch nothing without the developer's yes.**
- **Describe only what the card holds.**

## Self-test

`self-test/` holds this skill's fixtures, one directory each with a `manifest.json` and an
`expected.md`; `self-test/README.md` is their register. `tests/test_start_fixtures.py` checks their
structure and that every outcome above has one; judging a run against them is a read by hand.
