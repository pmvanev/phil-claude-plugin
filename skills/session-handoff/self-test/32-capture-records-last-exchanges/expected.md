# Expected — 32 (the last exchanges are recorded, verbatim and private)

**Expected decision:** `CAPTURE` + `PROJECTED`.

## What must be in `.session-handoff.md`

- **Exchanges 3, 4 and 5, oldest first**, inside `<!-- session-handoff:exchanges -->` and its closing
  marker, the region last in the file.
- **Exchange 5 is the handoff itself.** The prompt is `/phil:handoff "pausing before the migration"`
  exactly as typed — never the command body it expanded to. The reply is the report this run printed,
  byte-for-byte, because the script copied it from the transcript **after** it was printed. Step 9
  wrote no region at all, so no file on disk ever holds half an exchange.
- **None of it passed through this session.** Every word between the markers was placed by
  `session-exchanges.py record`; no Write, Edit, command or printed line of this run carries a prompt
  or a reply.
- **Exchange 4's reply is its printed text joined in order**, with both tool calls and their output left
  out. Its own `##` headings sit inside the markers, where no reader of `## Why`, `## Next` or
  `## Stack` looks for a section.
- The pasted stack trace in prompt 4 survives untouched. The prompt is the human's; the standard does
  not reach it.

## What must be in the report

One line saying three exchanges will be recorded — the report prints before `record` runs — and
nothing of their content. The echo is the proofread of what this session composed **for the record** —
the why, the next action. The exchanges were said before capture, and recording them composes nothing,
so there is nothing new in them to proofread. The one reply this run did compose is the report itself, held to the standard as it was
written.

## Gate failures

- **Recording the expanded command body.** It is the plugin's text, identical in every session, and it
  displaces the only part of the prompt that is the human's.
- **Recording a reply that differs from what was printed.** The record would then assert words nobody
  read. A reply regenerated for the file, however faithful, fails.
- **Projecting the exchanges.** A prompt holds whatever was pasted into it; the card is read by the team.
- **Omitting the handoff's reply by recording before printing.** The transcript holds only what was
  printed; `record` run first copies three exchanges, the last with a reply cut off before its report.
- **Printing anything after `RECORDED`.** The recorded reply ends at the report; a closing line would
  make what was printed differ from what was recorded.
- **Typing the exchanges.** Anthropic's classifier refuses a session reproducing its own output at
  length — 7 of 8 real 0.97.0 handoffs — and a retyped reply is not the reply anyway.
