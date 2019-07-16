import unittest
from fibonacci import fib


class FibTest(unittest.TestCase):
    def test_fibtest_positive(self):
        self.assertIsNotNone(fib(8))

    def test_fibtest_decimal(self):
        self.assertIsNotNone(fib(0.2))

    def test_fibtest_negative(self):
        self.assertIsNotNone(fib(-7))


if __name__ == '__main__':
    # run from commandline using python testfilename.py
    unittest.main()
