import unittest


class TestTuple(unittest.TestCase):
    def setUp(self):
        self.T = (1, 3, 4, 7, True, "test")

    def test_create(self):
        t = 1, 3, 4, 7, True, "test"
        t2 = (5,)
        t2 = 5,

    def test_create_from_list(self):
        t = tuple([1, 3])

    def test_create_from_str(self):
        t = tuple("Hello")
        self.assertEqual(t, ('H', 'e', 'l', 'l', 'o'))

    def test_get_element(self):
        self.assertEqual(self.T[1], 3)

    def test_unpacking(self):
        one, three, test = (1, 3, "test")

        self.assertEqual(one, 1)
        self.assertEqual(three, 3)
        self.assertEqual(test, "test")

        one, *rest = (1, 3, "test")
        self.assertEqual(one, 1)
        self.assertTrue(isinstance(rest, list))
        self.assertEqual(rest, [3, "test"])

        one, *rest, test = (1, 3, 5, "test")
        self.assertEqual(one, 1)
        self.assertTrue(isinstance(rest, list))
        self.assertEqual(rest, [3, 5])
        self.assertEqual(test, "test")

    def test_slice(self):
        self.assertEqual(self.T[1:3], (3, 4))

    def test_immutable(self):
        # TODO: Implement
        # with self.assertRaises(TypeError):
        #     self.STR[0] = "Q"
        raise NotImplementedError()



if __name__ == '__main__':
    unittest.main()
