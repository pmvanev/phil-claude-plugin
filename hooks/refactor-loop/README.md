# Refactor-Loop Hooks — wiring (human follow-up required)

Python hooks (Python 3.x) for the `/phil:refactor-loop` cage. They read the hook payload as
JSON on stdin and emit a JSON decision on stdout per the Claude Code hook protocol. All three
are **gated on the refactor-loop sentinel** (`.refactor-loop-ledger.md` in the project root
with `active-run: true`), so they are no-ops in any session that is not an active refactor-loop
run — they never trap unrelated work.

## Which hooks apply to which substrate (ADR-008)

The production orchestrator is the **Workflow tool** (`workflows/refactor-loop.js`). The
Workflow's JS owns the loop, so two of the three hooks are obviated under it:

| Script | Event | Guard | Workflow path | Interactive skill path |
|---|---|---|---|---|
| `agent-allowlist.py` | `PreToolUse` (Bash, Read, Write, Edit, NotebookEdit) | allow-list | **ships wired** (the boundary for each narrowed agent) | silent (the main session carries no agent type) |
| `block-test-file-write.py` | `PreToolUse` (Edit, Write) | G2 | **ships wired** (defense-in-depth) | **ships wired** (defense-in-depth; the skill's diff scan is primary) |
| `anti-premature-exit.py` | `Stop` | G10 | obviated (JS owns the loop) | wire it |
| `reinject-pinned-constraints.py` | `UserPromptSubmit` | G7 | obviated (JS holds state) | wire it |

**Under the Workflow substrate, the allow-list and G2 are the hooks that apply, and both ship wired
in `hooks/hooks.json`. G2 is defense-in-depth, not the primary guard.** The applier agent applies diffs via `git apply` (Bash), which bypasses the
`Edit|Write` PreToolUse matcher; so the *primary* test-file lockbox under the Workflow is the
**cage's in-JS diff scan** (`workflows/refactor-loop.js` refuses any proposed diff that touches a
test path, before applying). The G2 hook still catches any stray `Edit`/`Write` to a test file.

Wire G10/G7 only if you run the prose `skills/refactor-loop/SKILL.md` fallback (`--interactive`),
where the model executes the loop and those weaknesses (premature exit, context compaction)
return.

**Two guards distrust the ledger in opposite directions.** Once the ledger exists, G2 denies any
write it cannot check. G7 speaks only when git answers that the ledger is untracked: the loop never
commits its ledger, so a tracked one, or one git cannot vouch for, came from whoever can commit to
the repo or pack the archive, and re-injecting it would let them write every prompt's context. G7
is therefore silent outside a git repository. A tarball of a working copy carries its own `.git`,
so G7 also re-injects only header lines that match their key's grammar — `pinned: [slug, …]`,
`iter: N / max M`, `baseline: green|red @ <sha>`, `theta`, `status` — and never the free-text
`runner:`. No free text reaches the prompt, whoever wrote the ledger.

**The allow-list is where a narrowed agent's grant is enforced.** An agent file's `tools:` line picks
whole tools, never commands or paths: a probe agent granted `Bash(echo:*)` wrote files through `touch`,
a redirect, a chain and a substitution in bypass mode (2026-10-20). Claude Code puts the calling
subagent's `agent_type` in each `PreToolUse` payload, and a deny holds in bypass mode, so the hook
allows each narrowed role only its own paths and commands. It matches the type's last segment, so
`phil:refactor-ledger-writer` and a copied `refactor-ledger-writer` are both bounded. The ledger writer
may `Read` and `Write` only `.refactor-loop-ledger.md` at a repository root, never through a symlink.
The applier may `Read` and `Write` only `.refactor-loop-patch.diff` at a repository root, and run only
`git -C <repo> apply --recount [--check] <repo>/.refactor-loop-patch.diff`; the reverter holds `Bash`
alone and may run only the same command with `-R`. Shell syntax is refused before a command is split
into words, and the words must match exactly. Both act only in a repository whose ledger says `active-run: true`:
only the ledger writer can write that file, and a workflow agent's `cwd` is the session's, not the
target's. Before either command runs, the hook applies the patch to a scratch index made
from HEAD and lists every changed path, a rename as both sides. It refuses a test path, a loop file
(the ledger, the patch file, the commit message file), a file later sessions load as instructions
(`.claude`, `CLAUDE.md`, `CLAUDE.local.md`, `AGENTS.md`, `.mcp.json`), a symlink or submodule entry, and a
path starting with `:`, which `git add` would read as pathspec magic. The instruction list is not
complete — a file a `CLAUDE.md` imports, or a script a project's hook runs, also persists past the run
— and the test suite already runs the patch's code. It asks git because a header regex let through an unprefixed
rename, `rename old`/`rename new`, and octal-quoted names, and `--numstat` named only a rename's
destination; and because the cage scanned the proposer's diff, not the bytes the applier wrote. The
committer may `Read` and `Write` only `.refactor-loop-commit-msg`, stage exactly the paths that list holds, all of them
(`git -C <repo> --literal-pathspecs add -- <paths>`; a validator staged the whole tree through a file
named `:^nothing` before the flag), and commit only with `git -C <repo> commit -F
<repo>/.refactor-loop-commit-msg` — no `-m`, `--amend`, `--no-verify` or `push`. The repository's
own commit hooks still run its code. **Accepted residual:** the applier holds `Write`, so in parallel
tool calls it could replace the patch between the hook's check and git's apply. The candidate fix is a
hook that rewrites the command to apply a copy it checked, once a rewrite is shown not to auto-approve
the call. The hook is silent for the main session and every other agent type,
except for the ledger rule below.
A session started with `--agent` carries that agent's type in its main session too, so the ledger rule
applies to it.

**G2's switch guards the loop's own agents, not every agent.** The loop writes its ledger through the
ledger writer, the only subagent type the allow-list lets `Write` or `Edit` the ledger, and the cage
composes every byte it writes. Both diff scans refuse a proposed diff that touches the ledger. An agent
that still holds an unchecked shell can switch G2 off through `Bash`; that route closes when the gate
runner is narrowed (issue 48).

## Why this needs human follow-up

`hooks/hooks.json` ships **no `Stop` hook** — the toast/chime notifier that used to live there was
removed in 0.60.0. The G10 hook is a `Stop` hook (interactive path only), so wiring it *creates* the
`Stop` array rather than joining one. If a later hook adds a `Stop` entry, they must **coexist**: add
a second entry, do not replace. Because clobbering `hooks/hooks.json` (or a user's `settings.json`) is
easy to get wrong, wiring is a deliberate human step. Recommended: run the **`update-config`** skill
with the merge below, then verify with `/hooks`.

## The merge for the Workflow path (G2 only)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/refactor-loop/block-test-file-write.py\"" }
        ]
      }
    ]
  }
}
```

## Additional entries for the interactive skill path (G10 + G7)

Add these only when running the prose fallback. The G10 entry adds a `Stop` array, and must NOT
carry a trailing `&` — its stdout JSON decision must be read synchronously:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/refactor-loop/reinject-pinned-constraints.py\"" } ] }
    ],
    "Stop": [
      { "hooks": [ { "type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/refactor-loop/anti-premature-exit.py\"" } ] }
    ]
  }
}
```

## Interpreter note

The command uses `python3` (works on macOS/Linux and on this repo's Windows host, Python
3.14). If `python3` is not on PATH on a given Windows machine, use `python` or `py -3` in the
command string instead.

## Degradation without the hooks

Under the Workflow path, the in-JS diff scan still enforces the test-file lockbox even with no
hook wired; the G2 hook only adds defense-in-depth for stray Edit/Write. Under the interactive
skill path, G2/G7/G10 fall back to the in-prose checks in `skills/refactor-loop/SKILL.md`
(advisory, not platform-sound) until wired.
