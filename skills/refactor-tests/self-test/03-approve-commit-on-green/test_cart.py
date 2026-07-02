from cart import total


def test_total_sums_line_items():
    cart = {"widget": (10, 2), "gadget": (5, 1)}
    assert total(cart) == 25


def test_total_applies_discount():
    cart = {"widget": (10, 2), "gadget": (5, 1)}
    assert total(cart, 0.10) == 22.5
