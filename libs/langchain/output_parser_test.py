import unittest

from langchain_core.output_parsers import CommaSeparatedListOutputParser


class TestOutputParser(unittest.TestCase):
    def test_comma_separated_list_output_parser(self):
        output_parser = CommaSeparatedListOutputParser()
        str_list = output_parser.parse("one, two")
        self.assertEqual(str_list, ["one", "two"])


if __name__ == '__main__':
    unittest.main()
