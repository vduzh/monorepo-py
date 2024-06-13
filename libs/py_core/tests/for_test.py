import unittest


class TestFor(unittest.TestCase):
    def setUp(self):
        self.A = 3
        self.B = 6
        self.C = 10

    def test_for_in_range(self):
        for i in range(6):
            self.assertIn(i, [0, 1, 2, 3, 4, 5])

        for i in range(1, 6):
            self.assertTrue(1 <= i <= 5)

        for i in range(1, 6, 2):
            self.assertIn(i, [1, 3, 5])

    def test_for_in_string(self):
        for s in "Hello!":
            self.assertIn(s, ["H", "e", "l", "o", "!"])


if __name__ == '__main__':
    unittest.main()
