import unittest


class TestList(unittest.TestCase):
    def setUp(self):
        self.NUMBERS = [1, 3, 6, 7, 10]

    def test_create(self):
        lst = list([1, 2])
        self.assertEqual(lst, [1, 2])

        # unpacking
        lst = list((*[1, 2], *[3, 4]))
        self.assertEqual(lst, [1, 2, 3, 4])

        # list comprehension
        fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
        lst = [x for x in fruits if "a" in x]
        self.assertEqual(["apple", "banana", "mango"], lst)

    def test_list(self):
        lst = list(range(1, 4))
        self.assertEqual(lst, [1, 2, 3])

    def test_print(self):
        print(self.NUMBERS)

    def test_len(self):
        self.assertEqual(len(self.NUMBERS), 5)

    def test_get_element(self):
        self.assertEqual(self.NUMBERS[1], 3)
        self.assertEqual(self.NUMBERS[3], 7)

        self.assertEqual(self.NUMBERS[-1], 10)
        self.assertEqual(self.NUMBERS[-3], 6)

    def test_unpacking(self):
        one, three, six, seven, ten = self.NUMBERS

        self.assertEqual(one, 1)
        self.assertEqual(three, 3)
        self.assertEqual(six, 6)
        self.assertEqual(seven, 7)
        self.assertEqual(ten, 10)

        one, three, *rest = self.NUMBERS
        self.assertEqual(one, 1)
        self.assertEqual(three, 3)
        self.assertEqual(rest, [6, 7, 10])

        one, *rest, ten = self.NUMBERS
        self.assertEqual(one, 1)
        self.assertEqual(rest, [3, 6, 7])
        self.assertEqual(ten, 10)

        print(*self.NUMBERS)

        lst1 = [1, 2]
        lst2 = [3, 4]
        self.assertEqual([*lst1, lst2], [1, 2, 3, 4])

    def test_operators(self):
        lst = [1, 2, 3] + [4, 5]
        self.assertEqual(lst, [1, 2, 3, 4, 5])

    def test_modify_element(self):
        lst = [1, 2]
        lst[0] = 10
        self.assertEqual(lst, [10, 2])

    def test_add_element(self):
        lst = [1, 2]
        lst.append(10)
        self.assertEqual(lst, [1, 2, 10])

        lst = [1, 2]
        lst.insert(1, 99)
        self.assertEqual(lst, [1, 99, 2])

        lst = [1, 2]
        lst.extend([11, 13])
        self.assertEqual(lst, [1, 2, 11, 13])

        lst = [1, 2]
        ext = [10] * 3
        lst.extend(ext)
        self.assertEqual([1, 2, 10, 10, 10], lst)

        # if key >= len(self.marks):
        #     # extend the marks list
        #     off = key + 1 - len(self.marks)
        #     self.marks.extend([None] * off)

    def test_delete_element(self):
        lst = self.NUMBERS.copy()

        lst.pop()
        self.assertEqual(lst, [1, 3, 6, 7])

        lst.pop(0)
        self.assertEqual(lst, [3, 6, 7])

        lst.pop(-2)
        self.assertEqual(lst, [3, 7])

        lst = self.NUMBERS.copy()
        lst.remove(3)
        self.assertEqual(lst, [1, 6, 7, 10])

        lst.clear()
        self.assertEqual(lst, [])

        # using del - it is correct operation
        lst = [1, 2, 3]
        del lst[1]
        self.assertEqual([1, 3], lst)

    def test_count(self):
        self.assertEqual(self.NUMBERS.count(6), 1)

        lst = [6]
        lst.extend(self.NUMBERS)
        self.assertEqual(lst.count(6), 2)

    def test_sort(self):
        lst = [3, 1, 2]
        lst.sort()
        self.assertEqual(lst, [1, 2, 3])

    def test_reverse(self):
        lst = [3, 1, 2]
        lst.reverse()
        self.assertEqual(lst, [2, 1, 3])

    def test_multy_types(self):
        lst = [1, "one", True]
        print(lst)

    def test_for(self):
        for item in self.NUMBERS:
            item *= 2
            print(item)

        for i, el in enumerate(self.NUMBERS):
            print(i, "-", el)

    def test_slice(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(lst[1:-1:2], [2, 4, 6, 8])
        self.assertEqual(lst[8:], [9, 10])
        self.assertEqual(lst[-2:], [9, 10])

    def test_list_comprehension(self):
        fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
        lst = [x for x in fruits if "a" in x]
        self.assertEqual(["apple", "banana", "mango"], lst)

        s1 = "spam"
        s2 = "scam"
        lst = [s for s in s1 if s in s2]
        self.assertEqual(["s", "a", "m"], lst)

    def test_clean_list_and_copy_from_another_list(self):
        lst = [1, 2, 3]
        lst_id = id(lst)
        lst[:] = [10, 20, 30]
        lst_id_2 = id(lst)
        self.assertEqual(lst_id, lst_id_2)
        self.assertEqual([10, 20, 30], lst)

        lst = [1, 2, 3]
        lst[:] = [10, 20]
        self.assertEqual([10, 20], lst)


if __name__ == '__main__':
    unittest.main()
