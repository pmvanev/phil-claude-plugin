# Without a card — the session's own work

Part of the `done` skill. Read it whole before FIND when `/phil:done` runs with no argument. Its
`SKILL.md` governs this file too, and on GitLab, `gitlab.md` gives every call.

Some sessions do ad-hoc work that no card tracks. With no argument, `/phil:done` checks that work: every
ask the session took on, the pull requests it opened, and what they left behind. **It closes no card.**
Take a card only from the argument — never from the branch, a worktree's name or the conversation, even
where the session mentions one.

Each step runs as `SKILL.md` describes, except where this file says otherwise.

## FIND — the session's pull requests

Read the developer and the default branch without the card:

```bash
gh api graphql -f query='
query($o:String!,$r:String!){
  viewer{ login }
  repository(owner:$o,name:$r){
    defaultBranchRef{ name target{ ... on Commit{ oid statusCheckRollup{ state }
      history(first:20){ nodes{ oid statusCheckRollup{ state } } } } } } } }' \
  -f o=<owner> -f r=<repo>
```

On GitLab, `gitlab.md` gives the same reads.

The work is what the session shows:

- **Each pull request the conversation shows this session opening, pushing to or merging**, by its
  number or URL. Read it by number with the fields FIND's search reads —
  `repository{ pullRequest(number:<m>){ … } }`, or `projects/<p>/merge_requests/<m>`.
- **Each branch the conversation shows this session creating or pushing.** Read its tip: the local one
  with `git rev-parse --verify --quiet refs/heads/<branch>`, the remote one as `clear.md` reads it. Find
  its pull requests by head branch — `repository{ pullRequests(headRefName:"<branch>", first:20){ nodes{
  … } } }`, or `projects/<p>/merge_requests?state=all&source_branch=<branch>` — and keep only one whose
  `headRefOid` is that tip. An older pull request under a reused name is not this session's work. A
  branch whose tip no pull request holds has not landed: `NOT LANDED: <branch> has no pull request at
  its tip`.

**A branch the conversation never names is never a candidate**, whatever its name. Keep only the
developer's own pull requests, whose `author.login` is `viewer.login`; list anyone else's as not this
session's work. Where the conversation was compacted, say that what came before comes from the summary.

## ACCOUNT — every session ask

The asks are every request the developer made in this conversation that asked for a change, and every
task the session took on. A question the session answered in the conversation is no ask: it changed
nothing to verify. The card's checklist and headings do not apply; use the card evidence rows only for an
ask that edited a card the session names.

One evidence row joins `SKILL.md`'s table: **a commit pushed straight to `<default>`**, verified where
`ref(qualifiedName:"refs/heads/<default>"){ compare(headRef:"<sha>"){ status } }` reads `BEHIND` or
`IDENTICAL`, or as `gitlab.md` gives it.

## LANDED

Judge the session's pull requests as `SKILL.md` judges a card's. Where the session names none, print
`NOTHING TO LAND: the session names no pull request`, judge the run on its asks alone, and give CLEAR no
branch candidates.

## REPORT and RESOLVE

Open the report with `NO CARD — the session's own work`. RESOLVE runs unchanged; a dropped ask and its
reason go into the report, since no closing comment carries them.

## PLAN — CLEAR's lines alone

The plan holds no closing comment, no Status write, no close and no block refresh: only CLEAR's lines,
found as `clear.md` finds them, from the session's merged pull requests. Show the snapshot in this
checkout with its next action and stack, read through `session-exchanges.py head` as `clear.md` reads
any snapshot, so the developer can tell whose work it records.

- Where CLEAR holds a branch, a snapshot elsewhere or a force-delete, ask once, with the answers
  `SKILL.md` gives the plan.
- Where it holds only the snapshot in this checkout, ask once: **retire it** or **keep it**. Any other
  answer keeps it, and the snapshot is `LEFT`.
- Where the plan holds nothing, ask nothing.

## CLEAR

Skip CLOSE. On the yes, run CLEAR in the order `clear.md` gives, and report its lines as it does.

## The outcome

`FINISHED` — every session ask done or dropped, every pull request the session names landed or none
named, and the plan ran, held nothing to run, or kept the snapshot at the developer's answer:

```
FINISHED: no card — 4 asks done; PR 95 landed; 1 branch cleared
```

`NOT-READY` and `STOPPED` keep their meaning. A run without a card never reports `CLOSED` or
`CLOSE-FAILED`.
