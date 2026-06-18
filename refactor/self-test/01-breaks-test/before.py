"""Starting code for fixture 01. The test below passes against this version."""

__all__ = ["apply_discount"]


def apply_discount(price, pct):
    if pct < 0 or pct > 100:
        raise ValueError("pct must be between 0 and 100")
    return price - (price * pct / 100)
