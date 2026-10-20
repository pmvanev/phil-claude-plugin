import json

import guard


def _payload(path):
    return json.dumps({"tool_input": {"file_path": path}})


def test_refuses_a_test_write_while_the_loop_runs(tmp_path):
    (tmp_path / ".loop-active").touch()
    assert guard.refuse_test_write(_payload("/r/tests/test_a.py"), tmp_path) == "deny"


def test_allows_a_test_write_when_no_loop_runs(tmp_path):
    assert guard.refuse_test_write(_payload("/r/tests/test_a.py"), tmp_path) is None


def test_allows_production_code_while_the_loop_runs(tmp_path):
    (tmp_path / ".loop-active").touch()
    assert guard.refuse_test_write(_payload("/r/src/a.py"), tmp_path) is None


def test_keep_transcript_appends_each_exchange(tmp_path):
    guard.keep_transcript(tmp_path, [("hi", "hello")])
    assert "## Prompt\nhi" in (tmp_path / "run-transcript.md").read_text()
