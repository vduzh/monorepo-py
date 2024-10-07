import unittest


class BubbleSort(unittest.TestCase):

    def test_bubble_search(self):
        def sort(lst: list[int]):
            for i in range(len(lst)):
                for j in range(i + 1, len(lst)):
                    if lst[i] > lst[j]:
                        lst[j], lst[i] = lst[i], lst[j]

        data = [1, 3, 4, 2]
        sort(data)
        self.assertEqual([1, 2, 3, 4], data)
