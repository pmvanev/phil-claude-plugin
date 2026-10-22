# tally

A command-line tool that totals ledger files. `src/` holds the code, `tests/` the unittest suite, and
`docs/` the user guide. Work lands on `main` through a pull request whose checks passed.

## CI policy

- **Pipelines**: open MR only
- **Docs-only paths**: `docs/**`, `**/*.md`
- **MR**: everything
- **Main**: everything
- **Merge**: a passing MR pipeline is required
- **Secret scan**: every pipeline, docs-only included
- **Andon**: a failed main pipeline notifies the whole team, through an issue the repository's watchers are emailed about
