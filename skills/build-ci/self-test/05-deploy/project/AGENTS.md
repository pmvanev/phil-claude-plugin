# tally

A ledger-totalling service. `src/` holds the code, `test/` the Vitest suite, and `docs/` the user
guide. Run `npm test` before committing.

## Deploys

Decided 2026-09-02: every green main commit goes to staging; production is deployed by hand once
staging looks right. `scripts/deploy.sh <environment> <image>` points an environment at an image in
`registry.gitlab.example.invalid/acme/tally`, built from the `Dockerfile`. Each environment sets its own
`KUBE_CONTEXT` and `TALLY_LEDGER_DIR`.
