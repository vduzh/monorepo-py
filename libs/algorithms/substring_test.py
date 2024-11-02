import unittest

class TestSubstring(unittest.TestCase):

    def test_foo(self):
        data_set = [
            ('ab', 2),
            ('abbc', 4),
            ('aabbbaa', 5),
        ]

        for data in data_set:
            s, expected_value = data

            res = 0
            for i in range(len(s)):
                c = s[i]
                # print("c:", c)

                # check if this symbol has been processed
                if c not in s[:i]:
                    for j in range(i, len(s)):
                        # print("slice:" + s[i:j+1])
                        if s[i:j + 1].count(c) == j - i + 1:
                            # print("found silce", s[i:j+1], "at", i, j)
                            res += 1
            self.assertEqual(expected_value, res)


