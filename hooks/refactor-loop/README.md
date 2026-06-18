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
| `block-test-file-write.py` | `PreToolUse` (Edit, Write) | G2 | **wire it** (defense-in-depth) | **wire it** (primary) |
| `anti-premature-exit.py` | `Stop` | G10 | obviated (JS owns the loop) | wire it |
| `reinject-pinned-constraints.py` | `UserPromptSubmit` | G7 | obviated (JS holds state) | wire it |

**Under the Workflow substrate, G2 is the only hook to wire — and it is defense-in-depth, not
the primary guard.** The applier agent applies diffs via `git apply` (Bash), which bypasses the
`Edit|Write` PreToolUse matcher; so the *primary* test-file lockbox under the Workflow is the
**cage's in-JS diff scan** (`workflows/refactor-loop.js` refuses any proposed diff that touches a
test path, before applying). The G2 hook still catches any stray `Edit`/`Write` to a test file.

Wire G10/G7 only if you run the prose `skills/refactor-loop/SKILL.md` fallback (`--interactive`),
where the model executes the loop and those weaknesses (premature exit, context compaction)
return.

## Why this needs human follow-up

The plugin already ships a `Stop` hook in `hooks/hooks.json` (the toast/chime notifier). The
G10 hook is **also** a `Stop` hook (interactive path only). If you wire it, they must
**coexist** — add a second entry to the `Stop` array, do not replace it. Because clobbering
`hooks/hooks.json` (or a user's `settings.json`) is easy to get wrong, wiring is a deliberate
human step. Recommended: run the **`update-config`** skill with the merge below, then verify
with `/hooks`.

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

Add these only when running the prose fallback. The G10 entry joins the existing `Stop` array
as a **second** entry (the notifier keeps its trailing `&`; G10 must NOT have one — its stdout
JSON decision must be read synchronously):

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/refactor-loop/reinject-pinned-constraints.py\"" } ] }
    ],
    "Stop": [
      { "hooks": [ { "type": "command", "command": "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File ${CLAUDE_PLUGIN_ROOT}/scripts/notify-stop.ps1 &" } ] },
      { "hooks": [ { "type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/refactor-loop/anti-premature-exit.py\"" } ] }
    ]
  }
}
```

## Interpreter note

The command uses `python3` (works on macOS/Linux and on this repo's Windows host, Python
3.14). If `python3` is not on PATH on a given Windows machine, use `python` or `py -3` in the
command string instead. (The existing `scripts/notify-stop.ps1` stays PowerShell — it is a
Windows toast/chime notifier, genuinely OS-specific and unrelated to the refactor-loop guards.)

## Degradation without the hooks

Under the Workflow path, the in-JS diff scan still enforces the test-file lockbox even with no
hook wired; the G2 hook only adds defense-in-depth for stray Edit/Write. Under the interactive
skill path, G2/G7/G10 fall back to the in-prose checks in `skills/refactor-loop/SKILL.md`
(advisory, not platform-sound) until wired.
