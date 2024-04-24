import unittest
from pprint import pprint


class TestString(unittest.TestCase):
    def setUp(self):
        self.STR = "Hello World!"
        self.STR_2 = 'The quick brown fox jumps over the lazy dog'

    def test_multiline(self):
        s1 = "Foo\
            Bar"

        s1 = "Foo\n\
            Bar"

    def test_sum(self):
        # concatenate (polymorphism)
        self.assertEqual("FooBar", "Foo" + "Bar")
        # multiply
        self.assertEqual("=" * 3, "===")

        with self.assertRaises(TypeError):
            "=" + 1

    def test_str(self):
        self.assertEqual(str(3), "3")

    def test_as_list(self):
        self.assertEqual(self.STR[1], "e")
        self.assertEqual(self.STR[-1], "!")
        self.assertEqual(self.STR[len(self.STR) - 1], "!")
        self.assertEqual(self.STR[1:3], "el")
        self.assertEqual(self.STR[6:], "World!")  # [6:len(s)]
        self.assertEqual(self.STR[:5], "Hello")  # [0:5]
        self.assertEqual(self.STR[:], "Hello World!")  # [0:len(s)]
        self.assertEqual(self.STR.count("l"), 3)

    def test_immutable(self):
        with self.assertRaises(TypeError):
            self.STR[0] = "Q"

    def test_len(self):
        self.assertEqual(len(self.STR), 12)

    def test_dir(self):
        pprint(dir(self.STR))

    def test_upper(self):
        self.assertEqual("Test".upper(), "TEST")
        self.assertFalse("Test".isupper())

    def test_lower(self):
        self.assertTrue("test".islower())
        self.assertFalse("Test".islower())

    def test_capitalize(self):
        self.assertEqual("hello world".capitalize(), "Hello world")

    def test_find(self):
        self.assertEqual(self.STR.find("e"), 1)
        self.assertEqual(self.STR.find("x"), -1)

    def test_split(self):
        s = "One,Two,Three"
        lst = s.split(",")
        self.assertEqual(lst, ["One", "Two", "Three"])

        s = "One1, Two1, Three1"
        lst = s.split(", ")
        self.assertEqual(lst, ["One1", "Two1", "Three1"])

    def test_join(self):
        s = ", ".join(["One", "Two", "Three"])
        self.assertEqual(s, "One, Two, Three")

    def test_slice(self):
        s = "Hello World!"
        self.assertEqual(s[0:5], "Hello")
        self.assertEqual(s[1:2], "e")
        self.assertEqual(s[6:], "World!")

        # negative
        self.assertEqual(s[6:-1], "World")

        # step
        self.assertEqual(s[0:5:1], "Hello")
        self.assertEqual(s[0:5:2], "Hlo")
        self.assertEqual(s[0::2], "HloWrd")
        self.assertEqual(s[0:-1:2], "HloWrd")
        self.assertEqual(s[::-1], "!dlroW olleH")

    def test_format(self):
        s = "home"
        age = 2

        res = f"{s} {age}!"
        self.assertEqual(res, "home 2!")

        # with percentage (outdated)
        res = "%s %02d!" % (s, age)
        self.assertEqual(res, "home 02!")

        res = "%.1f" % (.1 + .2)
        self.assertEqual(res, "0.3")

        # with format (preferred)
        res = "Hello {}! Your age is {:02}.".format(s, age)
        self.assertEqual(res, "Hello home! Your age is 02.")

        res = "Hello {1}! Your age is {0:02}.".format(age, s)
        self.assertEqual(res, "Hello home! Your age is 02.")

        res = "Hello {s}! Your age is {age:02}.".format(s=s, age=age)
        self.assertEqual(res, "Hello home! Your age is 02.")

    def test_unpacking(self):
        (*data,) = "Hello"
        self.assertEqual(data, ['H', 'e', 'l', 'l', 'o'])

    def test_clone(self):
        s = "Hello"

        lst = list(s)  # (*lst,) = s
        lst[0] = "h"
        s2 = "".join(lst)
        self.assertEqual("hello", s2)

        # b = bytearray(b"Hello")
        # lst[0] = "h"
        # s2 = "".join(lst)
        # self.assertEqual("hello", s2)

    def test_generator(self):
        s1 = "Hello"
        s2 = "123"
        s3 = "12a"

        self.assertTrue(all([c.isalpha() for c in s1]))
        self.assertTrue(all([c.isnumeric() for c in s2]))
        self.assertFalse(all([c.isnumeric() for c in s3]))


if __name__ == '__main__':
    unittest.main()
