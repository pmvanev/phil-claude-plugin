# ROUTE — one route, its reason and its owner

Part of the `start` skill; `../SKILL.md` governs this step as much as this file does. Read this file
whole before naming a route.

1. **The repo's recorded build path.** Read the root's `CLAUDE.md` and `AGENTS.md`, where present, for a
   rule that names a command or skill to run for a kind of work — this plugin's own reads `Run nw-discuss
   before authoring a new feature, skill or command`. A principle that names no command, such as "test
   first", is no build path. Where the card's work is that kind, the rule decides: quote the rule and
   name its file, and report `BUILD-PATH`. Where the step the rule names has already run — for
   `nw-discuss`, a `feature-delta.md` in the `docs/feature/<feature>/` directory the card links — name
   the rule's next step instead; where it names none, go on to rule 2.
2. **The card's wave.** A `wave: <name>` label routes to that wave's command in the *Work this with*
   table of `${CLAUDE_PLUGIN_ROOT}/skills/nwave-issue-board/SKILL.md`; read the table there, and never
   restate it. Where a row names a wave command and a step command, route to the wave command and name
   the step command in the reason. A label the table has no row for goes on to rule 3, and the report
   says the table does not cover it.
3. **Who would see the change.** A change a user would see — a command, an output, a page, a behaviour
   — routes to `phil:edd`. A change nobody would see — a refactor, a migration, a cleanup, performance or
   a dependency — routes to `phil:work`.
4. **Whether it fits one sitting.** A card whose DONE WHEN holds exactly one item the card states, and
   whose OPEN names nothing, goes inline instead of rule 3's route: the session works it directly, under
   the repo's own rules. A `NO-DONE-WHEN` card never goes inline: nothing says when the work would stop.

Rules 1 and 2 decide wherever they apply, in that order. Otherwise rule 3 picks the route, and rule 4
overrides it for a card that fits one sitting.

Name one route, its reason in one clause, and the command or skill that owns it. Then ask once: **start
it** runs the route now, and it writes what that route writes; **not now** ends the run, leaving the
claim and the worktree as the report states them. **Launch nothing without the developer's yes.**

- **Yes** — `LAUNCHED`.
- **Other naming a route** — a skill or a command — launch that route instead: `LAUNCHED` with
  `ROUTE-OVERRIDDEN`. Quote the developer's reason where they gave one: an override is the evidence that
  the card and `CLAUDE.md` did not choose the route. Other naming no route is unanswered.
- **Not now, or no clear answer after a second ask** — `NOT-LAUNCHED`.

**Print the outcome tokens, then launch.** A launched route runs on past this skill, so nothing is
reported after it. Invoke a skill or command route through the `Skill` tool, by its name without the
leading slash (`nw-design`). An inline route has no skill: this skill ends, and the session works the
card under the repo's own rules, outside this command's grant, so its writes ask permission.

## The route line

The ROUTE line takes one of these shapes:

```
ROUTE: nw-discuss — CLAUDE.md: "Run `nw-discuss` before authoring a new feature, skill or command."
ROUTE: /nw-design — the card carries `wave: design`
ROUTE: phil:edd — a user would see the change: a new flag on /phil:done
ROUTE: phil:work — nobody would see the change: the hook moves to a shared module
ROUTE: inline — one done-when item, nothing open: fix a broken link in the README
```
