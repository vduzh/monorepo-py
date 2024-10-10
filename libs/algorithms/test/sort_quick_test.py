import random
import unittest

from libs.algorithms.util.timed import timed_func

data_set = (
    ([7], [7]),
    ([2, 7], [2, 7]),
    ([7, 2], [2, 7]),
    ([8, 8, 1, 4, 3, 2, 7, 1], [1, 1, 2, 3, 4, 7, 8, 8]),
    ([1, 4, 3, 2, 7], [1, 2, 3, 4, 7]),
    ([7, 2, 5], [2, 5, 7]),
    ([7, 2, 5, 8], [2, 5, 7, 8]),
    ([7, 7], [7, 7]),
)


class QuickSort(unittest.TestCase):

    def test_sort(self):
        def quick_sort(lst: list[int], left: int, right: int):
            if left < right:
                # calculate the value in the middle of the list
                middle = lst[(left + right) // 2]

                # split the list into two parts such that the left part is less than or equal to the right part
                i, j = left, right
                while i <= j:
                    # find the first element in the left part that is greater than or equal to the middle value
                    while lst[i] < middle:
                        i += 1
                    # find the first element in the right part that is less than or equal to the middle value
                    while lst[j] > middle:
                        j -= 1

                    # check if there are elements on both sides to swap
                    if i <= j:
                        # swap two elements
                        lst[i], lst[j] = lst[j], lst[i]
                        # move to the next element on the left
                        i += 1
                        # move to the next element on the right
                        j -= 1

                # sort the left part of the list
                quick_sort(lst, left, j)
                # sort the right part of the list
                quick_sort(lst, i, right)

            return lst

        for data in data_set:
            test_data, expected = data
            self.assertEqual(expected, quick_sort(test_data, 0, len(test_data) - 1))

        big_n = 1_000_000
        timed_func(
            quick_sort,
            [random.randint(1, 10_000) for i in range(big_n)],
            0, big_n - 1
        )

    def test_sort_simplified(self):
        def quick_sort_simplified(lst: list[int]):
            if len(lst) <= 1:
                return lst

            # calculate the medium value
            mid = lst[len(lst) // 2]

            # find all the values that less than mid
            less = [i for i in lst if i < mid]
            # find all the values that equal to mid
            equal = [i for i in lst if i == mid]
            # find all the values that greater than mid
            greater = [i for i in lst if i > mid]

            return (
                    quick_sort_simplified(less) +  # sort the 'less' values
                    equal +  # add the equal values to the sorted 'less' values
                    quick_sort_simplified(greater)  # add the sorted 'greater' values
            )

        for data in data_set:
            test_data, expected = data
            self.assertEqual(expected, quick_sort_simplified(test_data))

        big_n = 1_000_000
        timed_func(
            quick_sort_simplified,
            [random.randint(1, 10_000) for i in range(big_n)]
        )
