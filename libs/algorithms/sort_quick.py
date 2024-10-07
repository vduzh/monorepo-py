import unittest


class QuickSort(unittest.TestCase):

    def test_sort(self):
        def quick_sort(lst: list[int]):
            if len(lst) <= 1:
                return lst

            mid = lst[len(lst) // 2]

            less = [i for i in lst if i < mid]
            equal = [i for i in lst if i == mid]
            greater = [i for i in lst if i > mid]

            return quick_sort(less) + equal + quick_sort(greater)

        self.assertEqual([1, 2, 3, 4], quick_sort([1, 3, 4, 2]))
        self.assertEqual([2, 5, 7], quick_sort([7, 2, 5]))
