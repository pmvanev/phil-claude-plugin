# Expected outcome — fixture 03 (runner configuration)

A GitLab runner fleet on AWS: the runner manager's `config.toml` template, the runners' registration and
their job instances in Terraform, the repository's own small pipeline, and the configuration of the Azure
fleet it replaced. The `README.md` says which is live. Six defects are seeded, beside a correct setting
for each and a retired platform full of worse ones.

**Pins:** the review gathers runner configuration and its infrastructure code, reads `ci-runners.md`,
decides which platform is live, names each runner finding by its `RUN-n` id with the row's fix, records
the commit it read, and lists the live system as unread.

**How to drive it:** per `../README.md`, over a copy holding only the project's files, as a git
repository, since the review records the commit it read.

**Expected:** a `.ci-review.md` holding the six must-fix items in `expected-backlog.md`, matched on the
Row and on a Preferred form that is the row's form verbatim, alone or followed by ` — here: `:

1. **PIPE-10** — `test`'s `retry: 2` reruns any failure.
2. **RUN-1** — the open pool mounts the socket with `max_use_count = 10`, so ten jobs share each host's
   daemon.
3. **RUN-12** — `scale_factor = 1.0` with `scale_factor_limit = 8`: `ceil(1.0 × acquired)` never exceeds
   `acquired + idle_count`, so neither setting acts.
4. **RUN-4** — the deploy runner is registered `untagged = true` and `access_level = "not_protected"`,
   and its instances carry the deploy role.
5. **CWE-1357** — `scripts/ci.sh` exports requirements with `--no-hashes`, so `pip` installs the
   lockfile's versions unchecked.
6. **CWE-494** — `scripts/ci.sh` fetches a CA bundle with no checksum.

**Hard assertions (any failure blocks the change):**

- **`legacy-azure/` is named as retired history and not reviewed.** Its shell executor, privileged mode,
  `latest` image and `if-not-present` pull policy draw no item.
- **The deploy pool's socket is not RUN-1.** Its machines run one job each (`max_use_count = 1`). An
  Advisory to build daemonless is allowed.
- **No item is filed for** the metadata options (`http_tokens = "required"`, hop limit 1), the OIDC subject
  pinned to `main` under `StringEquals`, the deploy pool's `idle_count = 0`, the open pool's untagged and
  unprotected registration (its instances hold no role), or `gitleaks`'s retry on `runner_system_failure`
  and `scheduler_failure`.
- **The backlog records the commit it read**, names `legacy-azure/` on its History line, and lists the
  runner manager and the AWS account — the live system — under Not read.
- **The open pool's shared host daemon is one item, RUN-1.** A RUN-10 item for the same daemon cache fails:
  one defect two rows describe is filed under the closer row.
- **No reviewed file is edited.**

**Not a failure:** an Advisory item, such as the open pool's warm floor sized without measured queue
wait, or the deploy pool's socket on one-job machines; a
question whether `tests/render-config.sh`, which the pipeline calls, renders the template as reviewed;
the trigger matrix's cells, which no assertion names; line
numbers within ±2.
