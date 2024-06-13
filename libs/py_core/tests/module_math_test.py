import math
import unittest


class TestMath(unittest.TestCase):
    def test_ceil(self):
        n = 2.5
        self.assertEqual(math.ceil(n), 3)

    def test_floor(self):
        n = 2.5
        self.assertEqual(math.floor(n), 2)

    def test_sqrt(self):
        n = 121
        self.assertEqual(math.sqrt(n), 11)

    def test_sin(self):
        self.assertEqual(math.sin(math.pi/2), 1.0)

    if __name__ == '__main__':
        unittest.main()
