"""Tests for `scripts/session-exchanges.py` — the only writer of the snapshot's exchanges region.

Written BEFORE the script. The region shipped in 0.97.0 as prose: the session was told to copy its own
last three replies into `.session-handoff.md` word for word. That failed twice over, both measured
2026-09-28 across every transcript on the author's machine:

- **Anthropic's `reasoning_extraction` classifier stopped it.** 7 of 8 real 0.97.0 handoffs were
  refused as "duplicating model outputs", against 0 of 15 before the region existed. The stop landed on
  the Write whose content was ~80% the session's own earlier replies. The region was never once written.
- **The copy was not a copy.** The one withheld Write that survives is 58% similar to the reply it
  claimed to reproduce, and its longest exact stretch is 225 characters. A model asked to copy its own
  output retypes it from memory — the regeneration the skill forbids in the same paragraph.

So the words never pass through the model at all. The script reads the session's transcript, which
Claude Code already writes to disk, and places the region itself. It prints counts and hashes and
**never a word of any exchange** — the property `test_stdout_never_carries_an_exchange` pins, because a
script that echoed the region back would put the duplicate straight into the context it exists to keep
it out of.

The transcript shapes below are copied from real records, not guessed: the command-record spellings,
the `isMeta` body that follows a command the model acts on, the `local-command-stdout` that follows a
built-in, the `compact_boundary` whose `parentUuid` is null and whose `logicalParentUuid` is not. Forks
are real too — 18 of the 25 largest transcripts hold a rewound human turn, so file order interleaves
replies nobody sees any more, and only the parent chain names the live branch.
"""

import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "session-exchanges.py"

OPEN = "<!-- session-handoff:exchanges -->"
CLOSE = "<!-- /session-handoff:exchanges -->"

BODY = """<!-- session-handoff:v1 -->
captured: 2026-09-28T14:00Z
commit: 5f64d35
dirty: no
<!-- /session-handoff:v1 -->

## Why

- The words never pass through the model.

## Next

Ship the script.
"""


def load():
    """Import a module whose filename contains a hyphen."""
    spec = importlib.util.spec_from_file_location("session_exchanges", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


se = load()


def git_hash(path: Path) -> str:
    return subprocess.run(
        ["git", "hash-object", str(path)], capture_output=True, text=True, check=True
    ).stdout.strip()


class Transcript:
    """Builds a session transcript in Claude Code's JSONL shape, chained by `parentUuid`."""

    def __init__(self):
        self.records = []
        self.tip = None

    def _add(self, record, parent="tip"):
        record.setdefault("uuid", f"u{len(self.records):04d}")
        record["parentUuid"] = self.tip if parent == "tip" else parent
        record.setdefault("isSidechain", False)
        record.setdefault("sessionId", "s-test")
        record.setdefault("timestamp", f"2026-09-28T14:{len(self.records) % 60:02d}:00.000Z")
        self.records.append(record)
        self.tip = record["uuid"]
        return record["uuid"]

    def human(self, text, parent="tip"):
        return self._add({"type": "user", "message": {"role": "user", "content": text}}, parent)

    def command(self, name, args=None, body="Load the skill and follow it."):
        text = f"<command-message>{name[1:]}</command-message>\n<command-name>{name}</command-name>"
        if args is not None:
            text += f"\n<command-args>{args}</command-args>"
        self.human(text)
        self._add({"type": "user", "isMeta": True,
                   "message": {"role": "user", "content": [{"type": "text", "text": body}]}})

    def builtin(self, name, stdout="done"):
        self.human(f"<command-name>{name}</command-name>\n            "
                   f"<command-message>{name[1:]}</command-message>\n            <command-args></command-args>")
        self.human(f"<local-command-stdout>{stdout}</local-command-stdout>")

    def say(self, text, **extra):
        return self._add({"type": "assistant", **extra, "message": {
            "role": "assistant", "model": "claude-opus-5-5",
            "content": [{"type": "text", "text": text}]}})

    def think(self, text):
        self._add({"type": "assistant", "message": {
            "role": "assistant", "content": [{"type": "thinking", "thinking": text, "signature": "sig"}]}})

    def tool(self, command="ls", output="a.txt"):
        self._add({"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "toolu_1", "name": "Bash", "input": {"command": command}}]}})
        self._add({"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "toolu_1", "content": output}]}})

    def meta(self, text):
        self._add({"type": "user", "isMeta": True, "message": {"role": "user", "content": text}})

    def api_error(self, text):
        self._add({"type": "assistant", "isApiErrorMessage": True, "message": {
            "role": "assistant", "model": "<synthetic>", "content": [{"type": "text", "text": text}]}})

    def compact(self, summary):
        logical = self.tip
        self._add({"type": "system", "subtype": "compact_boundary", "logicalParentUuid": logical,
                   "content": "Conversation compacted"}, parent=None)
        self._add({"type": "user", "isCompactSummary": True,
                   "message": {"role": "user", "content": summary}})

    def sidechain(self, text):
        self._add({"type": "assistant", "isSidechain": True, "message": {
            "role": "assistant", "content": [{"type": "text", "text": text}]}})

    def write(self, path: Path) -> Path:
        with path.open("w") as f:
            for r in self.records:
                f.write(json.dumps(r) + "\n")
            # Records carrying no uuid are interleaved in real files and belong to no chain.
            f.write(json.dumps({"type": "last-prompt", "sessionId": "s-test"}) + "\n")
        return path


def five_exchanges():
    t = Transcript()
    for n in range(1, 5):
        t.human(f"prompt {n}")
        t.say(f"reply {n}")
    t.command("/phil:handoff", '"pausing before the migration"')
    t.say("CAPTURE. The report.")
    return t


def run(*args, env=None):
    return subprocess.run(["python3", str(SCRIPT), *args], capture_output=True, text=True, env=env)


# ---------------------------------------------------------------- what counts as an exchange


def test_the_last_three_exchanges_are_taken_oldest_first_with_the_handoff_last(tmp_path):
    ex = se.exchanges(se.read_records(five_exchanges().write(tmp_path / "t.jsonl")))

    assert ex[-3:] == [
        ("prompt 3", "reply 3"),
        ("prompt 4", "reply 4"),
        ('/phil:handoff "pausing before the migration"', "CAPTURE. The report."),
    ]


def test_a_command_prompt_is_the_line_as_typed_never_its_expanded_body(tmp_path):
    t = Transcript()
    t.command("/phil:resume", body="EXPANDED BODY")
    t.say("RESUME-CURRENT")
    t.command("/nw-deliver", "envelope-materials-library", body="EXPANDED BODY")
    t.say("delivering")

    ex = se.exchanges(se.read_records(t.write(tmp_path / "t.jsonl")))

    assert [p for p, _ in ex] == ["/phil:resume", "/nw-deliver envelope-materials-library"]
    assert "EXPANDED BODY" not in json.dumps(ex)


def test_a_builtin_command_opens_no_exchange(tmp_path):
    """`/model`, `/clear`, `/reload-plugins` are addressed to the harness, which answers them; the
    session prints nothing. Counting one would spend a place of three on an empty reply."""
    t = Transcript()
    t.human("prompt 1")
    t.say("reply 1")
    t.builtin("/reload-plugins", "Reloaded 3 plugins")
    t.human("prompt 2")
    t.say("reply 2")

    ex = se.exchanges(se.read_records(t.write(tmp_path / "t.jsonl")))

    assert ex == [("prompt 1", "reply 1"), ("prompt 2", "reply 2")]


def test_a_reply_is_the_printed_text_only_joined_in_order(tmp_path):
    t = Transcript()
    t.human("check the tree")
    t.think("PRIVATE REASONING")
    t.say("Checking.")
    t.tool(command="git status", output="TOOL OUTPUT")
    t.say("Clean.")

    ex = se.exchanges(se.read_records(t.write(tmp_path / "t.jsonl")))

    assert ex == [("check the tree", "Checking.\n\nClean.")]
    dumped = json.dumps(ex)
    assert "PRIVATE REASONING" not in dumped
    assert "TOOL OUTPUT" not in dumped and "git status" not in dumped


@pytest.mark.parametrize("harness_record", [
    lambda t: t.human("<task-notification>\n<task-id>a1</task-id>\n</task-notification>"),
    lambda t: t.meta("Your response above was stopped by a safety classifier — this is not a tool or API error."),
    lambda t: t.human("<bash-input>aws sso login</bash-input>"),
    lambda t: t.human("<bash-stdout>Attempting to open</bash-stdout><bash-stderr></bash-stderr>"),
    lambda t: t.human([{"type": "text", "text": "[Request interrupted by user]"}]),
    lambda t: t.api_error("API Error: Opus 5.5's safeguards flagged this message"),
    lambda t: t.sidechain("a subagent's reply"),
])
def test_records_the_harness_wrote_are_neither_prompts_nor_replies(tmp_path, harness_record):
    t = Transcript()
    t.human("prompt 1")
    t.say("reply 1")
    harness_record(t)
    t.say("reply 1, continued")

    ex = se.exchanges(se.read_records(t.write(tmp_path / "t.jsonl")))

    assert ex == [("prompt 1", "reply 1\n\nreply 1, continued")]


def test_a_prompt_keeps_what_was_pasted_into_it_and_drops_attached_images(tmp_path):
    pasted = "why does this fail?\n\nTraceback (most recent call last):\n  File \"x.py\", line 3\n"
    t = Transcript()
    t.human([{"type": "image", "source": {"type": "base64", "data": "AAAA"}},
             {"type": "text", "text": pasted}])
    t.say("Line 3.")

    ex = se.exchanges(se.read_records(t.write(tmp_path / "t.jsonl")))

    assert ex == [(pasted, "Line 3.")]


def test_a_rewound_branch_is_not_recorded(tmp_path):
    """Double-Esc edits a prompt by forking at its parent; the abandoned branch stays in the file."""
    t = Transcript()
    t.human("prompt 1")
    fork_point = t.say("reply 1")
    t.human("ABANDONED prompt")
    t.say("ABANDONED reply")
    t.human("prompt 2", parent=fork_point)
    t.say("reply 2")

    ex = se.exchanges(se.read_records(t.write(tmp_path / "t.jsonl")))

    assert ex == [("prompt 1", "reply 1"), ("prompt 2", "reply 2")]


def test_compacted_exchanges_are_recorded_from_the_transcript_and_the_summary_never(tmp_path):
    """0.97.0 counted compacted exchanges and recorded none of their words, because a model holding
    only the summary could not honestly reproduce them. The transcript still holds every word, so the
    reason is gone — but the summary is still never what was said."""
    t = Transcript()
    t.human("prompt 1")
    t.say("reply 1")
    t.compact("SUMMARY: the user asked about prompt 1")
    t.human("prompt 2")
    t.say("reply 2")

    ex = se.exchanges(se.read_records(t.write(tmp_path / "t.jsonl")))

    assert ex == [("prompt 1", "reply 1"), ("prompt 2", "reply 2")]
    assert "SUMMARY" not in json.dumps(ex)


# ---------------------------------------------------------------- rendering and placement


def test_the_region_numbers_exchanges_and_keeps_a_replys_own_headings_inside_the_markers():
    region = se.render([("p1", "## A heading of its own\n\ntext"), ("p2", "r2")])

    assert region == (
        f"{OPEN}\n### Prompt 1\n\np1\n\n### Reply 1\n\n## A heading of its own\n\ntext\n\n"
        f"### Prompt 2\n\np2\n\n### Reply 2\n\nr2\n{CLOSE}\n"
    )


def test_hash_is_git_hash_object(tmp_path):
    p = tmp_path / "f.md"
    p.write_text(BODY)
    assert se.git_blob_hash(p.read_bytes()) == git_hash(p)


def test_record_appends_the_region_last_and_leaves_every_byte_above_it(tmp_path):
    snap = tmp_path / ".session-handoff.md"
    snap.write_text(BODY)
    transcript = five_exchanges().write(tmp_path / "t.jsonl")

    result = run("record", "--file", str(snap), "--expect-sha", git_hash(snap), "--transcript", str(transcript))

    assert result.returncode == 0, result.stderr
    text = snap.read_text()
    assert text.startswith(BODY)
    assert text[len(BODY):].startswith("\n" + OPEN + "\n")
    assert text.endswith(CLOSE + "\n")
    assert "### Prompt 3" in text and "### Prompt 4" not in text
    assert result.stdout.split() == ["RECORDED", "3", git_hash(snap)]


def test_record_replaces_a_previous_sessions_region_rather_than_carrying_it(tmp_path):
    snap = tmp_path / ".session-handoff.md"
    snap.write_text(BODY + "\n" + se.render([("OLD prompt", "OLD reply")]))
    transcript = five_exchanges().write(tmp_path / "t.jsonl")

    run("record", "--file", str(snap), "--expect-sha", git_hash(snap), "--transcript", str(transcript))

    text = snap.read_text()
    assert "OLD" not in text
    assert text.count(OPEN) == 1 and text.startswith(BODY)


def test_record_refuses_when_the_file_changed_beneath_it(tmp_path):
    snap = tmp_path / ".session-handoff.md"
    snap.write_text(BODY)
    stale = git_hash(snap)
    snap.write_text(BODY + "\nanother writer\n")
    before = snap.read_bytes()

    result = run("record", "--file", str(snap), "--expect-sha", stale,
                 "--transcript", str(five_exchanges().write(tmp_path / "t.jsonl")))

    assert result.returncode == 3
    assert snap.read_bytes() == before
    assert result.stdout.split() == ["REFUSED", stale, git_hash(snap)]


def test_record_writes_nothing_when_the_transcript_cannot_be_read(tmp_path):
    snap = tmp_path / ".session-handoff.md"
    snap.write_text(BODY)

    result = run("record", "--file", str(snap), "--expect-sha", git_hash(snap),
                 "--transcript", str(tmp_path / "missing.jsonl"))

    assert result.returncode == 4
    assert snap.read_text() == BODY
    assert result.stdout.startswith("UNREADABLE ")


def test_record_finds_this_sessions_transcript_from_the_environment(tmp_path):
    config = tmp_path / "config"
    (config / "projects" / "-some-repo").mkdir(parents=True)
    five_exchanges().write(config / "projects" / "-some-repo" / "abc-123.jsonl")
    snap = tmp_path / ".session-handoff.md"
    snap.write_text(BODY)
    env = {"PATH": "/usr/bin:/bin", "CLAUDE_CONFIG_DIR": str(config), "CLAUDE_CODE_SESSION_ID": "abc-123"}

    result = run("record", "--file", str(snap), "--expect-sha", git_hash(snap), env=env)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "CAPTURE. The report." in snap.read_text()


def test_record_with_no_session_named_writes_nothing(tmp_path):
    snap = tmp_path / ".session-handoff.md"
    snap.write_text(BODY)

    result = run("record", "--file", str(snap), "--expect-sha", git_hash(snap),
                 env={"PATH": "/usr/bin:/bin", "CLAUDE_CONFIG_DIR": str(tmp_path)})

    assert result.returncode == 4
    assert snap.read_text() == BODY


def test_count_reports_how_many_exchanges_record_would_take(tmp_path):
    t = Transcript()
    t.human("only prompt")
    t.say("only reply")

    result = run("count", "--transcript", str(t.write(tmp_path / "t.jsonl")))

    assert result.returncode == 0
    assert result.stdout.split() == ["EXCHANGES", "1"]


def test_stdout_never_carries_an_exchange(tmp_path):
    """The whole point. Echoing the region would put the duplicate back into the session's context."""
    snap = tmp_path / ".session-handoff.md"
    snap.write_text(BODY)
    transcript = five_exchanges().write(tmp_path / "t.jsonl")

    outputs = [
        run("count", "--transcript", str(transcript)),
        run("record", "--file", str(snap), "--expect-sha", git_hash(snap), "--transcript", str(transcript)),
        run("head", "--file", str(snap)),
    ]

    for out in outputs:
        for word in ("prompt 3", "reply 3", "prompt 4", "reply 4", "CAPTURE. The report.", "pausing"):
            assert word not in out.stdout + out.stderr


# ---------------------------------------------------------------- push and pop: head and carry


def test_head_prints_the_file_above_the_region_and_none_of_it(tmp_path):
    snap = tmp_path / ".session-handoff.md"
    snap.write_text(BODY + "\n" + se.render([("a prompt", "a reply")]))

    result = run("head", "--file", str(snap))

    assert result.returncode == 0
    assert result.stdout == BODY + "\n"


def test_head_prints_the_whole_file_when_there_is_no_region(tmp_path):
    snap = tmp_path / ".session-handoff.md"
    snap.write_text(BODY)

    assert run("head", "--file", str(snap)).stdout == BODY


def test_head_names_the_hash_of_the_bytes_it_read_so_no_second_read_can_race_it(tmp_path):
    """The session's `h1` comes from here, never from `git hash-object`, which applies line-ending
    filters and may be SHA-256 — either would make the script refuse a file nobody else touched."""
    snap = tmp_path / ".session-handoff.md"
    snap.write_bytes(BODY.replace("\n", "\r\n").encode())

    result = run("head", "--file", str(snap))

    assert result.stderr.split() == ["SHA", se.git_blob_hash(snap.read_bytes())]


def test_head_on_a_missing_file_prints_nothing_and_says_absent(tmp_path):
    result = run("head", "--file", str(tmp_path / ".session-handoff.md"))

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr.split() == ["SHA", "absent"]


# ---------------------------------------------------------------- CAPTURE step 9: write


def test_write_replaces_the_file_with_the_body_and_drops_any_region(tmp_path):
    """CAPTURE's first write. The previous session's region goes; this session's is `record`'s."""
    snap = tmp_path / ".session-handoff.md"
    snap.write_text("old body\n\n" + se.render([("OLD prompt", "OLD reply")]))

    result = subprocess.run(
        ["python3", str(SCRIPT), "write", "--file", str(snap), "--body", "-", "--expect-sha", git_hash(snap)],
        input=BODY, capture_output=True, text=True)

    assert result.returncode == 0, result.stdout + result.stderr
    assert snap.read_text() == BODY
    assert result.stdout.split() == ["WROTE", se.git_blob_hash(BODY.encode())]


def test_write_creates_the_file_when_it_is_still_absent(tmp_path):
    snap = tmp_path / ".session-handoff.md"

    result = subprocess.run(
        ["python3", str(SCRIPT), "write", "--file", str(snap), "--body", "-", "--expect-sha", "absent"],
        input=BODY, capture_output=True, text=True)

    assert result.returncode == 0
    assert snap.read_text() == BODY


def test_write_refuses_when_the_file_changed_beneath_it(tmp_path):
    snap = tmp_path / ".session-handoff.md"
    snap.write_text(BODY)
    stale = git_hash(snap)
    snap.write_text(BODY + "\nanother writer\n")
    before = snap.read_bytes()

    result = subprocess.run(
        ["python3", str(SCRIPT), "write", "--file", str(snap), "--body", "-", "--expect-sha", stale],
        input=BODY, capture_output=True, text=True)

    assert result.returncode == 3
    assert snap.read_bytes() == before


def test_write_refuses_a_body_that_holds_a_region_of_its_own(tmp_path):
    snap = tmp_path / ".session-handoff.md"

    result = subprocess.run(
        ["python3", str(SCRIPT), "write", "--file", str(snap), "--body", "-", "--expect-sha", "absent"],
        input=BODY + "\n" + se.render([("typed", "typed")]), capture_output=True, text=True)

    assert result.returncode == 5
    assert not snap.exists()


def test_carry_replaces_the_body_and_keeps_the_region_byte_for_byte(tmp_path):
    region = se.render([("a prompt", "a reply ```with fences```\n\n## and a heading")])
    snap = tmp_path / ".session-handoff.md"
    snap.write_text(BODY + "\n" + region)
    new_body = tmp_path / "body.md"
    new_body.write_text(BODY + "\n## Stack\n\n1. A frame · pushed · open since 2026-09-28T14:00Z · crossed 0\n")

    result = run("carry", "--file", str(snap), "--body", str(new_body), "--expect-sha", git_hash(snap))

    assert result.returncode == 0, result.stdout + result.stderr
    assert snap.read_text() == new_body.read_text() + "\n" + region
    assert result.stdout.split() == ["CARRIED", git_hash(snap)]


def test_carry_reads_the_body_from_stdin_so_no_scratch_file_is_left_in_the_repo(tmp_path):
    region = se.render([("a prompt", "a reply")])
    snap = tmp_path / ".session-handoff.md"
    snap.write_text(BODY + "\n" + region)
    new_body = BODY + "\n## Stack\n\n1. A frame · pushed · open since 2026-09-28T14:00Z · crossed 0\n"

    result = subprocess.run(
        ["python3", str(SCRIPT), "carry", "--file", str(snap), "--body", "-", "--expect-sha", git_hash(snap)],
        input=new_body, capture_output=True, text=True)

    assert result.returncode == 0, result.stdout + result.stderr
    assert snap.read_text() == new_body + "\n" + region


def test_carry_refuses_when_the_file_changed_beneath_it(tmp_path):
    snap = tmp_path / ".session-handoff.md"
    snap.write_text(BODY)
    stale = git_hash(snap)
    snap.write_text(BODY + "\nanother writer\n")
    before = snap.read_bytes()
    new_body = tmp_path / "body.md"
    new_body.write_text(BODY)

    result = run("carry", "--file", str(snap), "--body", str(new_body), "--expect-sha", stale)

    assert result.returncode == 3
    assert snap.read_bytes() == before


def test_carry_creates_the_file_when_it_is_still_absent(tmp_path):
    snap = tmp_path / ".session-handoff.md"
    new_body = tmp_path / "body.md"
    new_body.write_text(BODY)

    result = run("carry", "--file", str(snap), "--body", str(new_body), "--expect-sha", "absent")

    assert result.returncode == 0
    assert snap.read_text() == BODY


def test_carry_refuses_a_file_that_appeared_after_it_was_found_absent(tmp_path):
    snap = tmp_path / ".session-handoff.md"
    snap.write_text("another writer's snapshot\n")
    new_body = tmp_path / "body.md"
    new_body.write_text(BODY)

    result = run("carry", "--file", str(snap), "--body", str(new_body), "--expect-sha", "absent")

    assert result.returncode == 3
    assert snap.read_text() == "another writer's snapshot\n"


def test_carry_refuses_a_body_that_holds_a_region_of_its_own(tmp_path):
    """A body carrying the opening marker means the model wrote exchanges itself — the defect."""
    snap = tmp_path / ".session-handoff.md"
    snap.write_text(BODY)
    new_body = tmp_path / "body.md"
    new_body.write_text(BODY + "\n" + se.render([("typed by the model", "typed by the model")]))

    result = run("carry", "--file", str(snap), "--body", str(new_body), "--expect-sha", git_hash(snap))

    assert result.returncode == 5
    assert snap.read_text() == BODY


def test_a_rewritten_snapshot_keeps_its_permissions(tmp_path):
    """`mkstemp` creates 0600, and `os.replace` would carry that onto the snapshot."""
    snap = tmp_path / ".session-handoff.md"
    snap.write_text(BODY)
    snap.chmod(0o644)

    run("record", "--file", str(snap), "--expect-sha", git_hash(snap),
        "--transcript", str(five_exchanges().write(tmp_path / "t.jsonl")))

    assert snap.stat().st_mode & 0o777 == 0o644
