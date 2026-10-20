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


@pytest.mark.skipif(not node, reason="node is not installed")
class TestPatchFileLockbox:
    """The applier writes each diff to one patch file that `git apply` and `git apply -R` name, so a diff
    that rewrites the patch file would change what the next revert reverses."""

    @pytest.mark.parametrize("diff", [
        "--- a/.refactor-loop-patch.diff\n+++ b/.refactor-loop-patch.diff\n",
        "diff --git a/x b/.refactor-loop-patch.diff\nrename from x\nrename to .refactor-loop-patch.diff\n",
        "--- a/.Refactor-Loop-Patch.DIFF\n+++ b/.Refactor-Loop-Patch.DIFF\n",
    ], ids=["edit", "rename", "case"])
    def test_a_diff_that_reaches_the_patch_file_is_refused(self, diff):
        assert _call("touchesPatchFile", diff) is True

    def test_a_diff_of_production_code_passes(self):
        assert _call("touchesPatchFile", "--- a/src/patch.diff\n+++ b/src/patch.diff\n") is False

    def test_the_cage_refuses_a_patch_file_diff_before_applying_it(self):
        src = WORKFLOW.read_text()
        assert src.index("touchesPatchFile(candidate.diff") < src.index("applyPrompt(candidate)")


# The proposer's diff arrives with an extra empty line at its end, which git reads as a context line the
# file lacks: every apply in the 2026-10-20 slice-03 run failed on it. The narrowed applier copies the
# diff byte for byte, so the cage hands it a diff that ends in exactly one newline.
@pytest.mark.skipif(not node, reason="node is not installed")
@pytest.mark.parametrize("given,expected", [
    ("--- a/x\n+++ b/x\n@@ -1 +1 @@\n-a\n+b\n\n", "--- a/x\n+++ b/x\n@@ -1 +1 @@\n-a\n+b\n"),
    ("--- a/x\n+++ b/x\n@@ -1 +1 @@\n-a\n+b", "--- a/x\n+++ b/x\n@@ -1 +1 @@\n-a\n+b\n"),
    ("@@ -1,2 +1,2 @@\n-a\n+b\n \n\n\n", "@@ -1,2 +1,2 @@\n-a\n+b\n \n"),
], ids=["extra-empty-line", "no-final-newline", "blank-context-line-kept"])
def test_the_patch_text_ends_in_exactly_one_newline(given, expected):
    assert _call("patchText", given) == expected


def test_the_applier_is_handed_the_normalised_patch():
    assert "patchText(p.diff)" in _js_function("applyPrompt")


@pytest.mark.skipif(not node, reason="node is not installed")
class TestCommitMessageLockbox:
    """The committer commits from one message file, so a diff that rewrites it rewrites the next commit."""

    @pytest.mark.parametrize("diff", [
        "--- /dev/null\n+++ b/.refactor-loop-commit-msg\n",
        "--- a/.Refactor-Loop-Commit-Msg\n+++ b/.Refactor-Loop-Commit-Msg\n",
    ], ids=["create", "case"])
    def test_a_diff_that_reaches_the_message_file_is_refused(self, diff):
        assert _call("touchesCommitMessage", diff) is True

    def test_a_diff_of_production_code_passes(self):
        assert _call("touchesCommitMessage", "--- a/src/msg.py\n+++ b/src/msg.py\n") is False

    def test_the_cage_refuses_a_message_file_diff_before_applying_it(self):
        src = WORKFLOW.read_text()
        assert src.index("touchesCommitMessage(candidate.diff") < src.index("applyPrompt(candidate)")


# The committer stages the paths the cage names; the hook checks each against what git says the patch
# touches, so a wrong name here costs a refused add, never a wider one.
@pytest.mark.skipif(not node, reason="node is not installed")
@pytest.mark.parametrize("diff,expected", [
    ("--- a/src/a.py\n+++ b/src/a.py\n", ["src/a.py"]),
    ("--- /dev/null\n+++ b/src/new.py\n", ["src/new.py"]),
    ("--- a/src/gone.py\n+++ /dev/null\n", ["src/gone.py"]),
    ("diff --git a/src/o.py b/src/n.py\nrename from src/o.py\nrename to src/n.py\n", ["src/o.py", "src/n.py"]),
    ("--- a/src/a.py\n+++ b/src/a.py\n--- a/src/b.py\n+++ b/src/b.py\n", ["src/a.py", "src/b.py"]),
    # Found by plugin-dev:plugin-validator, 2026-10-20: a mode-only change and a binary patch carry no
    # ---/+++ lines, and a removed `-- a/x` comment inside a hunk reads as a header.
    ("diff --git a/bin/run b/bin/run\nold mode 100644\nnew mode 100755\n", ["bin/run"]),
    ("diff --git a/img.png b/img.png\nindex 1..2 100644\nGIT binary patch\nliteral 1\nIc\n", ["img.png"]),
    ("diff --git a/q.sql b/q.sql\n--- a/q.sql\n+++ b/q.sql\n@@ -1,2 +1 @@\n--- a/x\n select 1\n", ["q.sql"]),
    ("--- a/src/a.py\t2026-10-20 10:00:00\n+++ b/src/a.py\t2026-10-20 10:01:00\n", ["src/a.py"]),
    ("--- a/src/a.py\r\n+++ b/src/a.py\r\n", ["src/a.py"]),
], ids=["edit", "create", "delete", "rename", "two", "mode-only", "binary", "comment-in-hunk", "timestamp",
        "crlf"])
def test_the_cage_names_every_path_a_diff_changes(diff, expected):
    assert _call("changedPaths", diff) == expected


def test_the_commit_prompt_names_the_message_file_and_the_paths():
    prompt = _js_function("commitPrompt")
    assert "${REPO}/${MESSAGE_PATH}" in prompt
    assert "changedPaths(p.diff)" in prompt
    assert "commit -F" in prompt
    assert "--literal-pathspecs add --" in prompt


# A refused or failed commit leaves the green change uncommitted; recording it as committed would lie.
def test_a_failed_commit_stops_the_run():
    src = WORKFLOW.read_text()
    assert re.search(r"if \(!c \|\| !c\.applied\) \{[^}]*stop = 'commit-failed'", src)


@pytest.mark.skipif(not node, reason="node is not installed")
def test_a_failed_commit_is_a_halt_with_its_reason():
    assert _call("finalStatus", "commit-failed", 2, 10) == {"status": "HALT", "reason": "commit-failed"}


# The hook reads the run's test command from the ledger header, which only the ledger writer writes and
# the cage composes; so the ledger is written before the first gate, and inactive again on any early halt.
def test_the_ledger_names_the_test_command_in_its_header():
    body = _js_function("ledgerMarkdown")
    assert body.index("test_cmd: ${TEST_CMD}") < body.index("## Nodes")


def test_the_ledger_is_written_before_the_baseline_gate():
    src = WORKFLOW.read_text()
    assert src.index("label: 'sentinel-on'") < src.index("gatePrompt('baseline')")


def test_an_early_halt_disarms_the_ledger():
    src = WORKFLOW.read_text()
    init = src[src.index("gatePrompt('baseline')"):src.index("phase('Loop')")]
    assert init.count("return {") == init.count("await disarm(")


def test_the_gate_runs_the_test_command_from_the_repo():
    assert "&& ${TEST_CMD}" in _js_function("gatePrompt")


# The hook matches the ledger's `test_cmd:` line exactly, and the ledger writer copies it through a code
# fence: a line break, trailing whitespace or a backtick fence would make every gate a refusal.
@pytest.mark.skipif(not node, reason="node is not installed")
@pytest.mark.parametrize("test_cmd", ["pytest\ntouch x", "pytest -q ", "pytest ```x```"],
                         ids=["multi-line", "trailing-space", "fence"])
def test_a_test_command_the_ledger_cannot_carry_is_refused(test_cmd):
    assert "test_cmd" in _call("readConfig", {"repo": "/r", "test_cmd": test_cmd, "plugin_root": "/p"})["missing"]


# Found by plugin-dev:plugin-validator, 2026-10-20: a throw after `sentinel-on` left the ledger armed, and
# no ledger write's result was checked.
def test_a_throw_after_arming_disarms_the_ledger():
    src = WORKFLOW.read_text()
    assert re.search(r"\} catch \(e\) \{\s*await disarm\('HALT'\)[^}]*throw e", src)


def test_a_failed_arming_halts_before_any_gate():
    src = WORKFLOW.read_text()
    arm = src.index("label: 'sentinel-on'")
    assert src.index("'ledger-write-failed'", arm) < src.index("gatePrompt('baseline')")


@pytest.mark.skipif(not node, reason="node is not installed")
@pytest.mark.parametrize("given,expected", [("a\nb", "a b"), ("x\r\ntest_cmd: y", "x  test_cmd: y"), (None, "")])
def test_a_ledger_cell_holds_one_line(given, expected):
    assert _call("ledgerCell", given) == expected


# A revert reverses the one patch file the applier applied: one allowed command, where `git checkout`
# plus `rm` would need paths the allow-list cannot bound (D5).
def test_revert_reverses_the_patch_file_and_never_checks_out():
    prompt = _js_function("revertPrompt")
    assert "apply --recount -R" in prompt
    assert "checkout" not in prompt


def test_apply_writes_the_diff_to_the_patch_file_and_applies_it_there():
    prompt = _js_function("applyPrompt")
    assert "${REPO}/${PATCH_PATH}" in prompt
    assert "apply --recount --check" in prompt


# Every path out of the land loop has already reverted its red attempt or applied nothing, so a final
# revert would reverse a patch that is not there.
def test_no_revert_runs_after_the_land_loop():
    assert "revert-final" not in WORKFLOW.read_text()


def test_a_failed_revert_stops_the_run():
    src = WORKFLOW.read_text()
    assert re.search(r"if \(!rv \|\| !rv\.applied\) \{[^}]*stop = 'revert-failed'", src)


@pytest.mark.skipif(not node, reason="node is not installed")
def test_a_failed_revert_is_a_halt_with_its_reason():
    assert _call("finalStatus", "revert-failed", 2, 10) == {"status": "HALT", "reason": "revert-failed"}


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


# The writing roles start as types whose grant the allow-list hook bounds to their own paths and
# commands, because `tools:` picks whole tools, never commands (CWE-250, issue 48).
NARROWED_CALLS = {
    "writeLedgerPrompt(": "phil:refactor-ledger-writer",
    "applyPrompt(": "phil:refactor-applier",
    "revertPrompt(": "phil:refactor-reverter",
    "commitPrompt(": "phil:refactor-committer",
    "gatePrompt(": "phil:refactor-gate-runner",
}


def test_every_agent_starts_as_a_narrowed_or_read_only_type():
    calls = [l for l in WORKFLOW.read_text().splitlines() if "await agent(" in l]
    assert calls and all("agentType: 'phil:refactor-" in l for l in calls), [l for l in calls if "agentType" not in l]


@pytest.mark.parametrize("call,agent_type", NARROWED_CALLS.items())
def test_a_writing_role_starts_as_its_narrowed_agent_type(call, agent_type):
    lines = [l for l in WORKFLOW.read_text().splitlines() if "await agent(" in l and call in l]
    assert len(lines) >= 1, f"no agent call builds {call}"
    for line in lines:
        assert f"agentType: '{agent_type}'" in line, line


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
    assert ("git -C <repo> status --porcelain -- . ':!.refactor-loop-ledger.md' ':!.refactor-loop-patch.diff'"
            " ':!.refactor-loop-commit-msg'") in body
    assert "commit or stash (`git stash -u`)" in body
    assert "git checkout" not in body


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
