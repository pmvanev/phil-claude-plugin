import unittest

from tally import total


class TotalTest(unittest.TestCase):
    def test_sums_the_last_column_of_every_ledger(self):
        self.assertEqual(total(["rent 10\nfood 2.5\n", "fuel 1\n"]), 13.5)


if __name__ == "__main__":
    unittest.main()
