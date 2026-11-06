---
name: autopilot
description: >-
  This skill should be used when the user runs /phil:autopilot, or asks to "carry card N hands-off",
  "run card N on autopilot", "autopilot card N" or "take this card through the build path", on GitHub
  or GitLab. It claims the card, reads and records the repo's build path, runs each step, and lands the
  work — push, pull or merge request, merge on a green pipeline — deciding questions by rule or
  recommendation and stopping only for a blocker, which it hands off. --plan stops before the first
  step. Not for choosing a card, and never for calling one done.
---

# Autopilot — carry a card through its repo's build path

`/phil:start` picks a card up and `/phil:done` puts one down. Autopilot carries a card between them
without the developer at every gate. It claims the card, reads the build path the repo records, prints
and records the reading, runs the steps and lands the work on a green pipeline, stopping for a blocker
the developer must clear. It never calls the work done: the developer inspects it and runs `/phil:done`.

**Running `/phil:autopilot` is the developer's yes to the claim, the worktree, the comments on the card
and the steps the path names.** Loaded any other way — from a question about which path autopilot
would follow — print the path and write nothing.

## Inputs

- **The argument** — a number, an issue URL, a title or a few words, then optionally `--plan`. Words
  after a card number or URL answer a standing blocker; with no blocker standing, the run says it
  ignored them. With no card, ask which to carry; never infer it from the branch. No answer is
  `CANNOT-RUN`.
- **The repo, the board constants and the developer** — as `/phil:start`'s *Inputs* section reads them.
  Pass `-R <owner/repo>` on every `gh issue` call, and pass the owner and repo as variables to every
  `gh api graphql` query, which takes no `-R`. With no forge line, name `/phil:board-setup`:
  `CANNOT-RUN`.
- **GitLab** — start's *Inputs* send the claim and the worktree through
  `${CLAUDE_PLUGIN_ROOT}/skills/start/references/gitlab.md`; the record's GitLab calls are in
  `references/record.md`.

## Asking

**Every ask this skill puts follows `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`.** Load it
before the first ask. The asks come before the run: the no-argument ask above and every ask
`/phil:start`'s steps put — which of several cards, narrower words, going on past a card in Done or
Blocked, someone else's card or a session in another worktree, which of several worktrees, entering a
locked one, and, on GitLab, which label is In Progress. Once RUN begins, nothing asks: RUN's rules
decide each question.

## CLAIM — through `/phil:start`'s steps

Read `${CLAUDE_PLUGIN_ROOT}/skills/start/SKILL.md` whole, and run its *Inputs* and its RESOLVE, CHECK,
CLAIM and WORKTREE steps as it writes them, reading each reference it names. Skip its DESCRIBE and ROUTE:
the build path replaces the route. Where start's text sends the run to DESCRIBE or ROUTE, names
`/phil:resume` as the next step, or ends the run `UNDERWAY`, go on to PATH instead. Where it ends the run
with a terminal outcome before the claim, end it there. In the `EnterWorktree` call's reasoning, say the
developer typed `/phil:autopilot`, which asks for the card's worktree.

Three changes:

- **No match** — say no open card matches, quoting the argument, and offer no filing: a new card is a
  write the path does not name. `NO-MATCH`.
- **A card underway** — report `UNDERWAY` and print start's worktree line without its `next:` clause.
  Where start entered the card's worktree, the session is there; where it cut nothing — an open pull
  or merge request, or a surviving branch, with no worktree here — say the session is not in the
  card's worktree, and run no step: `PLANNED`.
- **A failed claim or worktree** — after `CLAIM-FAILED` or `WORKTREE-FAILED`, go on to PATH and RECORD,
  and run no step: `PLANNED`.

## PATH — the steps the repo records

Read `CLAUDE.md` and `AGENTS.md` at the root of the session's working tree after WORKTREE, and any file
either names with an `@` import. Find the steps the repo takes for the card's kind of work: each command
or skill to run, check to pass, and write to make, in the order the prose gives them. A principle that
names no action, such as "test first", is no step, and neither is a condition, such as "before calling
it done". Read the card's title and body to know its kind of work.

**A declared path beats detection.** Where the prose records steps for this kind of work, use them, even
where the repo holds `.nwave/` or `docs/feature/`, and report `DECLARED-PATH`. A path may draw on several
headings: a build path under one, the landing under another.

Where the prose records none, fall back by `/phil:start`'s route rules 2 and 3, read in
`${CLAUDE_PLUGIN_ROOT}/skills/start/references/route.md`, name the rule that chose it, and report
`FALLBACK-PATH`:

- **A card with a `wave:` label** in a repo holding `.nwave/` or `docs/feature/` takes the waves in
  `${CLAUDE_PLUGIN_ROOT}/skills/nwave-issue-board/SKILL.md`'s *Work this with* table, from that label
  onward. Read the table there; quoting the row a step came from cites it. Where a row names a wave
  command and a step command, the step is the wave command.
- **Any other card** — no label, or a label the table has no row for — takes `phil:edd` where a user
  would see the change, and `phil:work` where nobody would, by rule 3.

**Show the reading.** Nothing can check a reading of prose, so print every step, numbered, beside the
line it came from, quoted in its own words, with the file and heading it sits under. A fallback step
quotes the rule or the table row that chose it. A step the prose implies but no line states is a
misreading: leave it out.

**Mark the steps already run.** A step has run where the repo holds its output for this card — for
`nw-discuss`, a `feature-delta.md` under `docs/feature/` whose `Board:` line names the card, or that the
card links — or where a step comment marks it done (`references/run.md`). Mark it `done`, keep it in
the list, and name the first step not done as the next.

**Leave done to the developer.** The developer inspects the work and calls it done. A step that closes
the card or calls it done prints marked `(yours)` and authorizes nothing: one naming `/phil:done` or a
close, a Done Status, or a done label, which a board workflow may turn into a close. The next step skips
it, and a step after it waits for it. Where only `(yours)` steps remain, print `Next: yours — step <k>`.

**List the authorized writes.** Starting the run authorizes only the writes the path names that leave
the machine, each beside the number of the step that names it: a push, a pull or merge request, a merge
once its pipeline passes. Commits in the card's worktree belong to the work. A write no step names is
not authorized, however usual, and a close never is. An authorized pull or merge request names the card as `issue <n>`, never after a closing
keyword such as `Closes`, `Fixes` or `Resolves`, which would close the card when it merges. A fallback
path names none: print `AUTHORIZED: none — the fallback path names no write`.

## RECORD — the path on the card

Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing any comment or the report, and apply it
to every word this run composes. Read `${CLAUDE_PLUGIN_ROOT}/skills/autopilot/references/record.md`
whole, then post the path comment as it says, unless the card holds it already.

## RUN — the steps

With `--plan`, stop before the first step of the path: `PLANNED`. Otherwise read
`${CLAUDE_PLUGIN_ROOT}/skills/autopilot/references/run.md` whole and run the path as it says: from the
first step not done, each through the command, skill or agent that owns it, every question decided by a
recorded rule, a blocker or the recommendation, each step's decisions posted on the card. A blocker is
described on the card. Every run that reaches RUN prints its report, then hands off through
`/phil:handoff`.

## REPORT

Print `/phil:start`'s CARD, claim and worktree lines; the PATH lines as the comment holds them; the
AUTHORIZED line; one line per step run, with its decisions counted; then where the run stopped and the
next step. Print it before the handoff, which is the run's last act. Record lines:

```
RECORDED: the path comment on the card — read back
ALREADY-RECORDED: the card's latest path comment holds this path — nothing posted
RECORD-FAILED: <the error> — nothing posted  |  <the error> — posted once, not found on read-back
LANDED: pull request 112 merged on a green pipeline; main green on 9e1f910
```

A fallback names its rule on the PATH line:

```
PATH (fallback — no build path in CLAUDE.md or AGENTS.md; route rule 3):
  1. phil:edd — route.md, rule 3: "A change a user would see — a command, an output, a page, a behaviour — routes to `phil:edd`."
```

End with the outcome tokens.

## Decision outcomes

Report exactly one terminal outcome, every run: `PLANNED` · `CARRIED` · `BLOCKED` · `STOPPED` ·
`NO-MATCH` · `REFUSED-CLOSED` · `CANNOT-RUN`.

- **`PLANNED`** — the run printed and recorded the path and ran no step: `--plan`, a failed claim or
  worktree, or a card underway with no worktree here.
- **`CARRIED`** — the run stopped at a `(yours)` step or the path's end, whether or not it ran a step.
- **`BLOCKED`** — a question, a check or a permission needs the developer; the run posted the blocker
  comment, or says the post failed.
- **`STOPPED`** — the developer stopped at one of `/phil:start`'s asks.
- **`NO-MATCH`** — the argument named no open card in this repo; nothing was filed.
- **`REFUSED-CLOSED`** — the card is closed.
- **`CANNOT-RUN`** — the run could not begin: no argument and no answer, no forge line, no signed-in
  account, or a failed read before the claim.

Report these alongside, each only when it fires:

- Autopilot's own: `DECLARED-PATH` (read from the repo's prose) · `FALLBACK-PATH` (none declared) ·
  `RECORDED` (the path comment posted and read back) · `ALREADY-RECORDED` (the same path was there;
  nothing posted) · `RECORD-FAILED` · `DONE-IS-YOURS` (a step closes the card or calls it done; printed
  as the developer's, authorized for no one) · `UNDERWAY` (the card had a worktree, an open pull or
  merge request, or a surviving branch) · `RESUMED` (step comments moved the start past what the disk
  shows) · `LANDED` (the request merged on a green pipeline, and the default branch read green after) ·
  `HANDED-OFF` (`/phil:handoff` wrote its snapshot) · `WROTE-NOTHING` (no write call, as
  `/phil:start` counts them: a claim write, a fetch, a cut worktree, a comment or note, or any write a
  step made is a write; entering a worktree is not).
- Carried from `/phil:start`: `PICKED` · `ANOTHERS-CARD` · `OPEN-IN-DONE` · `CLAIMED` · `NO-BOARD-BLOCK`
  · `NOT-ASSIGNED` · `CLAIM-FAILED` · `READ-BACK-MISMATCH` · `WORKTREE-CUT` · `WORKTREE-ENTERED` ·
  `WORKTREE-FAILED`.

## Invariants

- **Land only on green**: push without force, name the card in the request without a closing keyword,
  merge only on a pipeline the forge reports green, with the head commit matched, and delete no branch.
- **Write on the forge, in autopilot's own calls, only the claim, the comments and the landing**:
  `/phil:start`'s writes, `gh issue comment` or `glab issue note`, and the push, the request and the
  merge. File no card, and edit no card's body. A launched skill, agent or `/phil:handoff` writes under
  its own rules.
- **Leave done to the developer**: run no `/phil:done`, close no card, authorize no close.
- **Send only `query` documents through `gh api graphql`, and only GETs through `glab api`.**
- **Answer no question as the developer**: the run calls no question tool once RUN begins, and records
  as the developer's only their own answer to a blocker, quoted.
- **Quote the repo's lines in their own words**, and print no step without its line.
- **Authorize only what a step names.**
- **Leave a closed card for the developer to reopen, and every assignee in place.**

## Self-test

`self-test/` holds this skill's fixtures, one directory each with a `manifest.json` and an
`expected.md`; `self-test/README.md` is their register. `tests/test_autopilot_fixtures.py` checks their
structure and that every outcome autopilot adds has one; judging a run against them is a read by hand.
