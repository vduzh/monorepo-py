import unittest


def factorial(n: int) -> int:
    if n == 0 or n == 1:
        return 1

    return n * factorial(n - 1)


class CombinatoricsTest(unittest.TestCase):

    def test_number_of_permutations(self):
        data_set = [
            (3, 6),
            (5, 120),
        ]

        for data in data_set:
            n, expected = data

            # start of the task
            # n = int(input(""))

            res = factorial(n)
            print(res)
            # end of the task

            self.assertEqual(expected, res)

    def test_number_of_arrangements(self):
        data_set = [
            (4, 2, 12),
        ]

        for data in data_set:
            n, k, expected = data

            # start of the task
            # n, k = [int(s) for s in input("").split()]

            res = factorial(n) // factorial(n - k)
            print(res)
            # end of the task

            self.assertEqual(expected, res)

    def test_number_of_combinations(self):
        data_set = [
            (4, 2, 6),
        ]

        for data in data_set:
            n, k, expected = data

            # start of the task
            # n, k = [int(s) for s in input("").split()]

            res = factorial(n) // (factorial(n - k) * factorial(k))
            print(res)
            # end of the task

            self.assertEqual(expected, res)
