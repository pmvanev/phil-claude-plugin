# Artifacts a rework pass must list

| Artifact | Producing jobs | Consuming jobs |
|---|---|---|
| the `dist/` bundle | `build`, and again inside the Dockerfile's build stage by `build-image` and `deploy-staging` ✗ | `test`, `pack`, `build-image` |
| the app image | `build-image`, and `deploy-staging` again from source ✗ | `e2e`, `deploy-staging` |
| the npm package tarball | `pack` | `release` |
