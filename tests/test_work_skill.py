"""`skills/work/SKILL.md`: the defects with an obvious answer, fixed 2026-10-13. The delegate-contract
redesign — who commits, what each delegate's success and failure mean — is a board card, not this file.

- FRAME offered a preservation-only basis, but the two-gate spine, VERIFY and the Safety rules all
  demanded a goal metric, so an accepted preservation-only run could never be reported done.
- Resume had no rule for zero or several initiatives under `docs/work/`, and `progress.md` did not
  exist until a wave finished, so a run stopped on its first wave left nothing to resume.
- Only the FRAME confirmation followed the decision-request standard; the skill asks four other things.
- The self-test paragraph and the evolution summary named paths in the plugin's own repository.
- The standards were named but never said to be read.
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "work" / "SKILL.md"


def _flat():
    return " ".join(SKILL.read_text().split("---", 2)[2].split())


def _section(title):
    text = SKILL.read_text()
    return " ".join(text.split(f"## {title}", 1)[1].split("\n## ", 1)[0].split())


def test_a_preservation_only_run_can_be_done():
    assert "On an accepted preservation-only basis, the preservation floor is the only gate" in _flat()
    assert "On a preservation-only basis, skip the goal gate" in _section("VERIFY & DOCUMENT")
    assert "declared goal always" not in _section("Safety rules")


def test_resume_names_its_initiative_and_has_a_progress_file_to_read():
    body = _flat()
    assert "With several in-flight initiatives under `docs/work/`, ask which" in body
    assert "write `docs/work/<slug>/progress.md` with every wave `pending`" in _section("MAP — plan the waves")
    assert "ask before re-running the wave that stopped it" in body


def test_every_ask_follows_the_decision_request_standard():
    body = _flat()
    assert "Every question this skill puts to the developer follows" in body
    assert "${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md" in body


def test_paths_resolve_in_a_user_s_repository():
    """A backticked plugin path must carry the root; a bare one resolves against the user's repo."""
    body = _flat()
    assert "the plugin's existing `docs/evolution/` convention" not in body
    assert not re.findall(r"`(?:skills|commands|self-test)/", body)


def test_the_standards_are_read():
    assert "Read the standards to work under" in _flat()


def test_a_schema_migration_keeps_every_wave_a_rollback_target():
    """A migration routed as a re-architecture named no delivery standard, so a roadmap could expand and
    contract a schema in one wave and leave no release to roll back to (2026-10-22)."""
    mapping = _section("MAP — plan the waves")
    assert "${CLAUDE_PLUGIN_ROOT}/rules/continuous-delivery.md" in mapping
    assert "Plan expand and contract as separate waves" in mapping
    assert "still reads or writes the old shape" in mapping, "a release that only writes the old column needs it too"
    assert "is not a lone rename" in _section("FRAME — scope the initiative"), "FRAME must not off-ramp a column rename"
    assert "plan a backfill wave when existing rows hold data the new shape needs" in mapping
    assert "The expand wave adds the new shape and writes both" in mapping, "a blind drive had to guess where dual writes start"
    assert "relaxes any constraint that forces a write to the old shape, such as `NOT NULL`" in mapping, \
        "a blind drive stopped writing a column still NOT NULL (2026-10-22)"
    assert "the goal and its before reading" in _section("FRAME — scope the initiative"), "a paused run resumes in a new session"
    assert "into expand and contract waves (08)" in _section("Self-test (regression gate)")
    fixture = SKILL.parent / "self-test" / "08-migration-expand-contract"
    manifest = json.loads((fixture / "manifest.json").read_text())
    assert manifest["expected_decision"] == "SPLIT-EXPAND-CONTRACT"
    assert "roadmap" not in manifest, "the roadmap is MAP's output, not the driver's input"
    changes = [w["change"] for w in manifest["expected_roadmap"]]
    assert changes[0].startswith("expand") and changes[-1].startswith("contract"), changes
    assert any(c.startswith("stop writing") for c in changes), "the drop follows a release that no longer writes"
    assert "SPLIT-EXPAND-CONTRACT" in (fixture / "expected.md").read_text()


def test_a_wave_that_ships_alone_pauses_the_run_for_its_release():
    """MAP planned each migration wave as its own release while EXECUTE ran every wave in one sitting,
    so a run shipped expand and contract together (plugin-validator and skill-reviewer, 2026-10-22)."""
    assert "mark each of these waves `ships alone`" in _section("MAP — plan the waves")
    execute = _section("EXECUTE — run the roadmap, one gated wave at a time")
    assert "mark the wave `done` in `progress.md` with its commit sha and oracle result" in execute
    assert "if no wave remains, go on to VERIFY" in execute, "a last wave that ships alone goes on to VERIFY"
    assert "if this wave or the next is marked `ships alone`, mark the next wave `awaiting-release`" in execute
    assert "the commit its release must contain" in execute
    assert "Mark the wave `failed` in `progress.md`" in execute, "Resume tells the two stops apart"
    assert "**paused for release**" in execute
    resume = _flat()
    assert "When it is `awaiting-release`, ask the developer to confirm" in resume
    assert "On a yes, mark the wave `pending` and run it" in resume
    assert "pausing for a release" in resume and "A wave that ships alone pauses the run" in _section("Safety rules")
    assert "A run paused for release has not reached VERIFY" in _section("VERIFY & DOCUMENT")
    assert "pauses for release after a wave that ships alone (09)" in _section("Self-test (regression gate)")
    fixture = SKILL.parent / "self-test" / "09-pause-for-release"
    manifest = json.loads((fixture / "manifest.json").read_text())
    assert manifest["expected_decision"] == "PAUSE-FOR-RELEASE"
    assert manifest["resume"]["developer_confirms_release"] is False, "Resume's no-path is pinned"
    feature = (SKILL.parent / "acceptance.feature").read_text()
    assert "@fixture:08-migration-expand-contract" in feature and "@fixture:09-pause-for-release" in feature
    assert "PAUSE-FOR-RELEASE" in (fixture / "expected.md").read_text()
    assert "`09-pause-for-release/`" in (SKILL.parent / "self-test" / "README.md").read_text()
