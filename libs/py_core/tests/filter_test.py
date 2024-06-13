import unittest


class TestFilter(unittest.TestCase):
    def test_filter(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        res = list(filter(lambda x: x % 2 == 0, lst))
        self.assertEqual(res, [2, 4, 6, 8, 10])

        res = list(filter(lambda x: x % 2 != 0, lst))
        self.assertEqual(res, [1, 3, 5, 7, 9])


if __name__ == '__main__':
    unittest.main()
