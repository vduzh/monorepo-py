import unittest


class TestIter(unittest.TestCase):
    DAYS = ["Monday", "Tuesday", "Wednesday"]

    def test_next(self):
        i = iter(self.DAYS)
        self.assertEqual(next(i), "Monday")
        self.assertEqual(next(i), "Tuesday")

    def test_read_file(self):
        with open("data/multi-line.txt", "r") as fp:
            for line in iter(fp.readline, ''):
                print(line)
                



if __name__ == '__main__':
    unittest.main()
