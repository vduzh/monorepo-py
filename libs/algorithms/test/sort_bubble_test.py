import unittest


class BubbleSort(unittest.TestCase):

    def test_sort(self):
        def bubble_sort(lst: list[int]):
            for i in range(len(lst)):
                for j in range(len(lst) - 1):
                    if lst[j] > lst[j + 1]:
                        lst[j], lst[j + 1] = lst[j + 1], lst[j]
            return lst

        self.assertEqual([1, 2, 3, 4], bubble_sort([1, 3, 4, 2]))

    def test_task_inversion_count(self):
        data_set = [
            (3, [7, 2, 5], 2),
            (10, [12, 7, 92, 5, 18, 4, 32, 48, 11, 74], 18),
        ]

        for data in data_set:
            n, lst, expected_value = data

            # start of the task
            # n = int(input(""))
            # lst = [int(s) for s in input("").split()]

            count = 0
            for i in range(len(lst)):
                for j in range(len(lst) - 1):
                    if lst[j] > lst[j + 1]:
                        lst[j], lst[j + 1] = lst[j + 1], lst[j]
                        count += 1

            print(count)
            # end of the task

            self.assertEqual(expected_value, count)
