# Global Development Standards

Development and writing standards live in `${CLAUDE_PLUGIN_ROOT}/rules/`. Rules load automatically based on the files you touch — no manual reading required.

## Key Principles (always apply)

- **Test first.** Write a failing test before production code.
- **Separate structure from behavior.** Refactoring commits and behavior-change commits are separate.
- **Dependencies point inward.** Business rules never import infrastructure.
- **Make every word tell.** Active voice, no needless words, clear on first read.
- **Empirical design over speculation.** Solve for what is really there, not imagined futures.

## Build path for this plugin

This repo's product is a plugin — skills, commands, agents, rules. Two tools own the two halves, and
neither substitutes for the other:

- **Understand it with `nw-discuss`.** New feature, new skill, new command: run DISCUSS before
  authoring. It produces the persona, the JTBD, the locked decisions and the slice split that the
  `docs/feature/<name>/` artifacts then hold. Skip it and the slice brief is invented at authoring
  time by whoever is typing.
- **Author, review and vet with `plugin-dev`.** Consult `plugin-dev:skill-development`,
  `command-development`, `agent-development` or `plugin-structure` **before writing the file**, not
  after — they own the schema, the frontmatter fields and the layout. Then run
  `plugin-dev:skill-reviewer` and `plugin-dev:plugin-validator` over the result. Neither is optional
  because a sibling file is a convenient template: copying the shape of an existing command
  propagates whatever that command got wrong and records nothing about whether it was checked.

DESIGN/DISTILL/DELIVER do **not** run here — the deliverable is prose, and this repo settled twice
that skills are authored rather than waved (`todo.md` 2026-06-17; edd-loop DDD8).

**Say in the commit which of the two ran.** Slice 03 of `groom-issues` was authored on 2026-08-13
from the slice brief and its sibling commands, with `plugin-dev` never loaded — a deviation from the
build path its own `feature-delta.md` declares, invisible afterwards because nothing records
compliance either way.

## Repo invariants run themselves

`scripts/check-invariants.py` runs the repo's checks at `SessionStart` and reports **only
failures** — command mutation declarations, and job → persona traceability in `docs/product/`.
A check nobody runs reports compliance by staying quiet, which is this board's recurring defect;
a runner that announces success every session trains people to stop reading it.

Add a check here when a defect is found twice. `devon-ui-developer` was referenced by `jobs.yaml`
with no file for six weeks, noticed three times and recorded as out-of-scope twice — a shallow
check passes because the field is populated.

## Where a finding about a standard goes

Running a skill against this repo produces two kinds of finding: defects in the target, and defects
in **the standard being applied**. The second kind has three routes, and the discriminator is what
the finding would change.

1. **It changes what a skill asserts** → fold into that `SKILL.md`, **add the self-test fixture that
   would have caught it**, bump the version. The fixture is what separates a fold-back from a note;
   without it the next run re-discovers the same hole. Where the standard lives in more than one
   skill, fold into each — rule 4's gap needed `groom-issues` *and* `issue-board`, because one
   asserted the rule and the other owned the declaration it read.
2. **It changes what this repo does** → here, in `CLAUDE.md`, **with the mechanism that enforces
   it** — a script, a hook, a frontmatter key. A convention with no enforcement is exactly the thing
   that gets noticed twice and written down neither time.
3. **It changes neither** — the world is broken, or the work exceeds a paragraph → **a card**. Not a
   fold-back. Without this route everything looks foldable and real work gets buried mid-`SKILL.md`.

**Not `rules/`.** That directory is the plugin's product and ships to every consumer; a convention
about developing this repo would land in strangers' projects where it means nothing.

Measured 2026-08-13 across nine fold-backs: six took route 1, three route 2, one took both.

## Every command declares whether it can mutate

`mutates: true | false` in the frontmatter, beside the grant it constrains. Checked by
`scripts/check-readonly-commands.py`, which fails the build on a `mutates: false` command that
grants `Write`/`Edit`, bare `Bash`, or a `Bash(...)` verb outside its read-only allowlist — and on
any command carrying no declaration at all.

**It is a claim about the grant, not about intent.** That is the half a script can verify.
`mutates: false` asserts the tool list makes mutation impossible; `mutates: true` asserts only that
the grant permits it, and says nothing about whether the command means to. `adversarial-review` is
the standing example: it reports and never edits, yet runs the project's test suite as its
deterministic oracle, and executing project code can write. It declares `true`, and its skill
carries the intent in prose.

**Absence of `Write` never meant read-only, and presence of bare `Bash` never meant mutating.**
Audited 2026-08-13: `ai-eos` and `adversarial-review` were byte-identical on both signals — no
`Write`/`Edit`, bare `Bash` — while one must never write and the other must execute arbitrary code.
Only the skill's prose separated them, and no validator reads that. Hence the declaration.

Adding a verb to the allowlist is a promise that it has no writing mode. Check before adding one.

**A `Bash(...)` grant may not contain a path or a variable.** To scope a command to one script, grant
the interpreter, put the path in the invocation instruction, and carry the real intent in prose — the
`adversarial-review` pattern above. Checked by `scripts/check-readonly-commands.py` for **every**
command, not only `mutates: false` ones.

**The rule stands; the reason it was written does not.** This paragraph used to say `allowed-tools` does
**not** interpolate `${CLAUDE_PLUGIN_ROOT}`, so such a grant "matches nothing" and merely prompts on
every run. **Measured 2026-08-21 against the shipped Claude Code 2.1.239: it does interpolate.**
`a["allowed-tools"]` is passed through `hOe`, and `hOe` does
`e.replace(/${CLAUDE_PLUGIN_ROOT}/g, () => r(t.path))`. The grant becomes an absolute path, and since a
command's body is interpolated by the same function at the same load, an invocation written
`${CLAUDE_PLUGIN_ROOT}/x.py` produces the very string the rule holds. **It can match.**

Three reasons the rule is kept, none of them the original:

1. **The grant a human reads is not the grant enforced.** After interpolation it is an absolute,
   install- and version-specific path. A reviewer cannot tell what it permits without knowing the
   install root — and a declaration whose boundary is unreadable defeats its own purpose.
2. **It covers exactly one spelling.** Any other route to the same script — a relative path, a `cd`
   first, a different interpreter path — shares no prefix and silently prompts.
3. **De facto convention.** The 2026-08-17 survey of 211 `Bash()` grants across this repo and every
   installed plugin found exactly one carrying a slash or a variable; the other 210 name a bare
   executable.

**Whether those three are worth an enforced check is now open**, because the fact that motivated it is
gone. Recorded rather than quietly kept: a check whose stated rationale is false is this board's
recurring defect wearing a different hat. `tests/test_check_readonly_commands.py` pins the distinction —
the behaviour is asserted, and the three refuted sentences are asserted *absent*, so nobody re-derives
the old reason from the code.

**The original note is still true of the first version of the check**, and worth keeping for its own
lesson: it silently passed because the function was written and never called. Test that a new check
fails on the input that motivated it before trusting a green run.

Written 2026-08-17, when `board-setup` shipped exactly that grant.

## This file ships to every consumer, and that is accepted

`CLAUDE.md` is copied verbatim into every install — confirmed in the 0.12.0, 0.19.0 and 0.36.0 cache
snapshots — so strangers receive 19KB of instructions about developing *this* repo, which mean nothing
in their project. So do `rgr-loop.md`, `docs/`, `tests/` and `pytest.ini`.

**Claude Code warns about it on load:** *"`CLAUDE.md` at the plugin root is not loaded as project
context. Remove it from the plugin root. To ship context with your plugin, use a skill instead."*

**Decided 2026-08-21: accept it, do not exclude it.** The alternative is a packaging step, and a
mis-listed exclude removes a file from installs *silently* — a worse failure than the current noise,
because a missing skill is invisible while a redundant file is merely useless. The official
`superpowers` plugin ships its dev files the same way.

What this costs, stated so it is not rediscovered as a defect: the warning keeps printing, and it is
**not** a signal about your working tree. Do not "fix" it by moving this file — `rules/` is the wrong
home (see *Where a finding about a standard goes*), and a skill would make repo conventions loadable in
strangers' projects, which is the same defect one layer down.

The one thing that would change this decision: a consumer reporting that shipped dev files caused real
confusion. Nothing has.

## Which copy is under test

**The released copy is what a `/phil:*` command runs — never this working tree.** Claude Code loads
the plugin from `~/.claude/plugins/cache/pmvanev-plugins/phil/<version>/`, snapshotted at install
time. Editing a skill here changes nothing about what the command executes until the plugin updates.

**That is deliberate: dogfooding tests what users actually get.** The cost is that the skew is
otherwise silent — nothing errors, and a run against a stale snapshot is indistinguishable from one
against your edits. On 2026-08-13 the gap reached five versions.

So a `SessionStart` hook in this repo's `.claude/settings.json` reports it. It lives in the working
tree rather than in `hooks/hooks.json` on purpose: a detector shipped inside the plugin would load
from the cache and could not report the gap that exists before the first update.

**A dogfood claim must name the version it exercised.** "I ran `/phil:groom-issues` and it reported
X" is a claim about the loaded version, not about your edits. Either update the plugin first, or say
which version the run was against. A run that drove the loop by hand rather than through the command
must say that too — it exercised the prose, not the command.

Do not trust `gitCommitSha` in `installed_plugins.json` to identify what is installed; on
2026-08-13 it pointed at a 0.12.0 commit while `version` read 0.27.0. Use `version` / `installPath`.

## Resuming work

**Starting a session to continue existing work? Run `/phil:resume` before anything else.** It reads
the session snapshot (`.session-handoff.md`, git-ignored and machine-local) and states up front
whether it is current or stale against the tree, then names the command that owns the work without
running it. With no snapshot it reconstructs from the artifacts and says that is what it did.

**It also checks the snapshot against the board**, reporting `BOARD-AGREES`, `BOARD-DIVERGES` or
`BOARD-UNREADABLE` on every read-back that has a recorded next action. The tree and the board are two
records of what is in flight and they fail in opposite directions; the freshness verdict can only see
one of them. It names both sides of a divergence and **never resolves it** — neither source is
authoritative, so picking one discards the other's work while reporting success.

That is why `resume` declares **`mutates: true` while writing nothing**: reading Projects v2 needs
`gh api graphql`, which can carry a mutation, and `gh project item-list` — the read-only alternative —
can under-report, which in a divergence detector means a missed divergence. The grant is still narrow
(no `Write`, no `Edit`, no bare `Bash`) and the read-only intent lives in the command's prose and the
skill's never-do list. Sanctioned 2026-08-17 for issue #24; the enforced guarantee became a declared
one, and that trade is stated rather than discovered.

Put a session down with `/phil:handoff`. It records only what a fresh session cannot derive — the
decisions, the approaches ruled out, the intended next action — and refuses to copy anything the
artifacts already own.

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
- Forge: GitHub — pass `-R pmvanev/phil-claude-plugin` on every `gh` call. Issue #12 exists in every
  repo, so an inferred remote mutates the wrong one successfully.
- Board: user project 3, `phil plugin`. The kanban is view 2 —
  https://github.com/users/pmvanev/projects/3/views/2 (view 1 is the table).
- Status is a project **field**, not a label. An issue must be `gh project item-add`ed before any
  field can be set; editing one that was never added does nothing.
- IDs: project `PVT_kwHOANPp-M4Bf-px` · Status field `PVTSSF_lAHOANPp-M4Bf-pxzhaNnGs` · options
  Todo `f75ad846`, In Progress `47fc9ee4`, Done `98236657`, Blocked `39094273`.
- **`updateProjectV2Field`'s `singleSelectOptions` is a FULL REPLACEMENT.** The per-option `id` is
  documented as *"optional — include this to preserve the option"*, so omitting an existing id drops that
  option **and every card's assignment to it**. Adding `Blocked` on 2026-08-14 meant passing all three
  existing ids back; getting it wrong would have destatused 25 cards with a call that reports success.
  Read the input shape before writing, and read the item statuses back after.
- **The wave is a label, never a column.** Seven wave columns are noise to everyone filing non-nWave work,
  which is most of this board. Decided 2026-08-14, reversing a reversal — and the lesson generalises:
  *refuting a decision's recorded rationale does not refute the decision.*
- **Auto-close on Done is ENABLED.** Setting Status=Done closes the issue; a `gh issue close -c`
  afterwards reports "already closed" and **silently drops the comment**. Post the closing
  comment first, then set Status. Moving Done→Todo does not reopen — use `gh issue reopen`.
- **The mirror workflow is ENABLED too: closing an issue sets Status=Done.** So `gh issue close` is a
  board write, and a card closed from the CLI never sits outside Done long enough for the open-in-Done
  check below to see it. Both directions are readable — `projectV2 { workflows { name enabled } }`
  returns `Auto-close issue` and `Item closed` as enabled — which is how this line got written on
  2026-08-14, after six weeks in which only the forward direction was recorded. The API exposes
  `name` and `enabled` and **not** the configured trigger statuses, so *which* status fires the
  close is an assumption (`Done`), not a probed fact.
- **A closing keyword in a commit message closes the card *and* sets Status=Done.** It fires on the
  bare `#N` and the rest of the sentence is never read: `fixed #22's unlinked path` closed #22 on
  2026-08-13, in a commit whose subject was another issue's slice. Write `issue 22` or `the #22 body`
  whenever the commit is not the fix. Recovery is two steps, because **`gh issue reopen` restores the
  issue and not the field** — the card is left OPEN while sitting in Done, and no view flags that
  combination. Set Status back by hand, and check with the open-in-Done query below.
- Verify the two can't drift: an open issue in Done, or a closed one outside it, is always a defect.
  Compare `gh issue list --state open --json number` against the project's items and their Status —
  the same one call that reads the board already returns both halves.
- `gh auth` needs the `project` scope — present as of 2026-08-12; `gh auth refresh -s project` if it
  is lost.
- Read the board with `gh api graphql`, never `gh project item-list` — item-list served a stale
  title for #10 on 2026-08-12 and can under-report. GraphQL returns items in board-position order,
  and that order is authoritative: the top Todo card is what to work on next.
- Docs root for absolute links (GitHub emits relative paths verbatim and they 404):
  `https://github.com/pmvanev/phil-claude-plugin/blob/main/`
- **Label families.** `bug` · `documentation` · `enhancement` are **multi-valued by decision, not by
  neglect** — this plugin's product is prose, so `documentation` names a surface, never a kind of work
  that could compete with `enhancement`. The two answer different questions, so a card carrying both
  (#2, #4) is correct. This bullet is the declaration `phil:groom-issues` rule 4 reads for
  project-local families; label descriptions may echo it and lose on disagreement.

  `wave: *` needs no entry here. It is single-valued in every nWave repo on
  `phil:nwave-issue-board`'s authority, and rule 4 applies that by default rather than waiting for a
  local copy — a repo that forgot the copy would go dark on the one family with a documented failure
  mode. Only declare `wave: *` here to *override* that, which nothing should.
- Forge mechanics: `phil:issue-board`. nWave feature/slice/step mapping: `phil:nwave-issue-board`.
