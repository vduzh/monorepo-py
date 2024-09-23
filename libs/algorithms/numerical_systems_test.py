import unittest


class TestNumericalSystems(unittest.TestCase):

    def test_decimal_to_oter(self):
        def convert(value: int, base: int) -> str:
            res = ""
            while value > 0:
                res = str(value % base) + res
                value = value // base
            return res

        self.assertEqual("1100100", convert(100, 2))
        self.assertEqual("210154", convert(10996, 16))

    def test_decimal_to_binary_ones_count(self):
        def ones_count(value: int, base: int = 2) -> int:
            count = 0
            while value > 0:
                if value % base:
                    count += 1
                value = value // base
            return count

        self.assertEqual(2, ones_count(5))
        self.assertEqual(3, ones_count(7))

    def test_diff(self):
        def diff(value: int, base: int) -> int:
            m = 1
            s = 0
            while value > 0:
                m *= value % base
                s += value % base
                value = value // base
            return m - s

        self.assertEqual(90, diff(239, 8))
        self.assertEqual(-34, diff(1000000000, 7))
