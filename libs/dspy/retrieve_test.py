import unittest
from pprint import pprint


class TestRetrieve(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._foo = "foo"

    @classmethod
    def tearDownClass(cls):
        cls._foo = None

    def setUp(self):
        self._bar = "bar"

    def tearDown(self):
        self._bar = None

    def test_foo(self):
        # pprint("Testing foo")
        # self.assertTrue(True)
        raise NotImplementedError()


if __name__ == '__main__':
    unittest.main()
