class ReceiptMailer:
    """A port this codebase owns. Production wires it to the email gateway customers' receipts come from."""

    def send_receipt(self, customer, total):
        raise NotImplementedError


class Invoice:
    def __init__(self, customer, lines):
        self.customer = customer
        self.lines = lines
        self.paid = False

    @property
    def total(self):
        return sum(price * qty for price, qty in self.lines)

    def pay(self, mailer):
        self.paid = True
        mailer.send_receipt(self.customer, self.total)

    def __repr__(self):
        return f"Invoice({self.customer}, {self.total})"
