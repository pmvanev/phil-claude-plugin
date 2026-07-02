"""Tiny SUT for the refactor-tests self-test fixtures.

The SUT is NOT the thing being refactored -- the *test file* is. This module only
exists so `pytest` has something green to run. Kept dependency-free on purpose.
"""


def total(cart, discount=0.0):
    raw = sum(price * qty for price, qty in cart.values())
    return round(raw * (1 - discount), 2)
