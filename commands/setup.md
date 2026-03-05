---
name: setup
description: Install Phil's development rules and CLAUDE.md into ~/.claude/. Copies rule files and CLAUDE.md, warns before overwriting.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Setup Phil's Development Standards

Install rules and CLAUDE.md from this plugin into `~/.claude/`.

## Steps

1. **Create directories** — Ensure `~/.claude/rules/` exists.

2. **Check for existing files** — Before copying each file, check if it already exists at the destination. If it does, warn the user and show a diff summary of what would change. Ask before overwriting.

3. **Copy rule files** — Copy every `.md` file from `${CLAUDE_PLUGIN_ROOT}/rules/` to `~/.claude/rules/`:
   - `architecture.md`
   - `coding.md`
   - `continuous-delivery.md`
   - `definitions.md`
   - `refactoring.md`
   - `testing.md`
   - `ui.md`
   - `writing.md`

4. **Copy CLAUDE.md** — Copy `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` to `~/.claude/CLAUDE.md`.

5. **Report results** — List each file with its status:
   - `[created]` — new file, did not exist before
   - `[updated]` — existing file was overwritten
   - `[skipped]` — user chose not to overwrite

## Implementation

Use Bash to run the copies. Use `mkdir -p` for directory creation. Use `diff` or file comparison to detect changes before overwriting. Use the Read tool to show the user what differs when files conflict.

Do NOT copy skills, hooks, or scripts — those are handled automatically by the plugin system.
