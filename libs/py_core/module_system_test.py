import sys
import unittest


class TestSystem(unittest.TestCase):
    def test_path(self):
        p = sys.path
        print(p)

    if __name__ == '__main__':
        unittest.main()
