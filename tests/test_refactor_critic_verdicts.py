"""The refactor-loop critic's verdict vocabulary, and the guard that routes on it.

`refactor/rubric.md` defines `CANNOT_ASSESS` twice — a criterion the critic cannot judge abstains, and
generic praise with no `span` is coerced to it, never `accept`. Until 0.115.0 the agent's schema, the
workflow's `VERDICT_SCHEMA` and its prompt all listed `accept | revise | reject` and a boolean `met`,
while the agent's own anti-flattery section told it to emit `CANNOT_ASSESS`. Found 2026-10-13: documenting
the value in the agent alone made the critic emit `met: "false"` as a string, which the guard's
`c.met === false` never blocks on — a behaviour-changing diff would have landed.

These tests hold the four surfaces to one vocabulary, and drive the guard itself under Node, including
fixture 03's span-less `verdict.json`.
"""
import json
import re
import shutil
import subprocess

import pytest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WORKFLOW = REPO / "workflows" / "refactor-loop.js"
AGENT = REPO / "agents" / "refactor-critic-correctness.md"
SKILL = REPO / "skills" / "refactor-loop" / "SKILL.md"
RUBRIC = REPO / "refactor" / "rubric.md"
FIXTURE_03 = REPO / "refactor" / "self-test" / "03-no-span-praise" / "verdict.json"

VERDICTS = {"accept", "revise", "reject", "CANNOT_ASSESS"}


def _js_function(name):
    """The source of a top-level `function name(...) { ... }` in the workflow, braces balanced."""
    src = WORKFLOW.read_text()
    start = src.index(f"function {name}(")
    depth, i = 0, src.index("{", start)
    while True:
        depth += {"{": 1, "}": -1}.get(src[i], 0)
        i += 1
        if depth == 0:
            return src[start:i]


def test_every_surface_names_the_same_four_verdicts():
    schema_enum = re.search(r"verdict: \{ type: 'string', enum: \[([^\]]*)\]", WORKFLOW.read_text())
    assert schema_enum, "VERDICT_SCHEMA must enumerate the verdicts"
    assert set(re.findall(r"'([^']+)'", schema_enum.group(1))) == VERDICTS

    agent_line = re.search(r'"verdict": "([^"]+)"', AGENT.read_text())
    assert {v.strip() for v in agent_line.group(1).split("|")} == VERDICTS

    assert "accept|revise|reject|CANNOT_ASSESS" in _js_function("criticPrompt")
    assert all(f"`{v}`" in RUBRIC.read_text() for v in VERDICTS)


def test_met_admits_an_abstention_in_the_schema_and_the_agent():
    assert re.search(r"met: \{ enum: \[true, false, 'CANNOT_ASSESS'\] \}", WORKFLOW.read_text())
    assert '"met": false' in AGENT.read_text(), "the example keeps a JSON boolean, never a string"
    assert 'the string `"CANNOT_ASSESS"`' in AGENT.read_text()


def test_the_skill_never_routes_cannot_assess_to_apply():
    """`revise` with no blocking item proceeds to APPLY, so "treat it as revise" contradicted itself."""
    text = SKILL.read_text()
    assert "treat it as `revise`" not in text
    assert "`CANNOT_ASSESS` verdict is **not** an accept — back-prompt the proposer" in text


node = shutil.which("node")


def _route(verdict, theta=0.6):
    script = _js_function("routeVerdict") + f"\nconsole.log(JSON.stringify(routeVerdict({json.dumps(verdict)}, {theta})))"
    out = subprocess.run([node, "-e", script], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def _item(met, severity="nit", span="src/a.py:1"):
    return {"criterion": "behavior-preserved", "met": met, "severity": severity, "span": span,
            "mechanism": "m"}


@pytest.mark.skipif(not node, reason="node is not installed")
class TestTheGuard:
    def test_fixture_03_span_less_praise_is_coerced_and_never_applied(self):
        r = _route(json.loads(FIXTURE_03.read_text()))
        assert r["verdict"] == "CANNOT_ASSESS"
        assert r["route"] == "reprompt"

    def test_cannot_assess_reprompts(self):
        assert _route({"verdict": "CANNOT_ASSESS", "confidence": 0.9, "per_criterion": []})["route"] == "reprompt"

    def test_reject_reprompts(self):
        assert _route({"verdict": "reject", "confidence": 0.9, "per_criterion": [_item(False, "major")]})["route"] == "reprompt"

    def test_a_confident_major_failure_blocks_an_accept(self):
        v = {"verdict": "accept", "confidence": 0.7, "per_criterion": [_item(False, "major")]}
        assert _route(v)["route"] == "reprompt"

    def test_an_unconfident_major_failure_does_not_block(self):
        v = {"verdict": "revise", "confidence": 0.5, "per_criterion": [_item(False, "major")]}
        assert _route(v)["route"] == "apply"

    def test_an_accept_with_spans_applies(self):
        assert _route({"verdict": "accept", "confidence": 0.9, "per_criterion": [_item(True)]})["route"] == "apply"

    def test_an_abstaining_criterion_is_not_a_failure(self):
        v = {"verdict": "revise", "confidence": 0.9,
             "per_criterion": [_item(True), _item("CANNOT_ASSESS", "major")]}
        assert _route(v)["route"] == "apply"

    def test_the_string_false_still_blocks(self):
        """The regression that found this: `met: "false"` slipped past `c.met === false`."""
        v = {"verdict": "accept", "confidence": 0.9, "per_criterion": [_item("false", "major")]}
        assert _route(v)["route"] == "reprompt"

    def test_no_verdict_reprompts(self):
        assert _route(None)["route"] == "reprompt"

    def test_an_accept_spanned_on_some_criteria_applies(self):
        v = {"verdict": "accept", "confidence": 0.9, "per_criterion": [_item(True), _item(True, span=None)]}
        assert _route(v)["route"] == "apply"

    @pytest.mark.parametrize("span", ["   ", "n/a", "?", "the whole diff"])
    def test_a_span_that_names_no_file_line_is_no_span(self, span):
        v = {"verdict": "accept", "confidence": 0.9, "per_criterion": [_item(True, span=span)]}
        r = _route(v)
        assert (r["verdict"], r["route"]) == ("CANNOT_ASSESS", "reprompt")

    def test_a_revise_with_only_minor_failures_applies(self):
        v = {"verdict": "revise", "confidence": 0.9, "per_criterion": [_item(False, "minor")]}
        assert _route(v)["route"] == "apply"

    def test_an_unknown_verdict_reprompts(self):
        assert _route({"verdict": "looks good", "confidence": 0.9, "per_criterion": [_item(True)]})["route"] == "reprompt"

    @pytest.mark.parametrize("met", ["False", "FALSE", " false "])
    def test_any_spelling_of_false_blocks(self, met):
        v = {"verdict": "accept", "confidence": 0.9, "per_criterion": [_item(met, "major")]}
        assert _route(v)["route"] == "reprompt"

    @pytest.mark.parametrize("confidence", [None, "high"])
    def test_an_unreadable_confidence_fails_closed(self, confidence):
        v = {"verdict": "accept", "confidence": confidence, "per_criterion": [_item(False, "major")]}
        assert _route(v)["route"] == "reprompt"

    def test_failures_list_only_unmet_criteria(self):
        v = {"verdict": "reject", "confidence": 0.9,
             "per_criterion": [_item(True), _item(False, "major"), _item("CANNOT_ASSESS")]}
        assert len(_route(v)["failures"]) == 1


SHIPPED = [SKILL, AGENT, WORKFLOW]


@pytest.mark.parametrize("path", SHIPPED, ids=lambda p: p.name)
def test_the_rubric_is_named_from_the_plugin_root(path):
    """A bare `refactor/rubric.md` resolves against the user's repository, where it does not exist."""
    text = path.read_text()
    bare = [m.start() for m in re.finditer(r"refactor/rubric\.md", text)
            if not text[:m.start()].endswith("${CLAUDE_PLUGIN_ROOT}/")]
    assert not bare, f"{path.name} names the rubric without ${{CLAUDE_PLUGIN_ROOT}}"
