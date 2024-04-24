import os
import unittest


class TestOs(unittest.TestCase):
    def test_path(self):
        value = os.name
        print(value)

    def test_urandom(self):
        value = os.urandom(10)
        print(value)

    if __name__ == '__main__':
        unittest.main()
