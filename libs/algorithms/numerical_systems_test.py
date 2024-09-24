import unittest


def from_decimal(value: int, base: int) -> str:
    res = ""
    while value > 0:
        # calculate remainder from dividing value by base
        reminder = value % base
        # handle reminder
        res = str(reminder) + res
        # divide value by base without a remainder
        value = value // base
    return res


def to_decimal(value: str, base: int) -> int:
    res = 0
    for i in range(len(value)):
        # digit
        digit = int(value[i])
        # digit index
        digit_index = len(value) - i - 1
        # calculate and add to the res
        res += digit * base ** digit_index
    return res


class TestNumericalSystems(unittest.TestCase):

    def test_from_decimal(self):
        self.assertEqual("1100100", from_decimal(100, 2))
        self.assertEqual("210154", from_decimal(10996, 16))

    def test_to_decimal(self):
        self.assertEqual(0, to_decimal("0", 2))
        self.assertEqual(1, to_decimal("01", 2))
        self.assertEqual(2, to_decimal("10", 2))
        self.assertEqual(3, to_decimal("11", 2))
        self.assertEqual(100, to_decimal("1100100", 2))

    def test_binary_ones_count(self):
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

    def test_calculate(self):
        def calculate(value_1: str, value_2: str, base: int = 3) -> int:
            return to_decimal(value_1, base) + to_decimal(value_2, base)

        self.assertEqual(2, calculate('1', '1'))
        self.assertEqual(17, calculate('20', '102'))

    def test_bit_reverse(self):

        def b(value: int) -> int:
            return to_decimal(from_decimal(value, 2)[::-1], 2)

        self.assertEqual(1, b(4))
        self.assertEqual(3, b(6))
