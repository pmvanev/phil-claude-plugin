# ledger

A bookkeeping web app: `api/` serves it, `web/` renders it. Work lands on `main` through a merge
request whose pipeline passed.

## CI policy

- **Pipelines**: open MR only
- **Docs-only paths**: `docs/**`, `**/*.md`
- **MR**: tests and mutation for changed and affected code
- **Main**: everything except mutation
- **Schedule**: full mutation, weekly, off-hours, sharded
- **Merge**: a passing MR pipeline is required
- **Secret scan**: every pipeline, docs-only included
