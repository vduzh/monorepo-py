import pprint
import unittest


class TestPPrint(unittest.TestCase):
    def test_pprint(self):
        data = [
            {"id": 1, "name": "John"},
            {"id": 1, "name": "John"},
            {"id": 3, "name": "Max"},
            {"id": 4, "name": "Andy"},
            {"id": 5, "name": "Mike"}
        ]
        pprint.pprint(data)
        pprint.pprint(data, width=25)
        pprint.pprint(data, depth=2)

    if __name__ == '__main__':
        unittest.main()
