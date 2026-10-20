"""The refactor-loop allow-list — `hooks/refactor-loop/agent-allowlist.py`.

An agent file's `tools:` line picks whole tools, never commands or paths. A probe agent granted only
`Bash(echo:*)` wrote files through `touch`, a redirect, an `&&` chain and a `$( )` substitution in
bypass mode (2026-10-20). This hook is the other half of the boundary: keyed on the `agent_type` Claude
Code puts in every subagent's PreToolUse payload, it allows each narrowed loop role only its own paths
and commands, and refuses everything else (CWE-250, issue 48).

It stays silent for the main session and for every other agent type, except that no other subagent may
write the run ledger, whose `active-run:` arms G2 (CWE-807).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
HOOK = REPO / "hooks" / "refactor-loop" / "agent-allowlist.py"
LEDGER = ".refactor-loop-ledger.md"
WRITER = "phil:refactor-ledger-writer"


def decide(payload, cwd):
    """Returns (decision, reason); (None, None) when the hook allows by staying silent."""
    stdin = payload if isinstance(payload, str) else json.dumps(payload)
    proc = subprocess.run([sys.executable, str(HOOK)], input=stdin, cwd=cwd,
                          capture_output=True, text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    if not proc.stdout.strip():
        return None, None
    out = json.loads(proc.stdout)["hookSpecificOutput"]
    return out["permissionDecision"], out["permissionDecisionReason"]


def call(cwd, tool, tool_input, agent_type=WRITER):
    payload = {"tool_name": tool, "tool_input": tool_input, "cwd": str(cwd)}
    if agent_type is not None:
        payload["agent_type"] = agent_type
    return decide(payload, cwd)[0]


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / "work"
    root.mkdir()
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    return root.resolve()


# --------------------------------------------------------------------------- the ledger writer's grant


@pytest.mark.parametrize("tool", ["Write", "Read"])
def test_the_ledger_writer_may_write_and_read_the_ledger_at_a_repo_root(repo, tool):
    assert call(repo, tool, {"file_path": str(repo / LEDGER), "content": "x"}) is None


def test_the_ledger_writer_may_name_the_ledger_relative_to_its_cwd(repo):
    assert call(repo, "Write", {"file_path": LEDGER, "content": "x"}) is None


def test_the_ledger_writer_may_overwrite_an_existing_ledger(repo):
    (repo / LEDGER).write_text("active-run: true\n")
    assert call(repo, "Write", {"file_path": str(repo / LEDGER), "content": "x"}) is None


@pytest.mark.parametrize("path", [
    "README.md", "src/app.py", "tests/test_app.py", "../elsewhere.md", "/etc/hostname",
    "sub/.refactor-loop-ledger.md",
])
@pytest.mark.parametrize("tool", ["Write", "Read"])
def test_the_ledger_writer_is_refused_every_other_path(repo, tool, path):
    (repo / "sub").mkdir()
    assert call(repo, tool, {"file_path": path, "content": "x"}) == "deny"


def test_a_ledger_named_file_outside_any_repo_is_refused(tmp_path):
    plain = tmp_path / "plain"
    plain.mkdir()
    assert call(plain, "Write", {"file_path": str(plain / LEDGER), "content": "x"}) == "deny"


def test_a_ledger_that_is_a_symlink_is_refused(repo, tmp_path):
    target = tmp_path / "outside.md"
    target.write_text("")
    os.symlink(target, repo / LEDGER)
    assert call(repo, "Write", {"file_path": str(repo / LEDGER), "content": "x"}) == "deny"


def test_a_repo_reached_through_a_symlinked_directory_is_followed(repo, tmp_path):
    # Only a symlinked ledger can send the write elsewhere. A symlinked directory still ends at a repo
    # root, and refusing it would halt every run whose path crosses one, as macOS's /tmp does.
    os.symlink(repo, tmp_path / "alias")
    assert call(repo, "Write", {"file_path": str(tmp_path / "alias" / LEDGER), "content": "x"}) is None


@pytest.mark.parametrize("command", [
    "echo hi", "touch x", f"echo x > {LEDGER}", "echo a && touch b", "echo $(touch c)", "ls",
])
def test_the_ledger_writer_may_run_no_command(repo, command):
    assert call(repo, "Bash", {"command": command}) == "deny"


@pytest.mark.parametrize("tool", ["Edit", "NotebookEdit"])
def test_the_ledger_writer_may_not_edit_even_the_ledger(repo, tool):
    assert call(repo, tool, {"file_path": str(repo / LEDGER), "old_string": "a", "new_string": "b"}) == "deny"


def test_a_refusal_names_the_allow_list(repo):
    _, reason = decide({"tool_name": "Bash", "tool_input": {"command": "touch x"}, "cwd": str(repo),
                        "agent_type": WRITER}, repo)
    assert reason.startswith("refactor-loop allow-list:"), reason


# The type is matched on its last segment, so a copy of the agent in a project's `.claude/agents/`,
# which arrives without the plugin prefix, is restricted too. Restricting more agents is the safe side.
@pytest.mark.parametrize("agent_type", ["phil:refactor-ledger-writer", "refactor-ledger-writer"])
def test_the_grant_applies_with_or_without_the_plugin_prefix(repo, agent_type):
    assert call(repo, "Bash", {"command": "touch x"}, agent_type=agent_type) == "deny"


@pytest.mark.parametrize("tool_input", [None, "a string", [], {}, {"file_path": 7}, {"file_path": ""}])
def test_a_malformed_tool_input_from_a_narrowed_type_is_refused(repo, tool_input):
    assert call(repo, "Write", tool_input) == "deny"


# --------------------------------------------------------------------------- everyone else


@pytest.mark.parametrize("agent_type", [None, "general-purpose", "phil:refactor-proposer"])
@pytest.mark.parametrize("tool,tool_input", [
    ("Bash", {"command": "touch x && rm -rf build"}),
    ("Write", {"file_path": "src/app.py", "content": "x"}),
    ("Read", {"file_path": "/etc/hostname"}),
])
def test_the_hook_is_silent_for_every_other_caller(repo, agent_type, tool, tool_input):
    assert call(repo, tool, tool_input, agent_type=agent_type) is None


# The ledger's `active-run:` arms G2, so a subagent that rewrites it can switch the test-file guard off
# (CWE-807). Only the ledger writer, whose content the cage composes, may write it.
@pytest.mark.parametrize("tool", ["Write", "Edit", "NotebookEdit"])
@pytest.mark.parametrize("path", [LEDGER, "./" + LEDGER, ".Refactor-Loop-Ledger.md"])
def test_no_other_subagent_may_write_the_ledger(repo, tool, path):
    assert call(repo, tool, {"file_path": path, "content": "x"}, agent_type="general-purpose") == "deny"


def test_no_other_subagent_may_write_the_ledger_through_a_symlink(repo):
    os.symlink(repo / LEDGER, repo / "innocent.md")
    assert call(repo, "Write", {"file_path": "innocent.md", "content": "x"},
                agent_type="general-purpose") == "deny"


def test_the_main_session_may_write_the_ledger(repo):
    # The interactive skill path writes its ledger from the main session, which carries no agent type.
    assert call(repo, "Write", {"file_path": LEDGER, "content": "x"}, agent_type=None) is None


@pytest.mark.parametrize("stdin", ["", "not json", "[]", "7"])
def test_a_payload_that_is_not_an_object_is_let_through(repo, stdin):
    # Claude Code writes the payload, not the agent, so garbage here is no attack; refusing it would
    # stop every tool call in every session that installs the plugin.
    assert decide(stdin, repo) == (None, None)


# --------------------------------------------------------------------------- wiring


def test_the_hook_is_registered_on_every_tool_that_reads_writes_or_runs():
    hooks = json.loads((REPO / "hooks" / "hooks.json").read_text())["hooks"]["PreToolUse"]
    entry = next(h for h in hooks if any("agent-allowlist.py" in x["command"] for x in h["hooks"]))
    assert set(entry["matcher"].split("|")) == {"Bash", "Read", "Write", "Edit", "NotebookEdit"}


def test_the_ledger_writer_type_holds_only_read_and_write():
    text = (REPO / "agents" / "refactor-ledger-writer.md").read_text()
    assert "\ntools: Read, Write\n" in text
