# Upgrading to 4.2

Set `STORE_BACKEND=postgres` in `config/app.env` before upgrading.

Run `make migrate VERSION=4.2` from the repository root.

Restart with `systemctl restart app@4.2`.

The upgrade takes a few minutes on a small install.

| Step | Command |
|------|---------|
| Back up | `pg_dump app > app-4.1.sql` |
| Migrate | `make migrate VERSION=4.2` |
