import unittest


class TestNone(unittest.TestCase):
    def test_None(self):
        _none = None
        self.assertEqual(_none, None)

    def test_check_for_None(self):
        _none = None
        self.assertTrue(_none is None)


if __name__ == '__main__':
    unittest.main()
