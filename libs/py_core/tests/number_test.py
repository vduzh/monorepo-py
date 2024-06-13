import unittest


class TestNumbers(unittest.TestCase):
    def test_integer(self):
        num = 10
        self.assertTrue(isinstance(num, int))

    def test_float(self):
        num = 5.4
        self.assertTrue(isinstance(num, float))

    def test_operators(self):
        num = 6
        self.assertEqual(num ** 2, 36)

        self.assertEqual(num % 2, 0)
        self.assertEqual(num % 4, 2)

        self.assertEqual(num // 2, 3)
        self.assertEqual(num // 4, 1)



if __name__ == '__main__':
    unittest.main()
