import unittest

from accessify import private
from accessify.errors import InaccessibleDueToItsProtectionLevelException


class TestAccessifyModule(unittest.TestCase):
    def test_private(self):
        class Point:
            @private
            @staticmethod
            def validate(value):
                # private method
                if type(value) not in (int, float):
                    raise ValueError(f"Invalid value {value}. Expected int or float")

        with self.assertRaises(InaccessibleDueToItsProtectionLevelException):
            Point.validate(5)


if __name__ == '__main__':
    unittest.main()
