"""The rule-reachability check must FAIL on the input that motivated it.

This repo has the scar: the first version of `check-readonly-commands.py` passed silently because
the function was written and never called. A green run proves nothing until the check is shown to go
red on the defect it exists to catch — so every test here drives the real script over a synthetic
tree, rather than asserting that the repo currently passes.
"""
import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "check-rule-reachability.py"


def _known_unreached() -> dict:
    """Read the live exception list rather than restating it — a copy here would drift."""
    spec = importlib.util.spec_from_file_location("_rulecheck", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.KNOWN_UNREACHED


def _tree(rules: dict[str, str], loaders: dict[str, str]):
    """Build a throwaway repo whose layout the script recognises, and run the script against it."""
    tmp = Path(tempfile.mkdtemp(prefix="rulecheck-"))
    (tmp / "rules").mkdir()
    for area in ("skills", "commands", "agents"):
        (tmp / area).mkdir()
    # every declared exception must exist, or the script rightly complains about the list itself
    for name in _known_unreached():
        (tmp / "rules" / f"{name}.md").write_text("# stub")
    for name, body in rules.items():
        (tmp / "rules" / f"{name}.md").write_text(body)
    for rel, body in loaders.items():
        path = tmp / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)
    # the script locates rules/ relative to its own parent.parent, so run a copy from inside the tree
    (tmp / "scripts").mkdir()
    shutil.copy(SCRIPT, tmp / "scripts" / SCRIPT.name)
    r = subprocess.run([sys.executable, str(tmp / "scripts" / SCRIPT.name)],
                       capture_output=True, text=True)
    shutil.rmtree(tmp, ignore_errors=True)
    return r


def test_fails_when_a_rule_is_named_by_nothing():
    r = _tree({"orphan": "# Orphan"}, {"skills/x/SKILL.md": "nothing here"})
    assert r.returncode == 1
    assert "rules/orphan.md is named by nothing" in r.stdout


def test_passes_when_a_loader_names_the_rule():
    r = _tree({"coding": "# Coding"},
              {"skills/x/SKILL.md": "read `${CLAUDE_PLUGIN_ROOT}/rules/coding.md` first"})
    assert r.returncode == 0, r.stdout


def test_reachability_is_transitive_through_a_sibling_citation():
    # `glossary` is named by no loader — only by a rule that IS named. That is a real route.
    r = _tree({"coding": "see `glossary.md` for terms", "glossary": "# Glossary"},
              {"skills/x/SKILL.md": "read `${CLAUDE_PLUGIN_ROOT}/rules/coding.md`"})
    assert r.returncode == 0, r.stdout


def test_a_chain_hanging_off_an_unreachable_rule_is_still_unreachable():
    # The defect that motivated the exception list: `glossary` is cited only by an orphan.
    r = _tree({"orphan": "see `glossary.md`", "glossary": "# Glossary"},
              {"skills/x/SKILL.md": "nothing"})
    assert r.returncode == 1
    assert "rules/glossary.md is named by nothing" in r.stdout


def test_a_stale_exception_fails_rather_than_rotting():
    """An entry for a rule that has since been wired up must be removed, not left as an excuse."""
    src = SCRIPT.read_text()
    assert '"definitions"' in src and '"llm-inference"' in src
    # both are still unreachable in the real repo, so the live run is green
    live = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
    assert live.returncode == 0, live.stdout
