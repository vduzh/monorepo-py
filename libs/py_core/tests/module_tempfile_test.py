import os.path
import tempfile
import unittest


class TestTempFile(unittest.TestCase):
    def test_tempdir(self):
        value = tempfile.gettempdir()
        print("tempdir::", value)

    def test_tempprefix(self):
        value = tempfile.gettempprefix()
        print("tempprefix::", value)

    def test_TemporaryFile(self):
        data = "Test"
        with tempfile.TemporaryFile(mode="w+t") as f:
            f.write(data)
            f.seek(0)
            self.assertEqual(f.read(), data)

    def test_TemporaryDirectory(self):
        data = "Test"
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "temp_text.txt")
            with open(path, "w+t") as f:
                f.write(data)
                f.seek(0)
                self.assertEqual(f.read(), data)

    if __name__ == '__main__':
        unittest.main()
