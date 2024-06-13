import re
import unittest


class TestRe(unittest.TestCase):
    def test_match(self):
        match = re.match("Hello[ \t]*(.*)world", "Hello   Python world")
        res = match.group(1)
        print(res)
        raise NotImplementedError()


if __name__ == '__main__':
    unittest.main()
