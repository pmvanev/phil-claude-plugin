# phil plugin

This repo's product is the `phil` Claude Code plugin — skills, commands, agents, hooks and rules, mostly
prose.

## Build & test

- Run `python3 -m pytest -q` before committing. It drives the `*/self-test/` fixtures; `pytest.ini` keeps
  their inputs out of collection.
- `scripts/check-invariants.py` runs every repo check at `SessionStart` and prints only failures.
- Add a check to `scripts/check-invariants.py` when a defect is found twice. Wound: `jobs.yaml` named
  `devon-ui-developer` for six weeks with no file behind it.
- Before trusting a new check's green run, watch it refuse the input that motivated it. Wound: the first
  read-only check passed because its function was written and never called.

## Key Principles (always apply)

- **Test first.** Write a failing test before production code.
- **Separate structure from behavior.** Refactoring commits and behavior-change commits are separate.
- **Dependencies point inward.** Business rules never import infrastructure.
- **Make every word tell.** Write to `rules/writing.md`: active voice, no needless words, clear on first read.
- **Empirical design over speculation.** Solve for what is really there, not imagined futures.

## Rules load only when named

- A skill, command or agent that needs a standard from `rules/` names it and reads it;
  `scripts/check-rule-reachability.py` enforces it, exempting `definitions.md` and `llm-inference.md`.
  Plugins have no rules component, so nothing preloads them (Claude Code 2.1.252, 2026-08-31).
- The check proves a rule is *mentioned*, not *applied*. When every mention of a rule excludes it, split
  its checkable part into the standard a reviewer reads — as `ui.md` gave its checkable items to `ux.md`
  on 2026-08-31.
- A rule's `paths:` frontmatter takes effect only for a consumer who copies the rule into their own
  `.claude/rules/`.

## Commands declare mutation

- Declare `mutates: true` or `mutates: false` beside every command's `allowed-tools`;
  `scripts/check-readonly-commands.py` enforces it.
- Set `mutates:` by the grant, not the intent, and carry intent in the skill's prose. `adversarial-review`
  never edits yet declares `true`, because it runs the test suite; `resume` writes nothing yet declares
  `true`, because `gh api graphql` can mutate (sanctioned 2026-08-17, issue 24).
- Add a verb to the read-only allowlist only after confirming it has no writing mode. Wound: git's
  `--output=<file>` writes from `log`, `diff`, `show`, `blame`, `rev-list` and `shortlog` (git 2.53.0,
  2026-09-08).
- Name a bare executable in a `Bash(...)` grant — no path, no variable; to scope a command to one script,
  grant the interpreter and put the path in the invocation. `scripts/check-readonly-commands.py` enforces it.

## Board surfaces that compose prose

- A board surface that composes prose for the team names `rules/writing.md` and ships a fixture that
  fails without that citation. Eight surfaces do: `groom-ask`'s fields, the generated block's roster
  descriptions and clauses, the projected why/next/stack, a `## Chain` line's clause, the ranking basis,
  `assumed`-line rationales, `board-snapshot`'s descriptions and report lines, and `nwave-wave-summary`.
- Apply the standard only to words the surface composed; leave a human's words untouched. At `groom-ask`,
  decide per field by its provenance label: a suggestion or an `I rephrased your answer` rewrite is
  composed, a `you wrote` field is the human's.
- `groom-issues` composes nothing, and `groom-fix` writes a chain's edge but never its clause; each says
  in its own text that it applies no standard.
- A fixture supplies no candidate prose and asserts no word count. Wound: slice 01's candidates turned a
  composition test into "publish the shorter string". `tests/test_issue_board_fixtures.py` enforces both,
  for `issue-board` only. `tests/test_board_snapshot_fixtures.py` enforces word ceilings on purpose,
  because that skill specifies them.
- Open gaps: `groom-set`'s comments on an irreversible operation and `phil:rank-issues`' recorded basis
  cite the standard with no fixture. `nwave-issue-board` fixtures 30 and 31 have no driver (issue 42).
- A surface whose check has never fired says so in its own text and names what would change the verdict,
  as `board-snapshot` does (2026-09-08).
- Keep `groom-issues`' scan structural: five items, no style item.

## Build path for this plugin

- Run `nw-discuss` before authoring a new feature, skill or command. Stop after DISCUSS: the deliverable
  is prose, so DESIGN, DISTILL and DELIVER stay out (edd-loop DDD8).
- Read `plugin-dev:skill-development`, `command-development`, `agent-development` or `plugin-structure`
  before writing the file. Take the schema from plugin-dev, not from a sibling file — a copied shape
  carries the sibling's defects unchecked.
- Run `plugin-dev:skill-reviewer` and `plugin-dev:plugin-validator` over the result.
- Name in the commit message which of `nw-discuss` and `plugin-dev` ran. Wound: `groom-issues` slice 03
  was authored 2026-08-13 without plugin-dev, and nothing recorded it.

## Where a finding about a standard goes

| The finding changes | Route |
|---|---|
| What a skill asserts | Fold into every `SKILL.md` that holds the standard, add the self-test fixture that would have caught it, bump the version |
| What this repo does | Here, with the script, hook or frontmatter key that enforces it |
| Neither, or exceeds a paragraph | A card on the board |

Keep repo conventions out of `rules/`: that directory ships to every consumer.

## Decision requests

`decision-request: strict` — this repo opts in. `hooks/decision-request/check-ask.py` refuses any question
over 200 words, and here also any question or option naming an issue number, a file path or a bracketed
identifier. Rewrite a refused ask as the refusal directs.

## Resuming work

- To continue existing work, run `/phil:resume` before anything else. Put a session down with
  `/phil:handoff`; its snapshot, `.session-handoff.md`, is git-ignored and machine-local.

## This file ships to consumers

- Leave `CLAUDE.md` at the plugin root. Every install copies it, and Claude Code warns that it is not
  loaded as project context; the warning says nothing about the working tree.
- Decided 2026-08-21: a mis-listed packaging exclude would drop a file silently. Revisit if a consumer
  reports real confusion.

## Which copy is under test

- `/phil:*` commands run the released copy in `~/.claude/plugins/cache/pmvanev-plugins/phil/<version>/`,
  never this working tree. `scripts/check-plugin-skew.py` reports the gap at `SessionStart`; it lives in
  `.claude/settings.json` because a detector shipped in the plugin would load from the stale cache.
- A dogfood claim names the version it ran against, or says it drove the skill's prose by hand.
- Identify the installed copy by `version` or `installPath` in `installed_plugins.json`, never by
  `gitCommitSha`. Wound: on 2026-08-13 it named a 0.12.0 commit while `version` read 0.27.0.

## Issue board
<!-- phil:board-setup:v1:begin -->
generated 2026-08-17T20:47Z · do not edit inside these markers

Every line below carries its provenance and the query that produced it. Nothing here
was typed by a human; `assumed` lines say what is not knowable and why.

- Forge: GitHub at github.com — use `gh -R pmvanev/phil-claude-plugin` on every call *(probed · Q1)*
  issue #12 exists in every repo, so an inferred remote mutates the wrong one successfully
- Board: project `PVT_kwHOANPp-M4Bf-px` · number 3 · "phil plugin" · https://github.com/users/pmvanev/projects/3 *(probed · Q2+Q3)*
- Status mechanism: a project single-select FIELD named `Status` (id PVTSSF_lAHOANPp-M4Bf-pxzhaNnGs), not a label *(probed · Q4)*
  an issue must be `gh project item-add`ed before any field can be set; editing one that was never added does nothing
- Columns: Status options (4) on field `PVTSSF_lAHOANPp-M4Bf-pxzhaNnGs` — Todo `f75ad846` · In Progress `47fc9ee4` · Done `98236657` · Blocked `39094273` *(probed · Q4)*
  `updateProjectV2Field`'s `singleSelectOptions` is a FULL REPLACEMENT — omitting any of these 4 ids drops that option and every card's assignment to it, with a call that reports success
- Workflows: enabled — Auto-add sub-issues to project · Auto-close issue · Item added to project · Item closed · Pull request linked to issue · Pull request merged *(probed · Q5)*
  a status write is also an issue write when one of these is on, and the reverse
- Tier: not applicable on GitHub *(probed · Q1)*
  the tier bullet exists because GitLab gates scoped labels and `blocks` links behind Premium; GitHub gates neither, so no tier-dependent convention applies here
- Docs root: https://github.com/pmvanev/phil-claude-plugin/blob/main/ *(probed · Q1)*
  GitHub emits relative paths verbatim in issue bodies and they 404
- nWave: nWave repo — .nwave, docs/feature present; see `phil:nwave-issue-board` for the artifact to issue mapping *(probed · Q6)*
- Default branch: main *(probed · Q1)*
- How the board was found: NOT linked to the repository; found via the user's projects *(probed · Q2+Q3)*
  `repository.projectsV2` was empty, so the board was resolved from the user's one open project; a card reaches this board only via an explicit `gh project item-add`
- Views: 2 "View 2" https://github.com/users/pmvanev/projects/3/views/2 *(probed · Q7)*
  the LAYOUT is probed; which view a human calls `the kanban` is not
- `Auto-close issue` is enabled on this project, and **`Done` is assumed to fire it** *(assumed · Q5)*
  not knowable: which Status option fires it — `ProjectV2Workflow` exposes createdAt, enabled, fullDatabaseId, id, name, number, project, updatedAt — and no field for the configured trigger statuses
- `Item closed` is enabled on this project, and **`Done` is assumed to fire it** *(assumed · Q5)*
  not knowable: which Status option fires it — `ProjectV2Workflow` exposes createdAt, enabled, fullDatabaseId, id, name, number, project, updatedAt — and no field for the configured trigger statuses

**Queries**

- `Q1` — `gh repo view pmvanev/phil-claude-plugin --json nameWithOwner,defaultBranchRef,isFork,isPrivate`
- `Q2` — `{ repository(owner:"pmvanev", name:"phil-claude-plugin"){ projectsV2(first:20){ nodes { id number title url closed } } } }  → returned []`
- `Q3` — `{ user(login:"pmvanev"){ projectsV2(first:50){ totalCount nodes { id number title url closed } } } }`
- `Q4` — `{ user(login:"pmvanev"){ projectV2(number:3){ fields(first:50){ nodes { __typename ... on ProjectV2SingleSelectField { id name options { id name } } ... on ProjectV2Field { id name dataType } } } } } }`
- `Q5` — `{ user(login:"pmvanev"){ projectV2(number:3){ workflows(first:50){ nodes { name enabled } } } } }`
- `Q6` — `git ls-tree -d --name-only HEAD docs/feature .nwave`
- `Q7` — `{ user(login:"pmvanev"){ projectV2(number:3){ views(first:20){ nodes { number name layout } } } } }`

**Not probeable — only a human can declare these.** `label-families` (slice 03) · `local-task-system` (slice 03). Any answer appears in the *declared* region below, never here.
<!-- phil:board-setup:v1:end -->
<!-- phil:board-setup:declared:v1:begin -->
generated 2026-08-17T20:47Z · declarations, not probed facts — a human's answers

Nothing here was probed or inferred. `phil:groom-issues` rule 4 reads this region.

- Label family **(unprefixed)** (`bug`, `documentation`, `enhancement`): **multi-valued by decision** *(you declared · 2026-08-17)*
- Label family **wave** (`wave: discuss`): **single-valued** *(you declared · 2026-08-17)*
<!-- phil:board-setup:declared:v1:end -->
- The kanban is view 2 — https://github.com/users/pmvanev/projects/3/views/2 (view 1 is the table).
- Pass every existing option id back to `updateProjectV2Field`. `singleSelectOptions` replaces the whole
  list, and an omitted id drops that option and every card's assignment to it, in a call that reports
  success. Read the input shape before writing and the card statuses after. Wound: adding `Blocked` on
  2026-08-14 put 25 cards at risk.
- Track the wave with a `wave: *` label, never a column (decided 2026-08-14). Refuting a decision's
  recorded rationale does not refute the decision.
- Post a closing comment before setting Status=Done. Done closes the issue, and `gh issue close -c` on a
  closed issue drops the comment silently. Moving Done→Todo leaves the issue closed; reopen with
  `gh issue reopen`.
- `gh issue close` also sets Status=Done, so it is a board write.
- In a commit that does not fix an issue, write `issue 22` or `the #22 body`. A closing keyword fires on
  the bare `#N` whatever follows: `fixed #22's unlinked path` closed #22 on 2026-08-13. To recover, run
  `gh issue reopen`, then set Status by hand — reopening leaves the card in Done.
- An open issue in Done, or a closed one outside it, is a defect. The GraphQL read that loads the board
  returns both halves; compare them.
- `gh auth` needs the `project` scope: `gh auth refresh -s project`.
- Read the board with `gh api graphql`, never `gh project item-list`, which served a stale title for #10
  on 2026-08-12. GraphQL returns items in board order; the top Todo card is next.
- `documentation` names a surface, not a kind of work, so a card may carry it with `enhancement`.
  `wave: *` is single-valued on `phil:nwave-issue-board`'s authority; declare it here only to override.
- Forge mechanics: `phil:issue-board`. nWave feature, slice and step mapping: `phil:nwave-issue-board`.

Rationale and history cut 2026-10-13: git show 286274c:CLAUDE.md
