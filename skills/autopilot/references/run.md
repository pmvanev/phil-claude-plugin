# RUN — carry the card through its steps

Part of the `autopilot` skill; `../SKILL.md` governs this file as much as this file does. Read it whole
before the first step. Comments go on the card as
`${CLAUDE_PLUGIN_ROOT}/skills/autopilot/references/record.md` says.

## The developer's standing prompt

The developer wrote this for hands-off work. It holds for the whole run, verbatim:

> proceed as independently as possible (through each wave if using nwave). keep the issue updated as
> you go. only stop if a blocker absolutely requires me, in which case do a phil:handoff after
> describing the blocker. clean up worktrees and branches as we finish with them. go with our
> recommendations to questions/options that arise unless you feel I really need to weight in. use
> chrome tools and known test credentials where possible to do your own walks/tests/checks.

The rest of this file is how the run keeps it. The prompt's cleanup line is `/phil:done`'s: the
developer inspects the work and runs it (D13), so the run removes no worktree and deletes no branch.

## Where the run starts

Read the card's step and blocker comments, and the worktree's `.session-handoff.md` where one exists,
for what the last run left.

A step is done when the disk shows its output (PATH), or when a step comment by the developer's account
reads `— done` for it **and** quotes the same source line the path gives that step now. A step comment
that quotes a different line means the path changed since: treat that step as not done, and say so. A
step comment that reads `— work done, landing left` marks the step's work done and its landing not.

Start at the first step neither the disk nor a step comment marks done. Where step comments moved that
point past what the disk alone shows, report `RESUMED`.

**A standing blocker.** A blocker comment stands until the developer answers it, whatever step comments
follow it. Read what the latest blocker comment asked. A later comment on the card by the developer
answers it, and so do words after a card number or
URL in the argument. Take the answer, quote it in the step's comment as the developer's, and go on.
With no answer, the blocker stands: say so, post nothing new, and end as **A blocker** below says.

## Each step, by kind

Take the steps in order. After each one, post its step comment.

- **A step marked `(yours)`** — stop before it (see *When the run ends*).
- **A landing step** — a push, a pull or merge request, a merge. Read
  `${CLAUDE_PLUGIN_ROOT}/skills/autopilot/references/land.md` whole before the first, and land as it
  says.
- **A step that mixes work and landing**, such as "fix it in one merge request" — do the work, commit
  it, then land it. Where the landing stops on a blocker, its step comment reads
  `— work done, landing left`, posted before the blocker comment.
- **A step naming a command or skill** — launch it through the Skill tool, by name without the leading
  slash, passing the card's number or its feature where it takes one, and follow it to its end. In an
  nWave repo, run each wave this way, one after another. After each wave, launch
  `phil:nwave-issue-board` to move the card's `wave:` label and regenerate its block — the label and
  the block only, never the column. Then read the card's Status back: a Status other than In Progress
  is a blocker, since Done is the developer's and a board workflow may close a card in Done.
- **A step naming an agent**, such as `plugin-dev:skill-reviewer` — launch it through the Agent tool by
  its type, giving it the files the card's work touched. Fold its findings into the work, or record why
  a finding was left.
- **A check** — the tests, the repo checks. Run it, and fix what fails within the card's scope. Treat it
  as a circuit breaker, `k = 2`: a check that still fails after two fixes is a blocker. A check that
  fails before the run changed anything — a red default branch — is a blocker at once.
- **The work itself** — authoring, implementing, writing what the card asks. Do it under the repo's own
  rules, toward the card's done-when items, reading first any standard the path names. Commit the work
  in the card's worktree as the repo's rules say, naming the card as `issue <n>`, never after a closing
  keyword.

The steps' work runs under the session's own permissions; the command's grant covers only autopilot's
own calls. A tool call the session denies is a blocker: a permission only the developer can grant.

**An in-browser check** of the running product signs in only from a source the repo declares, through
Chrome DevTools or Playwright. With none declared, that check needs an input only the developer holds.
Never search for a credential, and never invent one.

## Questions

**Never call the question tool during a run**: nobody is there to answer it. Whenever a launched skill,
an agent, a step or the work raises a question — through the tool or in prose — decide it in this order:

1. **A recorded rule answers it** — `CLAUDE.md`, `AGENTS.md`, or the developer's saved preferences in
   the session's memory. Take its answer and quote the rule.
2. **One of the three kinds stops the run** — the developer must weigh in on:
   - an outward or irreversible write the path does not name: filing a card, publishing, deleting,
     force-pushing, discarding work, closing;
   - an input only the developer holds: their own material, an account, a secret, a permission, a
     judgement the card reserves for them, or an approval a launched route reserves for them — as
     `phil:edd`'s verdicts and `phil:work`'s approve-or-reject are;
   - a check that still fails after two fixes.
3. **Otherwise take the recommendation** — the option marked recommended, or, with none marked, the
   option the run would recommend — and record it with its reason.

Record each answer in the step's comment with its source: the rule, quoted; the run's recommendation,
with its reason; or the developer's own answer to a blocker, quoted from their comment or the argument.
Never record as the developer's an answer the run or a rule made, and never write that the developer
answered a question they were not asked. Work the run finds beyond the card goes in the step comment
under `- Found:`, for the developer to place; filing it is a write the path does not name.

## A blocker

Stop where the blocker arises, writing nothing more for that step. Post the blocker comment first,
then end as below. A blocker comment that fails to post never reached the card: the report says so.

## When the run ends

Every run that reached RUN ends the same way: print the REPORT with its outcome tokens, then run
`/phil:handoff` through the Skill tool as the run's last act, and report `HANDED-OFF` beside the
outcome. The snapshot carries what a fresh session needs; the step comments carry the decisions. A
handoff that fails or writes nothing leaves `HANDED-OFF` out, and the report says why.

- **A blocker** — `BLOCKED`. `Next: answer on the card, then /phil:autopilot <n>`.
- **A `(yours)` step with steps after it** — `CARRIED`. `Next: yours — step <k>`.
- **The path's end, or only `(yours)` steps left** — the run believes the work is finished: `CARRIED`.
  `Next: inspect the work, then /phil:done <n>`.
