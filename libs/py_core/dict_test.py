import unittest


class TestDict(unittest.TestCase):
    def setUp(self):
        self.DICT = {"home": 10, "bar": "test"}

    def test_create(self):
        d = {5: "home", True: "bar", (1, 5): 'baz'}
        d2 = dict(name="John", age=36, country="Norway")
        d3 = {
            "key": 123,
            "data": {
                "type": "bmp",
                "size": 1000
            }
        }

    def test_get_element(self):
        self.assertEqual(self.DICT['home'], 10)
        self.assertEqual(self.DICT.get('home'), 10)

    def test_update_element(self):
        self.DICT['home'] = 100
        self.assertEqual(self.DICT['home'], 100)

    def test_add_element(self):
        self.DICT['baz'] = True
        self.assertTrue(self.DICT['baz'])

    def test_delete_element(self):
        self.DICT.popitem()
        self.assertEqual(self.DICT, {"home": 10})

        self.DICT.pop('home')
        self.assertEqual(self.DICT, {})

    def test_clear(self):
        d = {5: "home", True: "bar", (1, 5): 'baz'}
        d.clear()

        self.assertEqual(self.DICT['home'], 10)

    def test_get_keys(self):
        keys = self.DICT.keys()
        print(keys)

    def test_get_values(self):
        values = self.DICT.values()
        print(values)

    def test_get_items(self):
        items = self.DICT.items()
        print(items)

    def test_iterate(self):
        for key in self.DICT:
            print(key)

        for key, value in self.DICT.items():
            print(key, '-', value)

    def test_complex_structure(self):
        data = {
            "user_1": {
                "id": 1,
                "name": "home"
            },
            "user_2": {
                "id": 1,
                "name": "home"
            }
        }

        self.assertEqual(data["user_1"]["name"], "home")

    def test_unpacking(self):
        foo, bar = self.DICT
        self.assertEqual(foo, "home")
        self.assertEqual(bar, "bar")

        foo, bar = self.DICT.items()
        self.assertEqual(foo, ("home", 10))
        self.assertEqual(bar, ("bar", "test"))

    def test_generate(self):
        src = [1, 2, 3]
        res = {"id_{}".format(i): i * 10 for i in src}
        print(res)

    def test_generate_join(self):
        team1 = {"Adams": 14, "White": 28}
        team2 = {"Shark": 16, "Brown": 2}

        res = {key: value for team in (team1, team2) for key, value in team.items()}

        print(res)

    if __name__ == '__main__':
        unittest.main()
