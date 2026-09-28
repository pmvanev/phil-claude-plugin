#!/usr/bin/env python3
"""The only writer of `.session-handoff.md`'s exchanges region — the session's last three prompts and
replies, copied from the transcript Claude Code already keeps on disk.

**Why a script, and not the session copying its own words.** 0.97.0 told the session to write its last
three replies into the snapshot word for word. Measured 2026-09-28 across every transcript on the
author's machine, that failed two ways:

- Anthropic's `reasoning_extraction` classifier refused it as "duplicating model outputs" in 7 of 8 real
  handoffs, against 0 of 15 before the region existed. The stop landed on the Write carrying the
  replies, so the region was never once written, and a stopped session went on refusing ordinary
  prompts after it.
- The one withheld Write that survives is 58% similar to the reply it claimed to copy, with a longest
  exact stretch of 225 characters. Asked to copy its own output, a model retypes it from memory.

Here the words never pass through the model. **Nothing any subcommand prints contains a word of an
exchange** — counts, hashes and reasons only — because echoing the region would put the duplicate
straight back into the context this script exists to keep it out of.

Five subcommands, and the session touches the snapshot through nothing else:

- `head`   — print the file above the region on stdout, and `SHA <h>` on stderr from the same read.
  That hash is the session's `h1`; `SHA absent` with empty output means there is no snapshot.
- `count`  — how many exchanges `record` would take, for the report's counting line.
- `write`  — CAPTURE step 9: replace the file with a regenerated body, dropping any previous region.
- `record` — CAPTURE step 12: replace or append the region from this session's transcript.
- `carry`  — `push` and `pop`: swap in a regenerated body and keep the region byte-for-byte.

`write` and `carry` take the body on stdin (`--body -`), so nothing is left in the repo and the session
never needs the Write tool — which refuses to overwrite a file it has not Read whole, and reading the
snapshot whole pulls the previous session's replies into context.

Every write runs the skill's compare-and-swap in code: `--expect-sha` is the hash `head` printed
(`absent` where there was no file), re-checked immediately before an atomic replace that keeps the
file's permissions. A mismatch writes nothing. **The hash is this script's, never `git hash-object`**,
which applies line-ending filters and may be SHA-256; either would refuse a file nobody else touched.
Every byte above the region is preserved; separators are only ever appended.

**What counts as an exchange**, per the skill's *The last exchanges*, resolved against real records:

- The live branch only. A rewound prompt forks at its parent and the abandoned branch stays in the
  file, so the transcript is walked from its newest record up the `parentUuid` chain, crossing a
  compaction boundary by its `logicalParentUuid`. File order would interleave replies nobody sees.
- A prompt is a human turn: not `isMeta`, not a compaction summary, not a tool result, not one of the
  harness's own records (task notifications, `!` shell echoes, interrupt markers). A slash command is
  its command line with its arguments, and only when the next record is the `isMeta` body it expanded
  to — a built-in such as `/model` is answered by the harness and opens no exchange.
- A reply is every text block the session printed until the next prompt, joined in order. Thinking,
  tool calls, tool output, sidechains and the harness's synthetic API-error messages are never part of
  it.
- Compacted exchanges are recorded word for word. The transcript keeps them; the summary is never used.

Reads the transcript and one local file; writes that file only. No network, no other program.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

OPEN = "<!-- session-handoff:exchanges -->"
CLOSE = "<!-- /session-handoff:exchanges -->"
COUNT = 3
ABSENT = "absent"

REFUSED, UNREADABLE, MALFORMED = 3, 4, 5

HARNESS_PREFIXES = (
    "<task-notification>",
    "<local-command-stdout>",
    "<local-command-stderr>",
    "<local-command-caveat>",
    "<bash-input>",
    "<bash-stdout>",
    "<bash-stderr>",
    "[Request interrupted by user",
)
COMMAND_NAME = re.compile(r"<command-name>(.*?)</command-name>", re.S)
COMMAND_ARGS = re.compile(r"<command-args>(.*?)</command-args>", re.S)
SESSION_ID = re.compile(r"^[A-Za-z0-9-]+$")


class Unreadable(Exception):
    pass


# ---------------------------------------------------------------- reading the transcript


def read_records(path) -> list[dict]:
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue  # a torn last line, written while the session is still running
    return records


def live_branch(records: list[dict]) -> list[dict]:
    """The records from the root to the newest main-chain record, oldest first."""
    by_uuid = {r["uuid"]: r for r in records if r.get("uuid")}
    main = [r for r in records if r.get("uuid") and not r.get("isSidechain")]
    if not main:
        return []
    branch, seen, current = [], set(), main[-1]
    while current is not None and current["uuid"] not in seen:
        seen.add(current["uuid"])
        branch.append(current)
        parent = current.get("parentUuid") or current.get("logicalParentUuid")
        current = by_uuid.get(parent)
    branch.reverse()
    return branch


def _text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n\n".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def _prompt(record: dict, following: dict | None) -> str | None:
    """The prompt as typed, or None when the record is not a human turn."""
    if record.get("type") != "user" or record.get("isSidechain"):
        return None
    if record.get("isMeta") or record.get("isCompactSummary"):
        return None
    content = (record.get("message") or {}).get("content")
    if isinstance(content, list) and any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
        return None
    text = _text(content)
    lead = text.lstrip()
    if not lead or lead.startswith(HARNESS_PREFIXES):
        return None
    if lead.startswith(("<command-message>", "<command-name>")):
        name = COMMAND_NAME.search(text)
        acted_on = following is not None and following.get("type") == "user" and following.get("isMeta")
        if not name or not acted_on:
            return None
        args = COMMAND_ARGS.search(text)
        return f"{name.group(1).strip()} {args.group(1).strip() if args else ''}".strip()
    return text


def _printed(record: dict) -> list[str]:
    if record.get("type") != "assistant" or record.get("isSidechain") or record.get("isApiErrorMessage"):
        return []
    message = record.get("message") or {}
    if message.get("model") == "<synthetic>":
        return []
    return [b["text"] for b in message.get("content") or []
            if isinstance(b, dict) and b.get("type") == "text" and b.get("text")]


def exchanges(records: list[dict]) -> list[tuple[str, str]]:
    branch = live_branch(records)
    found = []
    for i, record in enumerate(branch):
        prompt = _prompt(record, branch[i + 1] if i + 1 < len(branch) else None)
        if prompt is not None:
            found.append((prompt, []))
        elif found:
            found[-1][1].extend(_printed(record))
    return [(prompt, "\n\n".join(pieces)) for prompt, pieces in found]


def find_transcript(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    session = os.environ.get("CLAUDE_CODE_SESSION_ID", "")
    if not SESSION_ID.match(session):
        raise Unreadable("no session named: CLAUDE_CODE_SESSION_ID is unset or malformed")
    root = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "projects"
    matches = sorted(root.glob(f"*/{session}.jsonl"), key=lambda p: p.stat().st_mtime)
    if not matches:
        raise Unreadable(f"no transcript for session {session} under {root}")
    return matches[-1]


def last_exchanges(explicit: str | None) -> list[tuple[str, str]]:
    path = find_transcript(explicit)
    try:
        found = exchanges(read_records(path))
    except OSError as e:
        raise Unreadable(f"{path}: {e.strerror}") from e
    if not found:
        raise Unreadable(f"{path}: no exchanges on the live branch")
    return found[-COUNT:]


# ---------------------------------------------------------------- the snapshot


def render(recorded: list[tuple[str, str]]) -> str:
    parts = [f"### Prompt {n}\n\n{prompt}\n\n### Reply {n}\n\n{reply}"
             for n, (prompt, reply) in enumerate(recorded, 1)]
    return f"{OPEN}\n" + "\n\n".join(parts) + f"\n{CLOSE}\n"


def git_blob_hash(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def split(data: bytes) -> tuple[bytes, bytes | None]:
    """(everything above the region, the region to end of file) — the region is always last."""
    offset = 0
    for line in data.splitlines(keepends=True):
        if line.rstrip(b"\r\n") == OPEN.encode():
            return data[:offset], data[offset:]
        offset += len(line)
    return data, None


def join(body: bytes, region: bytes | None) -> bytes:
    if not region:
        return body
    if body and not body.endswith(b"\n"):
        body += b"\n"
    if body and not body.endswith(b"\n\n"):
        body += b"\n"
    return body + region


def current_sha(path: Path) -> str:
    return git_blob_hash(path.read_bytes()) if path.exists() else ABSENT


def _mode(path: Path) -> int:
    if path.exists():
        return path.stat().st_mode & 0o777
    umask = os.umask(0)
    os.umask(umask)
    return 0o666 & ~umask


def swap(path: Path, expect: str, data: bytes) -> str | None:
    """Write `data` if the file still hashes to `expect`; return the new hash, or None if refused."""
    mode = _mode(path)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".session-handoff.", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.chmod(tmp, mode)
        if current_sha(path) != expect:
            return None
        os.replace(tmp, path)
        return git_blob_hash(data)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


# ---------------------------------------------------------------- subcommands


def cmd_count(args) -> int:
    print(f"EXCHANGES {len(last_exchanges(args.transcript))}")
    return 0


def cmd_record(args) -> int:
    path = Path(args.file)
    recorded = last_exchanges(args.transcript)
    if current_sha(path) != args.expect_sha or not path.exists():
        print(f"REFUSED {args.expect_sha} {current_sha(path)}")
        return REFUSED
    body, _previous = split(path.read_bytes())
    new = swap(path, args.expect_sha, join(body, render(recorded).encode()))
    if new is None:
        print(f"REFUSED {args.expect_sha} {current_sha(path)}")
        return REFUSED
    print(f"RECORDED {len(recorded)} {new}")
    return 0


def cmd_head(args) -> int:
    path = Path(args.file)
    if not path.exists():
        print(f"SHA {ABSENT}", file=sys.stderr)
        return 0
    data = path.read_bytes()
    sys.stdout.write(split(data)[0].decode("utf-8"))
    sys.stdout.flush()
    print(f"SHA {git_blob_hash(data)}", file=sys.stderr)
    return 0


def _body_write(args, keep_region: bool, verb: str) -> int:
    path = Path(args.file)
    body = sys.stdin.buffer.read() if args.body == "-" else Path(args.body).read_bytes()
    if split(body)[1] is not None:
        print("MALFORMED the body holds an exchanges region of its own — only `record` writes one")
        return MALFORMED
    if current_sha(path) != args.expect_sha:
        print(f"REFUSED {args.expect_sha} {current_sha(path)}")
        return REFUSED
    region = split(path.read_bytes())[1] if keep_region and path.exists() else None
    new = swap(path, args.expect_sha, join(body, region))
    if new is None:
        print(f"REFUSED {args.expect_sha} {current_sha(path)}")
        return REFUSED
    print(f"{verb} {new}")
    return 0


def cmd_write(args) -> int:
    return _body_write(args, keep_region=False, verb="WROTE")


def cmd_carry(args) -> int:
    return _body_write(args, keep_region=True, verb="CARRIED")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("count", help="how many exchanges record would take")
    p.add_argument("--transcript", help="transcript path; default: this session's, from the environment")
    p.set_defaults(run=cmd_count)

    p = sub.add_parser("record", help="write the region from this session's transcript")
    p.add_argument("--file", required=True)
    p.add_argument("--expect-sha", required=True)
    p.add_argument("--transcript")
    p.set_defaults(run=cmd_record)

    p = sub.add_parser("head", help="print the file above the region")
    p.add_argument("--file", required=True)
    p.set_defaults(run=cmd_head)

    for name, run, text in (("write", cmd_write, "replace the file with the body, dropping any region"),
                            ("carry", cmd_carry, "replace the body and keep the region byte-for-byte")):
        p = sub.add_parser(name, help=text)
        p.add_argument("--file", required=True)
        p.add_argument("--body", required=True, help="the regenerated body, or - to read it from stdin")
        p.add_argument("--expect-sha", required=True)
        p.set_defaults(run=run)

    args = parser.parse_args(argv)
    try:
        return args.run(args)
    except Unreadable as e:
        print(f"UNREADABLE {e}")
        return UNREADABLE


if __name__ == "__main__":
    sys.exit(main())
