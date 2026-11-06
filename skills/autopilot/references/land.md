# LAND — merge the card's work on a green pipeline

Part of the `autopilot` skill; `../SKILL.md` governs this file as much as this file does. Read it whole
before the first landing step. The calls follow `gh` 2.97.0's and `glab` 1.112.0's `--help`; the
merge-request pipeline wait on GitLab has not been exercised.

Land only the writes the path names: a fallback path names none, so autopilot lands nothing there. The
moves below run in order. A step naming "push and open a pull request" covers moves 2 and 3; a step
naming "merge once its pipeline passes" covers 4 to 7. A path that names a push to the default branch is
a blocker: an outward write this skill never makes.

## The reads

Judge every state by reading the forge, never by a wait command's exit code.

**GitHub**, through `gh api graphql`, passing the owner, repo, branch and default branch as variables:

```graphql
query($o:String!,$r:String!,$b:String!,$d:String!){ repository(owner:$o,name:$r){
  mergeCommitAllowed squashMergeAllowed rebaseMergeAllowed deleteBranchOnMerge
  ref(qualifiedName:$d){ target{ ... on Commit{ oid statusCheckRollup{ state } } } }
  pullRequests(headRefName:$b, states:[OPEN, MERGED], first:5){ nodes{
    number state isDraft baseRefName headRefOid title body mergeCommit{ oid }
    closingIssuesReferences(first:20){ nodes{ number } }
    commits(last:100){ nodes{ commit{ oid message statusCheckRollup{ state } } } } } } } }
```

The pipeline state of a commit is its `statusCheckRollup.state`. For a commit no request holds, such as
the merge commit, read `repository{ object(oid:$sha){ ... on Commit{ statusCheckRollup{ state } } } }`.

**GitLab**, through `glab api --hostname <host>` GETs, with `<p>` as `/phil:start`'s GitLab reference
writes it:

- `projects/<p>` — `merge_method`, `remove_source_branch_after_merge`
- `projects/<p>/merge_requests?source_branch=<branch>&state=opened` — the open request, if any
- `projects/<p>/merge_requests/<iid>` — `sha`, `state`, `draft`, `target_branch`, `title`,
  `description`, `head_pipeline` (`sha`, `status`, `ref`, `web_url`), `merge_commit_sha`,
  `squash_commit_sha`
- `projects/<p>/merge_requests/<iid>/closes_issues` and `projects/<p>/merge_requests/<iid>/commits`
- `projects/<p>/pipelines?ref=<default>&sha=<sha>` — a commit's pipelines on the default branch

## Green, red, pending

| Verdict | GitHub `statusCheckRollup.state` | GitLab pipeline `status` |
|---|---|---|
| Green | `SUCCESS` | `success` |
| Red — a check; counts toward `k = 2` | `FAILURE`, `ERROR` | `failed` |
| Pending — wait | `PENDING`, `EXPECTED`, or none yet | `created`, `waiting_for_resource`, `preparing`, `pending`, `running`, `scheduled`, or none yet; `canceled` where a newer push superseded it |
| Blocker | still pending or none at the cap | `manual`, `skipped`, `canceled` with nothing newer, or still pending or none at the cap |

A pipeline judges a commit only when its commit is the request's head and the local `HEAD`: GitHub's
rollup on the commit whose `oid` is `headRefOid`; GitLab's `head_pipeline.sha` equal to `sha`. Right after
a push, the forge may still show the last commit's pipeline: that is pending, not a verdict.

**The wait.** Run each wait call with the Bash tool's `timeout: 600000`, then read the state. Wait again
while it is pending. A pipeline that has not registered after 10 minutes is absent, and a pipeline still
pending after 60 minutes is stuck; each is a blocker, because "merge once its pipeline passes" cannot be
met. The wait calls are:

- GitHub: `gh pr checks <pr> -R <owner/repo> --watch`. It may exit at once with "no checks reported"
  before the checks register: read, then wait again.
- GitLab: `glab ci status -R <repo> -b <ref> --wait`, where `<ref>` is the head pipeline's `ref` — the
  branch, or `refs/merge-requests/<iid>/head` for a merge-request pipeline.

## The moves

1. **Read the default branch's head.** Red there is a blocker before anything lands, citing the repo's
   own rule where it has one, such as "A red main stops the line".
2. **Push** the card's branch: `git push -u origin <branch>`. Never push with `--force` or
   `--force-with-lease`, and never to the default branch.
3. **Find or open the request.** Reuse the open request for the branch where its base is the default
   branch; a request on another base, or a draft, is a blocker. Otherwise open one, titled with the
   card's title with every `#` written as `issue `, its body saying what changed and that the decisions
   are on the card, naming the card as `issue <n>` and never after a closing keyword:
   - GitHub: `gh pr create -R <owner/repo> --base <default> --head <branch> --title '<title>' --body-file -`,
     the body on standard input.
   - GitLab: `glab mr create -R <repo> -s <branch> -b <default> -t '<title>' -d '<body>' --remove-source-branch=false --yes`.
     Start no line of the body with `/`: GitLab runs quick actions in a description.

   Write each `'` in a single-quoted title or body as `'\''`.
4. **Check that merging closes nothing.** Read the request's closing references and its commits'
   messages, title and body. A closing reference to the card, or a closing keyword such as `Closes`,
   `Fixes` or `Resolves` before any issue reference, is a blocker: merging would close a card, and done
   is the developer's.
5. **Wait and judge.** Wait as above, and judge the head commit. A red pipeline is a check: fix it
   within the card's scope, commit, push, and wait again — a pipeline still red after two fixes is a
   blocker.
6. **Merge** the head commit the run judged green, with the method a recorded rule names:
   - GitHub — else the first the repo allows of a merge commit, a squash, a rebase:
     `gh pr merge <pr> -R <owner/repo> --merge --match-head-commit <sha>`, with `--squash` or `--rebase`
     in place of `--merge`.
   - GitLab — the project's `merge_method` decides; pass no `--rebase`, which would push a head no
     pipeline judged: `glab mr merge <mr> -R <repo> --sha <sha> --auto-merge=false --yes`.

   Never merge with `--admin` or `--auto`, and on GitLab always pass `--auto-merge=false`, since
   `glab mr merge` sets auto-merge by default: each skips or hands off the check the merge waits for.
   Never pass `--delete-branch`, or `--remove-source-branch` without `=false`: the branches are
   `/phil:done`'s to remove. Where the repo deletes merged branches itself — GitHub's
   `deleteBranchOnMerge`, GitLab's `remove_source_branch_after_merge` — say so in the step comment.

   Read the merge back: `state` `MERGED` on GitHub, `merged` on GitLab, and the merge commit's SHA —
   GitHub's `mergeCommit.oid`; GitLab's `merge_commit_sha`, else `squash_commit_sha`, else `sha`. A merge
   the forge refuses — behind its base, a conflict, a fast-forward it cannot make — is a blocker,
   quoting the error.
7. **Watch the default branch on the merge commit.** Wait for its pipeline to register and finish —
   GitHub: `gh run list -R <owner/repo> --branch <default> --commit <sha>` until a run appears, then
   `gh run watch <id> -R <owner/repo>` for each; GitLab: `glab ci status -R <repo> -b <default> --wait`
   — and judge the merge commit itself, through the commit reads above, never the request's pipeline.
   A red default branch after the merge is a blocker. A default branch that runs no pipeline at all
   lands on the request's green; the step comment says so.

Report `LANDED` once the merge reads back merged and the default branch reads green on the merge commit,
or runs no pipeline. A landing is done on a later run only where both still hold. Leave the Status at In
Progress: the merge is not done, and the developer inspects before calling it so.
