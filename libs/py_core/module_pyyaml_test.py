import unittest
import yaml


class TestPyyaml(unittest.TestCase):

    def test_str_to_dict(self):
        json_str = "id: 1\ntitle: foo"

        data = yaml.safe_load(json_str)

        self.assertEqual(data['id'], 1)
        self.assertEqual(data['title'], 'foo')
        self.assertEqual({"id": 1, "title": "foo", }, data)

    def test_dict_to_str(self):
        data = {"id": 1, "title": "foo"}
        txt = yaml.dump(data, default_flow_style=False)
        # print(txt)
        self.assertEqual('id: 1\ntitle: foo\n', txt)

    def test_file_to_dict(self):
        with open("data/data.yaml", 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            # print(data)
            self.assertEqual({"id": 1, "title": "foo", "body": "bar"}, data)

    def test_dict_to_file(self):
        data = {"id": 1, "title": "Foo"}

        with open("tmp/data.yaml", 'w') as file:
            yaml.dump(data, file)


if __name__ == '__main__':
    unittest.main()
