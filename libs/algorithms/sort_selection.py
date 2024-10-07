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

    def test_task_max_indexes(self):
        data_set = [
            (5, [40, 30, 20, 40, 20], "0 3 1 0 0"),
            (3, [1, 2, 3], "2 1 0"),
        ]

        for data in data_set:
            n, lst, expected_value = data

            # start of the task
            # n = int(input(""))
            # lst = [int(s) for s in input("").split()]

            # store indexes
            indexes = []
            for i in range(n):
                # select max value and its index
                max_value = lst[0]
                max_value_index = 0
                for j in range(1, len(lst)):
                    # check id the current value is max
                    if lst[j] > max_value:
                        # rewrite max value and its index
                        max_value = lst[j]
                        max_value_index = j

                # add the right index to the list
                indexes.append(max_value_index)

                # exchange the max value and the last value
                lst[max_value_index], lst[len(lst) - 1] = lst[len(lst) - 1], lst[max_value_index]

                # exclude the latest element from the list
                lst = lst[0: n - i - 1]

            # converts the indexes to the str
            res = " ".join([str(i) for i in indexes])
            # print the result
            print(res)
            # end of the task

            self.assertEqual(expected_value, res)
