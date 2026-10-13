# Locate the Test Runner

Shared procedure for determining how to run a project's test suite, so every consumer detects
the runner the same way. The loaders are listed in `skills/shared/README.md` and derived by
`tests/test_shared_fragment_registry.py` — this header names none, because a hand-kept list once
named a skill that did not reference this file.

1. **Check CLAUDE.md first.** Read the project's `CLAUDE.md` for a declared test command
   (look for headings or keys like "Test", "Testing", "Test Commands", "test runner", or
   shell commands like `npm test`, `pytest`, `cargo test`, `go test`). If found, use it —
   the user has told you the answer.
2. If CLAUDE.md has no test command, auto-detect:
   - Check for `package.json` scripts (`test`, `test:unit`)
   - Check for `pytest.ini`, `setup.cfg`, `pyproject.toml`
   - Check for `Makefile` test targets
   - Check for `go.mod` (`go test ./...`), `Cargo.toml` (`cargo test`), etc.
3. Run the test command once to verify it works before starting.

If no test runner is found by either method, tell the user that nothing will catch a behaviour
change, and use AskUserQuestion to confirm before proceeding.
