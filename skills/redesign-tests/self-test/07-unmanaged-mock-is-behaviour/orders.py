"""Tiny SUT for fixture 07.

The repository is owned and in-process. `EmailSender` is owned too, but it stands in for an email
gateway — an unmanaged dependency whose received messages a customer observes. Dependency-free on purpose.
"""


class EmailSender:
    """A port this codebase owns. Production wires it to the SMTP gateway customers' mail arrives from."""

    def send_confirmation(self, order_id):
        raise NotImplementedError


class InMemoryOrderRepo:
    def __init__(self):
        self._orders = {}

    def save(self, order):
        self._orders[order["id"]] = dict(order)

    def get(self, order_id):
        return self._orders.get(order_id)


class OrderService:
    def __init__(self, repo, mailer):
        self._repo = repo
        self._mailer = mailer

    def place(self, order_id, amount):
        order = {"id": order_id, "amount": amount, "status": "placed"}
        self._repo.save(order)
        self._mailer.send_confirmation(order_id)
        return order_id
