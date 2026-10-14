# The scan's own invariants — `/phil:groom-issues`

Part of the `groom-issues` skill. `/phil:groom-issues` reads it whole, with `SKILL.md`, before its first
call. Its `SKILL.md` governs this file too.

## Invariants

`SKILL.md` § *Invariants* holds the ones all four commands share; these bind this command as well.

`/phil:groom-issues` (the scan) also:

- **Writes nothing** — no issue edits, labels, comments or milestones. It holds no `Write` and no
  `Edit`, so a session that finds itself needing one has misread the command.
- **Sends only `query` documents through `gh api graphql`, never a `mutation` document.** No tool
  boundary backs this one. Refuse rather than improvise: a resolution that needs a forge write is
  `/phil:groom-set`'s, and handing it over is the design.
- **Confines the graphql grant to the parent edge alone.** Anything else it could reach is a check nobody
  has reasoned about, arriving without a rule, an evidence tier or a fixture.
