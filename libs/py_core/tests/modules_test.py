import datetime as dt
import time
import unittest
from math import sqrt, ceil

import cowsay
import emoji

# from projects.py_core.module_custom_in_file import custom_func, CustomClass
from module_custom_in_file import custom_func, CustomClass


class TestModule(unittest.TestCase):
    def test_foo(self):
        value = time.time()

    def test_alias(self):
        value = dt.time()

    def test_import_some_functions(self):
        value = sqrt(9)
        self.assertEqual(value, 3)

        value = ceil(1.2)
        self.assertEqual(value, 2)

    def test_custom_module(self):
        value = custom_func("John")
        ojb = CustomClass("Jane")
        self.assertEqual(value, "John")
        self.assertEqual(ojb.value, "Jane")

    def test_pip_lib(self):
        cowsay.cow('Hello')
        print(emoji.emojize('Python is :thumbs_up:'))

    if __name__ == '__main__':
        unittest.main()
