import configparser
import unittest


class TestConfigParser(unittest.TestCase):
    def test_read(self):
        parser = configparser.ConfigParser()
        parser.read("data/test.cfg")

        self.assertTrue(parser.has_section('Section 1'))
        self.assertTrue(parser.has_section('Section 2'))

        self.assertEqual(parser.sections(), ['Section 1', 'Section 2'])

    def test_read_defaults(self):
        parser = configparser.ConfigParser()
        parser.read("data/test.cfg")

        self.assertEqual(parser['DEFAULT']['port'], '8080')
        self.assertEqual(parser['DEFAULT'].getint('port'), 8080)

    if __name__ == '__main__':
        unittest.main()
