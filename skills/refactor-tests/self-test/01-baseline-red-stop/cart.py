"""Buggy SUT for fixture 01: total() ignores quantity, so the green-intent tests
fail at baseline. The refactor-tests loop must detect the red baseline and STOP --
it never refactors on red (D7 / DD6).
"""


def total(cart, discount=0.0):
    raw = sum(price for price, qty in cart.values())  # BUG: ignores qty
    return round(raw * (1 - discount), 2)
