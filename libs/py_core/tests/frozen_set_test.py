import unittest


class TestFrozenSet(unittest.TestCase):
    def setUp(self):
        self.SET = {1, 2, 3}

    def test_create(self):
        s = frozenset([1, 2, 2, 3])
        self.assertEqual(s, {1, 2, 3})


    if __name__ == '__main__':
        unittest.main()
