import os
import unittest


class TestOs(unittest.TestCase):
    def test_name(self):
        value = os.name
        print(value)

    def test_path_expanduser(self):
        str_value = os.path.expanduser('~')
        print("user home:", str_value)

    def test_path_abspath(self):
        file_dir_name = os.path.abspath(__file__)
        print("Abs path:", file_dir_name)

    def test_path_dirname(self):
        file_dir_name = os.path.dirname(__file__)
        print("Dir name:", file_dir_name)

    def test_path_basename(self):
        base_name = os.path.basename(__file__)
        print("Base name:", base_name)

    def test_urandom(self):
        value = os.urandom(10)
        print(value)

    if __name__ == '__main__':
        unittest.main()
