---
description: "Write a repo's board constants into its CLAUDE.md before they are learned by contact — probing the forge for the project and Status field ids, every option id, the enabled workflows, the tier and the docs root, into a delimited region where every line names the query that produced it. Reads the forge; never writes to it."
argument-hint: "[<owner/repo>]"
mutates: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3:*), Bash(git remote:*), Bash(git rev-parse:*), Bash(git ls-tree:*), AskUserQuestion, Skill
---

Load the `board-setup` skill at `${CLAUDE_PLUGIN_ROOT}/skills/board-setup/SKILL.md` and run
CONFIRM → PROBE → PLACE → WRITE → REPORT.

`$ARGUMENTS`, when present, is the forge target. Confirm it against the git remote rather than
trusting it; when absent, derive a candidate from the remote and **confirm it before any call**.
Issue `#12` exists in every repo, so an inferred target reads the wrong board successfully.

**Probe with the script, never from memory**, and invoke it by these exact spellings — targets first,
which makes no forge call, then the probe once the target is confirmed:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/probe-board.py --list-targets
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/probe-board.py --repo OWNER/REPO
```

A `--list-targets` status of `ambiguous` — two remotes, or a fork — is a **question**, never a pick.

A relative path would resolve against the target repo, where the script does not exist. Every value
inside the markers comes out of that JSON; a value typed from recall is indistinguishable in the
finished file from a probed one, which is the failure this feature exists to close.

**This command writes, and the honest account of its grant is this: `mutates: true` is a claim about
the grant, not about intent.** It holds `Write`/`Edit` for one file — the `CLAUDE.md` in the working
tree, never a sibling checkout — and it grants `Bash(python3:*)` plus read-only `git remote`,
`git rev-parse` and `git ls-tree`. No bare `Bash`, no `gh`, no `glab`, no `gh project`.

`Bash(python3:*)` is **wider than this command's intent**, and the widening is stated rather than
papered over: it permits any Python, including `python3 -c`. A grant naming the script's path was
tried first and is not viable — `allowed-tools` does not interpolate `${CLAUDE_PLUGIN_ROOT}` and
permission rules are literal prefix matches, so such a rule matches nothing and merely prompts on
every run while *looking* narrow. `scripts/check-readonly-commands.py` now fails any grant carrying a
path or a variable, so that mistake cannot be made again quietly.

The intent the grant cannot express lives here and in the skill's prose, which is the pattern
`CLAUDE.md` already documents for `adversarial-review`: **this command runs exactly one program, the
probe script, and that script only reads.** It uses list-argv `subprocess` throughout with no
`shell=True` and no interpolation into command strings. Adding a mutating call to it would widen this
command's reach without changing a line of frontmatter — the script is the boundary, and reviewing it
is how the boundary is kept.

**Slice 01 only.** The target must be a `CLAUDE.md` with no `## Issue board` section; coexisting with
hand-written prose is slice 02, so a target that already has one stops with `SECTION-EXISTS`. Ask
nothing beyond confirming the forge target — a question here is a defect, because the measurement is
what comes out with none. Report half-probed values rather than writing them, and say plainly that
grooming will keep reporting rule 4 **unevaluated** until slice 03 ships the elicitation.
