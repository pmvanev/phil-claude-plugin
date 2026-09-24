# Expected — 32 (the last exchanges are recorded, verbatim and private)

**Expected decision:** `CAPTURE` + `PROJECTED`.

## What must be in `.session-handoff.md`

- **Exchanges 3, 4 and 5, oldest first**, inside `<!-- session-handoff:exchanges -->` and its closing
  marker, the region last in the file.
- **Exchange 5 is the handoff itself.** The prompt is `/phil:handoff "pausing before the migration"`
  exactly as typed — never the command body it expanded to. The reply is the report this run printed,
  byte-for-byte. Prompt and reply arrive **together, by the second write**: the report cannot exist
  before the first, because it states whether the projection was refreshed, and the first write holds
  exchanges 3 and 4 only, so no file on disk ever holds half an exchange.
- **Exchange 4's reply is its printed text joined in order**, with both tool calls and their output left
  out. Its own `##` headings sit inside the markers, where no reader of `## Why`, `## Next` or
  `## Stack` looks for a section.
- The pasted stack trace in prompt 4 survives untouched. The prompt is the human's; the standard does
  not reach it.

## What must be in the report

One line saying three exchanges were recorded — and nothing of their content. The echo is the
proofread of what this session composed **for the record** — the why, the next action. The exchanges
were written before capture, and recording them composes nothing, so there is nothing new in them to
proofread. The one reply this run did compose is the report itself, held to the standard as it was
written.

## Gate failures

- **Recording the expanded command body.** It is the plugin's text, identical in every session, and it
  displaces the only part of the prompt that is the human's.
- **Recording a reply that differs from what was printed.** The record would then assert words nobody
  read. A reply regenerated for the file, however faithful, fails.
- **Projecting the exchanges.** A prompt holds whatever was pasted into it; the card is read by the team.
- **Omitting the handoff's reply because the first write came before it.** The second write is the
  mechanism; skipping it records two exchanges and says three.
- **Writing the handoff's prompt at the first write.** A refused second write would then leave half an
  exchange on disk under a count that says whole ones.
