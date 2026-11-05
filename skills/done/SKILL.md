---
name: done
description: >-
  This skill should be used when the user asks "is this card done", "can I close this issue", "close out
  card N", "mark this card done", "did everything I asked for land", "wrap up this session", "clean up
  my merged branches", "remove this session's worktree", "clean up this card's worktree", or runs
  /phil:done. It lists every ask with verified evidence, checks every pull request merged into a green
  default branch, then, on one yes, comments, sets Status to Done, closes the issue, retires its
  snapshots, deletes its branches and removes the work's clean worktrees, listing the rest. With no
  card, it checks the session's own asks and pull requests and clears what they left. GitHub or GitLab;
  never merges or forces. For unfinished work, use /phil:handoff.
---

# Done — is this card ready to close?

`/phil:handoff` puts a session down unfinished. This skill answers the question that comes before
putting one down **finished**: did every ask land, and did the work reach the default branch? Then, on
the developer's one yes, it closes the card comment-first, reads it back, and clears what the work left
behind: it retires the handoff snapshots, deletes the branches, removes the work's clean, unlocked
worktrees, whoever made them, and lists the rest for the developer to remove. With no card, it asks the
same of the session's own work and closes nothing.

## Inputs

- **The card** — the issue number from the argument. With none, run without a card, and never infer
  one from the branch. Read `${CLAUDE_PLUGIN_ROOT}/skills/done/references/no-card.md` whole before FIND:
  it checks the session's own asks and pull requests and closes no card.
- **The repo** — the forge line in the working tree's `CLAUDE.md`; `git rev-parse --show-toplevel` finds
  the root. Pass `-R <owner/repo>` on every `gh issue` call, and the owner and repo as variables to every
  `gh api graphql` query, which takes no `-R`: an inferred remote reads the wrong repo's issues
  successfully (`phil:issue-board`). With no forge line, stop and name `/phil:board-setup`.
- **GitLab** — Read `${CLAUDE_PLUGIN_ROOT}/skills/done/references/gitlab.md` whole before FIND where
  the forge line names GitLab. It gives each call below its `glab` form; every rule here stands.
- **The board constants** — the project id, the `Status` field id and the `Done` option id, from the
  same `CLAUDE.md` block; on GitLab, the status label family. Read them; never probe for them. With
  none, skip the Status write, report the skip, and name `/phil:board-setup`.

Run `git` only for `rev-parse`, the `log` reads of the block refresh and of FORCE, and CLEAR's
`worktree list`, `worktree remove`, `remote get-url`, `merge-base --is-ancestor`, `branch -d`,
`branch -D` and `push --delete`. Look files up on the forge: a `<branch>:<path>` lookup through local git reads a ref
that may be stale.

## FIND — the card, its pull requests and the default branch

Read the issue body with `gh issue view <n> -R <owner/repo> --json body,state`. Then read the default
branch and the pull requests the forge links to the card:

```bash
gh api graphql -f query='
query($o:String!,$r:String!,$n:Int!){
  viewer{ login }
  repository(owner:$o,name:$r){
    defaultBranchRef{ name target{ ... on Commit{ oid statusCheckRollup{ state }
      history(first:20){ nodes{ oid statusCheckRollup{ state } } } } } }
    issue(number:$n){ closedByPullRequestsReferences(first:50, includeClosedPrs:true){
      pageInfo{ hasNextPage } nodes{ number title state merged baseRefName headRefName headRefOid
      isCrossRepository author{ login } } } } } }' \
  -f o=<owner> -f r=<repo> -F n=<n>
```

Then search every page for the pull requests that mention the card, filtering in `--jq`:

```bash
gh api graphql --paginate -f query='
query($q:String!,$endCursor:String){
  search(query:$q, type:ISSUE, first:50, after:$endCursor){ pageInfo{ hasNextPage endCursor }
    nodes{ ... on PullRequest{ number title body state merged mergedAt baseRefName headRefName
      headRefOid isCrossRepository author{ login } } } } }' \
  -f q='repo:<owner>/<repo> is:pr <n> in:title,body' \
  --jq '.data.search.nodes[] | select((.title+" "+.body) | test("(#|issue )<n>([^0-9]|$)"; "i"))'
```

The default branch is `defaultBranchRef.name`; call it `<default>` below.

**Find the card's pull requests, never by a branch name.** Keep every linked pull request, and every
search hit whose title or body contains `#<n>` or `issue <n>`, case-insensitive, with `<n>` not followed
by a digit: `line 75` and `#175` do not name issue 75. Some repos mention a card in prose and never link
it, because a closing keyword closes the card early; the search finds those.

**Judge no list the query cut short.** Where the linked list's `hasNextPage` is true or a search page
errors, report the pull request list incomplete and the card `NOT-READY`.

## ACCOUNT — every ask, with evidence or open

Collect the asks from the card and the current session:

1. **The card.** Every checklist item in the issue body, ticked or not; every item under a heading
   containing *Done when*; and every item, numbered or bulleted, under a heading containing
   *What it does*, *Scope*, *Requirements* or *Acceptance criteria*.
2. **The current session.** Each request the developer made in this conversation that bears on the
   card, and each task the session took on for it. Quote the developer's words as written; follow a
   terse reply with what it approved, in parentheses, so the ask reads on its own:
   `"proceed" (commit, push, open the pull request)`. Where the conversation holds no such request, say
   so; earlier sessions' requests are not read. Where the conversation was compacted, say that asks
   before the compaction come from its summary.

List an ask once even when both places hold it. Mark each **done** or **open**. Done needs evidence a
call in this run verified, against `<default>`:

| Evidence | Verified when | Lookup |
|---|---|---|
| A pull request | `merged` is true and `baseRefName` is `<default>` | `pullRequest(number:<p>){ merged baseRefName }` |
| A commit | one of its associated pull requests merged into `<default>` | `object(expression:"<sha>"){ ... on Commit{ associatedPullRequests(first:5){ nodes{ number merged baseRefName } } } }`; a short sha works |
| A file | it exists at `<default>`'s head | `object(expression:"<branch>:<path>"){ id }`, with `<branch>` = `<default>`; null means absent |
| The card's body | the body holds the change an ask made to the card | `gh issue view <n> -R <owner/repo> --json body` |
| The card's board state | Status, assignee or label reads as the ask set it | `issue(number:<n>){ assignees(first:5){ nodes{ login } } labels(first:20){ nodes{ name } } projectItems(first:5){ nodes{ project{ id } fieldValueByName(name:"Status"){ ... on ProjectV2ItemFieldSingleSelectValue{ name } } } } }` |

Each GraphQL lookup goes inside `repository(owner:$o,name:$r){ … }` in a `gh api graphql` query. Use
the card's body and board state only for an ask that edits the card or the board; code needs code's
evidence.

**Look for evidence an ask does not name.** Search the pull requests FIND kept for one whose title or
body carries the ask, and look up any file the ask names. Verify each find. Where nothing turns up, the
ask is open: `no evidence found`, naming the lookups that came back empty.

A sentence saying an ask was done is not evidence — not the developer's, not this session's, not a
comment's. A ticked box is not evidence either: it is a claim that the work happened, and a ticked ask
gets the same search as any other. Unverifiable evidence is not evidence: report the ask open and name
the call that failed.

## LANDED — merged into the default branch, and the branch green

The work **landed** when:

1. at least one pull request merged into the default branch, and none is open; and
2. `<default>`'s head commit has a `statusCheckRollup` of `SUCCESS`, or the repo has no pipeline.

A pull request closed unmerged is listed and counts for nothing. A pull request merged into any other
base has not landed: list it as `merged into <base>, not <default>`. Report **not landed**, naming every
cause: a pull request open, none merged into `<default>`, a merge into another base, an incomplete list,
or a head rollup of anything but `SUCCESS`, naming the state.

Where neither the head nor any of the last 20 commits on `<default>` carries a rollup, the repo has no
pipeline: report `no pipeline`, never green, and judge landing on the pull requests alone. Where older
commits carry one and the head does not, the pipeline has not reported yet: not landed.

**Never merge, and never offer to.** A pull request still open is the developer's to merge, or
`superpowers:finishing-a-development-branch`'s.

## REPORT

Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing the report, and apply it to every word
this run composed: active voice, no needless words, the evidence named concretely. Leave quoted asks in
the developer's own words. Print one line for every ask the count claims:

```
ASKS 3: 2 done, 1 open
  done  Close the card comment-first — PR 81 merged into main
  done  Add the no-pipeline fixture — skills/done/self-test/05-no-pipeline/ at main
  open  "make sure it cleans up a stale session-handoff.md" — no evidence found (PR search, file lookup)
LANDED: PR 81 merged into main; main green at 7358cad
NOT READY: 1 open ask
```

The LANDED line takes one of these shapes, with every cause that fired:

```
LANDED: PR 90 merged into main; no pipeline
NOT LANDED: PR 82 open
NOT LANDED: PR 84 closed unmerged; no pull request for the card merged
NOT LANDED: PR 85 merged into finish-work/slice-02, not main
NOT LANDED: no pull request names or links to the card
NOT LANDED: main red at 7358cad (FAILURE)
NOT LANDED: main's head has not reported yet
NOT LANDED: pull request list incomplete (a search page failed)
```

The last line, `READY` or `NOT READY: <causes>`, is for the developer. The decision outcome tokens
below are a separate output, reported when the run ends.

Where the work has not landed, stop here: `NOT-READY`. Closing nothing is the only answer to an open pull
request or a red default branch.

## RESOLVE — every open ask answered

**Every ask this skill puts — here and at PLAN — follows
`${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`.** Load it before the first ask. Quote the open
ask in the context block above the question, and describe it in plain words in the question itself: a
quoted ask often holds a path or an issue number, which a strict repo's hook refuses in a question.

Ask about each open ask on its own, with `AskUserQuestion`, offering three answers and Other:

- **do it** — stop here and go do it: `NOT-READY`;
- **name its evidence** — verify it as ACCOUNT would; where it fails, the ask stays open: `NOT-READY`;
- **stop** — `STOPPED`, with `OPEN-ASKS`.

To drop it with a reason, the developer chooses Other and types the reason. A dropped ask leaves the
list with its reason, typed as given; it is never marked done. The closing comment quotes every dropped
ask with its reason.

## PLAN — one yes

Read `${CLAUDE_PLUGIN_ROOT}/skills/done/references/clear.md` whole before composing the plan: it finds
the work's snapshots, branches and worktrees, holds what must survive, asks FORCE's question for each of
the developer's own unmerged branches, and adds the cleanup lines and the third answer.

Compose the closing comment: one short paragraph naming the pull requests that landed and the asks they
met, then each dropped ask quoted with its reason. Apply `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` to
every word this run composed; quoted asks keep the developer's words.

Show the plan: the comment in full, the Status write, the close, the generated block's refresh by its
writer where the card's body holds `<!-- nwave:status:begin -->`, and CLEAR's lines. Put the comment in
the context block above the ask, outside its word count. Ask once, with `AskUserQuestion`: **yes**,
**yes, and retire the snapshot here too** where CLEAR offers it, or **stop**. Any answer but the two
yeses, Other included, is a stop: this skill asks the plan once, a tighter cap than the standard's. A
`stop` writes nothing: `STOPPED`. Write nothing before the developer's yes.

## CLOSE — comment first, then Done, then read it back

On the yes, run these in order, and **stop at the first write that fails**: report which writes ran,
quote the error, and repair nothing: `CLOSE-FAILED`. Where the error names a missing `project` scope, name
`gh auth refresh -s project`.

1. **Post the closing comment** — quote the heredoc's delimiter, because the body quotes the developer's
   words and an unquoted one runs their backticks and `$`:

   ```bash
   gh issue comment <n> -R <owner/repo> --body-file - <<'EOF'
   …
   EOF
   ```

   Keep the comment URL it prints.
2. **Write Status=Done** — read `issue(number:<n>){ projectItems(first:5){ nodes{ id project{ id } } } }`
   and take the node whose `project.id` is the board's project id; none means the card is not on this
   board, so skip the write and say so. Then `gh project item-edit --id <item> --project-id <project>
   --field-id <status-field> --single-select-option-id <done>`.
3. **Close the issue if it is still open** — read `issue(number:<n>){ state }` and run
   `gh issue close <n> -R <owner/repo>` only on `OPEN`, and never `gh issue close -c`: on a closed issue
   it drops the comment silently. A board workflow may close the issue moments after the read; a plain
   close on a closed issue writes nothing.
4. **Refresh the generated block through its one writer**, where the card's body holds
   `<!-- nwave:status:begin -->`: run `phil:nwave-issue-board`'s refresh for the card, which renders a
   closed card as finished. Edit nothing between the markers yourself.

The comment goes first because Done can close the issue, and a comment on a closed issue is easy to lose.
**Read the card back** with `issue(number:<n>){ state comments(last:5){ nodes{ url } }
projectItems(first:5){ nodes{ project{ id } fieldValueByName(name:"Status"){ ... on
ProjectV2ItemFieldSingleSelectValue{ name } } } } }`. The card must read closed, hold the comment's URL,
and — where a Status write ran — read Done on the board's project. Report any difference as found, and
repair nothing: an open card in Done, or a closed one outside it, is a defect for the developer.

**Clear what the work left behind** only after the read-back, as
`${CLAUDE_PLUGIN_ROOT}/skills/done/references/clear.md` orders it. Any refusal or error there leaves that
item and goes on; it is not a failed close.

The CLOSE line takes one of these shapes:

```
CLOSED: comment posted, Status Done, issue closed — read back clean
CLOSED: comment posted, Status skipped (card not on this board), issue closed — read back clean
CLOSED: read back closed but in Todo — expected Done
CLOSE FAILED: comment posted; Status write failed: <error> — nothing else ran
```

## Decision outcomes

Report exactly one terminal outcome, every run: `NOT-READY` · `STOPPED` · `CLOSED` · `CLOSE-FAILED` ·
`FINISHED`.

- **`NOT-READY`** — an ask stayed open or the work had not landed. Name every cause; never only the
  first.
- **`STOPPED`** — the developer answered stop, at RESOLVE or at the plan.
- **`CLOSED`** — the comment posted, the Status write ran or was reported skipped, the issue reads
  closed — by this run or a workflow — and the card was read back.
- **`CLOSE-FAILED`** — a write failed and the run stopped there.
- **`FINISHED`** — a run without a card: every session ask done or dropped, the session's pull requests
  landed or none named, and the plan ran, held nothing to run, or kept the snapshot at the developer's
  answer.

Report these alongside, each only when it fires: `OPEN-ASKS` (any ask open after ACCOUNT) ·
`NOT-LANDED` (a pull request open, missing or merged elsewhere, or a head rollup of anything but success
where a pipeline exists, or a list cut short) · `NO-PIPELINE` (no commit carries a check rollup) ·
`ASK-DROPPED` (the developer dropped an ask with a reason) · `READ-BACK-MISMATCH` (the card did not
read back closed, with the comment, in Done where a Status write ran) · `BLOCK-REFRESHED` (the generated
block was refreshed) · `CLEARED` (CLEAR deleted at least one item) · `LEFT` (an item survived: held,
kept at the developer's answer, or refused).

Report `WROTE-NOTHING` on every run that wrote nothing. It asserts that every call the run made was a
read: the grant accepts writes, and only the invariants below forbid them before the yes.

## Invariants

- **Write nothing before the developer's yes**, and after it only the comment, the Status, the close,
  the generated block's refresh, and CLEAR's snapshot retires, worktree removals and branch deletes.
  Remove only a worktree on the work's merged branch that reads `CLEAN` at the merged tip and that no
  other session locks, as CLEAR says; list every other with its commands. The command grants no `Write`
  and no `Edit`.
- **Run `python3` only on `${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py`, with `head` or `retire`,
  and on `${CLAUDE_PLUGIN_ROOT}/scripts/worktree-state.py`.**
- **Never pass `--force` or `-f`.** Pass `-D` only for a branch the developer chose to force-delete at
  its own question. The one force-family flag allowed is CLEAR's `--force-with-lease=<ref>:<oid>`, which
  makes a remote delete refuse a tip that moved.
- **Send only `query` documents through `gh api graphql`, never `mutation`.** Writes go through
  `gh issue comment`, `gh project item-edit`, `gh issue close` and, for the refresh alone,
  `gh issue edit --body-file`. Use none of `gh issue comment --edit-last` or `--delete-last`,
  `gh project item-edit --clear`, or any other `gh issue edit` flag. No tool boundary backs this.
- **On GitLab, send `glab api` only GETs.** Writes go through `glab issue note`, `glab issue close` and
  `glab issue update` with `--unlabel` for the status labels or, for the refresh alone,
  `--description`. Pipe `jq` only from `glab api`.
- **Leave every merge and every new pull request to the developer.**
- **Count only verified evidence.** An unverified ask is open.
- **Find the work by the forge's link or the card's number in a title or body, never by a branch name.**

## Self-test

`self-test/` holds this skill's fixtures, one directory each with a `manifest.json` and an
`expected.md`. `tests/test_done_fixtures.py` checks their structure and that every outcome above has
one; judging a run against them is a read by hand.
