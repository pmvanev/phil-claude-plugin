---
name: autopilot
description: >-
  This skill should be used when the user runs /phil:autopilot, or asks to "carry card N hands-off",
  "run card N on autopilot", "autopilot card N" or "take this card through the build path". It claims
  the card through /phil:start's steps, reads the repo's build path from CLAUDE.md and AGENTS.md, prints
  each step beside its source line with the writes the path authorizes, records both on the card, and
  stops before the first step. GitHub only. Not for choosing which card to carry.
---

# Autopilot — carry a card through its repo's build path

`/phil:start` picks a card up and `/phil:done` puts one down. Autopilot will carry a card between them
without the developer at every gate. This release claims the card, reads the build path the repo
records, prints the reading, records it on the card, and stops. **Stop before the first step of the
path.**

**Running `/phil:autopilot` is the developer's yes to the claim, the worktree and the path comment.**
Loaded any other way — from a question about which path autopilot would follow — print the path and
write nothing.

## Inputs

- **The argument** — a number, an issue URL, a title or a few words. With none, ask which card to carry;
  never infer it from the branch. No answer is `CANNOT-RUN`.
- **The repo, the board constants and the developer** — as `/phil:start`'s *Inputs* section reads them.
  Pass `-R <owner/repo>` on every `gh issue` call, and pass the owner and repo as variables to every
  `gh api graphql` query, which takes no `-R`. With no forge line, name `/phil:board-setup`:
  `CANNOT-RUN`.
- **GitLab** — this skill covers GitHub only. Where the forge line names GitLab, say the command covers
  GitHub only, and stop before RESOLVE: `CANNOT-RUN` with `GITHUB-ONLY`.

## Asking

**Every ask this skill puts follows `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`.** Load it
before the first ask. The asks are the no-argument ask above and every ask `/phil:start`'s steps put:
which of several cards, narrower words, going on past a card in Done or Blocked, someone else's card or a
session in another worktree, which of several worktrees, and entering a locked one.

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
  request or a surviving branch with no worktree here — say the session is not in the card's worktree.
  Then go on to PATH.
- **A failed claim or worktree** — after `CLAIM-FAILED` or `WORKTREE-FAILED`, go on to PATH and RECORD.

## PATH — the steps the repo records

Read `CLAUDE.md` and `AGENTS.md` at the root of the session's working tree after WORKTREE, and any file
either names with an `@` import. Find the steps the repo takes for the card's kind of work: each command
or skill to run, check to pass, and write to make, in the order the prose gives them. A principle that
names no action, such as "test first", is no step. Read the card's title and body to know its kind of
work.

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
card links. Mark it `done`, keep it in the list, and name the first step not done as the next.

**List the authorized writes.** Starting the run authorizes only the writes the path names, each beside
the number of the step that names it: a commit, a push, a pull request, a merge once its pipeline passes,
a version bump, a close. A write no step names is not authorized, however usual. A fallback path names
none: print `AUTHORIZED: none — the fallback path names no write`.

## RECORD — one comment on the card

Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing the comment and the report, and apply it
to every word this run composes. Leave every quoted line of the card, `CLAUDE.md` or `AGENTS.md` in its
own words.

The comment's first line is exactly `**Autopilot · build path**`. Then come the steps and the authorized
writes. This repo's path reads:

```
**Autopilot · build path**

1. nw-discuss (done) — CLAUDE.md, Build path for this plugin: "Run `nw-discuss` before authoring a new feature, skill or command."
2. author after plugin-dev — CLAUDE.md, Build path for this plugin: "Read `plugin-dev:skill-development`, `command-development`, `agent-development` or `plugin-structure` before writing the file."
3. …
6. push and open a pull request — CLAUDE.md, CI workflow: "Land every change on `main` through a pull request: push a feature branch, open a pull request, and merge once its pipeline passes."
7. merge once its pipeline passes — CLAUDE.md, CI workflow: (the same line)

Next: step 2.
Starting the run authorizes: commit (step 5), push (step 6), pull request (step 6), merge once its pipeline passes (step 7).
```

Before posting, read the card's comments:

```bash
gh api graphql -f query='
query($o:String!,$r:String!,$n:Int!){ repository(owner:$o,name:$r){ issue(number:$n){
  comments(last:50){ nodes{ body author{ login } } } } } }' \
  -f o=<owner> -f r=<repo> -F n=<n>
```

A read that fails posts nothing: `RECORD-FAILED`, quoting the error. Otherwise take the latest comment by
`viewer.login` whose first line is `**Autopilot · build path**`. Where it holds the same quoted lines,
in the same order, with the same `done` marks and the same step numbers on its authorized writes, post
nothing: `ALREADY-RECORDED`. The words this run composed may differ; they are not compared. Otherwise
post the comment:

```bash
gh issue comment <n> -R <owner/repo> --body-file - <<'EOF'
<the comment>
EOF
```

Use `gh issue comment` only with `-R` and `--body-file -`; never `--edit-last` or `--delete-last`. Read
the comments back once: the comment found is `RECORDED`. A post that fails, or does not read back, is
`RECORD-FAILED`, quoting the error. Post once only, and repair nothing: a timed-out post may have landed.

## REPORT

Print `/phil:start`'s CARD, claim and worktree lines, then the PATH lines as the comment holds them, the
next step, the AUTHORIZED line and one record line:

```
RECORDED: the path comment on the card — read back
ALREADY-RECORDED: the card's latest path comment holds this path — nothing posted
RECORD-FAILED: <the error> — nothing posted  |  <the error> — posted once, not found on read-back
```

A fallback names its rule on the PATH line: `PATH (fallback — no build path in CLAUDE.md or AGENTS.md;
route rule 3):` then `1. phil:edd — route.md, rule 3: "A change a user would see — a command, an output,
a page, a behaviour — routes to `phil:edd`."`. End with the outcome tokens.

## Decision outcomes

Report exactly one terminal outcome, every run: `PLANNED` · `STOPPED` · `NO-MATCH` · `REFUSED-CLOSED` ·
`CANNOT-RUN`.

- **`PLANNED`** — the run printed the path and the authorized writes, and stopped before the first step.
- **`STOPPED`** — the developer stopped at one of `/phil:start`'s asks.
- **`NO-MATCH`** — the argument named no open card in this repo; nothing was filed.
- **`REFUSED-CLOSED`** — the card is closed.
- **`CANNOT-RUN`** — the run could not begin: no argument and no answer, no forge line, a GitLab forge,
  no signed-in account, or a failed read before the claim.

Report these alongside, each only when it fires:

- Autopilot's own: `DECLARED-PATH` (read from the repo's prose) · `FALLBACK-PATH` (none declared) ·
  `RECORDED` (the comment posted and read back) · `ALREADY-RECORDED` (the same path was there; nothing
  posted) · `RECORD-FAILED` · `GITHUB-ONLY` (the forge is GitLab) · `UNDERWAY` (the card had a worktree,
  an open pull request or a surviving branch) · `WROTE-NOTHING` (no write call, as `/phil:start` counts
  them: a claim write, a fetch, a cut worktree or a comment is a write; entering a worktree is not).
- Carried from `/phil:start`: `PICKED` · `ANOTHERS-CARD` · `OPEN-IN-DONE` · `CLAIMED` · `NO-BOARD-BLOCK`
  · `NOT-ASSIGNED` · `CLAIM-FAILED` · `READ-BACK-MISMATCH` · `WORKTREE-CUT` · `WORKTREE-ENTERED` ·
  `WORKTREE-FAILED`.

## Invariants

- **Stop before the first step of the path**, launching no skill or command it names.
- **Write only the claim, the worktree and one path comment**: `/phil:start`'s writes, and one
  `gh issue comment`. File no card.
- **Send only `query` documents through `gh api graphql`.**
- **Quote the repo's lines in their own words**, and print no step without its line.
- **Authorize only what a step names.**
- **Leave a closed card for the developer to reopen, and every assignee in place.**

## Self-test

`self-test/` holds this skill's fixtures, one directory each with a `manifest.json` and an
`expected.md`; `self-test/README.md` is their register. `tests/test_autopilot_fixtures.py` checks their
structure and that every outcome autopilot adds has one; judging a run against them is a read by hand.
