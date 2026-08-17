---
description: "Write a repo's board constants into its CLAUDE.md before they are learned by contact — probing the forge for the project and Status field ids, every option id, the enabled workflows, the tier and the docs root, into a delimited region where every line names the query that produced it. Reads the forge; never writes to it."
argument-hint: "[<owner/repo>]"
mutates: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3:*), AskUserQuestion, Skill
---

Load the `board-setup` skill at `${CLAUDE_PLUGIN_ROOT}/skills/board-setup/SKILL.md` and run
CONFIRM → PROBE → CLASSIFY → PLACE → DRIFT → OFFER → WRITE → REPORT.

`$ARGUMENTS`, when present, is the forge target. Confirm it against the git remote rather than
trusting it; when absent, derive a candidate from the remote and **confirm it before any call**.
Issue `#12` exists in every repo, so an inferred target reads the wrong board successfully.

**Probe with the script, never from memory**, and invoke it by these exact spellings — targets first,
which makes no forge call, then the probe once the target is confirmed:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/probe-board.py --list-targets
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/probe-board.py --repo OWNER/REPO
```

**Classify, place and diff with the second script, never by hand** — placement and line arithmetic
are where a silent one-line error destroys prose no probe can regenerate:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/region-place.py --file CLAUDE.md --classify
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/region-place.py --file CLAUDE.md --drift PROBE.json
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/region-place.py --file CLAUDE.md --place REGION.md --expect-sha SHA
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/region-place.py --file CLAUDE.md --retire LINE --expect-sha SHA
```

Pass back the `sha256` that `--classify` returned. A file that moved between read and write is
refused, not overwritten.

A `--list-targets` status of `ambiguous` — two remotes, or a fork — is a **question**, never a pick.

A relative path would resolve against the target repo, where the script does not exist. Every value
inside the markers comes out of that JSON; a value typed from recall is indistinguishable in the
finished file from a probed one, which is the failure this feature exists to close.

**This command writes, and the honest account of its grant is this: `mutates: true` is a claim about
the grant, not about intent.** It grants `Bash(python3:*)` and `Write`/`Edit`. No bare `Bash`, no
`gh`, no `glab`, no `gh project`, and no `git` — the scripts reach `git` through list-argv
`subprocess`, so a separate `Bash(git …)` rule would widen the grant while granting nothing new.

**`Write`/`Edit` are unscoped, and nothing in the frontmatter narrows them.** The *intent* is one
file, the `CLAUDE.md` in the working tree and never a sibling checkout — but that is a promise in
prose, not a property of the tool list, and it is stated that way round deliberately. In practice the
scripts own every write to the target, including creating an absent file; the grant exists for their
output path, not as a hand-placement fallback when a call refuses.

`Bash(python3:*)` is **wider than this command's intent**, and the widening is stated rather than
papered over: it permits any Python, including `python3 -c`. A grant naming a script's path was
tried first and is not viable — `allowed-tools` does not interpolate `${CLAUDE_PLUGIN_ROOT}` and
permission rules are literal prefix matches, so such a rule matches nothing and merely prompts on
every run while *looking* narrow. `scripts/check-readonly-commands.py` now fails any grant carrying a
path or a variable, so that mistake cannot be made again quietly.

The intent the grant cannot express lives here and in the skill's prose, the pattern `CLAUDE.md`
already documents for `adversarial-review`. **This command runs exactly two programs, and only one of
them writes:**

- `probe-board.py` — **reads only.** The forge and the git remotes; it creates no project, field,
  option or label, and writes no file.
- `region-place.py` — **writes exactly one file**, the `CLAUDE.md` passed as `--file`, and only under
  `--place` or `--retire`. `--classify` and `--drift` write nothing. Every write is guarded by
  `--expect-sha` and by a byte-identity check on the content outside the markers, run before anything
  reaches disk.

Both use list-argv `subprocess` with no `shell=True` and no interpolation into command strings.
Adding a mutating call to either would widen this command's reach without changing a line of
frontmatter — **the two scripts are the boundary, and reviewing them is how the boundary is kept.**

**Slices 01 and 02.** The target may be a `CLAUDE.md` with no `## Issue board` section or with a
hand-written one; a file that already contains a region stops with `REGION-PRESENT`, because safe
re-run is slice 05's.

**Content outside the markers is byte-identical on every path**, including failure and refusal. The
one exception is the retire offer: one whole line, deleted, on an explicit answer. Silence is not an
answer, and no line is ever rewritten or reflowed.

Ask exactly two things and no more — the forge target, and the retire offer on a contradicting line.
Any other question is a defect. Report half-probed values rather than writing them, and say plainly
that grooming will keep reporting rule 4 **unevaluated** until slice 03 ships the elicitation.
