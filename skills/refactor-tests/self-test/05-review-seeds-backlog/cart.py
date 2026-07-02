"""Tiny SUT for the review fixture. The test file (`test_cart_smells.py`) is what
`--review` scans; this module only exists so the smell-laden tests are runnable and green.
"""


def total(cart, discount=0.0):
    raw = sum(price * qty for price, qty in cart.values())
    return round(raw * (1 - discount), 2)
