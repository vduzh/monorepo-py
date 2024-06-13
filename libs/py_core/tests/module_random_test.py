import random
import string
import unittest


class TestRandom(unittest.TestCase):

    def test_random(self):
        self.assertTrue(0 <= random.random() <= 1)

    def test_uniform(self):
        self.assertTrue(1 <= random.uniform(1, 100) <= 100)

    def test_int(self):
        self.assertTrue(1 <= random.randint(1, 100) <= 100)

    def test_randrange(self):
        value = random.randrange(1, 100, 2)
        self.assertTrue(1 <= value <= 99)
        self.assertEqual(value % 2, 1)

    def test_seed(self):
        random.seed(1)
        value1 = random.random()
        value2 = random.random()

        random.seed(1)
        value3 = random.random()
        value4 = random.random()

        self.assertEqual(value1, value3)
        self.assertEqual(value2, value4)

    def test_seed(self):
        colors = ['red', 'green', 'blue']
        res = random.choices(colors, k=10)
        print(res)
        self.assertEqual(len(res), 10)

        weights = [30, 2, 15]
        res = random.choices(colors, weights, k=10)
        print(res)
        self.assertEqual(len(res), 10)

    if __name__ == '__main__':
        unittest.main()
