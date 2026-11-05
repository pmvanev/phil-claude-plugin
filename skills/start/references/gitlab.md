# GitLab — the same steps through `glab`

Part of the `start` skill. Read it whole before RESOLVE where the forge line names GitLab. `../SKILL.md`,
`claim.md`, `worktree.md` and `route.md` govern this file too: every step, report line and outcome
stands, and this file replaces their `gh` calls and GitHub fields. Where this file and those differ, this
file governs on GitLab. It adds no outcome. GitLab calls
a pull request a merge request; report it as `!<n>`.

Every read below was run against a GitLab 18 instance with `glab` 1.112.0 on 2026-11-05. The
two writes take their flags from `glab issue update --help` and `glab issue create --help`.

## Every call

- **Name the target.** Take the host and `<group/project>` from the forge line. Pass
  `-R https://<host>/<group/project>` on every `glab issue` call and `--hostname <host>` on every
  `glab api` call: outside a checkout of `<host>`, `glab` 1.112.0 sends a bare `-R <group/project>` to
  gitlab.com. Below, `<repo>` is that URL. In a `glab api` path, write the project as its URL-encoded
  path, with every `/` written `%2F` — `<group>%2F<project>`, `<p>` below — never `:id` or
  `:fullpath`, which `glab` fills in from the working directory's remote.
- **Read with GETs only.** `glab api` sends a GET until a field is added, then a POST. Put every
  parameter in the URL's query string, and wrap the URL in double quotes. Never pass `-f`, `-F`,
  `--field`, `--raw-field`, `--input`, `--form`, `-X` or `--method`.
- `glab api` takes no JSON flag and has no `--jq`: pipe it to `jq` to filter.
- Pass `--paginate` on every list but the search. A paginated list prints one JSON array per page, so
  filter it with `jq '.[] | …'`, which reads every page, and never count it with `length`, which counts
  each page alone. Where any page errors, the list was cut short: judge nothing from it.
- Quote `glab`'s real message, never a bare ERROR banner printed before it.
- Treat a card read answering `404 Not found` as an answer, `NO-MATCH`. Any other failed read before
  CLAIM is `CANNOT-RUN`, quoting the error, as `../SKILL.md` says.
- A write refused for `insufficient_scope` needs a token with the `api` scope: name
  `glab auth login --hostname <host>`.

## The board constants

A GitLab board is a view over labels: a column is a label, and its name is its only id. The constants
are the **status family** — the labels the `CLAUDE.md` board block names as its status mechanism, such
as `status::to-do`, `status::in-progress` and `status::blocked`. There is no project item, field id or
option id to read.

Find three labels in the family by name, ignoring case, reading the part after `::` where there is one:

- **In Progress** reads `in-progress`, `in progress` or `doing`.
- **Blocked** reads `blocked`.
- **Done** reads `done`. A family with no done label never fires that check: the board's closed list is
  its Done.

A card's **status labels** are the labels the family lists, and any other label sharing their scope,
such as a stale `status::review` beside `status::to-do`. A `wave::` label is never a status label, even
where the block lists the waves as a column family.

**Where none or several labels match In Progress, ask which label to use** before the first claim
write, listing the family in the context block, and write no status label until the developer answers.
Accept only an answer the family lists; Other naming any other label, or no answer, is `STOPPED`, with
nothing written. Nothing records the answer, so the next run asks again.

**The tier** comes from the block's `Tier:` line. GitLab Free holds one assignee per issue, and a block
that names no tier counts as Free (`phil:issue-board`).

**With no board block, or a block that names no status family**, the claim writes no status label and
reports `NO-BOARD-BLOCK`, naming `/phil:board-setup`. CHECK then reads a done or blocked label by the
same names from every label the card carries.

## RESOLVE

Read `projects/<p>` first: its `default_branch` serves WORKTREE, and any failure here is `CANNOT-RUN`.
A mistyped project, or one the token cannot see, answers `404 Project Not Found`, never a missing card.

| GitHub read | GitLab call | Fields |
|---|---|---|
| `viewer{ login }` | `user` | `username` is `viewer.login` |
| the number query | `projects/<p>/issues/<n>` | `iid`, `title`, `description`, `state` (`opened` or `closed`), `labels`, `assignees[].username`, `web_url` |
| the search | below | `iid`, `title` |

- **No signed-in account** — `user` answers 401: name `glab auth login --hostname <host>`:
  `CANNOT-RUN`.
- **A number names an issue or nothing.** Issue and merge-request numbers are separate on GitLab, so
  `projects/<p>/issues/<n>` answering `404 Not found` is `NO-MATCH`. A URL ending
  `/-/merge_requests/<n>` names a merge request: `NO-MATCH`, as a pull request is on GitHub. A URL
  ending `/-/issues/<n>` in this project names the card.
- **The search** — GitLab's `search` has no qualifiers to strip, and it matches every word, in any
  order. Percent-encode the argument, every character but letters, digits, `-`, `_`, `.` and `~`, so
  no `&`, quote or `$` reaches the URL or the shell:

  ```bash
  glab api --hostname <host> \
    "projects/<p>/issues?state=opened&search=<encoded argument>&in=title,description&per_page=21" |
    jq -c '.[] | {iid, title}'
  ```

  This is the one list read without `--paginate`: RESOLVE asks only whether more than 20 matched, and a
  21st entry on the one page answers it. Count the entries. At 21, say more than 20 matched: the page
  holds no total.

## Filing a card

Where `claim.md`'s *Filing a card* runs `gh issue create`, run:

```bash
glab issue create -R <repo> --title '<the words>' --description '' --yes
```

Write each `'` in the words as `'\''`. Use `glab issue create` only with `-R`, `--title`,
`--description ''` and `--yes`: a label, an assignee, a milestone, a template or `--web` would put words
or state on the card that are not the developer's. Settled 2026-11-05 with `glab` 1.112.0 outside a
terminal: `--description ''` gets past the non-interactive check and opens no editor, and without it
`glab` refuses with `'--title' and '--description' (or '--template') required for non-interactive mode`.
Take the number from the `/-/issues/<n>` URL it prints. The claim's label swap puts the new card in its
column; there is no item to add.

## CHECK

1. **A closed card** — `state` reads `closed`: name `glab issue reopen <n> -R <repo>`:
   `REFUSED-CLOSED`.
2. **A done label on an open card** is `OPEN-IN-DONE`, asked as `../SKILL.md` says. **A blocked label**
   asks the same way, with no outcome token of its own.
3. **Someone else's card** — compare `assignees[].username` with `username`. On Free, the ask says
   going on cannot keep both: the card stays theirs, the run swaps the label and assigns no one, and
   the claim reports `NOT-ASSIGNED`.
4. **Worktrees** — `worktree.md`'s *Find the card's worktrees*, with the merge-request read below.

## CLAIM

`claim.md`'s order, rules and outcomes stand, with two writes in place of three. **The claim runs no
`item-add`**: the label write alone moves the card into its column (`phil:issue-board`). Skip a write
that would change nothing.

1. **Swap the status label** — first confirm the In Progress label exists with a GET of
   `projects/<p>/labels/<encoded label>`: `--label` with a name the project lacks creates that label,
   exits 0 and reads back as set, while the card leaves every board list. A `404 Label Not Found` writes
   nothing: `CLAIM-FAILED`, naming `/phil:board-setup`. Then add the In Progress label and remove every
   other status label the card carries, in one call, on every tier: Premium drops a scoped sibling
   server-side, and Free drops nothing.

   ```bash
   glab issue update <n> -R <repo> --label '<in-progress>' --unlabel '<others>'
   ```

   `<others>` joins the labels with `,`. Where the card carries no other status label, leave out
   `--unlabel`; where it carries In Progress and no other, skip the write. **Never create a board
   list**: it reports success, adds a column and leaves the card where it was. This is the claim's board
   write: a failed one is `CLAIM-FAILED`, read back once first.
2. **Assign the developer** — add, never replace:

   ```bash
   glab issue update <n> -R <repo> --assignee +<login>
   ```

   A login without the `+` replaces every assignee and still exits 0 (`glab issue update --help`,
   1.112.0), which would remove a teammate the run promised to keep. A failed assign is `NOT-ASSIGNED`.
   On Free, assign only a card with no assignee: CHECK said so before the claim.

**Read the claim back** with `projects/<p>/issues/<n>`:

- the card carries the In Progress label and no other status label — only where a status label was
  written or found. A sibling left beside it on Free is `READ-BACK-MISMATCH`;
- `username` is among `assignees[].username` — only where the assign did not fail;
- every login RESOLVE read is still among them. A missing one is `READ-BACK-MISMATCH`, naming it.

Re-read once before concluding. A sibling that survives the re-read is a mismatch, never lag: GitLab has
no Projects v2 lag and no add-to-project workflow.

The claim line names labels where GitHub names a Status:

```
CLAIMED: status::in-progress set, status::to-do removed, assigned to pvanevery — read back
CLAIMED: already status::in-progress and assigned to pvanevery — nothing written
CLAIMED: status::in-progress set, status::to-do removed, assigned to pvanevery beside colleague — read back
NO BOARD BLOCK: no status family — run /phil:board-setup; assigned to pvanevery — read back
CLAIM FAILED: setting status::in-progress failed: <error> — read back: status::to-do, unassigned
READ-BACK MISMATCH: status::in-progress set, and status::to-do is still on the card
READ-BACK MISMATCH: colleague is no longer among the assignees
CLAIM FAILED: status::in-progress is not a label on this project — nothing written; run /phil:board-setup
NOT ASSIGNED: status::in-progress set — read back; GitLab Free holds one assignee, and the card stays colleague's
```

The CARD line names the card's status label where GitHub names its Status, or `no status label`.

## WORKTREE

`worktree.md`'s fetch, cut, entry and lock ask stand. A worktree is the card's where it is checked out on
the `source_branch` of the developer's open merge request naming the card. Find those on every page:

```bash
glab api --hostname <host> --paginate \
  "projects/<p>/merge_requests?state=opened&author_username=<login>&per_page=100" |
  jq -c '.[] | select((.title+" "+(.description//"")) | test("(#|issue )<n>([^0-9]|$)"; "i"))
    | {iid, title, source_branch}'
```

Read the default branch's name as `default_branch` from `projects/<p>`, and the remote's head as
`commit.id` from `projects/<p>/repository/branches/<default>`, URL-encoding any `/` in the branch name
as `%2F`. Compare the new worktree's base with that head, where `worktree.md` reads
`defaultBranchRef`.

The author and the state narrow the list; the `jq` pattern finds the card, because GitLab's `search`
may drop a short word such as a two-digit number.

The underway line names the merge request:

```
UNDERWAY: !12 is open on worktree-issue-58-show-who-owns-an-item, with no worktree here — nothing cut; next: /phil:resume
```

## ROUTE

`route.md`'s rules stand. Read `wave::<name>` as `wave: <name>` at its rule 2:
`phil:nwave-issue-board` writes the scoped form where scoped labels exist.
