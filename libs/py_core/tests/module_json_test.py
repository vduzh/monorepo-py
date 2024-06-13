import json
import unittest


class TestJson(unittest.TestCase):

    def test_str_to_dict(self):
        json_str = '{"id": 1,"title": "foo"}'

        data = json.loads(json_str)

        self.assertEqual(data['id'], 1)
        self.assertEqual(data['title'], 'foo')
        self.assertEqual({"id": 1, "title": "foo", }, data)

    def test_dict_to_str(self):
        data = {"id": 1, "title": "foo"}
        txt = json.dumps(data)
        print(txt)
        self.assertEqual('{"id": 1, "title": "foo"}', txt)

    def test_file_to_dict(self):
        with open("data/data.json", 'r') as fp:
            data = json.load(fp)

            self.assertEqual({"id": 1, "title": "foo", "body": "bar"}, data)

    def test_dict_to_file(self):
        data = {"id": 1, "title": "foo"}

        with open("tmp/data.json", 'w') as fp:
            json.dump(data, fp, indent=3)


if __name__ == '__main__':
    unittest.main()
