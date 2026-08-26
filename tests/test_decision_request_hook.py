"""Tests for `hooks/decision-request/check-ask.py` — in-flight enforcement, and its limits.

This hook denies a real tool call in a real conversation, **including in projects that merely install
this plugin**. That is a sharper instrument than anything else this feature ships, so the tests are
weighted accordingly: more of them assert it stays out of the way than assert it fires.

Three properties, in order of what they cost if wrong:

1. **It fails open.** Any malformed payload, any surprising shape, any error — allow the call. A hook
   that breaks a stranger's conversation is worse than the defect it detects.
2. **It never denies a conforming ask.** Every recorded fixture in
   `skills/shared/self-test/decision-request/` that conforms must pass through untouched, and so must
   the real asks this feature's own sessions emitted.
3. **It denies the two breaches it is for**, with a reason that names the remedy rather than the rule.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
HOOK = REPO / "hooks" / "decision-request" / "check-ask.py"
SELFTEST = REPO / "skills" / "shared" / "self-test" / "decision-request"

CLEAN = {"questions": [{
    "header": "Way", "question": "Which way should this go?",
    "options": [
        {"label": "This way", "description": "Cheap, and it loses the audit trail."},
        {"label": "That way", "description": "Slower, and nothing is lost."},
    ]}]}


def _strict_project(tmp):
    """A project directory that has opted into the wording rule."""
    (tmp / "CLAUDE.md").write_text("# a project\n\ndecision-request: strict\n")
    return str(tmp)


def run(payload):
    """Returns the decision dict, or None when the hook allows the call by staying silent."""
    proc = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(payload),
                          capture_output=True, text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    if not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)["hookSpecificOutput"]


def ask(tool_input, tool_name="AskUserQuestion", cwd=None):
    """`cwd` decides whether the wording rule applies; the length rule ignores it.

    Always passed explicitly. The first version of these tests let it default to the ambient working
    directory, so they passed only because pytest happens to run from the one repository that has opted
    in — a test whose result depends on where it was invoked from.
    """
    return run({"tool_name": tool_name, "tool_input": tool_input, "cwd": cwd or str(REPO)})


# --------------------------------------------------------------------------- fails open


@pytest.mark.parametrize("payload", [
    "not json at all",
    "{}",
    '{"tool_name": "AskUserQuestion"}',
    '{"tool_name": "AskUserQuestion", "tool_input": null}',
    '{"tool_name": "AskUserQuestion", "tool_input": []}',
    '{"tool_name": "AskUserQuestion", "tool_input": {"questions": null}}',
    '{"tool_name": "AskUserQuestion", "tool_input": {"questions": [{}]}}',
    '{"tool_name": "AskUserQuestion", "tool_input": {"questions": [{"options": "nope"}]}}',
    '{"tool_name": "AskUserQuestion", "tool_input": {"questions": [{"options": [null]}]}}',
])
def test_a_surprising_payload_allows_the_call(payload):
    """Fail open, every time. This is the property that makes shipping a denial defensible."""
    proc = subprocess.run([sys.executable, str(HOOK)], input=payload,
                          capture_output=True, text=True, timeout=30)
    assert proc.returncode == 0
    assert proc.stdout.strip() == "", f"denied on {payload!r}"


def test_another_tool_is_not_this_hooks_business():
    assert ask({"file_path": "/tmp/x"}, tool_name="Write") is None


# --------------------------------------------------------------------------- stays out of the way


def test_a_conforming_ask_passes():
    assert ask(CLEAN) is None


@pytest.mark.parametrize("fixture", sorted(p.parent.name for p in SELFTEST.glob("*/manifest.json")))
def test_the_recorded_fixtures_agree_with_the_hook(fixture):
    """The hook and the fixture suite must not disagree about the two clauses they share.

    A fixture whose manifest declares OVER-CEILING must be denied; one that does not must not be denied
    *for length*. Vocabulary is deliberately allowed to differ — the hook's list is the portable subset,
    so a fixture failing on a wave label or a skill name is correctly invisible here, and that
    divergence is asserted rather than assumed.
    """
    d = json.loads((SELFTEST / fixture / "manifest.json").read_text())
    options = json.loads((SELFTEST / fixture / d["options_file"]).read_text())
    out = ask(options)
    reason = (out or {}).get("permissionDecisionReason", "")
    denied_for_length = "the limit is 200" in reason
    assert denied_for_length == ("OVER-CEILING" in d["expected_findings"]), (
        f"{fixture}: hook says over-ceiling={denied_for_length}, manifest says "
        f"{'OVER-CEILING' in d['expected_findings']}"
    )


def test_the_portable_list_is_narrower_than_the_standard_and_that_is_deliberate():
    """Fixture 02 carries a card number AND a slice id. The card number travels — it is an identifier
    from a system the reader may not share — and the slice id does not, because it is this repo's
    vocabulary. A hook that denied on the second would be refusing a stranger's question for a local
    reason, so the narrowing is asserted rather than left as a comment.
    """
    d = json.loads((SELFTEST / "03-the-jargon-wall" / "manifest.json").read_text())
    assert "skill or command name" in d["mechanical_assertions"]["forbidden_token_kinds"]
    options = json.loads((SELFTEST / "03-the-jargon-wall" / "options.json").read_text())
    reason = (ask(options) or {}).get("permissionDecisionReason", "")
    assert "issue or ticket number" in reason, "a card number is portable jargon and must be denied"
    assert "slice" not in reason.lower(), "a repo-local identifier must not reach a consumer's denial"


# --------------------------------------------------------------------------- denies what it is for


def test_an_over_long_question_is_denied_with_the_remedy():
    """The arithmetic clause. No judgement is involved, so this can never misfire on wording."""
    long = json.loads(json.dumps(CLEAN))
    long["questions"][0]["options"][0]["description"] = "a consideration " * 120
    out = ask(long)
    assert out["permissionDecision"] == "deny"
    assert "the limit is 200" in out["permissionDecisionReason"]
    assert "never below the sentence naming each option's cost" in out["permissionDecisionReason"], (
        "the remedy must carry its own floor, or the fix deletes what the standard requires"
    )


@pytest.mark.parametrize("token,label", [
    ("see #412 for the history", "an issue or ticket number"),
    ("described in docs/product/brief.md", "a file path"),
    ("recorded as CLAUDE.md", "a file path"),
    ("tracked as [ABC-77]", "a bracketed identifier"),
])
def test_portable_jargon_in_the_counted_text_is_denied(token, label):
    """The three classes that are jargon in any project. Each is an identifier from a system the reader
    may not share, which is the entire basis of the rule."""
    dirty = json.loads(json.dumps(CLEAN))
    dirty["questions"][0]["options"][1]["description"] += " " + token
    out = ask(dirty)
    assert out["permissionDecision"] == "deny"
    assert label in out["permissionDecisionReason"]


def test_a_preview_pane_is_not_counted_and_not_scanned():
    """The standard rules a preview to be context: outside the count, and free to carry what the ask
    may not. A hook that counted previews would deny the mock-ups the tool exists to show."""
    with_preview = json.loads(json.dumps(CLEAN))
    with_preview["questions"][0]["options"][0]["preview"] = (
        "see docs/x.md and #99\n" + "word " * 400)
    assert ask(with_preview) is None


def test_the_denial_names_where_the_identifier_should_go():
    """A denial the model cannot act on is a loop. The reason must carry the remedy, not the rule."""
    dirty = json.loads(json.dumps(CLEAN))
    dirty["questions"][0]["question"] = "Should we close #33?"
    reason = ask(dirty)["permissionDecisionReason"]
    assert "context block above the question" in reason
    assert "decision-request.md" in reason, "the model must be able to read the standard it breached"


def test_every_question_is_checked_not_only_the_first():
    """A three-question turn is three decisions. Checking only the first is the singular assumption
    this feature has already been bitten by once."""
    two = json.loads(json.dumps(CLEAN))
    second = json.loads(json.dumps(CLEAN["questions"][0]))
    second["header"] = "Second"
    second["options"][0]["description"] = "a consideration " * 120
    two["questions"].append(second)
    out = ask(two)
    assert out["permissionDecision"] == "deny" and "Second" in out["permissionDecisionReason"]


def test_the_hook_is_registered_for_the_right_tool():
    """A hook nobody wires is the written-and-never-called defect with extra steps."""
    manifest = json.loads((REPO / "hooks" / "hooks.json").read_text())
    entries = [e for e in manifest["hooks"]["PreToolUse"] if e.get("matcher") == "AskUserQuestion"]
    assert len(entries) == 1
    command = entries[0]["hooks"][0]["command"]
    assert "${CLAUDE_PLUGIN_ROOT}/hooks/decision-request/check-ask.py" in command, (
        "a bare relative path in a shipped hook resolves against the user's project"
    )


def test_the_header_states_which_clauses_it_cannot_reach():
    """The same discipline as the build check: a partial enforcer that does not say what it misses
    reads as a complete one."""
    body = " ".join(HOOK.read_text().split())
    assert "Two remain unreachable and always will be" in body
    assert "whether each option names its cost" in body
    assert "the framing is not in the payload" in body
    assert "portable subset, deliberately" in body


# --------------------------------------------------------------------------- the opt-in split


def test_the_length_rule_applies_to_a_project_that_never_opted_in(tmp_path):
    """Arithmetic ships unconditionally. It is content-neutral, so there is no wording it can misjudge
    and no project where 200+ words of options is readable."""
    long = json.loads(json.dumps(CLEAN))
    long["questions"][0]["options"][0]["description"] = "a consideration " * 120
    out = ask(long, cwd=str(tmp_path))
    assert out["permissionDecision"] == "deny" and "the limit is 200" in out["permissionDecisionReason"]


def test_the_wording_rule_does_not_apply_to_a_project_that_never_opted_in(tmp_path):
    """The measurement that forced the split: 81% of this repo's 73 recorded asks would have been
    denied, and the dominant cause was filenames. Here a filename is internal jargon; in an ordinary
    project `"edit config.json or settings.yaml?"` is the clearest way to name the decision, and denying
    it would be this plugin refusing a stranger's work for a reason that does not apply to them.
    """
    dirty = json.loads(json.dumps(CLEAN))
    dirty["questions"][0]["question"] = "Should I edit config.json or settings.yaml?"
    assert ask(dirty, cwd=str(tmp_path)) is None


def test_the_wording_rule_applies_where_a_project_opts_in(tmp_path):
    dirty = json.loads(json.dumps(CLEAN))
    dirty["questions"][0]["question"] = "Should I edit config.json or settings.yaml?"
    out = ask(dirty, cwd=_strict_project(tmp_path))
    assert out["permissionDecision"] == "deny" and "a file path" in out["permissionDecisionReason"]


def test_this_repository_has_opted_in():
    """The complaint that started this feature was about asks in THIS repo, so this is where the
    stricter half has to be on. If the marker is ever removed, these asks stop being checked and
    nothing else would say so."""
    assert "decision-request: strict" in (REPO / "CLAUDE.md").read_text()


def test_a_url_is_not_a_path(tmp_path):
    """A link the reader can open is not an identifier from a system they may not share. Found by
    inspecting all 42 distinct matches over the corpus — it was the only false one."""
    linked = json.loads(json.dumps(CLEAN))
    linked["questions"][0]["options"][0]["description"] += " See https://github.com/o/r/blob/main/x.md"
    assert ask(linked, cwd=_strict_project(tmp_path)) is None
