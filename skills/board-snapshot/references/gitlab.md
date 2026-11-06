# GitLab — the same snapshot through `glab`

Part of the `board-snapshot` skill. Read it whole before the first call where the forge line names
GitLab. `../SKILL.md` governs this file too: both modes, the ceiling, every report line, every outcome
and every invariant stand. This file replaces the GitHub reads and adds no outcome; where this file and
`../SKILL.md` differ, this file governs on GitLab.

## The constants

Read them from the target repo's `CLAUDE.md` board block, as on GitHub: the host and `<group/project>`
from the forge line, and the **status family** — the labels the block names as its status mechanism.
With no status family, stop and name `/phil:board-setup`, as the command does for missing constants.
Below, `<p>` is `<group/project>` with every `/` written `%2F`.

## Every call

- Pass `--hostname <host>` on every `glab api` call. Write the project as `<p>`, never `:id` or
  `:fullpath`, which `glab` fills in from the working directory's remote.
- Send GETs only: every parameter in the URL's query string, in double quotes.
- Pipe `glab api` to `jq`: it prints JSON and has no `--jq`.
- Quote `glab`'s own message whole, never only an `ERROR` banner it prints before one.

## The read

Read each column, and the Open list, as *Read a GitLab board's columns*, in
`${CLAUDE_PLUGIN_ROOT}/skills/issue-board/SKILL.md`, says: confirm each status label exists, then read
the open issues carrying it, in board order, every page. That section also names which label in the
family is In Progress, Blocked, To Do and Done. A missing label, or several labels matching one name,
is `SNAPSHOT-PARTIAL`, naming the labels and `/phil:board-setup`.

| Section or line | GitLab read |
|---|---|
| **Blocked** | the Blocked label's column |
| **In flight** | the In Progress label's column |
| **Queued** | the To Do label's column, its first *N* |
| **Uncolumned** | open issues carrying no label in the family: the board's Open list |
| **Drift** | an open issue carrying the Done label, or carrying two status labels |

The Open list's read also serves `--all`, which needs every open card.

- **A blocked card's reason** is its `description`'s `## Chain` line, already in the column's
  response: no call per card. Where it has none, say the blocker is unrecorded.
- **A family with no To Do label** queues the Open list instead, in board order, and reports no
  uncolumned cards: on that board the Open list is the queue.
- **A closed card outside Done never fires on GitLab**: every closed issue sits in the Closed list,
  whatever labels it carries. Read no closed issue.
- **A card carrying two status labels** appears in each column it holds; one drift line names it and
  `phil:groom-issues`, since it is a card in two columns.
- **A card in a family column outside the four**, such as `status::review`, sits in no mode 1 section,
  as a card in a fifth Status option does on GitHub. `--all` gives it a row.
- **`OFF-BOARD` never fires on GitLab**: a board is a view over the project's issues, so every open
  issue is on it. Make no reconciliation call.
- **`--all`** renders the columns in the order the board block lists the family, each in board order,
  then the Open list, marked as uncolumned, or as the queue where the family names no To Do label.
  Compose each description from the issue's `description`.
- **A page that errors** makes the read partial: `SNAPSHOT-PARTIAL`.

Say where the queued order came from as on GitHub: the board's own order, not this command's.
