import unittest


class TestIf(unittest.TestCase):
    def setUp(self):
        self.A = 3
        self.B = 6
        self.C = 10

    def test_if(self):
        if self.A < self.C:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def test_inline(self):
        value = 4

        if value != self.A:
            if value < self.B:
                self.assertTrue(True)
                return

        self.assertTrue(False)

    def test_else(self):
        if self.C < self.B:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_elif(self):
        value = 4
        if value > self.B:
            self.assertTrue(False)
        elif value > self.A:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def test_if_tern(self):
        value = "less" if self.A < self.B else "failure"
        self.assertEqual(value, "less")

        value = "failure" if self.A > self.B else "more"
        self.assertEqual(value, "more")

if __name__ == '__main__':
    unittest.main()
