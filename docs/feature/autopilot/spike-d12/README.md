# Spike D12 — how autopilot answers a launched skill's question

Run 2026-11-05 on Claude Code 2.1.318, with Sonnet 5.5 driving, against a throwaway plugin (`plugin/`). Its
`asker` skill calls the question tool with one option marked `(Recommended)`, then writes the chosen
label to `answer.txt`. Its `PreToolUse` hook on `AskUserQuestion` (`plugin/hooks/auto.py`) passes,
denies or pre-fills the ask by `SPIKE_MODE`.

## Results

| # | Session | Mechanism | Result |
|---|---|---|---|
| 1 | headless `claude -p` | none | The question tool does not exist in print mode, even with `--tools` naming it. The skill's ask finds no tool, no hook fires, and the model refuses to choose for the developer. |
| 2 | headless | the orchestrator's instructions: take the recommendation, record it | It took `Blue (Recommended)`, wrote it, and logged the decision in `decisions.md`. |
| 3 | interactive (tmux) | none | The question reaches a human and waits. |
| 4 | interactive | hook **denies**, naming the recommendation | It took `Blue (Recommended)` and reported "By a hook… The user didn't answer." |
| 5 | interactive | hook **allows** with `updatedInput.answers` pre-filled | The transcript reads "User answered Claude's questions"; the model cannot tell the hook from the developer. A record built on this would be false. |
| 6 | interactive | hook denies with a reason carrying D1's three blocker kinds | A question about the developer's own unpublished essays stopped: `BLOCKED: … — an input only the developer holds`. |
| 7 | interactive | the same reason, on the colour question | It judged "Not a blocker", took the recommendation, and named the hook. |

Each interactive row is one run, with one model. Rows 6 and 7 show that the deny reason can carry the
classification; they do not measure how reliable it is.

## Conclusion

Answer a launched route's questions with a `PreToolUse` hook on `AskUserQuestion` that **denies** each
ask during an autopilot run. Its reason names D1's three blocker kinds and the recommended option.
Never pre-fill `answers`: the answer would read as the developer's. Keep the same instruction in the
skill, because a headless run has no question tool and so no hook fires.

## Rerun

```bash
python3 run.py r0-nohook off "/spikeap:auto"                   # rows 1 and 2: headless
python3 run.py r3-instructed off "/spikeap:auto-instructed"
python3 tmux_run.py i1-deny deny "/spikeap:auto"               # rows 3 to 7: interactive, via tmux
python3 tmux_run.py i2-answer answer "/spikeap:auto"
python3 tmux_run.py i3-blocker deny-classify "/spikeap:auto-blocker"
python3 show.py i3-blocker
```

Each run writes to `runs/<name>/`. The interactive driver accepts the folder-trust dialog, which
defaults to "No, exit".
