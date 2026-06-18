"""Behavioral test for fixture 02. Passes against before.py and after the bad diff —
the breakage is a silent public-API broadening, not a behavior change, so only the
public-API diff (G4) catches it, not the test gate (G3)."""

from before import total


def test_totals_line_items():
    assert total([(2, 10), (1, 5)]) == 25
