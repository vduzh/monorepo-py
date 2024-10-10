import math
import unittest

DATA = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
    13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
    25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
    37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
    49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
    61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72,
    73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84,
    85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96,
    97, 98, 99, 100
]


class TestBinarySearch(unittest.TestCase):

    def test_binary_search_complexity(self):
        self.assertEqual(7, math.ceil(math.log2(100)))
        self.assertEqual(4, math.ceil(math.log2(10)))
        self.assertEqual(63, math.ceil(math.log2(5 * 10 ** 18)))

    def test_search_ints(self):
        def search(left: int, right: int, target: int):
            while left < right:
                # find the middle position
                mid = (left + right) // 2

                # check the middle and correct either the left or the right position
                if target > mid:
                    # correct the left position as the result is on the right side
                    left = mid + 1
                else:
                    # correct the right position as the result is on the left side
                    right = mid
            # now left == mid == right
            return left

        for gess_num in [3, 2, 5, 9]:
            self.assertEqual(gess_num, search(2, 9, gess_num))

    def test_search_in_int_list(self):
        def search(numbers: list[int], target: int) -> int:
            # init the left and right positions
            left = 0
            right = len(numbers) - 1

            # walking through the positions
            while left < right:
                # find the middle position
                mid = (left + right) // 2

                # get the value at the middle positions
                mid_value = numbers[mid]

                if target > mid_value:
                    left = mid + 1
                else:
                    right = mid
            target_index = left

            return target_index

        self.assertEqual(86, search(DATA, 87))
        self.assertEqual(10, search(DATA, 11))

    def test_search_floats(self):
        def search(left: float, right: float, eps: float, target: float):
            while left < right:
                mid = (left + right) / 2

                if (target - mid) > eps:
                    left = mid
                elif (mid - target) > eps:
                    right = mid
                else:
                    left = right = mid

            # print(f"target: {target}, left: {left}, eps: {round(target - left, 2)}")
            return left

        eps_value = 0.5
        for gess_num in [3.0, 2.1, 3.4, 7.1, 8.8]:
            self.assertTrue(
                gess_num,
                abs(search(2.0, 9.0, eps_value, gess_num) - gess_num) <= eps_value
            )

    def test_search_in_float_list(self):
        def search(numbers: list[float], target: float) -> int:
            left = 0
            right = len(numbers) - 1

            while left < right:
                mid = (left + right) // 2

                mid_value = numbers[mid]

                if target > mid_value:
                    left = mid + 1
                else:
                    right = mid
            target_index = left

            return target_index

        self.assertEqual(86, search(DATA, 87.0))
        self.assertEqual(10, search(DATA, 11.00))

    def test_search_in_float_lis(self):
        def search(numbers: list[float], target: float) -> int:
            left = 0
            right = len(numbers) - 1

            while left < right:
                mid = (left + right) // 2

                mid_value = numbers[mid]

                if target > mid_value:
                    left = mid + 1
                else:
                    right = mid
            target_index = left

            return target_index

        self.assertEqual(86, search(DATA, 87.0))
        self.assertEqual(10, search(DATA, 11.00))

    def test_task_min_time_to_copy(self):
        data_set = [
            (4, 1, 1, 3),
            (5, 1, 2, 4),
            (30, 2, 3, 38),
            (135, 2, 5, 194),
            (173, 3, 5, 327),
        ]

        for data in data_set:
            n, x, y, expected_value = data

            # start of the task
            # n, x, y = [int(s) for s in input("").split()]

            res = 0
            if n == 1:
                res = min(x, y)
            else:
                # make first copy
                res = min(x, y)

                # make n-1 copies
                left = 0
                right = max(x, y) * (n - 1)
                while left < right:
                    mid = (left + right) // 2
                    # calculate the number of copies after mid seconds
                    copies_count = mid // x + mid // y

                    # check if we need more copies
                    if n - 1 > copies_count:
                        # yes -> find the better time at the right
                        left = mid + 1
                    else:
                        # now -> find the better time at the left
                        right = mid

                # left = mid = right at the end of the loop
                # add found time to the res
                res += left
            print(res)
            # end of the task

            self.assertEqual(expected_value, res)

    def test_task_max_length(self):
        data_set = [
            (2, 2, 2, 2, 2),
            (10, 10, 0, 0, 3),
            (2, 1, 7, 1, 1),
        ]

        for data in data_set:
            a_1, a_2, a_3, a_4, expected_value = data

            # start of the task
            # a_1, a_2, a_3, a_4 = [int(s) for s in input("").split()]

            # calculate the number of squares
            squares_count = min(a_1, a_2) + min(a_3, a_4)

            max_length = 0
            # init
            left = 0
            right = squares_count
            while left < right:
                # choose the possible length as the middle
                mid = (left + right) // 2
                # calculate the number of squares to build the squares with the side of the mid length
                required_squares_count = mid ** 2

                if squares_count >= required_squares_count:
                    # save mid as possible result
                    max_length = mid
                    # correct left to try to find a better length
                    left = mid + 1
                else:
                    # correct right to try to find a better length
                    right = mid

            print(max_length)
            # end of the task

            self.assertEqual(expected_value, max_length)