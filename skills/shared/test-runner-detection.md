# Locate the Test Runner

Shared procedure for determining how to run a project's test suite. Referenced by
`skills/refactor/SKILL.md` and `skills/refactor-loop/SKILL.md` so both detect the runner
the same way.

1. **Check CLAUDE.md first.** Read the project's `CLAUDE.md` for a declared test command
   (look for headings or keys like "Test", "Testing", "Test Commands", "test runner", or
   shell commands like `npm test`, `pytest`, `cargo test`, `go test`). If found, use it —
   the user has told you the answer.
2. If CLAUDE.md has no test command, auto-detect:
   - Check for `package.json` scripts (`test`, `test:unit`)
   - Check for `pytest.ini`, `setup.cfg`, `pyproject.toml`
   - Check for `Makefile` test targets
   - Check for `go.test`, `cargo test`, etc.
3. Run the test command once to verify it works before starting.

If no test runner is found by either method, warn the user: "No test runner detected.
Refactoring without tests is risky. Continue anyway?" Use AskUserQuestion and await
confirmation before proceeding.
