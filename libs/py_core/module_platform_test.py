import platform
import unittest


class TestPlatform(unittest.TestCase):
    def test_path(self):
        value = platform.system()
        print(value)

if __name__ == '__main__':
    unittest.main()
