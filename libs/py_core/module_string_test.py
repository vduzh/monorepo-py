import string
import unittest


class TestString(unittest.TestCase):
    def test_string(self):
        print(string.ascii_letters)
        print(string.punctuation)
        print(string.hexdigits)
        print(string.digits)

    def test_join_with_generators(self):
        res = "".join([c for c in 'One1Two' if c in string.ascii_letters])
        self.assertEqual(res, 'OneTwo')


if __name__ == '__main__':
    unittest.main()
