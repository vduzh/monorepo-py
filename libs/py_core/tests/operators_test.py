import unittest


class TestOperators(unittest.TestCase):
    def test_compare(self):
        self.assertTrue(5 == 5)
        self.assertTrue(5 != 4)

    def test_logical(self):
        self.assertTrue(5 == 5 and 3 == 3)
        self.assertTrue(5 == 5 or 4 == 3)


if __name__ == '__main__':
    unittest.main()
