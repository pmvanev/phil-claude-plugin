# ci-runners

The GitLab runner fleet. **`aws/` is the live fleet**: one gateway runs the runner manager, which
autoscales two pools of EC2 job instances. **`legacy-azure/` is the retired Azure fleet**, decommissioned
2026-10-08 and kept as history; nothing in it runs.

- `open` takes every project's MR and branch jobs. Its instances hold no cloud role.
- `deploy` runs the dev and production deploy jobs. Its instances carry the `deploy` instance role.
