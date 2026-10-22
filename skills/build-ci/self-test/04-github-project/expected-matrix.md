# Trigger matrix a build must reach

| Job | MR | docs-only MR | main push | docs-only main | schedule | tag | web or API |
|---|---|---|---|---|---|---|---|
| (pipeline) | created | created | created | created | created | — | — |
| gitleaks | runs | runs | runs | runs | runs | — | — |
| lint | runs | exits early | runs | exits early | — | — | — |
| typecheck | runs | exits early | runs | exits early | — | — | — |
| unit-tests | runs | exits early | runs | exits early | — | — | — |
| build | runs | exits early | runs | exits early | — | — | — |
| mutation-diff | runs | exits early | — | — | — | — | — |
| mutation-full | — | — | — | — | runs | — | — |
| andon | — | — | on failure | on failure | on failure | — | — |
| tell-author | on failure | on failure | on failure | on failure | — | — | — |
