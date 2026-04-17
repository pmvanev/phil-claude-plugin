---
name: create-plugin-feature
description: Skill bundle for phil:create-plugin-feature command — capture a session's workflow as a plugin feature idea
---

# Create Plugin Feature Idea

You are capturing the workflow the user just executed in this session as a **feature idea** for the phil-claude-plugin. The output is a single markdown file that a future Claude (or the user) will read to design a new command, skill, rule, or hook.

The goal is **faithful capture**, not design. Do not propose the final implementation — record what happened clearly enough that the future implementer has everything they need.

---

## Process

1. **Reconstruct the session** from the conversation so far. Do not ask the user to re-summarize what they just did — you were there.
2. **Gather repo context** with shell commands (below).
3. **Draft the feature idea file** in memory.
4. **Show the draft** and ask the user to fill in gaps via `AskUserQuestion`.
5. **Write the file** to the resolved output path.
6. **Report the path** and suggest a next step.

---

## Resolve Output Path

In priority order:

1. If the argument looks like a path (contains `/` or ends in `.md`), use it verbatim.
2. Else if `C:/Users/PhilVanEvery/Git/github/pmvanev/phil-claude-plugin/feature-ideas/` exists or can be created, write there.
3. Else write to the current working directory.

Filename: `YYYY-MM-DD-<slug>.md` where slug comes from the argument or from a short kebab-case summary of the session (e.g., `bug-fix-regression-harness`, `prose-edit-pass`).

Create the `feature-ideas/` directory if it does not exist.

---

## Gather Repo Context

Run these in parallel:

- `git rev-parse --show-toplevel` — find the repo root of the CWD
- `git log --oneline -20` — recent commits
- `git status --short` — uncommitted changes
- `git diff --stat HEAD` — scope of modifications this session
- `git config --get remote.origin.url` — remote for identification

If not a git repo, note that and capture the CWD only.

---

## Reconstruct From Transcript

Scan your own conversation memory for:

- **Trigger** — what the user said at the start, or the state that prompted the work
- **Workflow steps** — the sequence of actions taken (search → read → edit → test → repeat)
- **Commands / prompts run** — every slash command, bash command, or significant tool call, in order
- **Files touched** — what was created, edited, deleted
- **Decisions** — judgment calls the user made or confirmed (not pattern-matching)
- **Pain points** — friction the user mentioned or that showed up as rework
- **Techniques used** — patterns, heuristics, mental models applied

If the session was long enough that details have been compressed away, say so in the draft rather than inventing specifics.

---

## Draft Structure

```markdown
# Feature Idea: <title>

**Captured:** <YYYY-MM-DD>
**Repo:** <repo name or path>
**Remote:** <remote URL if any>
**Branch:** <current branch>

## One-line pitch

<One sentence: what workflow this automates and who benefits.>

## What I just did

<2-4 sentences describing the big-picture workflow. Plain prose. No bullet lists yet.>

## Triggering circumstances

<What state was the repo or the user in when this workflow started? What kicked it off?>

## Workflow steps (observed)

1. <step>
2. <step>
…

## Commands and prompts run

| # | Kind | Command or prompt | Purpose |
|---|------|-------------------|---------|
| 1 | slash | /phil:review-code | … |
| 2 | bash | git log --oneline -10 | … |
| 3 | prompt | "fix the failing test in X" | … |

## Files touched

- `path/to/file` — <what changed>
…

## Techniques and heuristics used

- <technique> — <why it mattered>
…

## What makes this worth automating

<Why should this exist as a plugin feature? What recurring cost does it remove? What quality does it improve?>

## Open design questions

- <question the future implementer will need to answer>
…

## Suggested shape (tentative — implementer decides)

- **Mechanism:** <command | skill | rule | hook | combination>
- **Tentative name:** `/phil:<name>` or `<rule-name>.md`
- **Inputs:** <what the user passes in>
- **Outputs:** <what the feature produces>
- **Known prior art in this plugin:** <existing commands/rules this overlaps with>

## Notes

<Anything else. Links, screenshots, related issues, things the user said should be preserved.>
```

---

## Gap-Filling Questions

After drafting, ask the user **in a single `AskUserQuestion` call** with a small number of questions (2-4 max). Prefer these:

1. **Title / slug** — confirm or override the proposed title and filename slug.
2. **Missing context** — "Anything from the original trigger that I missed or got wrong?"
3. **Priority** — `now` / `soon` / `someday` / `reference-only`.
4. **Mechanism hint** — only ask if you genuinely cannot tell whether this is a command, skill, rule, or hook. Usually you can.

Skip questions whose answers you already have from the transcript. Do not pad the question list.

After answers come back, revise the draft, then write the file.

---

## Write Rules

- **Preserve the user's own words** for pain points and intent. Paraphrase only for structure.
- **Flag uncertainty.** Where you are reconstructing from memory and unsure, write `(unconfirmed)` inline rather than stating a firm claim.
- **No implementation plan.** Do not outline prompts, skill steps, or file layouts for the future feature — that is the implementer's job.
- **Keep it under ~200 lines.** Shorter is better. This is a capture, not a spec.
- **Do not modify any other files.** The only write is the feature-idea markdown.

---

## Reporting

When done, output:

- The absolute path to the written file
- A one-line summary of what was captured
- A suggested next step (e.g., "when you're ready to build this, open the file and ask Claude to turn it into a command + skill")

Do not commit the file. The user decides when to commit.
