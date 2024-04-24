import unittest
import calendar


class TestCalendar(unittest.TestCase):
    def test_month(self):
        cal = calendar.month(2023, 1)
        print(type(cal))
        print(cal)


if __name__ == '__main__':
    unittest.main()
