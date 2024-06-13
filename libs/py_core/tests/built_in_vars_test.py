import unittest


class TestBuiltInVariables(unittest.TestCase):
    def test__name__(self):
        self.assertEqual("built_in_vars_test",  __name__)


if __name__ == '__main__':
    unittest.main()
