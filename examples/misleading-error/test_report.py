import json
from pathlib import Path
import unittest

from report import average_paid_amount, summary


HERE = Path(__file__).resolve().parent


def load_orders():
    return json.loads((HERE / "orders.json").read_text(encoding="utf-8"))


class ReportTest(unittest.TestCase):
    def test_summary_uses_every_paid_order(self):
        self.assertEqual(summary(load_orders()), "Average paid order: 50.00")

    def test_upper_case_status_still_counts(self):
        orders = [{"id": 9, "status": "PAID", "amount": 10.0}]
        self.assertEqual(average_paid_amount(orders), 10.0)


if __name__ == "__main__":
    unittest.main()
