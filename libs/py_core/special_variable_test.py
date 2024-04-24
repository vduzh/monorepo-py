import unittest


class TestSpecialVariable(unittest.TestCase):
    def test__file__(self):
        # contains the module’s path
        print(__file__)


if __name__ == '__main__':
    unittest.main()
