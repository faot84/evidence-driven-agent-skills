import unittest

from calculator import quote_total


class QuoteTotalTests(unittest.TestCase):
    def test_valid_discount(self):
        self.assertEqual(quote_total(1000, 10), 900)

    def test_negative_subtotal(self):
        with self.assertRaises(ValueError):
            quote_total(-1, 10)


if __name__ == "__main__":
    unittest.main()
