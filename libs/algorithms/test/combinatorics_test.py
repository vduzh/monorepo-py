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

    def test_arrangements_hockey(self):
        data_set = [
            (3, 6),
            (20, 6840),
        ]

        for data in data_set:
            n, expected = data

            # start of the task
            # n = int(input(""))
            k = 3

            res = factorial(n) // factorial(n - k)
            print(res)
            # end of the task

            self.assertEqual(expected, res)

    def test_combinations_salads(self):
        """
        Task: https://acmp.ru/asp/do/index.asp?main=task&id_course=2&id_section=16&id_topic=21&id_problem=106
        """
        data_set = [
            (3, 4),
            (4, 11),
        ]

        for data in data_set:
            n, expected = data

            # start of the task
            # n = int(input(""))

            res = 0
            for k in range(2, n + 1):
                combinations = factorial(n) // (factorial(n - k) * factorial(k))
                res += combinations
            print(res)
            # end of the task

            self.assertEqual(expected, res)
