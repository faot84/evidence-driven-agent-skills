import unittest

from app import format_label


class LabelTests(unittest.TestCase):
    def test_name_has_initial_capital(self):
        self.assertEqual(format_label("  ALPHA  "), "Alpha")


if __name__ == "__main__":
    unittest.main()
