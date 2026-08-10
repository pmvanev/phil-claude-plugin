# Evolution — issue-board (2026-08-10)

## What shipped

`skills/issue-board/SKILL.md` — a knowledge-only skill (no paired command) carrying the semantics
for driving GitLab and GitHub issue boards from the command line with `glab` and `gh`.

It is the residue of two research passes that both concluded **buy, don't build**:

- `docs/research/tooling/local-markdown-kanban-backlog-tooling-research.md` — local markdown kanban
  tooling. Outcome: adopt Backlog.md plus its VS Code extension.
- `docs/research/tooling/claude-driven-forge-issue-boards-research.md` — whether an agent can drive
  forge issue boards without custom code. Outcome: `gh` and `glab`, no MCP server, no plugin, no
  sync layer.

Both reports carry supersession blocks recording what execution overturned in them.

## Why

Nothing needed building except knowledge. The CLIs already do the work; what neither
`glab --help` nor `gh --help` explains is the handful of semantics where a wrong guess **reports
success**:

- GitLab boards are label views, so a card move is a label swap. Creating a board list instead
  reports success, adds a column, and leaves the card where it was.
- Scoped labels (`key::value`) are **Premium or Ultimate**. On Free they are labels with colons in
  them and nothing enforces exclusion — the failure appears only on someone else's instance.
- GitHub has no scoped labels at all. A board is a Projects v2 Status *field* on a separate API,
  and an issue must be `item-add`ed before it has a field to set.
- Both CLIs infer the project from the current directory's git remote, and issue #12 exists in
  every project.

## The design, in one idea

**Generic semantics ship; instance constants don't.** The skill carries what is true of any GitLab
or GitHub, and ends with a `CLAUDE.md` template each project fills in with its own host, IDs, and
tier. That split is why this is a distributable skill rather than a note in one repo's `CLAUDE.md`.

Knowledge-only, with no command, because there is no workflow, gate, artifact, or argument to
parse. Every command in `commands/` fronts a multi-step gated process; a `/phil:issue-board` would
be a lookup wrapper.

## Outcome (before → after)

| | Before | After |
|---|---|---|
| Driving a board | Hand-rolled API scripts per project | `glab` / `gh`, one command per operation |
| Tier awareness | None — a Premium-only mechanism assumed universal | Tier probe first, Free path documented |
| Target safety | `glab issue update 12` against whatever the cwd pointed at | `-R` on every invocation, stated as a rule |
| Certificate handling | Process-wide TLS disabling | CA import as the fix; host-scoped bypass as a warned, developer-authorized stopgap |

## Scope / accepted limitations

- **No sync.** The skill states the partition rule — one system of record per scope, joined by an
  issue reference — and explicitly declines bidirectional sync.
- **Two command forms ship marked unverified**: the `glab config set skip_tls_verify` flag and the
  `blocks`-link creation call. Both are labelled in the text rather than presented as settled.
- **Projects v2 remains owner-scoped**, so a GitHub board cannot be driven by a repository-scoped
  token. Noted, not solved.

## Follow-ups

- `plugin-dev:skill-reviewer` raised ~30 medium/low findings across today's three skills that were
  not folded into this change; queue them as issues.
- The repo has **no `LICENSE`**. `ai-eos` summarizes a CC BY-SA source with attribution present, so
  the share-alike question is open until a license statement exists somewhere in the repo.
- `nw-skill-reviewer` approved all three of today's skills with zero actionable findings, including
  one verifiably false certification. Treat it as a structure check, not a quality gate.
