# Tiny target for fixture 04 — a code artifact (has a runnable test suite).
# The point of the fixture is the ROUTING decision, not this code. A long function
# stands in for "a wave that changes executable code."

def summarize_order(items, tax_rate, discount, currency):
    subtotal = 0
    for name, price, qty in items:
        subtotal += price * qty
    discounted = subtotal - discount
    if discounted < 0:
        discounted = 0
    tax = discounted * tax_rate
    total = discounted + tax
    label = f"{currency}{total:.2f}"
    return {"subtotal": subtotal, "total": total, "label": label}
