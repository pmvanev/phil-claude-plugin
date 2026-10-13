---
description: "Write a repo's board constants into its CLAUDE.md before they are learned by contact — probing GitHub or GitLab for the project and Status field ids, every option id, the enabled workflows, the tier and the docs root, into a delimited region where every line names the query that produced it and carries `probed` or `assumed`. Asks only what no forge records, coexists with prose it cannot regenerate, and re-runs writing zero bytes when nothing moved. Reads the forge; never writes to it."
argument-hint: "[<owner/repo>]"
mutates: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3:*), AskUserQuestion, Skill
---

Load the `board-setup` skill at `${CLAUDE_PLUGIN_ROOT}/skills/board-setup/SKILL.md` and run
CONFIRM → PROBE → CLASSIFY → RENDER → PLACE/REFRESH → DRIFT → ELICIT → OFFER → REPORT.

## Target

`$ARGUMENTS`, when present, names the forge target; confirm it against the git remote. When absent,
derive a candidate from the remote and **confirm it before any call**. Issue `#12` exists in every repo,
so an inferred target reads the wrong board successfully.

Confirm on every `--list-targets` status: `ok` — one candidate, confirm it anyway; `ambiguous` — more
than one distinct repo across the remotes — is a **question** presenting the candidates, never a pick,
and never prefers `origin`; `none` — ask for the target.

## Scripts

Every value inside the markers comes out of the probe's JSON: a value typed from recall looks exactly
like a probed one in the finished file. A relative script path would resolve against the target repo,
where the script does not exist. `SCRATCH_DIR` below is the session's scratch directory, spelled as an
absolute path; a bare intermediate name lands in the target repo.

**Probe with `probe-board.py`**, invoked by these exact spellings — targets first, which makes no forge
call, then the probe once the target is confirmed:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/probe-board.py --list-targets
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/probe-board.py --repo OWNER/REPO
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/probe-board.py --repo GROUP/PROJ --host gitlab.com
```

**Render both regions with `render-block.py`.** A re-run writes zero bytes only because rendering is
deterministic; by hand, order and wording drift, every run diffs, and the diffs stop being read:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/render-block.py --probe SCRATCH_DIR/PROBE.json --stamp UTC_MINUTE
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/render-block.py --probe SCRATCH_DIR/PROBE.json --stamp UTC_MINUTE \
    --declarations SCRATCH_DIR/ANSWERS.json --declared-only
```

**Classify, place and diff with `region-place.py`.** By hand, placement and line arithmetic are where a
silent one-line error destroys prose no probe can regenerate:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/region-place.py --file CLAUDE.md --classify
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/region-place.py --file CLAUDE.md --drift SCRATCH_DIR/PROBE.json
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/region-place.py --file CLAUDE.md --place SCRATCH_DIR/REGION.md \
    --expect-sha SHA
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/region-place.py --file CLAUDE.md --retire LINE --expect-sha SHA
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/region-place.py --file CLAUDE.md --refresh SCRATCH_DIR/REGION.md \
    --expect-sha SHA
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/region-place.py --file CLAUDE.md --declare SCRATCH_DIR/DECL.md \
    --expect-sha SHA
```

Pass each writing call the file's current `sha256`: the one `--classify` returned, or the previous
write's `sha256_after`; after a write that returns none, such as `--retire`, run `--classify` again. A
file that moved between read and write is refused, not overwritten. On `file-absent` the `sha256` is
`null`, the one case where a writing call may omit `--expect-sha`.

## Reach

Run exactly these three programs; only `region-place.py` writes:

- `probe-board.py` reads the forge (`gh` / `glab`) and the git remotes. It creates no project, field,
  option, label or issue, and writes no file.
- `render-block.py` is a pure function of probe JSON and a timestamp. It makes no call and writes
  nothing.
- `region-place.py` writes one file, the `CLAUDE.md` passed as `--file`: under `--place`, `--refresh`,
  `--declare` and `--retire`, never under `--classify` or `--drift`.

The target is one file, the working tree's `CLAUDE.md`, never a sibling checkout's. The scripts make
every write to it, including creating an absent file; the grant exists for their output path, not as a
hand-placement fallback when a call refuses. The intermediates — `PROBE.json`, `REGION.md`,
`ANSWERS.json`, `DECL.md` — go to the session's scratch directory under the same `Write` grant, never
into the target repo, which gains exactly one modified file.

The grant holds no `gh`, `glab` or `git`; the scripts reach them through list-argv `subprocess`. It does
admit `python3 -c` and shell redirection to any path, and `Write` and `Edit` are unscoped: these rules,
not the frontmatter, hold the command to one file.

## Run

- Handle every target: absent, sectionless, hand-written or already configured, on GitHub or GitLab.
  **Refresh** a file that already carries a region; the refresh writes zero bytes when the board has not
  moved.
- **Ask exactly three things**: the forge target, the label-family question per family, and the retire
  offer on a contradicting line.
- Settle each label family by its question, never from the labels in use — that would mint the very
  declaration `phil:groom-issues` rule 4 exists to read. A decline writes nothing at all, not even a note
  that it was declined.
- Keep content outside both regions byte-identical on every path, including failure and refusal. Two
  exceptions, and no others: the **retire offer** deletes one whole line on an explicit answer, and the
  **declared region** is inserted once on an answer, contributing one newline as its own terminator.
  Silence is never an answer. Rewrite or reflow no existing line.
- Every line inside the markers carries exactly one of `probed` / `assumed`. A half-probed value is
  written as `assumed`, stating what is not knowable and why. A value the forge would not return carries
  `unread` and never enters the region.
- No line in the probed region is composed at run time: `render-block.py` emits every line, an `assumed`
  line's *not knowable … why* clause included, from the probe JSON and the scripts' own strings. Leave
  rendered lines as rendered. `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` governs the rationale strings at
  build time, in `probe-board.py`, for whoever edits them. See the skill's table of provenance labels.

When the script set or its write surface changes, update **Reach** in the same commit. It went stale
once: it listed one read-only program after a second, writing one had been added.
