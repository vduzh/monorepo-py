import unittest


class SelectionSort(unittest.TestCase):

    def test_sort(self):
        def selection_sort(lst: list[int]):
            for i in range(len(lst)):
                for j in range(i + 1, len(lst)):
                    if lst[i] > lst[j]:
                        lst[j], lst[i] = lst[i], lst[j]

        data = [1, 3, 4, 2]
        selection_sort(data)
        self.assertEqual([1, 2, 3, 4], data)

    def test_task_max_index(self):
        # TODO:
        data_set = [
            (5, [40, 30, 20, 40, 20], [0, 3, 1, 0, 0, ]),
        ]

        for data in data_set:
            n, lst, expected_value = data

            # start of the task
            # n = int(input(""))
            # lst = [int(s) for s in input("").split()]

            res = []
            for i in range(len(lst)):
                index = i
                for j in range(i + 1, len(lst)):
                    if lst[i] > lst[j]:
                        index = i
                        lst[j], lst[i] = lst[i], lst[j]
                res.append(index)

            print(res)
            # end of the task

            self.assertEqual(expected_value, res)
