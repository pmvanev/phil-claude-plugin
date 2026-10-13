# Expected outcome — fixture 06 (a skill keeps its frontmatter and its shape)

**Situation.** `SKILL.md.input`, copied in as `SKILL.md`, so the skill profile applies. It ships under
another name because a file called `SKILL.md` below `skills/` risks discovery as a real, broken skill. Its frontmatter `description` holds a
prohibition, its procedure routes with "go back to step N", and its rules are prohibitions plus one
described retry protocol.

**Pass.**
- The frontmatter is byte-for-byte unchanged, prohibition included. The report may flag the
  description; it never edits it, because the description decides when the skill triggers.
- The report names the profile as **Skill** and the standards read: `agent-instructions.md` and
  `plugin-dev:skill-development`.
- No project-memory layout appears: no "Build & test" section, no 200-line verdict, no section reorder.
- Each rule keeps its meaning in positive form, or names its alternative. The retry rule names a
  circuit breaker and keeps the count the prose gave — "a couple" is two, so `k = 2`.
- The report flags the procedure's step-routing as a checklist that would serve better as targets.

**Fail.**
- Any change to the frontmatter.
- A project-memory item judged or imposed on the skill.
- The `internal` exclusion or the no-invented-PR rule disappears.
- A retry count other than two.
- Step 6 disappears, or the report calls `CHANGELOG.md` stale. A skill runs in the user's repository;
  a file missing from the copy says nothing about whether the user has one.

This fixture states properties, not a target text: a fixture that supplies the rewrite turns a
composition test into "emit this string".
