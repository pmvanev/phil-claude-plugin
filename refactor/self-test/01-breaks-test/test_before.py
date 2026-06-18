"""Behavioral test pinning the contract of apply_discount. Passes against before.py."""

import pytest

from before import apply_discount


def test_applies_percentage_discount():
    assert apply_discount(100, 10) == 90
    assert apply_discount(200, 10) == 180  # discriminator: price - pct would give 190


def test_rejects_out_of_range_percentage():
    with pytest.raises(ValueError):
        apply_discount(100, 150)
