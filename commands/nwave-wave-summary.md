---
description: "Say what a finished stage of work decided, in 200 words or fewer of plain English — the decisions and what they rule out, with no file paths, handles, decision numbers or card numbers. Reads one feature artifact and prints; writes nothing and derives no status. For where the work stands use /phil:nwave-slice-status; for what you were doing, /phil:resume."
argument-hint: "[<feature>]"
mutates: false
allowed-tools: Read, Glob, Grep, Bash(git log:*)
---

Load the `nwave-wave-summary` skill at
`${CLAUDE_PLUGIN_ROOT}/skills/nwave-wave-summary/SKILL.md` and render the summary it describes.

With no argument, resolve the most recently touched feature and **say that is what was resolved** — no
artifact records completion, so the default is not the most recently *completed* stage and must not be
described as one.

**This command's read-only grant is checked rather than merely declared.** No `Write`, no `Edit`, and a
`Bash` holding one verb, `git log`, which is on `scripts/check-readonly-commands.py`'s allowlist.
`board-snapshot` and `resume` both declare `mutates: true` while writing nothing, because a forge grant
accepts a mutation document; this one touches no forge, so the narrower declaration is available.

**It is not the first command to manage that, and an earlier draft of this paragraph said it was.**
`nwave-slice-status` has declared `mutates: false` with the identical `Bash(git log:*)` verb since before
this feature existed, and `ai-eos` and `spirit-walk` do the same plugin-wide. Corrected 2026-09-08: the
distinction is against `board-snapshot` and `resume` specifically, not against the plugin.

**And "checked" is one level short of "proven".** `CLAUDE.md` states that an allowlist entry is a promise
that a verb has no writing mode — `git log -p --ext-diff` runs a diff driver the target repo configures,
so even this verb reaches arbitrary code in principle. The claim worth making is that the grant is
verified against an allowlist, which is still more than the rest of this family has.

**What that costs, stated rather than discovered.** No interpreter is granted, so nothing counts the
rendered output at run time. The 200-word ceiling is enforced by fixtures at build time and by the
skill's prose at run time. Granting `python3` would make the count mechanical and the read-only
guarantee promissory again — trading an enforced guarantee for an enforced check, on the one command
whose distinction is the enforced guarantee.

**Every word of the summary is composed, so `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` governs all of it** —
there is nothing quoted here to exempt. Read it as *compose well, never compose short*: the ceiling
already bounds length, and the standard bears on active voice, positive form and putting the emphatic
word last, in a read whose whole value is being finishable in one pass.

Report the outcome by name, per the skill's `## Decision outcomes`, and name the artifact read with its
date so a wrong target is visible rather than inferred.
