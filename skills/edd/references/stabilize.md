# STABILIZE — the pin dispatch, its checks, and the reviews

The full STABILIZE step of `skills/edd/SKILL.md`. Read in full before pinning anything.

## 1. Pin

Send each accepted expectation that no test yet pins — except one spot-checked by hand — and each row
trusted to the tests, to the engine that built it, with `${CLAUDE_PLUGIN_ROOT}/rules/testing.md` and
`${CLAUDE_PLUGIN_ROOT}/rules/test-patterns.md`: the engine writes to them, and only
`phil:review-code`'s Priority 6 enforces them. Ask for:

- a checkable expectation — a test `rules/testing.md` accepts, asserting the behaviour the accepted
  scenario showed;
- a qualitative expectation, or an output too large to assert — an approval test whose approved output
  is the evidence the developer accepted, verbatim. The developer's accept was the first human read;
  the test shows them every later change as a diff;
- a row trusted to the tests — the name of the test that already pins it.

The engine commits the pins and names the test that pins each expectation. Ask it to run its oracle
with the pins committed and return that run. Capture it as `oracle_result`, replacing the last.
Then check three things; none re-runs a check in the oracle's place:

- **Test files only.** The pin commit touches only test files and approved-output files; a change
  outside test files is a rebuild — follow BUILD's rebuild rule.
- **Green.** Each pinning test passes in the engine's oracle run after pinning. A pin that run omits,
  or shows red, is no pin.
- **Matched.** Each approved-output file equals the evidence the developer accepted, byte for byte. A
  difference is no pin.

An accepted expectation or trusted row left without a pin goes to FINDINGS. One spot-checked by hand
cannot be pinned in the loop, and the article asks for more stabilizing there, not less: in a
separate dispatch, ask the engine for a test that runs outside the loop, where the thing can run — a
browser test, a CI job, a staging check. Its commit may touch test files and CI configuration, and it
is exempt from the green check, since no oracle run here contains it. Record it as `pinned, not run
here`, or `pinned by nothing` when no such test can be written; either way it goes to FINDINGS with
only `waive` and `stop`, since nothing here can show it green.

## 2. Review the code

List every file changed since `base`: `git diff --name-only <base>` and the untracked files from
`git ls-files --others --exclude-standard`, leaving out the review backlogs. Run `phil:review-code`
(Skill tool) once per changed file, pinning tests included: it takes one path, and its `--changes`
sees only the last commit. Each run adds a `Scope:` block to `.refactoring-backlog.md`; read only the
blocks this run wrote. A file's run also judges that file's tests, so two runs can file the same item:
items naming the same file, lines and smell are one finding, however many runs filed it.

- **Blocking** — every Priority 1 item, except an item whose Smell is `Advisory` or an `LWS-n` id: one
  is a question for the author, the other a load-time finding, and both advise. And every Priority 6
  item whose File holds a pinning test: a weak pin is no regression alarm.
- **Advisory** — every other item, for REPAIR.

## 3. Audit the UI

When a changed file is UI — a component, a template, a stylesheet — run `phil:ux-review` (Skill tool)
once per UI file. A `must-fix` blocks done and goes to FINDINGS. Record every `consider` as advisory:
no repair skill owns one, so REPAIR lists it and runs nothing.

## Re-entry

After a rebuild, or a pinning fix from FINDINGS, repeat all three over everything changed since
`base`. Match each new finding with the old by FINDINGS' sameness rule. A blocker the re-run does not
reproduce is cleared; one it reproduces keeps its fix-round count.
