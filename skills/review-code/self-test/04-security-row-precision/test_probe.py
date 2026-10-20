import json

import probe


def _payload(**tool_input):
    return json.dumps({"tool_input": tool_input})


def test_paths_in_finds_a_file_path():
    assert probe.paths_in("see docs/setup.md first") == ["docs/setup.md"]


def test_wording_gate_refuses_a_long_question():
    assert probe.wording_gate(_payload(question="word " * 201)) == "deny"


def test_wording_gate_allows_a_short_question():
    assert probe.wording_gate(_payload(question="Ship it?")) is None


def test_protect_tests_refuses_a_test_file():
    assert probe.protect_tests(_payload(file_path="/r/tests/test_a.py")) == "deny"


def test_protect_tests_allows_production_code():
    assert probe.protect_tests(_payload(file_path="/r/src/a.py")) is None
