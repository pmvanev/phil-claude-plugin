"""The refactor loop's write guard, and the transcript it keeps of each run."""
import json
from pathlib import Path

PROTECTED = "/tests/"


def loop_active(cwd):
    """The loop's agent works in `cwd` with `Write` on any path inside it."""
    return (Path(cwd) / ".loop-active").exists()


def refuse_test_write(raw, cwd):
    """PreToolUse hook: while the loop runs, its agent may not edit the tests that judge it."""
    payload = json.loads(raw)
    path = payload["tool_input"]["file_path"]
    if loop_active(cwd) and PROTECTED in path:
        return "deny"
    return None


def keep_transcript(cwd, exchanges):
    """Append each prompt and reply of the run, verbatim, for the next session to resume from."""
    log = Path(cwd) / "run-transcript.md"
    with log.open("a") as out:
        for prompt, reply in exchanges:
            out.write(f"## Prompt\n{prompt}\n\n## Reply\n{reply}\n\n")
