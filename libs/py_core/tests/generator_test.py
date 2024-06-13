import unittest


class TestGenerator(unittest.TestCase):
    # [] - generator
    # [expr] - expression to create a value of a list
    # [expr for] - for points to values used to create new value
    # [expr for values] - sources values
    def test_generator(self):
        lst = [1, 2, 3]
        res = [x * 2 for x in lst]
        self.assertEqual(res, [2, 4, 6])

    # [expr for values if boolean_expr] - filters the sources values
    def test_with_if(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        res = [x for x in lst if x % 2 == 0]
        self.assertEqual(res, [2, 4, 6, 8, 10])

    def test_pairs(self):
        lst1 = [0, 1, 2, 3]
        lst2 = [4, 5, 6, 7]

        pairs = [(n1, n2) for n1 in lst1 if n1 % 2 == 0 for n2 in lst2 if n2 % 2 != 0]
        print(pairs)

    def test_inner_generators(self):
        lst = [[i for i in range(j)] for j in range(5)]
        print(lst)

    def test_set(self):
        lst = [1, 2, 2, 4]
        res_set = {i * 2 for i in lst}
        self.assertEqual(len(res_set), 3)

    def test_string(self):
        string = 'The quick brown fox jumps over the lazy dog'
        res_set = {s.upper() for s in string if not s.isspace()}
        print(res_set)

    def test_dict(self):
        src = [1, 2, 3]
        res = {"id_{}".format(i): i * 10 for i in src}
        print(res)



if __name__ == '__main__':
    unittest.main()
