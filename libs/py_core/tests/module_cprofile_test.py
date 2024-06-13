import unittest
import cProfile


class TestCProfile(unittest.TestCase):
    def test_(self):
        cProfile.run("20 * 100")


if __name__ == '__main__':
    unittest.main()
