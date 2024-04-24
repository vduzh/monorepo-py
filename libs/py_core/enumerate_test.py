import unittest


class TestEnumerate(unittest.TestCase):
    def test_for(self):
        counties = ['Belarus', "Germany", "Poland"]
        for item in enumerate(counties, start=1):
            print(item)

        for index, country in enumerate(counties, start=1):
            print(index, '-', country)


if __name__ == '__main__':
    unittest.main()
