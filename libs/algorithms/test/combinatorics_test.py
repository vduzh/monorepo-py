import math
import unittest


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

            # res = math.perm(n, n)
            res = math.factorial(n)

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

            # res = math.perm(n, k)
            res = math.factorial(n) // math.factorial(n - k)
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

            # res = math.comb(n, k)
            res = math.factorial(n) // (math.factorial(n - k) * math.factorial(k))
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

            # res = math.factorial(n) // math.factorial(n - k)
            res = math.perm(n, k)
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
                # combinations = math.factorial(n) // (math.factorial(n - k) * math.factorial(k))
                combinations = math.comb(n, k)
                res += combinations
            print(res)
            # end of the task

            self.assertEqual(expected, res)

    def test_chess(self):
        """
        Task: https://acmp.ru/asp/do/index.asp?main=task&id_course=2&id_section=16&id_topic=21&id_problem=107
        """
        data_set = [
            (8, 8, 40320),
        ]

        for data in data_set:
            n, k, expected = data

            # start of the task
            # n, k = [int(s) for s in input("").split()]

            # all the options below are Ok
            # num_of_rows = math.factorial(n) // (math.factorial(n - k) * math.factorial(k))
            num_of_rows = math.comb(n, k)

            # all the options below are Ok
            # num_of_cells = math.factorial(n) // (math.factorial(n - k) * math.factorial(n - k))
            # num_of_cells = math.comb(n, k)
            num_of_cells = num_of_rows

            # all the options below are Ok
            # num_of_permutations = math.perm(k, k)
            num_of_permutations = math.factorial(k)

            # calculate
            res = num_of_rows * num_of_cells * num_of_permutations

            print(res)
            # end of the task

            self.assertEqual(expected, res)

    def test_cards(self):
        """
        Task: https://acmp.ru/asp/do/index.asp?main=task&id_course=2&id_section=16&id_topic=21&id_problem=108

        Topic: Arrangements with repetition
        """

        data_set = [
            ("solo", 12),
        ]

        for data in data_set:
            txt, expected = data

            # start of the task
            # txt = input("")

            # calculate the dividend first
            dividend = math.factorial(len(txt))

            # calculate the divider then
            divider = 1
            unique_chars = set(txt)
            for c in unique_chars:
                count = txt.count(c)
                divider *= math.factorial(count)

            # calculate the result
            res = dividend // divider

            print(res)
            # end of the task

            self.assertEqual(expected, res)
