import unittest
import gc
from sys import getrefcount


class TestDynamicTyping(unittest.TestCase):
    def test_ref_to_object(self):
        a_ref = 123
        print(getrefcount(123))

    def test_ref_to_objects_various_types(self):
        a_ref = 123
        a_ref = "test"
        a_ref = 1.5

        print(getrefcount(123))
        print(getrefcount("test"))
        print(getrefcount(1.5))

    def test_objects_have_types(self):
        # names do not have types only values

        self.assertEqual(int, type(123))
        self.assertEqual(str, type("test"))
        self.assertEqual(float, type(1.5))

    def test_shared_refs(self):
        a_ref = 123
        b_ref = a_ref

    def test_compare_objects_by_values(self):
        one = [1, 2]
        two = one
        three = [1, 2]

        self.assertTrue(one == two)
        self.assertTrue(one == three)
        self.assertTrue(two == three)

        x = 42
        y = 42
        self.assertTrue(x == y)

    def test_compare_objects_by_ref(self):
        one = [1, 2]
        two = one
        three = [1, 2]

        self.assertTrue(one is two)
        self.assertFalse(one is three)

    def test_compare_objects_by_ref_with_cache(self):
        x = 42
        y = 42
        self.assertTrue(x is y)

        x = "home"
        y = "home"
        self.assertTrue(x is y)


    def test_garbage_collector(self):
        a = 123
        a = "test"
        # the memory of the int object 123 will be cleared as there is no reference to it


if __name__ == '__main__':
    unittest.main()
