---
name: claude-md
description: Skill bundle for phil:claude-md command — review and revise any CLAUDE.md or AGENTS.md file, in this repo or elsewhere, so each rule lives where the model cannot lose it
---

# CLAUDE.md Reviewer

Revise an instruction file against two standards. **Read both first** — nothing loads them for you:

- `${CLAUDE_PLUGIN_ROOT}/rules/claude-md.md` — what belongs in the file and how it is laid out.
- `${CLAUDE_PLUGIN_ROOT}/rules/agent-instructions.md` — how each instruction is phrased and where it lives.

Every edit tightens the file and keeps every rule that still binds.

## Parse the Argument

`$ARGUMENTS` holds one or more paths, separated by spaces. A quoted path may contain spaces.

| Pattern | Type | Example |
|---------|------|---------|
| Names a file, whatever its name | File path | `CLAUDE.md`, `AGENTS.md`, `~/other-repo/CLAUDE.md`, `/abs/path/notes.md` |
| Ends with `/` or is a directory | Directory path | `./`, `src/`, `~/other-repo/` |
| Empty or omitted | Current directory | — |

Expand a leading `~` to the home directory. A path outside the current repository is valid; process it the same way. Report a path that does not exist and skip it.

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
2. Read both rules.
3. Find the root.
4. Find the **generated regions** (see Safety) and set them aside.
5. Check whether history can be recovered (see **Recoverability**).
6. Run the **audit**.
7. Apply the **revision rules**.
8. **Report**.

**An `AGENTS.md` is read by agents other than Claude Code.** Skip the items that only Claude Code honours: `CLAUDE.local.md`, `.claude/rules/`, hooks and `@imports`.

## Directory Path

1. Glob the given directory — not the root — for `**/CLAUDE.md`, `**/CLAUDE.local.md` and `**/AGENTS.md`.
2. Drop every match under `self-test/`, `node_modules/`, `vendor/` or `.git/`. Self-test inputs are flawed on purpose; a run that "fixes" them destroys the test. Drop any other match that `git -C <root> check-ignore -q <rel>` reports ignored, except `CLAUDE.local.md`, which is ignored by design.
3. With no matches left, report that and stop.
4. Apply the **File Path** process to each file found.
5. Report per file.

---

## Recoverability

Run, with `<rel>` the target's path relative to the root:

```
git -C <root> status --porcelain --ignored -- <rel>
git -C <root> log -1 --format=%h -- <rel>
```

- **Empty status and a hash** → the pre-revision text sits at that commit. History may be cut. Leave one line, outside every generated region, as the file's last line — `Rationale and history cut <date>: git show <hash>:<rel>` — replacing any earlier line of that form, and repeat it in the report. This pointer is the one line the skill may add.
- **Anything else** — modified, untracked, ignored, no root, or an error → cut no history. Compress each wound to one line and keep the rest, flagged in the report as recoverable nowhere.

---

## Audit

Score the file against each criterion. Flag violations before editing.

### Structure
- [ ] Under 200 lines, generated regions included (warn at 200–300; flag over 300)
- [ ] Markdown headers group sections
- [ ] Bullets, not paragraphs, carry instructions
- [ ] One or two lines of project context, then build and test, then the order in revision rule 9

### Content
- [ ] Includes build and test commands
- [ ] Every instruction tells Claude something it cannot infer from the code
- [ ] No file-by-file codebase descriptions
- [ ] No standard language conventions
- [ ] No tutorials (links allowed)
- [ ] No stale instructions for removed features

### Writing
- [ ] Each bullet states one instruction
- [ ] Imperative mood ("Run X", not "You should run X")
- [ ] Specific over vague ("2-space indent", not "consistent formatting")
- [ ] At most two IMPORTANT markers
- [ ] No platitudes ("write clean code")

### Placement — per `agent-instructions.md`
- [ ] A rule a hook or script enforces takes one line naming the check
- [ ] A mechanically checkable rule with no check is flagged for one
- [ ] Each non-obvious rule leads with its reflex and carries at most one line of wound
- [ ] Prohibitions name their alternative, or become reflexes
- [ ] A described protocol is named instead (Makefile, circuit breaker, `Key: Value`, EBNF)
- [ ] No invented tags or sigils
- [ ] No numbered workflow with "go back to step N" routing

### Scoping
- [ ] Personal preferences live in `CLAUDE.local.md`
- [ ] Path-specific rules live in `.claude/rules/` with frontmatter
- [ ] Multi-step workflows live in skills
- [ ] Deterministic rules live in hooks

---

## Revision Rules

Apply these in order.

### 1. Delete What Claude Already Knows

Remove standard conventions, framework defaults and obvious practices.

### 2. Delete Stale Instructions

Grep the codebase for every file, command and tool a rule names. Cut the rule when its subject no longer exists.

### 3. Collapse Enforced Rules

For each rule, search the root's `scripts/`, `hooks/`, `.claude/settings.json`, CI config and `tests/` for a check that enforces it. For an `AGENTS.md`, count only checks every agent meets — CI, tests, git hooks — never a Claude Code hook.

- **A check exists and a test exercises it** — a test that runs the check on the input it must refuse. The check is proven. Collapse the rule to one line: the reflex, then the check's path. Delete the explanation of how the check works; the check's own header owns it.
- **A check exists and no test exercises it.** The check is unproven. Keep the rule's prose, and name the check and the missing test in the report.
- **The rule is mechanically checkable and no check exists.** Keep the rule, and name the missing check in the report.

Write no hook, script or test. Collapsing keeps the rule; deleting it is never this step's outcome.

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

Keep at most two IMPORTANT markers: the two rules whose breach costs most.

### 9. Impose Structure

Order sections: one or two lines of project context, then build and test, code style, architecture, workflow, gotchas. Keep sections the project needs that this list lacks. Delete empty ones. Turn instruction paragraphs into bullets.

### 10. Flag Misplaced Content

Name in the report any path-specific rule, personal preference, multi-step workflow or numbered checklist that belongs elsewhere, and where it belongs. Move nothing.

### 11. Apply Writing Standards

Tighten each sentence per `${CLAUDE_PLUGIN_ROOT}/rules/writing.md`: active voice, positive form, no needless words.

### 12. Trim to 200 Lines

If the file still exceeds 200 lines, name the least-essential rules and where each could move. Generated regions count toward the total and are never cut.

---

## Report

- Lines and words, before and after.
- The audit, with each failed item.
- Each rule cut, and why: stale or inferable.
- Each rule collapsed to one line, with the proven check that enforces it.
- Each check found but unproven, and each check worth writing.
- Each rule rewritten, one line each.
- History cut, with its recovery command — or history kept because it is recoverable nowhere.
- Content to move, and where.
- Generated regions found and left unchanged.

---

## Safety

- **Leave generated regions byte-for-byte unchanged.** A region runs from a `<!-- …:begin -->` marker to its matching `<!-- …:end -->`. A "do not edit" banner with no end marker freezes everything from the banner to the next markdown heading, or to the end of the file. A `begin` without its `end`, or an `end` without its `begin`, stops the run: edit nothing in that file and report the broken marker. The region's owner regenerates it; an edit is overwritten or, worse, corrupts data its owner reads back.
- **Keep every rule that still binds.** Delete a rule only when it is stale or inferable from code. A rule a proven check enforces collapses to one line; it stays.
- **Keep team conventions.** Branch names and PR process stay, even when they look obvious.
- **Create no files.** Name where content should go; the user decides.
- **Invent no instructions.** Tighten, rename, reorder or delete. Add no rule, wound or parameter the file did not hold; the recovery pointer is the one exception.
- **Flag uncertainty.** When unsure whether a rule is stale or enforced, keep it and say so in the report.
