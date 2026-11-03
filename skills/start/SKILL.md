---
name: start
description: >-
  This skill should be used when the user asks to "start card N", "start issue N", "work on #N", "pick
  up the card about X", "what does this card ask and how should I work it", or runs /phil:start. It
  resolves the argument to one open GitHub card, refuses a closed one, asks before one in Done or someone
  else's, restates what it asks and when it is done, and recommends one route, launched only on a yes.
  Writes nothing before the launch. Not for choosing which card to start; for a card underway, use
  /phil:resume.
---

# Start — pick a card up

`/phil:done` puts a card down finished. This skill picks one up: it settles on exactly one open card,
refuses finished work and asks before someone else's, restates the card in plain English, and recommends
how to work it — the way the repo records, not by habit.

**This version writes nothing before the launch.** It claims no card, assigns no one and cuts no
worktree. It does not yet check whether a card is already underway; for one that is, the developer runs
`/phil:resume`.

## Inputs

- **The argument** — a number, an issue URL, a title, or a few words of description. With none, ask
  which card to start; never infer it from the branch. No answer is `CANNOT-RUN`.
- **The repo** — the forge line in the working tree's `CLAUDE.md`; `git rev-parse --show-toplevel` finds
  the root. Pass the owner and repo as variables to every `gh api graphql` query, which takes no `-R`: an
  inferred remote reads the wrong repo's issues successfully (`phil:issue-board`). With no forge line,
  name `/phil:board-setup`: `CANNOT-RUN`. On a GitLab forge line, say this skill covers GitHub only:
  `CANNOT-RUN`.
- **The board** — the project id from the same `CLAUDE.md` block, to read the card's Status on this
  board. With none, read Status from every project the card is on, and say no board block was found.

Run `git` only for `rev-parse --show-toplevel`. A `gh` call that fails for any reason but `NOT_FOUND` —
auth, network, rate limit — is `CANNOT-RUN`, quoting the error.

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
        projectItems(first:10){ nodes{ project{ id title } fieldValueByName(name:"Status"){
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
- **No match** — say so, quoting the argument: `NO-MATCH`. File nothing: this version cannot file a card.

## CHECK — finished work and someone else's

Check in this order, and stop at the first stop.

1. **Refuse a closed card.** Say it is closed, name `gh issue reopen <n> -R <owner/repo>` for the
   developer to run, and stop: `REFUSED-CLOSED`. Never reopen it, and never describe or route it as
   though it were open.
2. **An open card in `Done` is a defect**: the board says finished and the forge says open. Read Status
   from the board's project item where the board block names a project; otherwise Done on any project
   counts, and the report names that project. State the defect and ask whether to go on — **go on**
   continues the report and leaves the card in Done; **stop** is `STOPPED`. Report `OPEN-IN-DONE` either
   way.
3. **Someone else's card stays theirs.** Where the card has assignees and `viewer.login` is not among
   them, name every assignee's login and ask whether to go on — **go on** continues the report and leaves
   the assignees as they are; **stop** is `STOPPED`. Report `ANOTHERS-CARD` either way. **Never remove an
   assignee.** A card assigned to the developer, or to no one, needs no ask.

The developer is the signed-in account, `viewer.login` — never git's `user.name`, a display name no
forge resolves to a login. Where `viewer` cannot be read, say so, name `gh auth status`, and treat every
assignee as someone else.

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

1. **The repo's recorded build path.** Read the root's `CLAUDE.md` and `AGENTS.md`, where present, for a
   rule that names a command or skill to run for a kind of work — this plugin's own reads `Run nw-discuss
   before authoring a new feature, skill or command`. A principle that names no command, such as "test
   first", is no build path. Where the card's work is that kind, the rule decides: quote the rule and
   name its file, and report `BUILD-PATH`. Where the step the rule names has already run — for
   `nw-discuss`, a `feature-delta.md` in the `docs/feature/<feature>/` directory the card links — name
   the rule's next step instead; where it names none, go on to rule 2.
2. **The card's wave.** A `wave: <name>` label routes to that wave's command in the *Work this with*
   table of `${CLAUDE_PLUGIN_ROOT}/skills/nwave-issue-board/SKILL.md`; read the table there, and never
   restate it. Where a row names a wave command and a step command, route to the wave command and name
   the step command in the reason. A label the table has no row for goes on to rule 3, and the report
   says the table does not cover it.
3. **Who would see the change.** A change a user would see — a command, an output, a page, a behaviour
   — routes to `phil:edd`. A change nobody would see — a refactor, a migration, a cleanup, performance or
   a dependency — routes to `phil:work`.
4. **Whether it fits one sitting.** A card whose DONE WHEN holds exactly one item the card states, and
   whose OPEN names nothing, goes inline instead of rule 3's route: the session works it directly, under
   the repo's own rules. A `NO-DONE-WHEN` card never goes inline: nothing says when the work would stop.

Rules 1 and 2 decide wherever they apply, in that order. Otherwise rule 3 picks the route, and rule 4
overrides it for a card that fits one sitting.

Name one route, its reason in one clause, and the command or skill that owns it. Then ask once: **start
it** runs the route now, and it writes what that route writes; **not now** ends the run with nothing
written. **Launch nothing without the developer's yes.**

- **Yes** — `LAUNCHED`.
- **Other naming a route** — a skill or a command — launch that route instead: `LAUNCHED` with
  `ROUTE-OVERRIDDEN`. Quote the developer's reason where they gave one: an override is the evidence that
  the card and `CLAUDE.md` did not choose the route. Other naming no route is unanswered.
- **Not now, or no clear answer after a second ask** — `NOT-LAUNCHED`.

**Print the outcome tokens, then launch.** A launched route runs on past this skill, so nothing is
reported after it. Invoke a skill or command route through the `Skill` tool, by its name without the
leading slash (`nw-design`). An inline route has no skill: this skill ends, and the session works the
card under the repo's own rules, outside this command's grant, so its writes ask permission.

## REPORT

Print the report before the route question:

```
CARD 76 · New command: /phil:autopilot — carry a card through its repo's build path, and stop only for a blocker that needs the developer · open · Todo · unassigned
ASKS: a command that carries a card through its repo's build path, stopping only for a blocker the developer must clear.
DONE WHEN: 6 items — the command and its skill exist, through nw-discuss and plugin-dev; fixtures pin that a taken recommendation is recorded on the card, a developer's decision stops the run, a blocker leaves a comment and a snapshot, a declared build path beats nWave directories, and a missing credential declaration blocks.
OPEN: 4 questions — what counts as a blocker, what marks a declared build path, where test credentials live, which recorded rules it cannot override.
ROUTE: nw-discuss — CLAUDE.md: "Run `nw-discuss` before authoring a new feature, skill or command."
```

The CARD line carries the title as the forge holds it, and `on no board` where the card is on none. The
ROUTE line takes one of these shapes:

```
ROUTE: nw-discuss — CLAUDE.md: "Run `nw-discuss` before authoring a new feature, skill or command."
ROUTE: /nw-design — the card carries `wave: design`
ROUTE: phil:edd — a user would see the change: a new flag on /phil:done
ROUTE: phil:work — nobody would see the change: the hook moves to a shared module
ROUTE: inline — one done-when item, nothing open: fix a broken link in the README
```

## Decision outcomes

Report exactly one terminal outcome, every run: `LAUNCHED` · `NOT-LAUNCHED` · `STOPPED` · `NO-MATCH` ·
`REFUSED-CLOSED` · `CANNOT-RUN`.

- **`LAUNCHED`** — the developer said yes, or named another route, and the route was launched.
- **`NOT-LAUNCHED`** — the report and its route printed; the developer said not now, or gave no clear
  answer.
- **`STOPPED`** — the developer stopped before the route: picked no card, gave no narrower words, or
  declined a card in Done or someone else's.
- **`NO-MATCH`** — the argument named no open card in this repo, or named a pull request.
- **`REFUSED-CLOSED`** — the card is closed.
- **`CANNOT-RUN`** — the run could not begin: no argument and no answer, no forge line, a GitLab forge, or
  a failed read.

Report these alongside, each only when it fires: `PICKED` (several matched and the developer picked) ·
`ANOTHERS-CARD` (assigned to someone else) · `OPEN-IN-DONE` (open, but in Done) · `NO-DONE-WHEN` (the card
says no way to tell when it is done) · `BUILD-PATH` (the repo's recorded build path chose the route) ·
`ROUTE-OVERRIDDEN` (the developer launched another route).

Report `WROTE-NOTHING` on every run. It asserts that every call this run made before the launch was a
read: the `gh api graphql` grant accepts a mutation document, and only the invariants below forbid one.

## Invariants

- **Write nothing before the launch.** No Status, assignee, label, comment, branch, worktree or file. A
  launched route, inline included, writes under its own rules.
- **Send only `query` documents through `gh api graphql`, never `mutation`.** No tool boundary backs this.
- **Let the developer pick among several matches.**
- **Leave a closed card for the developer to reopen, and every assignee in place.**
- **Launch nothing without the developer's yes.**
- **Describe only what the card holds.**

## Self-test

`self-test/` holds this skill's fixtures, one directory each with a `manifest.json` and an
`expected.md`; `self-test/README.md` is their register. `tests/test_start_fixtures.py` checks their
structure and that every outcome above has one; judging a run against them is a read by hand.
