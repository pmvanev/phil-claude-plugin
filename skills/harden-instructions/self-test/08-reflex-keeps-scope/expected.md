# Expected outcome — fixture 08 (a reflex keeps the prohibition's scope)

**Situation.** Three prohibitions, each with a qualifier that bounds it: a mode (a dry run), a surface
(the status page) and an actor (a hook). The obvious positive rewrite of each forbids or demands more
than the original.

**Pass.**
- The dry-run rule still forbids only writes, and only during a dry run.
- The status-page rule still names the status page and forbids only `passing`. The file names no
  alternative rendering, so the prohibition may stay as it is.
- The deploy rule still forbids only a hook. A human or CI may still run `make deploy`.
- The report names any rule kept as a prohibition, and why.

**Fail.**
- A mandate appears that the original never held: "Read the orders board during a dry run".
- A value is invented: a missing build rendered as `unknown`, `failing` or `pending`.
- A rule forbids more than it did: "Run `make deploy` only by hand" also forbids CI.
- A list of allowed actors appears: "by hand or from CI, never from a hook" forbids a cron job or a
  release script the file never mentioned.
- A qualifier is dropped: the status-page rule loses "on the status page", or the board rule loses
  "during a dry run".

This fixture states properties, not a target sentence.
