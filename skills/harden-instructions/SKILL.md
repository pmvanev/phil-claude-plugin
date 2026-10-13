---
name: harden-instructions
description: Skill bundle for phil:harden-instructions command — revise any file a model reads as instructions (CLAUDE.md, AGENTS.md, a skill, an agent, a command, a rule), in this repo or elsewhere, so each rule lives where the model cannot lose it and what stays in prose is phrased to be recalled
---

# Harden Instructions

Revise an instruction file so each rule sits on the highest tier it can reach — enforced, derived, named or
stated — and whatever stays in prose is phrased for the model to recall rather than reinvent.

**Read `${CLAUDE_PLUGIN_ROOT}/rules/agent-instructions.md` first** — it is the standard every file gets, and
nothing loads it for you. A file's **profile** (below) adds a layout standard on top.

Every edit tightens the file and keeps every rule that still binds.

## Parse the Argument

`$ARGUMENTS` holds one or more paths, separated by spaces. A quoted path may contain spaces.

| Pattern | Type | Example |
|---------|------|---------|
| Names a file, whatever its name | File path | `CLAUDE.md`, `skills/foo/SKILL.md`, `~/other-repo/AGENTS.md` |
| Ends with `/` or is a directory | Directory path | `./`, `skills/`, `~/other-repo/` |
| Empty or omitted | Current directory | — |

Expand a leading `~` to the home directory. A path outside the current repository is valid; process it the same way. Report a path that does not exist and skip it.

## Pick the Profile

| Profile | The file is | Layout standard | Budget |
|---|---|---|---|
| **Project memory** | `CLAUDE.md`, `CLAUDE.local.md`, `.claude/CLAUDE.md`, `AGENTS.md` | `${CLAUDE_PLUGIN_ROOT}/rules/claude-md.md` | 200 lines, generated regions included |
| **Skill** | `SKILL.md` | `plugin-dev:skill-development`: imperative voice, detail in `references/` | Body 1,500–2,000 words; flag over 3,000 |
| **Agent** | a `.md` under an `agents/` directory | `plugin-dev:agent-development`: second person, addressing the agent | Body 500–3,000 characters; flag over 10,000 |
| **Command** | a `.md` under a `commands/` directory | `plugin-dev:command-development` | None |
| **Reference** | a `.md` under a `rules/` directory, a skill's `references/*.md`, any other file given by path | None | None |

**Shipped and local files.** Project memory runs in the repository it sits in. A skill, agent, command or plugin rule ships: it runs in a user's repository, not the one it was written in. Revision rules 2, 3 and the recovery pointer treat the two differently, as each says.

Read the profile's layout standard alongside `agent-instructions.md`. For a plugin-dev standard, Glob `~/.claude/plugins/cache/*/plugin-dev/*/skills/<name>/SKILL.md` and Read the file — never load it through the Skill tool, because `command-development` carries an inline shell example the Skill tool executes and fails on. When plugin-dev is not installed, say so in the report and apply `agent-instructions.md` alone.

**An `AGENTS.md` is read by agents other than Claude Code.** Skip the items only Claude Code honours: `CLAUDE.local.md`, `.claude/rules/`, Claude Code hooks and `@imports`.

## Find the Target's Repository

Every search and every git read runs against **the target's repository**, never the working directory:

```
git -C <target's directory> rev-parse --show-toplevel
```

Call the result the **root**. Search the root with Grep and Glob when judging a rule; pass `-C <root>` to every git read, with the target's path relative to the root.

Run only `rev-parse`, `status`, `log` and `check-ignore`. The grant admits any `git -C` call; this skill reads and never writes through git.

With no root — `~/.claude/CLAUDE.md`, an unversioned directory — skip revision rules 2 and 3 and keep every rule they would have judged, flagged in the report.

---

## File Path

1. Read the target file. Resolve a symlink and process the file it points to once.
2. Pick the profile and read its standards.
3. Find the root.
4. Set aside the **frozen parts**: frontmatter and generated regions (see Safety).
5. Check whether history can be recovered (see **Recoverability**).
6. Run the **audit**.
7. Apply the **revision rules**.
8. **Report**.

## Directory Path

1. Glob the given directory — not the root — for `**/CLAUDE.md`, `**/CLAUDE.local.md`, `**/AGENTS.md`, `**/SKILL.md`, `**/skills/*/references/*.md`, and `**/*.md` under any `agents/`, `commands/` or `rules/` directory that sits at the root, in `.claude/`, or beside a `.claude-plugin/` directory. A `docs/agents/` folder is not an agents directory.
2. Drop every match under `self-test/`, `node_modules/`, `vendor/` or `.git/`. Self-test inputs are flawed on purpose; a run that "fixes" them destroys the test. Drop any other match that `git -C <root> check-ignore -q <rel>` reports ignored, except `CLAUDE.local.md`, which is ignored by design.
3. With no matches left, report that and stop.
4. With only project-memory matches, apply the **File Path** process to each and report per file.
5. Otherwise list every match by profile, with its line and word counts, edit nothing and stop. A directory can hold dozens of skills and rules; the user reruns with the paths to process.

---

## Recoverability

Run, with `<rel>` the target's path relative to the root:

```
git -C <root> status --porcelain --ignored -- <rel>
git -C <root> log -1 --format=%h -- <rel>
```

- **Empty status and a hash** → the pre-revision text sits at that commit. History may be cut. Name `git show <hash>:<rel>` in the report. For project memory only, also leave it as the file's last line, outside every frozen part — `Rationale and history cut <date>: git show <hash>:<rel>` — replacing any earlier line of that form. This pointer is the one line the skill may add. A shipped file gets no pointer: its body is prompt text, and the hash names a repository its users do not have.
- **Anything else** — modified, untracked, ignored, no root, or an error → cut no history. Compress each wound to one line and keep the rest, flagged in the report as recoverable nowhere.

---

## Audit

Score the file against each criterion. Flag violations before editing.

### Placement — every profile
- [ ] A rule a tested check enforces takes one line naming the check
- [ ] A mechanically checkable rule with no check is flagged for one
- [ ] The model learns its position from disk or forge state, never a remembered step number
- [ ] Each non-obvious rule leads with its reflex and carries at most one line of wound
- [ ] Prohibitions name their alternative, or become reflexes
- [ ] A described protocol is named instead (Makefile, circuit breaker, `Key: Value`, EBNF)
- [ ] No invented tags or sigils
- [ ] No numbered workflow with "go back to step N" routing
- [ ] Someone other than the maker verifies each gate

### Writing — every profile
- [ ] Each bullet states one instruction
- [ ] Imperative mood ("Run X", not "You should run X") — an agent's body addresses the agent in the second person instead
- [ ] Specific over vague ("2-space indent", not "consistent formatting")
- [ ] No platitudes ("write clean code")
- [ ] No stale instructions for removed files, commands or features

### Layout — per profile
- **Project memory:** at most two IMPORTANT markers, and the Structure, Content and Scoping items in `rules/claude-md.md` — one or two lines of project context, then build and test; build and test commands present; nothing Claude infers from code; personal preferences in `CLAUDE.local.md`; path-specific rules in `.claude/rules/`; workflows in skills; deterministic rules in hooks.
- **Skill:** body within budget; detail that is reference material, not procedure, named for `references/`; every bundled file the body names exists.
- **Agent, Command:** the body is instructions for the model, not documentation for a human.
- **Reference:** no layout items.

---

## Revision Rules

Apply these in order. Rules 1 and 9 apply to project memory only; the rest apply to every profile.

### 1. Delete What Claude Already Knows

Project memory only. Remove standard conventions, framework defaults and obvious practices.

### 2. Delete Stale Instructions

Grep the root for every file, command and tool a rule names. Cut the rule when its subject no longer exists.

In a shipped file, judge only names inside its own bundle: `${CLAUDE_PLUGIN_ROOT}` paths, the skill's own `references/`, `scripts/` and `assets/`, and the plugin's other skills, agents and commands. A name in the user's repository — `CHANGELOG.md`, `src/`, `npm test` — refers to a repository that does not exist yet; keep it.

### 3. Collapse Enforced Rules

For each rule, search the root's `scripts/`, `hooks/`, `.claude/settings.json`, CI config and `tests/` for a check that enforces it. For an `AGENTS.md`, count only checks every agent meets — CI, tests, git hooks — never a Claude Code hook.

- **A check exists and a test exercises it** — a test that runs the check on the input it must refuse. The check is proven. Collapse the rule to one line: the reflex, then the check's path. Delete the explanation of how the check works; the check's own header owns it.
- **A check exists and no test exercises it.** The check is unproven. Keep the rule's prose, and name the check and the missing test in the report.
- **The rule is mechanically checkable and no check exists.** Keep the rule, and name the missing check in the report.

Write no hook, script or test. Collapsing keeps the rule; deleting it is never this step's outcome.

In a shipped file, a check enforces a rule only if it runs where the instruction runs — a hook the same plugin ships. A development-time test or script in the authoring repository never reaches the user's session; keep the prose, and name the check in the report as authoring-time only.

### 4. Rewrite Rule Anatomy

Give each surviving non-obvious rule its reflex first, as one imperative line. Follow it with the trap in one clause and the wound in one line when the file already holds them. Cut the remaining history if **Recoverability** allows; otherwise keep it beneath the rule and flag it.

Add no wound the file did not hold. Keep a rule that has none.

### 5. State Reflexes

Rewrite each "never X" or "do not X" as the invariant that must hold. Where a prohibition must stay, name the alternative in the same sentence.

### 6. Name the Protocol

Replace prose that describes a known protocol with that protocol's name and the exact parameters from the prose. Leave the rule's meaning unchanged: "retry twice, then ask" becomes `circuit breaker, k = 2`, never `k = 3`. Replace an invented tag or sigil with plain words or a known formalism.

### 7. Consolidate Redundancy

Merge rules that say the same thing.

### 8. Sharpen Vague Instructions

| Before | After |
|--------|-------|
| Format code properly | Use 2-space indentation and Prettier defaults |
| Write good tests | Run `npm test` before committing |
| Follow best practices | (delete — too vague to act on) |

In project memory, keep at most two IMPORTANT markers: the two rules whose breach costs most.

### 9. Impose Structure

Project memory only. Order sections: one or two lines of project context, then build and test, code style, architecture, workflow, gotchas. Keep sections the project needs that this list lacks. Delete empty ones. Turn instruction paragraphs into bullets.

A skill, agent, command or reference keeps its own section order.

### 10. Flag Misplaced Content

Name in the report any content that belongs elsewhere, and where: in project memory, a path-specific rule, personal preference or multi-step workflow; in a skill, reference material bound for `references/`; anywhere, a numbered checklist that would serve better as targets. Move nothing.

### 11. Apply Writing Standards

Tighten each sentence per `${CLAUDE_PLUGIN_ROOT}/rules/writing.md`: active voice, positive form, no needless words.

### 12. Fit the Budget

Project memory over 200 lines, a skill body over 2,000 words, or an agent body over 3,000 characters: name the least-essential content and where each part could move. Report the profile's flag threshold when the file crosses it. Project memory counts its generated regions toward the 200 lines; a skill or agent counts its body only, never its frontmatter. Frozen parts are never cut.

---

## Report

- The profile, and the standards read.
- Lines and words, before and after.
- The audit, with each failed item.
- Each rule cut, and why: stale or inferable.
- Each rule collapsed to one line, with the proven check that enforces it.
- Each check found but unproven, and each check worth writing.
- Each rule rewritten, one line each.
- History cut, with its recovery command — or history kept because it is recoverable nowhere.
- Content to move, and where.
- Frozen parts found and left unchanged.

---

## Safety

- **Leave frontmatter byte-for-byte unchanged.** A skill's `description` decides when it triggers; a command's `allowed-tools` and `mutates` are checked by tooling. Report a frontmatter defect instead of fixing it.
- **Leave generated regions byte-for-byte unchanged.** A region runs from a `<!-- …:begin -->` marker to its matching `<!-- …:end -->`. A "do not edit" banner with no end marker freezes everything from the banner to the next markdown heading, or to the end of the file. A `begin` without its `end`, or an `end` without its `begin`, stops the run: edit nothing in that file and report the broken marker. The region's owner regenerates it; an edit is overwritten or, worse, corrupts data its owner reads back.
- **Keep every rule that still binds.** Delete a rule only when it is stale or inferable from code. A rule a proven check enforces collapses to one line; it stays.
- **Keep team conventions.** Branch names and PR process stay, even when they look obvious.
- **Create no files.** Name where content should go; the user decides.
- **Invent no instructions.** Tighten, rename, reorder or delete. Add no rule, wound or parameter the file did not hold; the recovery pointer is the one exception.
- **Flag uncertainty.** When unsure whether a rule is stale or enforced, keep it and say so in the report.
