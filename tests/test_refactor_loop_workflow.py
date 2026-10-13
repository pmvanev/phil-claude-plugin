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
