import unittest
from pathlib import Path


class TestPathlib(unittest.TestCase):
    def test_home_dir(self):
        home_dir = Path.home()

        print(home_dir)

        # file_path = home_dir / "example_directory" / "example_file.txt"
        # print(file_path)


if __name__ == '__main__':
    unittest.main()
