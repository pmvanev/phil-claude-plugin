---
name: done
description: >-
  This skill should be used when the user asks "is this card done", "is this card ready to close",
  "can I close this issue", "did everything I asked for land", "wrap up this card", or runs /phil:done.
  It lists every ask the card received, each with verified evidence or marked open, and checks that every
  pull request merged into the default branch and that branch is green. Read-only, GitHub only, never
  merges. For unfinished work, use /phil:handoff.
---

# Done — is this card ready to close?

`/phil:handoff` puts a session down unfinished. This skill answers the question that comes before
putting one down **finished**: did every ask land, and did the work reach the default branch? It reports
`READY` or `NOT-READY` with the evidence behind each line.

**This version reports and writes nothing.** Closing the card and clearing what the work left behind are
not part of it.

## Inputs

- **The card** — the issue number from the argument. With none, ask for it; never infer it from the
  branch name.
- **The repo** — the forge line in the working tree's `CLAUDE.md`; `git rev-parse --show-toplevel` finds
  the root. Use `git rev-parse` for nothing else: a `<branch>:<path>` lookup reads a local ref that may be
  stale. Pass `-R <owner/repo>` on every `gh issue` call, and the owner and repo as variables to every
  `gh api graphql` query, which takes no `-R`: an inferred remote reads the wrong repo's issues
  successfully (`phil:issue-board`). With no forge line, stop and name `/phil:board-setup`. On a GitLab
  forge line, stop and say this skill covers GitHub only.

## FIND — the card, its pull requests and the default branch

Read the issue body with `gh issue view <n> -R <owner/repo> --json body`. Then run one query for the
default branch, the pull requests the forge links to the card, and the pull requests that mention it:

```bash
gh api graphql -f query='
query($o:String!,$r:String!,$n:Int!,$q:String!){
  repository(owner:$o,name:$r){
    defaultBranchRef{ name target{ ... on Commit{ oid statusCheckRollup{ state }
      history(first:20){ nodes{ oid statusCheckRollup{ state } } } } } }
    issue(number:$n){ closedByPullRequestsReferences(first:20, includeClosedPrs:true){
      pageInfo{ hasNextPage } nodes{ number title state merged baseRefName } } } }
  search(query:$q, type:ISSUE, first:50){ issueCount nodes{ ... on PullRequest{
    number title body state merged mergedAt baseRefName } } } }' \
  -f o=<owner> -f r=<repo> -F n=<n> -f q='repo:<owner>/<repo> is:pr <n> in:title,body'
```

The default branch is `defaultBranchRef.name`; call it `<default>` below.

**Find the card's pull requests, never by a branch name.** Keep every linked pull request. Keep a search
hit only where its title or body contains `#<n>` or `issue <n>`, case-insensitive, with `<n>` not
followed by a digit: `line 75` and `#175` do not name issue 75. Some repos mention a card in prose and
never link it, because a closing keyword closes the card early; the search finds those.

**Judge no list the query cut short.** Where `issueCount` exceeds 50 or `hasNextPage` is true, report
the pull request list incomplete and the card `NOT-READY`.

## ACCOUNT — every ask, with evidence or open

Collect the asks from the card and the current session:

1. **The card.** Every checklist item in the issue body, ticked or not, and every item under a heading
   containing *Done when*.
2. **The current session.** Each request the developer made in this conversation that bears on the
   card, and each task the session took on for it. Quote the developer's words as written. Where the
   conversation holds no such request, say so; earlier sessions' requests are not read. Where the
   conversation was compacted, say that asks before the compaction come from its summary.

List an ask once even when both places hold it. Mark each **done** or **open**. Done needs evidence a
call in this run verified, against `<default>`:

| Evidence | Verified when | Lookup |
|---|---|---|
| A pull request | `merged` is true and `baseRefName` is `<default>` | `pullRequest(number:<p>){ merged baseRefName }` |
| A commit | one of its associated pull requests merged into `<default>` | `object(expression:"<sha>"){ ... on Commit{ associatedPullRequests(first:5){ nodes{ number merged baseRefName } } } }`; a short sha works |
| A file | it exists at `<default>`'s head | `object(expression:"<branch>:<path>"){ id }`, with `<branch>` = `<default>`; null means absent |

Each lookup goes inside `repository(owner:$o,name:$r){ … }` in a `gh api graphql` query.

**Look for evidence an ask does not name.** Search the pull requests FIND kept for one whose title or
body carries the ask, and look up any file the ask names. Verify what you find. Where nothing turns up,
the ask is open: `no evidence found`, naming the lookups that came back empty.

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
NOT LANDED: PR 85 merged into finish-work/slice-02, not main
NOT LANDED: main red at 7358cad (FAILURE)
NOT LANDED: pull request list incomplete (73 search hits)
```

The last line, `READY` or `NOT READY: <causes>`, is for the developer. Then report the decision outcome
tokens below; the two are separate outputs.

## Decision outcomes

Report exactly one terminal outcome, every run: `READY` · `NOT-READY`.

- **`READY`** — every ask is done with verified evidence, and the work landed.
- **`NOT-READY`** — anything else. Name every cause; never only the first.

Report these alongside, each only when it fires: `OPEN-ASKS` (any ask open) · `NOT-LANDED` (a pull
request open, missing or merged elsewhere, or a head rollup of anything but success where a pipeline
exists, or a list cut short) · `NO-PIPELINE` (no commit carries a check rollup).

Report `WROTE-NOTHING` on every run. It asserts that every call this run made was a read: the
`gh api graphql` grant accepts a mutation document, and only the invariants below forbid one.

## Invariants

- **Write nothing.** No comment, label, Status, close or edit; no file. The command grants no `Write`
  and no `Edit`.
- **Send only `query` documents through `gh api graphql`, never `mutation`.** No tool boundary backs
  this.
- **Leave every merge and every new pull request to the developer.**
- **Count only verified evidence.** An unverified ask is open.
- **Find the work by the forge's link or the card's number in a title or body, never by a branch name.**

## Self-test

`self-test/` holds this skill's fixtures, one directory each with a `manifest.json` and an
`expected.md`. `tests/test_done_fixtures.py` checks their structure and that every outcome above has
one; judging a run against them is a read by hand.
