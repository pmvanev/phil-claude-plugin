# GitLab — the same steps through `glab`

Part of the `done` skill. Read it whole before FIND when the forge line names GitLab. `SKILL.md` and
`clear.md` govern this file too: every rule, step, report line and outcome stands, and this file
replaces only their `gh` calls and GitHub fields. GitLab calls a pull request a merge request; report it
as `!<n>`: `LANDED: !193 merged into main; main green at 071dc6b8`.

Every call below was run against a GitLab 18 instance with `glab` 1.112.0 on 2026-11-03, except the
three writes, whose flags come from `glab <subcommand> --help`.

## Every call

- **Name the target.** Take the host and `<group/project>` from the forge line. Pass
  `-R https://<host>/<group/project>` on every `glab issue` call and `--hostname <host>` on every
  `glab api` call: a bare `-R <group/project>` sends the call to gitlab.com outside a checkout of
  `<host>` (`glab` 1.112.0, 2026-11-03). Below, `<repo>` is that URL. In a `glab api` path,
  write the project as its URL-encoded path, `<group>%2F<project>` — `<p>` below — never `:id` or
  `:fullpath`, which `glab` fills in from the working directory's remote. URL-encode a branch or a file
  path inside a path segment too: `/` becomes `%2F`.
- **Read with GETs only.** `glab api` sends a GET until a field is added, then a POST. Put every
  parameter in the URL's query string. Never pass `-f`, `-F`, `--field`, `--raw-field`, `--input`,
  `--form`, `-X` or `--method`.
- `glab api` takes no JSON flag and has no `--jq`: pipe it to `jq` to filter.
- Pass `--paginate` on every list. Where any page errors, the list was cut short: judge nothing from it.
  A paginated list prints one JSON array per page, so filter it with `jq '.[] | …'`, which reads every
  page, and never count it with `length`, which counts each page alone (`glab` 1.112.0, 2026-11-03).
- `glab` prints a bare `ERROR` line before the real message; quote the message.
- A 404 on a branch or a file is an answer — absent — but any other error leaves the evidence
  unverified.

## FIND

| GitHub read | GitLab call | Fields |
|---|---|---|
| `viewer{ login }` | `user`, then `user/emails` | `username` is `viewer.login`. The developer's commit identities are `email`, `commit_email` and every `email` from `user/emails` |
| the card | `projects/<p>/issues/<n>` | `description`, `state` (`opened` or `closed`), `labels`, `assignees` |
| `defaultBranchRef` | `projects/<p>`, then `projects/<p>/repository/branches/<default>` | `default_branch`; the head is `commit.id` |
| `closedByPullRequestsReferences` | `projects/<p>/issues/<n>/closed_by?per_page=100` | GitLab's closing link |
| the search | below | the same card pattern |

```bash
glab api --hostname <host> --paginate \
  "projects/<p>/merge_requests?state=all&search=<n>&in=title,description&per_page=100" |
  jq -c '.[] | select((.title+" "+(.description//"")) | test("(#|issue )<n>([^0-9]|$)"; "i"))
    | {iid, title, state, target_branch, source_branch, sha, source_project_id, target_project_id,
       author: .author.username}'
```

Read each merge request's fields as GitHub's:

| GitHub | GitLab |
|---|---|
| `number` | `iid` |
| `state`, `merged` | `state`: `merged`, `opened`, `closed`, or `locked`, which counts as open |
| `baseRefName` | `target_branch` |
| `headRefName` | `source_branch` |
| `headRefOid` | `sha` |
| `isCrossRepository` | `source_project_id` differs from `target_project_id` |
| `author{ login }` | `author.username` |

**The default branch's pipeline is the rollup.** Read
`projects/<p>/pipelines?ref=<default>&sha=<head>&per_page=1`, whose first entry is the head's newest
pipeline. Only `success` is green; name any other status — `running`, `pending`, `created`, `failed`,
`canceled`, `skipped`, `manual` — as not landed. Where the head has no pipeline, read
`projects/<p>/pipelines?ref=<default>&per_page=1`: an entry there means the head has not reported yet,
and none means the repo has `no pipeline`, never green.

## ACCOUNT

| Evidence | GitLab call | Verified when |
|---|---|---|
| A merge request | `projects/<p>/merge_requests/<m>` | `state` is `merged` and `target_branch` is `<default>` |
| A commit | `projects/<p>/repository/commits/<sha>/merge_requests` | one merged into `<default>`; a short sha works |
| A file | `projects/<p>/repository/files/<path>?ref=<default>` | it answers; a 404 means absent |
| The card's body | the card read | `description` holds the change |
| The card's board state | the card read | `labels` and `assignees` read as the ask set them |
| A commit pushed to `<default>` with no merge request (`no-card.md`) | `projects/<p>/repository/compare?from=<default>&to=<sha>` | it lists no commits |

## CLOSE

A GitLab board column is a label, and the board's closed list is its Done. The status labels are the
family the `CLAUDE.md` board block names as its status mechanism. Where it names none, skip the label
write, report the skip and name `/phil:board-setup`, as `SKILL.md` says. On the yes, run these in
order, and stop at the first write that fails:

1. **Post the closing note** — the quoted delimiter keeps the developer's backticks and `$` inert:

   ```bash
   glab issue note <n> -R <repo> -m "$(cat <<'EOF'
   …
   EOF
   )"
   ```

   Keep the URL it prints.
2. **Remove the status labels** — read the card's `labels`, and remove every status label it carries:
   `glab issue update <n> -R <repo> --unlabel '<label>,<label>'`. Where it carries none, skip the write
   and say so. Never add a label, and never create a board list.
3. **Close the issue if it is still open** — read `state` again, and run `glab issue close <n> -R <repo>`
   only on `opened`.
4. **Refresh the generated block** through `phil:nwave-issue-board`, as `SKILL.md` says. Its write:

   ```bash
   glab issue update <n> -R <repo> --description "$(cat <<'EOF'
   …
   EOF
   )"
   ```

**Read the card back** with the card read and `projects/<p>/issues/<n>/notes/<id>`, taking `<id>` from
the `#note_<id>` the note's URL ends in: the label removal and the close add system notes, which can
push the closing note off a page of recent ones. The card must read `closed`, carry no status label,
and answer that note. The CLOSE line names the label:
`CLOSED: note posted, status::in-progress removed, issue closed — read back clean`.

## CLEAR

`clear.md`'s rules stand; these are its calls.

- **Candidates** — merge requests merged into `<default>` from the same project, whose
  `author.username` is the developer's.
- **Remote branch** — `projects/<p>/repository/branches/<branch>` gives the tip as `commit.id` and
  `protected`, which holds the branch where it reads true. A 404 means the merge deleted it; skip it.
  `projects/<p>/merge_requests?state=opened&source_branch=<branch>` and
  `projects/<p>/merge_requests?state=opened&target_branch=<branch>` find an open merge request that
  uses it; any hit holds it.
- **The remote** — every push URL `git remote get-url --push --all <remote>` prints names
  `<group/project>` on `<host>`: `git@<host>:<group/project>.git`,
  `ssh://git@<host>[:<port>]/<group/project>.git` or `https://<host>/<group/project>.git`.
- **FORCE, remote copy** — read the tip from the branch read, then
  `projects/<p>/repository/compare?from=<default>&to=<branch>`, whose `commits` list what the delete
  would lose with `short_id`, `title`, `author_name` and `author_email`; then read the tip again. Where
  the two reads differ, hold the branch: the list may not be the tip's. Keep the tip as the shown tip.
  The branch descends from the merge request's `sha` where
  `projects/<p>/repository/compare?from=<branch>&to=<sha>` lists no commits. A commit is the
  developer's where its `author_email` is one of the developer's commit identities. Past 50 commits,
  offer nothing.
- **FORCE, local copy** — `clear.md`'s `git` calls, with each `%ae` checked against the same
  identities.
- **Deletes** — `clear.md`'s `git branch -d`, `git branch -D` and leased `git push --delete`, unchanged.
