import unittest


class TestBuiltIn(unittest.TestCase):
    def test_all(self):
        self.assertTrue(all([True, True, True]))
        self.assertTrue(all([True, 1, 'some']))
        self.assertTrue(all(char.isdigit() for char in '1234'))

        self.assertFalse(all([True, False, True]))
        self.assertFalse(all(char.isdigit() for char in '123b'))

    def test_any(self):
        self.assertTrue(any([True, False, True]))
        self.assertTrue(any(char.isdigit() for char in 'ab1c'))

        self.assertFalse(any([False, False, False]))
        self.assertFalse(any(char.isdigit() for char in 'abc'))

    def test_id(self):
        self.assertEqual(id("abc"), id("abc"))

    def test_hash(self):
        self.assertEqual(hash("abc"), hash("abc"))

        with self.assertRaises(TypeError):
            # unhashable type
            hash(["abc"])

    def test_range(self):
        # range is a class
        r = range(5)
        print(r)


    if __name__ == '__main__':
        unittest.main()
