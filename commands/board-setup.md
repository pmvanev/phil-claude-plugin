---
description: "Write a repo's board constants into its CLAUDE.md before they are learned by contact — probing GitHub or GitLab for the project and Status field ids, every option id, the enabled workflows, the tier and the docs root, into a delimited region where every line names the query that produced it and carries `probed` or `assumed`. Asks only what no forge records, coexists with prose it cannot regenerate, and re-runs writing zero bytes when nothing moved. Reads the forge; never writes to it."
argument-hint: "[<owner/repo>]"
mutates: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3:*), AskUserQuestion, Skill
---

Load the `board-setup` skill at `${CLAUDE_PLUGIN_ROOT}/skills/board-setup/SKILL.md` and run
CONFIRM → PROBE → CLASSIFY → PLACE/REFRESH → DRIFT → ELICIT → OFFER → WRITE → REPORT.

`$ARGUMENTS`, when present, is the forge target. Confirm it against the git remote rather than
trusting it; when absent, derive a candidate from the remote and **confirm it before any call**.
Issue `#12` exists in every repo, so an inferred target reads the wrong board successfully.

**Probe with the script, never from memory**, and invoke it by these exact spellings — targets first,
which makes no forge call, then the probe once the target is confirmed:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/probe-board.py --list-targets
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/probe-board.py --repo OWNER/REPO
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/probe-board.py --repo GROUP/PROJ --host gitlab.com
```

**Render both regions with the renderer, never by hand.** Determinism is what makes a re-run write
zero bytes, and a model cannot hold it — ordering and wording drift, every run diffs, and the diffs
stop being read:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/render-block.py --probe PROBE.json --stamp UTC_MINUTE
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/render-block.py --probe PROBE.json --stamp UTC_MINUTE \
    --declarations ANSWERS.json --declared-only
```

**Classify, place and diff with the second script, never by hand** — placement and line arithmetic
are where a silent one-line error destroys prose no probe can regenerate:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/region-place.py --file CLAUDE.md --classify
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/region-place.py --file CLAUDE.md --drift PROBE.json
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/region-place.py --file CLAUDE.md --place REGION.md --expect-sha SHA
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/region-place.py --file CLAUDE.md --retire LINE --expect-sha SHA
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/region-place.py --file CLAUDE.md --refresh REGION.md --expect-sha SHA
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/region-place.py --file CLAUDE.md --declare DECL.md --expect-sha SHA
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
already documents for `adversarial-review`. **This command runs exactly three programs, and only one
of them writes:**

- `probe-board.py` — **reads only.** The forge (`gh` / `glab`) and the git remotes. It creates no
  project, field, option, label or issue, and writes no file.
- `render-block.py` — **reads only.** A pure function of probe JSON plus a timestamp; it writes
  nothing and makes no call of any kind.
- `region-place.py` — **writes exactly one file**, the `CLAUDE.md` passed as `--file`. It writes under
  `--place`, `--refresh`, `--declare` and `--retire`, and **never** under `--classify` or `--drift`.
  Every write is guarded by `--expect-sha`; `--place` and `--refresh` additionally run a byte-identity
  check on the content outside both regions before anything reaches disk. `--declare` inserts a new
  region and `--retire` deletes one sanctioned line, so neither can satisfy that check by
  construction — each is guarded instead by refusing to touch any line inside either region.

**Only `probe-board.py` runs a subprocess at all**, through a single `run()` chokepoint: list-argv, no
`shell=True`, no interpolation, 60s timeout, non-zero exit becomes a refusal. `render-block.py` and
`region-place.py` make no call of any kind. Adding a mutating call to any of the three would widen this
command's reach without changing a line of frontmatter — **the three scripts are the boundary, and
reviewing them is how the boundary is kept.**

**The model also writes intermediates** — `PROBE.json`, `REGION.md`, `ANSWERS.json`, `DECL.md` — under
the same `Write` grant. They go to the session's scratch directory and **never** into the target repo,
which gains exactly one modified file. Stated here because an auditor checking the grant against this
paragraph would otherwise find writes it does not predict.

`Bash(python3:*)` also permits shell redirection: `python3 anything.py > /any/path` matches the same
literal prefix, so the grant can write any path with none of the three scripts involved. Smaller than
`python3 -c` in practice, but this paragraph's job is completeness.

**This paragraph is the compensating control for the over-wide `Bash(python3:*)` grant, and it is the
thing most likely to go quietly stale.** It has already been caught wrong once: it claimed one
read-only program after a second, writing one had been added. When the script set or its write
surface changes, this list changes in the same commit.

**All six slices.** The target may be absent, sectionless, hand-written, or already configured; the
forge may be GitHub or GitLab. A file already carrying a region is **refreshed**, writing zero bytes
when the board has not moved.

**Ask exactly three things and no more**: the forge target, the label-family question per family, and
the retire offer on a contradicting line. A label family is **never** inferred from the labels in use —
that would mint the very declaration `phil:groom-issues` rule 4 exists to read. A decline writes
nothing at all, not even a note that it was declined.

**Content outside both regions is byte-identical on every path**, including failure and refusal, with
two sanctioned exceptions and no others:

- the **retire offer** — one whole line, deleted, on an explicit answer;
- the **declared region** — inserted once on an answer, contributing one newline as its own
  terminator.

Silence is never an answer, and no existing line is ever rewritten or reflowed.

Half-probed values are now **written as `assumed`**, stating what is not knowable and why. Every line
inside the markers carries exactly one of `probed` / `assumed`; a value the forge would not return
carries `unread` and never enters the region at all.
