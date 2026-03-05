# phil-plugin

Portable Claude Code plugin — development standards, skills, hooks, and setup command.

## Quickstart

Install the plugin locally from inside Claude Code:

```
/plugin install --local /path/to/phil-claude-plugin
```

Then copy rules and CLAUDE.md into `~/.claude/`:

```
/phil:setup
```

## What's included

**Auto-loaded by the plugin system:**
- `/phil:clean-comments` — tidy comments and docstrings
- `/phil:extract-method` — extract cohesive code blocks into named methods
- Stop hook — Windows toast notification + chime when Claude finishes

**Installed by `/phil:setup`:**
- 8 rule files (architecture, coding, continuous-delivery, definitions, refactoring, testing, ui, writing)
- `CLAUDE.md` with global development principles
