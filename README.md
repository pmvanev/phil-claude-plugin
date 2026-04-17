# phil-plugin

Portable Claude Code plugin — development standards, rules, skills, and hooks.

## Quickstart

### Option 1: Install from marketplace (no clone needed)

From inside Claude Code:

```
/plugin marketplace add pmvanev/claude-marketplace
/plugin install phil@pmvanev-plugins
```

### Option 2: Install locally from a clone

```bash
git clone git@github.com:pmvanev/phil-claude-plugin.git
```

Then from inside Claude Code:

```
/plugin install --local /path/to/phil-claude-plugin
```

## What's included

Everything loads automatically from the plugin directory — no setup step needed.

- **Rules** — architecture, claude-md, coding, continuous-delivery, definitions, refactoring, refactoring-catalog, testing, ui, writing
- **Skills** — `/phil:claude-md`, `/phil:clean-comments`, `/phil:create-plugin-feature`, `/phil:eos`, `/phil:extract-method`, `/phil:refactor`, `/phil:review-code`
- **Hooks** — Windows toast notification + chime when Claude finishes
- **CLAUDE.md** — global development principles
