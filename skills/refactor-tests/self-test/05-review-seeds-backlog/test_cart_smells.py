from cart import total


# --- SMELL A: duplicated setup (same cart literal built in two tests) ---
# Named move (D5): Extract Fixture/Helper.
def test_total_sums_line_items():
    cart = {"widget": (10, 2), "gadget": (5, 1)}
    assert total(cart) == 25


def test_total_applies_discount():
    cart = {"widget": (10, 2), "gadget": (5, 1)}
    assert total(cart, 0.10) == 22.5


# --- SMELL B: vague name (says nothing about what is verified) ---
# Named move (D5): Rename.
def test_it_works():
    assert total({"a": (1, 1)}) == 1


# --- SMELL C: missing AAA (arrange/act/assert interleaved, no separation) ---
# Named move (D5): reorder into Arrange-Act-Assert.
def test_discount_behaviour():
    cart = {"x": (100, 1)}
    assert total(cart) == 100
    cart["y"] = (50, 1)
    assert total(cart) == 150
    assert total(cart, 0.5) == 75


# --- SMELL D: long test with an extractable, repeated block ---
# Named move (D5): Extract Test Helper.
def test_many_carts_total_correctly():
    cart_a = {"widget": (10, 2)}
    assert total(cart_a) == 20
    cart_b = {"gadget": (5, 3)}
    assert total(cart_b) == 15
    cart_c = {"widget": (10, 1), "gadget": (5, 1)}
    assert total(cart_c) == 15
    cart_d = {"widget": (10, 2), "gadget": (5, 2)}
    assert total(cart_d, 0.10) == 27.0
