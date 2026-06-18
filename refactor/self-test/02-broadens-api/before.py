"""Starting code for fixture 02. Only `total` is part of the public surface."""

__all__ = ["total"]


def _line_total(qty, price):
    return qty * price


def total(items):
    return sum(_line_total(qty, price) for qty, price in items)
