import unittest

from model import get_llm


class TestLCEL(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._llm = get_llm()

    @classmethod
    def tearDownClass(cls):
        cls._llm = None

    def test_foo(self):
        pass


if __name__ == '__main__':
    unittest.main()
