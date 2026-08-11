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

- **Rules** — architecture, best-simple-system-for-now, claude-md, coding, continuous-delivery, cpp, definitions, llm-inference, modern-software-engineering, python, react, refactoring, refactoring-catalog, technical-communication, testing, typescript, ui, ux, writing
- **Skills** — `/phil:adversarial-review`, `/phil:ai-eos`, `/phil:claude-md`, `/phil:clean-comments`, `/phil:edd`, `/phil:eos`, `/phil:extract-method`, `/phil:red-team-prose`, `/phil:redesign-tests`, `/phil:refactor`, `/phil:refactor-loop`, `/phil:refactor-tests`, `/phil:review-code`, `/phil:nwave-slice-status`, `/phil:spirit-walk`, `/phil:ux-review`, `/phil:work`
- **Knowledge skills** (auto-load on relevance, no command) — `issue-board` (driving GitLab/GitHub issue boards with `glab` and `gh`), `nwave-issue-board` (mapping an nWave feature, slice, and step onto that board)
- **Hooks** — Windows toast notification + chime when Claude finishes
- **CLAUDE.md** — global development principles
