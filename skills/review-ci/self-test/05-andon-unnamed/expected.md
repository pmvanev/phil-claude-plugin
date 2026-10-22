# Expected outcome — fixture 05 (andon, no channel named)

The project of fixture 04 with two changes: its Andon field keeps the default text, "a failed main
pipeline notifies the whole team", which names no channel; and its one workflow, `ci.yml`, has no andon
job.

**Pins:** on GitHub, PIPE-25 is must-fix only where the Andon field names an issue or a webhook, which
only a job can carry out. Where the field names no channel, a chat app's subscription the review cannot
read may pull the cord, so the item is a question.

**How to drive it:** per `../README.md`, over a copy holding only the project's files.

**Expected:** a `.ci-review.md` whose Policy line lists the seven declared fields and whose backlog holds
the one question in `expected-backlog.md`, matched on the Row, the Severity and a Preferred form that is
the row's form verbatim, alone or followed by ` — here: ` and this pipeline's change.

**Hard assertions (any failure blocks the change):**

- **PIPE-25 is a question, not a must-fix item**, filed once, at the Andon field in `CLAUDE.md`: no job
  carries the field out, and the rule files such a field's item at the field.
- **"Not read" names chat-app subscriptions**, or the repository's notification settings, as the source
  that could hold the cord.
- **No must-fix item** names PIPE-25 or any other row: the rest of the pipeline is fixture 04's, which
  drew none.
- **No reviewed file is edited.** The run writes `.ci-review.md` and nothing else.

**Not a failure:** an Advisory item, such as the merge gate or an MR run left running when a newer one
starts; listing branch
protection and the required checks under "Not read"; line numbers within ±2; a differently worded title.

**Driven 2026-10-22** blind, against this working tree's `SKILL.md` at 1.8.0. The first drive filed
PIPE-25 as a question with the row's form verbatim and named chat-app subscriptions under "Not read",
but filed it at the Andon field, not at `ci.yml` as this file first expected. The drive was right: the
rule files a field no job carries out at the field, and this file now says so.
