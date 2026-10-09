import json
from pathlib import Path
from unittest.mock import Mock

from invoice import Invoice, ReceiptMailer


def test_total_matches_recorded_case():
    case = json.loads((Path(__file__).parent / "invoice_cases.json").read_text())
    invoice = Invoice(case["customer"], case["lines"])
    assert invoice.total == case["expected_total"]


def test_each_line_contributes_to_total():
    lines = [(10, 2), (5, 0), (3, 1)]
    for i in range(len(lines)):
        invoice = Invoice("acme", lines[: i + 1])
        if lines[i][1] == 0:
            assert invoice.total == Invoice("acme", lines[:i]).total
        else:
            assert invoice.total > Invoice("acme", lines[:i]).total


def test_invoice_records_customer_and_total():
    invoice = Invoice("acme", [(10, 3)])
    assert repr(invoice) == "Invoice(acme, 30)"


def test_paying_sends_a_receipt():
    mailer = Mock(spec=ReceiptMailer)
    invoice = Invoice("acme", [(10, 3)])
    invoice.pay(mailer)
    mailer.send_receipt.assert_called_once_with("acme", 30)
