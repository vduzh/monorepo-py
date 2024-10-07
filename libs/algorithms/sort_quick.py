import random
import unittest

from libs.algorithms.util.timed import timed_func


class QuickSort(unittest.TestCase):

    def test_sort(self):
        def quick_sort(lst: list[int]):
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
                    quick_sort(less) +  # sort the 'less' values
                    equal +  # add the equal values to the sorted 'less' values
                    quick_sort(greater)  # add the sorted 'greater' values
            )

        self.assertEqual([1, 2, 3, 4], quick_sort([1, 3, 4, 2]))
        self.assertEqual([2, 5, 7], quick_sort([7, 2, 5]))

        timed_func(
            quick_sort,
            [random.randint(1, 10_000) for i in range(500_000)]
        )
