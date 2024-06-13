import unittest


class TestZip(unittest.TestCase):
    def test_zip(self):
        lst1 = [1, 2, 3]
        lst2 = ["a", "b", "c"]

        res = list(zip(lst1, lst2))
        self.assertEqual(res, [(1, 'a'), (2, 'b'), (3, 'c')])

    def test_iterate(self):
        lst1 = [1, 2, 3]
        lst2 = ["a", "b", "c"]

        for index, value in zip(lst1, lst2):
            print(f'{index} - {value}')

    def test_strict(self):
        lst1 = [1, 2, 3]
        lst2 = ["a", "b", "c", "d"]

        res = list(zip(lst1, lst2, strict=True))

        self.assertEqual(res, [(1, 'a'), (2, 'b'), (3, 'c')])

    def test_dict(self):
        lst1 = [1, 2, 3]
        lst2 = ["a", "b", "c"]

        res = dict(zip(lst2, lst1))

        self.assertEqual(res['a'], 1)
        self.assertEqual(res['b'], 2)
        self.assertEqual(res['c'], 3)

    def test_unzip(self):
        lst = [(1, 'a'), (2, 'b')]

        res1, res2 = zip(*lst)

        self.assertEqual(res1, (1, 2))
        self.assertEqual(res2, ('a', 'b'))


if __name__ == '__main__':
    unittest.main()
