# Refactor-Loop Hooks — wiring (human follow-up required)

Three hooks give the `/phil:refactor-loop` cage defence in depth. All three are **gated on
the refactor-loop sentinel** (`.refactor-loop-ledger.md` in the project root with
`active-run: true`), so they are no-ops in any session that is not an active refactor-loop
run — they never trap unrelated work.

| Script | Event | Guard | Purpose |
|---|---|---|---|
| `block-test-file-write.ps1` | `PreToolUse` (Edit, Write) | G2 | Deny writes to test paths during an active run (the proposer must never edit the oracle). |
| `anti-premature-exit.ps1` | `Stop` | G10 | Block an early turn-end until the loop's DONE/HALT predicate is satisfied. |
| `reinject-pinned-constraints.ps1` | `UserPromptSubmit` | G7 | Re-assert the durable pinned constraints from the ledger header so compaction cannot evict them. |

## Why this needs human follow-up

The plugin already ships a `Stop` hook in `hooks/hooks.json` (the toast/chime notifier). The
G10 anti-premature-exit hook is **also** a `Stop` hook. They must **coexist** — do not
replace the existing `Stop` array, add a second entry to it. Because clobbering
`hooks/hooks.json` (or a user's `settings.json`) is easy to get wrong, wiring is left as a
deliberate human step rather than an automatic edit.

Recommended: run the **`update-config`** skill and give it the merge below, or hand-merge it
into `hooks/hooks.json`. Verify with `/hooks` afterward.

## The merge (add to `hooks/hooks.json`, do not overwrite)

The existing file has a `Stop` array with the notifier. After merging, `Stop` holds **both**
entries:

```json
{
  "description": "Notification on Stop — Windows toast and chime; refactor-loop guards (G2/G7/G10).",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File ${CLAUDE_PLUGIN_ROOT}/hooks/refactor-loop/block-test-file-write.ps1"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File ${CLAUDE_PLUGIN_ROOT}/hooks/refactor-loop/reinject-pinned-constraints.ps1"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File ${CLAUDE_PLUGIN_ROOT}/scripts/notify-stop.ps1 &"
          }
        ]
      },
      {
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File ${CLAUDE_PLUGIN_ROOT}/hooks/refactor-loop/anti-premature-exit.ps1"
          }
        ]
      }
    ]
  }
}
```

> The existing notifier entry keeps its trailing `&` (fire-and-forget). The G10 entry must
> **not** have a trailing `&` — its JSON decision on stdout is what blocks the stop, so it
> must run synchronously and its output must be read.

## Degradation without the hooks

If the hooks are not wired, the loop still runs. G2, G7, and G10 fall back to the in-prose
checks in `skills/refactor-loop/SKILL.md` — the model is instructed to honor them, but they
are no longer enforced at the platform boundary. Wire the hooks to make those boundaries
sound rather than advisory.

## Platform note

These scripts are PowerShell, matching the plugin's existing `scripts/notify-stop.ps1` and
its `powershell.exe`-based hook command. They read the hook payload as JSON on stdin and emit
a JSON decision on stdout per the Claude Code hook protocol. On a non-Windows host, port them
to a shell/Node equivalent that reads the same stdin JSON and emits the same decision shapes.
