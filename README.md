# phil-plugin

Portable Claude Code plugin — development standards, skills, hooks, and setup command.

## Quickstart

### Option 1: Install from marketplace (no clone needed)

From inside Claude Code:

```
/plugin marketplace add pmvanev/claude-marketplace
/plugin install phil@pmvanev-plugins
/phil:setup
```

### Option 2: Install locally from a clone

```bash
git clone git@github.com:pmvanev/phil-claude-plugin.git
```

Then from inside Claude Code:

```
/plugin install --local /path/to/phil-claude-plugin
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
