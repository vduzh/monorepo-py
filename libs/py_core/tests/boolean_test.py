import unittest


class TestBoolean(unittest.TestCase):
    def test_true(self):
        b = True
        self.assertTrue(b)

    def test_false(self):
        b = False
        self.assertFalse(b)

    def test_bool(self):
        self.assertFalse(bool(0))
        self.assertFalse(bool(''))
        self.assertFalse(bool(None))
        self.assertFalse(bool([]))
        self.assertFalse(bool(()))
        self.assertFalse(bool({}))

    def test_and(self):
        self.assertTrue(True and True)
        self.assertFalse(True and False)
        self.assertFalse(False and False)

    def test_add(self):
        self.assertIsInstance(True + False, int)

        self.assertEqual(2, True + True)
        self.assertEqual(1, True + False)
        self.assertEqual(0, False + False)

        self.assertEqual(3, True + True + True)


if __name__ == '__main__':
    unittest.main()
