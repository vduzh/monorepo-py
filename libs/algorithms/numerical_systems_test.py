import unittest


class TestNumericalSystems(unittest.TestCase):

    def test_decimal_to_other_base(self):
        def convert(value: int, base: int) -> str:
            res = ""
            while value > 0:
                # calculate remainder from dividing value by base
                reminder = value % base
                # handle reminder
                res = str(reminder) + res
                # divide value by base without a remainder
                value = value // base
            return res

        self.assertEqual("1100100", convert(100, 2))
        self.assertEqual("210154", convert(10996, 16))

    def test_other_base_to_decimal(self):
        def convert(value: str, base: int) -> str:
            res = 0
            for i in range(len(value)):
                # digit
                digit = int(value[i])
                # digit index
                digit_index = len(value) - i - 1
                # calculate and add to the res
                res += digit * base ** digit_index
            return res

        self.assertEqual(0, convert("0", 2))
        self.assertEqual(1, convert("01", 2))
        self.assertEqual(2, convert("10", 2))
        self.assertEqual(3, convert("11", 2))
        self.assertEqual(100, convert("1100100", 2))

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

    def test_bit_reverse(self):

        def b(value: int, base: int = 2) -> int:
            bits = ""
            while value > 0:
                bits += str(value % base)
                value = value // base

            res = 0
            for i in range(len(bits)):
                value = bits[len(bits) - 1 - i]
                res += int(value) * base ** i
            return res

        self.assertEqual(1, b(4))
        self.assertEqual(3, b(6))
