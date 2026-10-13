---
description: "Say what a finished stage of work decided, or with --slice what a finished slice actually landed as against what its brief promised — in 200 words or fewer of plain English — the decisions and what they rule out, with no file paths, handles, decision numbers or card numbers. Reads one feature artifact and prints; writes nothing and derives no status. For where the work stands use /phil:nwave-slice-status; for what you were doing, /phil:resume."
argument-hint: "[<feature>] [--slice [NN]]"
mutates: false
allowed-tools: Read, Glob, Grep, Bash(git log:*), Bash(git show:*)
---

Load the `nwave-wave-summary` skill at
`${CLAUDE_PLUGIN_ROOT}/skills/nwave-wave-summary/SKILL.md` and render the summary it describes.

`--slice [NN]` reconciles a slice brief against the commits that shipped, naming what landed that the
brief did not describe and what the brief promised that did not land. Attribution is by the brief's own
history and by the commit-subject convention — **which fails on precursor commits**, so the count of
unattributable commits is reported rather than absorbed. `git show --stat` serves that reconciliation.

With no argument, resolve the most recently touched feature and **say that is what was resolved** — no
artifact records completion, so the default is not the most recently *completed* stage and must not be
described as one.

**Every word of the summary is composed, so `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` governs all of it.**
Read it as *compose well, never compose short*: the ceiling already bounds length, and the standard bears
on active voice, positive form and putting the emphatic word last, in a read whose whole value is being
finishable in one pass.

No interpreter is granted, so nothing counts the rendered output at run time: the skill's prose alone
holds the 200-word ceiling here, and fixtures hold it at build time.

`mutates: false` asserts more than the grant delivers. `git log` and `git show` both accept
`--output=<file>`, which writes any path, unconditionally (git 2.53.0, 2026-09-08); `git log -p
--ext-diff` runs a diff driver the target repo configures. A prefix-match grant cannot exclude a flag.

Report the outcome by name, per the skill's `## Decision outcomes`, and name the artifact read with its
date so a wrong target is visible rather than inferred.
