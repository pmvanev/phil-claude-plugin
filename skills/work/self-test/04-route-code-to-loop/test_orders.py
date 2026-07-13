# The wave's preservation oracle IS this suite (delegate-owned, via refactor-loop).
# phil:work must NOT run its own gate — it delegates and inherits this one.
from orders import summarize_order


def test_summarize_totals_and_label():
    result = summarize_order([("widget", 10, 2), ("gadget", 5, 1)], 0.1, 5.0, "$")
    assert result["subtotal"] == 25
    assert result["total"] == 22.0
    assert result["label"] == "$22.00"


def test_discount_floors_at_zero():
    result = summarize_order([("cheap", 1, 1)], 0.0, 100.0, "$")
    assert result["total"] == 0
