# Trigger matrix a build must reach

| Job | MR | docs-only MR | main push | docs-only main | schedule | tag | web or API |
|---|---|---|---|---|---|---|---|
| (pipeline) | created | created | created | created | created | — | created |
| gitleaks | runs | runs | runs | runs | runs | — | runs |
| lint | runs | exits early | runs | exits early | — | — | runs |
| typecheck | runs | exits early | runs | exits early | — | — | runs |
| unit-tests | runs | exits early | runs | exits early | — | — | runs |
| build | runs | exits early | runs | exits early | — | — | runs |
| mutation-diff | runs | exits early | — | — | — | — | — |
| mutation-full | — | — | — | — | runs | — | — |
