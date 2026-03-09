---
paths:
  - "**/CLAUDE.md"
  - "**/CLAUDE.local.md"
  - "**/.claude/CLAUDE.md"
---

# CLAUDE.md Guide

## Purpose

CLAUDE.md gives Claude Code persistent, project-level instructions. It loads at every session start. Every line competes for context with actual work — make each one count.

---

## Structure

Keep the file under 200 lines. Organize with markdown headers and bullets. Group by topic, not chronology.

### Recommended Sections

| Section | Content |
|---------|---------|
| **Project context** | One or two lines: what is this, what stack. Orients Claude immediately |
| **Build & test** | Commands Claude cannot guess: `npm test`, `make build`, `cargo clippy` |
| **Code style** | Rules that differ from language defaults: indentation, import style, naming |
| **Architecture** | Layer boundaries, key directories, dependency direction |
| **Workflow** | Branch naming, commit conventions, PR process |
| **Gotchas** | Non-obvious behaviors, required environment variables, platform quirks |

Order sections by frequency of use. Put build and test commands first — Claude reaches for them most often.

---

## What Belongs Here

Write instructions Claude cannot infer from the code itself:

- Shell commands for building, testing, linting, deploying
- Style rules that break from language convention
- Architectural constraints (e.g., "business logic never imports infrastructure")
- Repository etiquette (branch prefixes, PR templates)
- Environment requirements (required env vars, minimum versions)

## What Does Not Belong

- Standard language conventions Claude already knows
- Code style rules a linter or formatter enforces — never send an LLM to do a linter's job
- File-by-file descriptions of the codebase
- Long explanations or tutorials (link to docs instead)
- Information that changes frequently
- Self-evident practices ("write clean code," "handle errors")
- Detailed API documentation

## @imports

Reference external files with `@path/to/file` instead of inlining their content. Claude expands imports at load time.

```markdown
See @README.md for project overview and @package.json for available commands.
```

Imports resolve relative to the file that contains them. Maximum depth: five hops.

---

## Writing Style

1. **Be specific.** "Use 2-space indentation" beats "format code properly."
2. **Be imperative.** "Run `npm test` before committing" — not "you should consider running tests."
3. **One instruction per bullet.** Compound bullets blur priority.
4. **Skip justification.** State the rule; omit the rationale unless the rule seems arbitrary.
5. **Reserve emphasis.** Mark one or two items IMPORTANT. If everything screams, nothing stands out.

---

## Scoping

Use the right file for the right audience:

| Scope | File | Audience |
|-------|------|----------|
| **Project** | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Whole team (commit to git) |
| **Personal per-project** | `./CLAUDE.local.md` | You alone (gitignore this) |
| **Personal global** | `~/.claude/CLAUDE.md` | You alone, all projects |
| **Organization** | Managed policy path | All users on machine |

More specific files override broader ones. Subdirectory CLAUDE.md files load on demand when Claude reads files there — use them in monorepos to scope instructions by package.

---

## When to Split

Move instructions out of CLAUDE.md when:

- The file exceeds 200 lines — extract topic files to `.claude/rules/` with `paths` frontmatter
- A rule applies only to certain file types — use a path-scoped rule
- A rule defines a multi-step workflow — create a skill in `.claude/skills/`
- A rule must be enforced deterministically — implement it as a hook

---

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| **Kitchen sink** — instructions for every scenario | Prune to essentials; split the rest into rules |
| **Over-specification** — restating what Claude infers from code | Delete rules Claude would follow without them |
| **Conflicting instructions** — two rules that contradict | Audit periodically; resolve in favor of the more specific scope |
| **Emphasis overload** — every line marked IMPORTANT | Reserve emphasis for one or two critical rules |
| **Stale instructions** — rules for removed features or old patterns | Review after major refactors; delete what no longer applies |
| **Linter duplication** — enforcing style rules Claude cannot guarantee | Use formatters and linters via hooks; reserve CLAUDE.md for judgment calls |
| **Uncurated /init output** — accepting auto-generated content as-is | Run `/init`, then prune aggressively |
| **Progressive disclosure failure** — documenting everything up front | Teach Claude where to find information, not all the information |

---

## Maintenance

- **Audit quarterly.** Read every line. Delete what Claude would do without being told.
- **Test compliance.** Ask Claude to search for violations of a rule. Many violations signal a rule that needs a hook, not a CLAUDE.md line.
- **Review after refactors.** Architectural changes invalidate architectural instructions.
- **Prefer `/init` as a starting point.** Run `claude /init` on a new project, then prune the output.
