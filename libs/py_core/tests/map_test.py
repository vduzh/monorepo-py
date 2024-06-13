import unittest


class TestMap(unittest.TestCase):
    def test_map(self):
        lst = [1, 2, 3]
        res = list(map(lambda x: x * 2, lst))
        self.assertEqual(res, [2, 4, 6])


if __name__ == '__main__':
    unittest.main()
