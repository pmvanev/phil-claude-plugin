---
name: claude-md
description: Review and revise a project's CLAUDE.md file against best practices — trim bloat, fix structure, sharpen instructions. Use on any CLAUDE.md to make it concise, specific, and well-organized.
argument-hint: <file-path | directory-path>
allowed-tools: Read, Edit, Glob, Grep
---

# CLAUDE.md Reviewer

You are revising a project's CLAUDE.md file using the best practices from the `claude-md` rule. Every edit tightens the file without losing essential instructions.

## Parse the Argument

| Pattern | Type | Example |
|---------|------|---------|
| Has a file extension or ends with `CLAUDE.md` | File path | `CLAUDE.md`, `./frontend/CLAUDE.md` |
| Ends with `/` or is a directory | Directory path | `./`, `src/` |
| Empty or omitted | Current directory | — |

For a directory, find all CLAUDE.md and CLAUDE.local.md files within it and process each.

---

## File Path

1. Read the target CLAUDE.md file.
2. Read the `claude-md` rule to load the full best-practice checklist.
3. Run the **audit** below.
4. Apply the **revision rules** below.
5. Report a summary: lines before, lines after, what changed.

---

## Directory Path

1. Glob for `**/CLAUDE.md` and `**/CLAUDE.local.md`.
2. Apply the **File Path** process to each file found.
3. Summarize changes per file.

---

## Audit

Score the file against each criterion. Flag violations before editing.

### Structure
- [ ] Under 200 lines (warn if 200-300; flag if over 300)
- [ ] Uses markdown headers to group sections
- [ ] Uses bullets, not paragraphs, for instructions
- [ ] Sections ordered by frequency of use (build/test first)

### Content
- [ ] Includes build and test commands
- [ ] Every instruction tells Claude something it cannot infer from code
- [ ] No file-by-file codebase descriptions
- [ ] No standard language conventions Claude already knows
- [ ] No long explanations or tutorials (links allowed)
- [ ] No stale instructions for removed features

### Writing
- [ ] Each bullet states one instruction
- [ ] Instructions use imperative mood ("Run X" not "You should run X")
- [ ] Specific over vague ("2-space indent" not "consistent formatting")
- [ ] Emphasis used sparingly (at most two IMPORTANT markers)
- [ ] No self-evident platitudes ("write clean code," "handle errors")

### Scoping
- [ ] Personal preferences live in CLAUDE.local.md, not CLAUDE.md
- [ ] Path-specific rules belong in `.claude/rules/` with frontmatter, not here
- [ ] Multi-step workflows belong in skills, not here
- [ ] Deterministic rules belong in hooks, not here

---

## Revision Rules

Apply these in order.

### 1. Delete What Claude Already Knows

Remove instructions that restate standard language conventions, framework defaults, or obvious practices. If Claude would do it without being told, the line wastes context.

### 2. Move Linter-Enforceable Rules to Hooks

Flag any instruction that a linter or formatter handles deterministically (indentation, trailing commas, import order, line length). Suggest enforcing these via hooks instead. Never send an LLM to do a linter's job.

### 3. Delete Stale Instructions

Remove references to features, files, tools, or patterns that no longer exist in the project. Grep the codebase to verify before deleting — if the referenced file or command no longer exists, cut the instruction.

### 4. Consolidate Redundancy

Merge bullets that say the same thing in different words. One clear statement beats two fuzzy ones.

### 5. Sharpen Vague Instructions

Replace vague guidance with specific, actionable instructions.

| Before | After |
|--------|-------|
| Format code properly | Use 2-space indentation and Prettier defaults |
| Write good tests | Run `npm test` before committing; assert behavior, not implementation |
| Follow best practices | (delete — too vague to act on) |

### 6. Impose Structure

Reorganize into standard sections in this order:

1. **Project context** — one or two lines: what is this, what stack
2. **Build & test** — shell commands for building, testing, linting
3. **Code style** — rules that differ from language defaults
4. **Architecture** — layer boundaries, key directories, dependency direction
5. **Workflow** — branch naming, commit conventions, PR process
6. **Gotchas** — non-obvious behaviors, required env vars, platform quirks

Delete empty sections. Add missing sections only if the project needs them.

### 7. Move Misplaced Content

- Path-specific rules → suggest moving to `.claude/rules/` with `paths` frontmatter
- Personal preferences → suggest moving to `CLAUDE.local.md`
- Multi-step workflows → suggest creating a skill
- Note these suggestions in the summary; do not move files automatically

### 8. Suggest @imports

If the file inlines content from other files (README excerpts, package.json scripts, API docs), suggest replacing with `@path/to/file` imports. Imports keep CLAUDE.md lean and let Claude expand them on demand.

### 9. Apply Writing Standards

Tighten each bullet using Elements of Style principles:
- Active voice
- Positive form
- Omit needless words
- Imperative mood
- One instruction per bullet

### 10. Trim to 200 Lines

If the file still exceeds 200 lines after all passes, identify the least-essential instructions and suggest moving them to rules files. Cut until the file fits.

---

## Safety

- **Preserve essential instructions.** Never delete a build command, test command, or architectural constraint without confirming it is stale.
- **Preserve team conventions.** Do not remove workflow rules (branch naming, PR process) even if they seem obvious — teams chose them deliberately.
- **Do not create files.** Suggest where to move content; let the user decide.
- **Do not invent instructions.** Only tighten, reorganize, or delete. Never add rules the project did not already have.
- **Flag uncertainty.** If unsure whether an instruction is stale, keep it and note the uncertainty in the summary.
