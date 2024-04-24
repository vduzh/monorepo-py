import itertools
import unittest


class TestItertools(unittest.TestCase):
    DAYS = ["Monday", "Tuesday", "Wednesday"]

    def test_cycle(self):
        cycle_days = itertools.cycle(self.DAYS)
        self.assertEqual(next(cycle_days), self.DAYS[0])
        self.assertEqual(next(cycle_days), self.DAYS[1])
        self.assertEqual(next(cycle_days), self.DAYS[2])

        self.assertEqual(next(cycle_days), self.DAYS[0])

    def test_count(self):
        counter = itertools.count(100, 10)

        self.assertEqual(next(counter), 100)
        self.assertEqual(next(counter), 110)
        self.assertEqual(next(counter), 120)

    def test_accumulate(self):
        prices = [10, 5, 30, 20]
        acc = itertools.accumulate(prices)

        self.assertEqual(next(acc), 10)
        self.assertEqual(next(acc), 15)
        self.assertEqual(next(acc), 45)
        self.assertEqual(next(acc), 65)

        acc = itertools.accumulate(prices, max)

        self.assertEqual(next(acc), 10)
        self.assertEqual(next(acc), 10)
        self.assertEqual(next(acc), 30)
        self.assertEqual(next(acc), 30)

    def test_group_by(self):
        data = [1, 2, 2, 3, 4, 4, 4, 5, 1]
        for i, j in itertools.groupby(data):
            print(i, list(j))


if __name__ == '__main__':
    unittest.main()
