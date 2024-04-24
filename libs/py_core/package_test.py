import unittest

from custom_package.bar_module import bar_func
from custom_package.foo_module import foo_func
from custom_package_2 import foo_value, bar_value


class TestPackage(unittest.TestCase):
    def test_foo_func(self):
        self.assertEqual("Foo", foo_func())

    def test_bar_func(self):
        self.assertEqual("Bar", bar_func())

    def test_foo_value(self):
        self.assertEqual("Foo", foo_value)

    def test_bar_value(self):
        self.assertEqual("Bar", bar_value)


if __name__ == '__main__':
    unittest.main()
