import unittest


class TestSet(unittest.TestCase):
    def setUp(self):
        self.SET = {1, 2, 3}

    def test_create(self):
        s = {1, 2, 2, 3}
        self.assertEqual(s, {1, 2, 3})

        s = set([1, 2, 2, 3])
        self.assertEqual(s, {1, 2, 3})

        s = set("hello")
        self.assertEqual(s, {"h", "e", "l", "o"})

    def test_add_element(self):
        self.SET.add(4)
        self.assertEqual(self.SET, {1, 2, 3, 4})

        self.SET.add(4)
        self.assertEqual(self.SET, {1, 2, 3, 4})

        self.SET.update([4, 5])
        self.assertEqual(self.SET, {1, 2, 3, 4, 5})

    def test_delete_element(self):
        self.SET.remove(2)
        self.assertEqual(self.SET, {1, 3})

        self.SET.pop()
        self.assertEqual(self.SET, {3})

    def test_delete_all(self):
        self.SET.clear()
        self.assertEqual(self.SET, {})

    def test_iterate(self):
        for value in self.SET:
            print(value)


    if __name__ == '__main__':
        unittest.main()
