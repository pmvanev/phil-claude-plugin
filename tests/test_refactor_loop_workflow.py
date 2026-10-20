"""`workflows/refactor-loop.js`: its configuration and its final status, driven as pure functions under
Node, and the command that launches it.

Found 2026-10-13:
- `RULES` was the single-quoted literal '${CLAUDE_PLUGIN_ROOT}/rules'. Nothing substitutes inside a
  workflow script, so every proposer and critic prompt named a path no agent could open. The command,
  whose body is substituted, now passes `plugin_root`.
- `max_fix_attempts` was honoured only as a JSON number, so "3" silently became 2, and `theta: 0`
  silently became 0.6. A value outside its range now takes the default instead of reaching the loop.
- A proposer that answered `no_actionable` on the last allowed iteration reported `HALT-INCOMPLETE`,
  a proposer agent that failed outright reported `DONE`, and a failed fix agent was recorded as a
  judgement of infeasibility.
- The command passed `scriptPath: workflows/refactor-loop.js`, which resolves against the user's
  repository, launched a run that reverts with `git checkout -- <files>` on a dirty tree, and asked the
  user to confirm a hook that never fires on this path.
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from js_source import js_function

REPO = Path(__file__).resolve().parent.parent
WORKFLOW = REPO / "workflows" / "refactor-loop.js"
COMMAND = REPO / "commands" / "refactor-loop.md"


def _js_function(name):
    return js_function(WORKFLOW, name)


node = shutil.which("node")


def _call(name, *args):
    script = _js_function(name) + f"\nconsole.log(JSON.stringify({name}(...{json.dumps(list(args))})))"
    out = subprocess.run([node, "-e", script], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


@pytest.mark.skipif(not node, reason="node is not installed")
class TestConfig:
    BASE = {"repo": "/r", "test_cmd": "pytest", "plugin_root": "/plug"}

    def test_rules_come_from_the_plugin_root_argument(self):
        assert _call("readConfig", self.BASE)["RULES"] == "/plug/rules"

    @pytest.mark.parametrize("missing", ["repo", "test_cmd", "plugin_root"])
    def test_each_required_argument_is_reported_missing(self, missing):
        args = {k: v for k, v in self.BASE.items() if k != missing}
        assert missing in _call("readConfig", args)["missing"]

    def test_a_string_argument_is_parsed(self):
        assert _call("readConfig", json.dumps(self.BASE))["missing"] == []

    @pytest.mark.parametrize("given, expected", [(3, 3), ("3", 3), (0, 0), ("0", 0), ("x", 2), (None, 2),
                                                 ("-1", 2), (-1, 2), ("1.5", 2)])
    def test_max_fix_attempts_reads_a_numeric_string_and_refuses_nonsense(self, given, expected):
        assert _call("readConfig", {**self.BASE, "max_fix_attempts": given})["MAX_FIX"] == expected

    @pytest.mark.parametrize("given, expected", [(5, 5), ("5", 5), (None, 10), ("x", 10), (0, 10),
                                                 ("2.5", 10), (-3, 10)])
    def test_max_iterations_reads_a_numeric_string(self, given, expected):
        assert _call("readConfig", {**self.BASE, "max_iterations": given})["MAX_ITER"] == expected

    @pytest.mark.parametrize("given, expected", [(0, 0), ("0.7", 0.7), (2, 0.6), (-0.1, 0.6)])
    def test_theta_is_a_probability(self, given, expected):
        assert _call("readConfig", {**self.BASE, "theta": given})["THETA"] == expected

    def test_no_literal_plugin_root_outside_a_comment(self):
        code = [l for l in WORKFLOW.read_text().splitlines() if not l.lstrip().startswith("//")]
        assert not [l for l in code if "${CLAUDE_PLUGIN_ROOT}" in l]


@pytest.mark.skipif(not node, reason="node is not installed")
class TestFinalStatus:
    def test_convergence_on_the_last_iteration_is_done(self):
        assert _call("finalStatus", "converged", 3, 3) == {"status": "DONE", "reason": None}

    def test_running_out_of_iterations_is_incomplete_with_a_reason(self):
        assert _call("finalStatus", None, 3, 3) == {"status": "HALT-INCOMPLETE",
                                                    "reason": "max-iterations"}

    def test_a_failed_proposer_is_a_halt_not_done(self):
        assert _call("finalStatus", "proposer-failed", 1, 10) == {"status": "HALT",
                                                                  "reason": "proposer-failed"}


@pytest.mark.skipif(not node, reason="node is not installed")
class TestTestPathLockbox:
    """The primary test-file guard under the Workflow: `git apply` bypasses the G2 hook.

    A diff names its paths in more lines than `---`/`+++`: a pure rename or copy carries only
    `rename to` or `copy to`, and a binary patch only `diff --git`. Wound: those slipped past, and so
    did `Tests/` on a case-insensitive filesystem (CWE-180, issue 48).
    """

    @pytest.mark.parametrize("diff", [
        "--- a/tests/test_a.py\n+++ b/tests/test_a.py\n@@ -1 +1 @@\n-x\n+y\n",
        "--- a/Tests/helpers.py\n+++ b/Tests/helpers.py\n",
        "--- a/src/CONFTEST.PY\n+++ b/src/CONFTEST.PY\n",
        "diff --git a/src/a.py b/tests/test_a.py\nsimilarity index 100%\n"
        "rename from src/a.py\nrename to tests/test_a.py\n",
        "diff --git a/src/a.py b/test_a.py\nsimilarity index 100%\n"
        "rename from src/a.py\nrename to test_a.py\n",
        "diff --git a/src/a.py b/spec/a_spec.rb\nsimilarity index 100%\n"
        "copy from src/a.py\ncopy to spec/a_spec.rb\n",
        "diff --git a/tests/data.bin b/tests/data.bin\nGIT binary patch\nliteral 3\n",
    ], ids=["edit", "case-dir", "case-leaf", "rename", "rename-top-level", "copy", "binary"])
    def test_a_diff_that_reaches_a_test_path_is_refused(self, diff):
        assert _call("touchesTestPath", diff) is True

    def test_a_diff_of_production_code_passes(self):
        assert _call("touchesTestPath", "diff --git a/src/a.py b/src/a.py\n"
                                        "--- a/src/a.py\n+++ b/src/a.py\n+contest = 1\n") is False


@pytest.mark.skipif(not node, reason="node is not installed")
class TestLedgerLockbox:
    """The ledger's `active-run: true` arms the G2 hook, so a diff that rewrites, renames or deletes
    the ledger disarms it (CWE-807, issue 48). The cage writes the ledger itself; a diff never may."""

    @pytest.mark.parametrize("diff", [
        "--- a/.refactor-loop-ledger.md\n+++ b/.refactor-loop-ledger.md\n-active-run: true\n",
        "--- a/.refactor-loop-ledger.md\n+++ /dev/null\n",
        "diff --git a/.refactor-loop-ledger.md b/old.md\nsimilarity index 100%\n"
        "rename from .refactor-loop-ledger.md\nrename to old.md\n",
        "--- a/.Refactor-Loop-Ledger.MD\n+++ b/.Refactor-Loop-Ledger.MD\n",
    ], ids=["edit", "delete", "rename", "case"])
    def test_a_diff_that_reaches_the_ledger_is_refused(self, diff):
        assert _call("touchesLedger", diff) is True

    def test_a_diff_of_production_code_passes(self):
        assert _call("touchesLedger", "--- a/src/ledger.md\n+++ b/src/ledger.md\n") is False

    def test_the_cage_refuses_a_ledger_diff_before_applying_it(self):
        src = WORKFLOW.read_text()
        assert src.index("touchesLedger(candidate.diff") < src.index("applyPrompt(candidate)")


# The read-only roles start as agent types whose grant is Read, Grep and Glob, so "never touch disk"
# is a limit on the tools rather than a line in the prompt (CWE-250, issue 48). A two-agent workflow
# run on 2026-10-20 confirmed that `agentType` enforces the agent file's `tools:` inside a workflow:
# both types listed only Read, Grep and Glob, and neither could write or run a command.
READ_ONLY_CALLS = {
    "proposerPrompt(": "phil:refactor-proposer",
    "fixPrompt(": "phil:refactor-proposer",
    "criticPrompt(": "phil:refactor-critic-correctness",
}


@pytest.mark.parametrize("call,agent_type", READ_ONLY_CALLS.items())
def test_a_read_only_role_starts_as_its_read_only_agent_type(call, agent_type):
    lines = [l for l in WORKFLOW.read_text().splitlines() if "await agent(" in l and call in l]
    assert lines, f"no agent call builds {call}"
    for line in lines:
        assert f"agentType: '{agent_type}'" in line, line


@pytest.mark.parametrize("agent_type", sorted(set(READ_ONLY_CALLS.values())))
def test_the_read_only_agent_types_grant_only_read_search_and_list(agent_type):
    text = (REPO / "agents" / f"{agent_type.split(':', 1)[1]}.md").read_text()
    assert re.search(r"^tools: Read, Grep, Glob$", text, re.M), agent_type


def test_the_loop_wires_each_stop_to_its_cause():
    """The pure function is only right if the loop sets `stop` from the right branch."""
    src = WORKFLOW.read_text()
    assert re.search(r"if \(!p\) \{ stop = 'proposer-failed'", src)
    assert re.search(r"if \(p\.no_actionable\) \{ stop = 'converged'", src)
    assert "...(reason ? { reason } : {})" in src
    assert "The fix agent failed; nobody judged this refactor infeasible." in src


@pytest.mark.skipif(not node, reason="node is not installed")
def test_the_whole_workflow_parses(tmp_path):
    """The runtime wraps the script in an async function, so a top-level `return` is legal there."""
    body = WORKFLOW.read_text().replace("export const meta", "const meta", 1)
    wrapped = tmp_path / "wf.js"
    wrapped.write_text("(async () => {\n" + body + "\n})\n")
    subprocess.run([node, "--check", str(wrapped)], check=True, capture_output=True)


def _body():
    return " ".join(COMMAND.read_text().split("---", 2)[2].split())


def test_the_command_names_the_workflow_from_the_plugin_root():
    assert "scriptPath: ${CLAUDE_PLUGIN_ROOT}/workflows/refactor-loop.js" in _body()
    assert re.search(r'plugin_root: "\$\{CLAUDE_PLUGIN_ROOT\}"', COMMAND.read_text())


def test_the_command_refuses_a_dirty_tree():
    body = _body()
    assert "git -C <repo> status --porcelain -- . ':!.refactor-loop-ledger.md'" in body
    assert "commit or stash (`git stash -u`)" in body


def test_the_command_no_longer_asks_for_a_hook_that_never_fires():
    body = _body()
    assert "confirm the test-file lockbox hook" not in body
    assert "the hook does not fire on this path" in body


def test_the_command_relays_every_halt_with_its_reason():
    body = _body()
    for status in ("DONE", "HALT-INCOMPLETE", "HALT-CONFIG", "HALT"):
        assert f"`{status}`" in body
    assert "relay its `reason`" in body
    assert "proven infeasible" not in body
