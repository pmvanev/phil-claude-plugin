"""`skills/edd/SKILL.md`: the evidence gate's loops must end, and its dispatch must reach its agent.

Found 2026-10-13, all predating that day's hardening:
- A developer rejecting reused evidence as irrelevant went through the reject branch, which rebuilds via
  the engine; fixture 03 says it commissions fresh evidence only.
- A reject looped back through the engine with no exit, and DOCUMENT ran only "on completion", so a run
  stopped over a standing reject recorded nothing.
- A producer reporting that it could not execute was neither narration nor evidence, and the only branch
  re-commissioned it forever.
- The dispatch named `agents/edd-evidence-producer`, not the Agent type, and passed none of the inputs the
  agent's contract expects.
- "The plugin's evolution convention" names a directory a user's repository does not have.
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "edd" / "SKILL.md"


def _flat():
    return " ".join(SKILL.read_text().split())


def test_an_irrelevance_reject_commissions_evidence_and_rebuilds_nothing():
    assert "commission fresh evidence and rebuild nothing" in _flat()


def test_the_developer_can_stop_over_a_standing_reject_and_the_trail_records_it():
    body = _flat()
    assert "The developer may stop instead" in body
    assert "a run stopped over a standing reject writes the trail too" in body


def test_a_producer_that_cannot_execute_goes_to_the_developer():
    assert "cannot produce executed evidence" in _flat()
    assert "report it to the developer rather than re-commissioning" in _flat()


def test_the_dispatch_names_the_agent_type_and_its_inputs():
    body = _flat()
    assert "`phil:edd-evidence-producer`" in body
    assert "`expectation`, `target` and any `context`" in body


def test_the_evolution_summary_has_a_home_in_any_repo():
    body = _flat()
    assert "the plugin's evolution convention" not in body
    assert "creating `docs/evolution/` if absent" in body
