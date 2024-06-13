import unittest


class TestFile(unittest.TestCase):
    def test_open_and_close(self):
        f = open("text.txt", "r")
        f.close()

    def test_open_in_folder(self):
        f = open("data/text.txt", "r")
        f.close()

    def test_auto_create(self):
        f = open("tmp/text.txt", "w")
        f.close()

    def test_create_and_write(self):
        f = open("tmp/write.txt", "w")
        f.write("Hello")
        f.write("World\n!")
        f.close()

    def test_append(self):
        # re-create file
        f = open("tmp/append.txt", "w")
        f.write("Hello")
        f.close()

        # append to the existing file
        f = open("tmp/append.txt", "a")
        f.write(" World!")
        f.close()

    def test_read_all(self):
        f = open("data/text.txt", "r")
        s = f.read()
        # print(s)
        f.close()

    def test_read_n(self):
        f = open("data/text.txt", "r")
        s = f.read(5)
        # print(s)
        f.close()

        self.assertEqual(len(s), 5)

    def test_read_lines(self):
        lst = []

        f = open("data/text.txt", "r")
        for line in f:
            print(line, end="")
            lst.append(line)
        f.close()

        self.assertEqual(len(lst), 2)

    def test_try_except_finally(self):
        f = None

        try:
            f = open("home.txt")
        except FileNotFoundError:
            print("File not found")
        finally:
            if f is not None:
                f.close()

    def test_with_as(self):
        try:
            with open("home.txt") as f:
                f.read()
        except FileNotFoundError:
            print("File not found")

if __name__ == '__main__':
    unittest.main()
