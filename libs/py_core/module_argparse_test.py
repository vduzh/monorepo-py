import unittest
import argparse


class TestArgparse(unittest.TestCase):
    def test_parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--task", default="return a list of numbers")
        parser.add_argument("--language", default="python")

        args = parser.parse_args()

        self.assertEqual("return a list of numbers", args.task)
        self.assertEqual("python", args.language)


if __name__ == '__main__':
    unittest.main()
