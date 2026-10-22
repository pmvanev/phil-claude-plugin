# ledger

A bookkeeping library. Work lands on `main` through a merge request whose pipeline passed.

## CI policy

- **Pipelines**: open MR only
- **Docs-only paths**: `docs/**`, `**/*.md`
- **MR**: everything
- **Main**: everything
- **Merge**: a passing MR pipeline is required
- **Secret scan**: every pipeline, docs-only included
- **Notify**: a failure or a warning names whoever started the pipeline
