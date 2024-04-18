import unittest
from pprint import pprint


class TestTemplate(unittest.TestCase):

    def test_foo(self):
        pprint("Testing foo")
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
