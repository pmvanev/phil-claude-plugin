# Expected — BSNAP-SELFTEST-14

`SNAPSHOT-RENDERED` · `OFF-BOARD` · `READ-ONLY`

## What must happen

The three sections render from the nine cards the project holds. One line reports that four open issues
are not on the board, and names `phil:issue-board` as what adds them.

## What must NOT happen

The four are not rendered as cards. They have no Status and no board position, and giving them one would
misreport the board.

They are not omitted in silence. The skill forbids a completeness claim over a partial read, and this is
the same failure reached structurally: the query returned everything it could, and everything it could
was not everything there is.

Nothing is added to the project.

## Why this fixture exists

`CLAUDE.md` records that this board is **not linked to the repository** and that a card reaches it only
via an explicit add. So the gap is not hypothetical here — it is the default state of the board this
skill was written against.
