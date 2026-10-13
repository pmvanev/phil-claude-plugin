# Widget Service

## Workflow

- Every command file declares `mutates: true` or `mutates: false` in its frontmatter. We added this
  in August after an audit found two commands with identical tool grants, where one must never write
  and the other must run arbitrary code; only prose told them apart, and no validator reads prose. The
  check fails the build on a `mutates: false` command that grants `Write`, `Edit` or bare `Bash`, and
  on any command with no declaration. The first version of the check was written and never called, so
  test that a new check fails on the input that motivated it before trusting a green run.
