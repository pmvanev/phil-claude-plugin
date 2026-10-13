"""`commands/nwave-wave-summary.md` loads `skills/nwave-wave-summary/SKILL.md`; what it restates must
agree with the skill, and the skill must agree with itself.

Found 2026-10-13, all predating that day's hardening:
- The command said fixtures hold the 200-word ceiling at build time. The skill says no fixture applies
  the counter, and `tests/test_wave_summary_fixtures.py` uses it only on counterexamples.
- The command said to "name the artifact read", the wording the skill retracted because an artifact's
  name is a path and no identifier may reach the summary.
- The command said "report the outcome", singular; the skill requires a terminal outcome, `READ-ONLY`
  every run, and two companion outcomes when they apply.
- The skill's `READ-ONLY` paragraph called the tool list a guarantee, while its own never-do list and
  the command record that `--output=<file>` writes through either granted git verb.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COMMAND = REPO / "commands" / "nwave-wave-summary.md"
SKILL_DIR = REPO / "skills" / "nwave-wave-summary"
SKILL = SKILL_DIR / "SKILL.md"


def _flat(path):
    return " ".join(path.read_text().split("---", 2)[2].split())


def _skill_texts():
    return {p.relative_to(SKILL_DIR): " ".join(p.read_text().split())
            for p in SKILL_DIR.rglob("*") if p.suffix in (".md", ".json")}


def test_nothing_in_the_command_or_skill_claims_a_test_holds_the_ceiling():
    body = _flat(COMMAND)
    assert "fixtures hold it" not in body
    assert "no test counts it" in body and "over the whole rendered output" in body
    for path, text in _skill_texts().items():
        assert not re.search(r"ceiling is (enforced|held) by fixtures", text), path


def test_nothing_says_to_name_the_artifact_rather_than_the_feature():
    """An artifact's name is a path, and no identifier may reach the summary."""
    assert "never its path" in _flat(COMMAND)
    for path, text in {Path("command"): _flat(COMMAND), **_skill_texts()}.items():
        assert not re.search(r"names? the artifact( read| it read| and its date)", text, re.I), path


def test_the_command_reports_every_outcome_the_skill_requires():
    body = _flat(COMMAND)
    assert "Report the outcome by name" not in body
    assert "every outcome the skill's `## Decision outcomes` requires" in body
    section = SKILL.read_text().split("## Decision outcomes", 1)[1].split("\n## ", 1)[0]
    assert "`READ-ONLY` is reported on every run" in section
    assert "`READ-ONLY`" in body


def test_the_command_and_skill_forbid_both_flags_and_patch_output():
    """`git show <sha>` and `git log -p` ran a configured textconv filter on git 2.53.0; `--stat`,
    `--oneline` and `--format` did not (verified 2026-10-13)."""
    for text in (_flat(COMMAND), _flat(SKILL)):
        assert "Pass neither `--output` nor `--ext-diff`" in text
        assert "never as a patch" in text


def test_every_git_call_the_skill_spells_avoids_patch_output():
    calls = re.findall(r"^git (?:log|show)[^\n]*", SKILL.read_text(), re.M)
    assert calls, "the skill spells no git call"
    for call in calls:
        assert re.search(r"--stat|--oneline|--format", call), call


def test_read_only_is_a_claim_about_the_run_not_the_tool_list():
    for path, text in _skill_texts().items():
        assert "already guarantees" not in text, path
        assert not re.search(r"read-only (guarantee|property) is (mechanical|an enforced guarantee)",
                             text, re.I), path
    assert "a claim about the calls this run made, not about the tool list" in _flat(SKILL)


def test_a_slice_number_resolves_inside_one_feature():
    """Slice numbers repeat across features — thirteen had a slice 03 on 2026-10-13."""
    skill = _flat(SKILL)
    assert "Resolve the feature first" in skill
    assert "a slice number names a brief inside that feature" in skill


def test_the_identifier_invariant_keeps_the_slice_number_exemption():
    invariants = " ".join(SKILL.read_text().split("## Invariants", 1)[1].split("\n## ", 1)[0].split())
    assert "except the slice's own number in `--slice` mode" in invariants


def test_every_inline_git_call_uses_a_patch_free_form():
    """The line-anchored check misses calls written mid-sentence."""
    prescribed = SKILL.read_text().split("## Invariants", 1)[0]  # the Invariants name the forbidden forms
    for call in re.findall(r"`(git (?:log|show) [^`]+)`", prescribed):
        assert re.search(r"--stat|--oneline|--format", call), call


def test_slice_mode_names_where_meaning_comes_from():
    assert "commit messages (`--format=%B`)" in _flat(SKILL)
