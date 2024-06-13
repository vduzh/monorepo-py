import unittest
import zipfile


def create_zip(name="tmp/zip_file.zip", mode="w"):
    zip_file = zipfile.ZipFile(name, mode)
    zip_file.write("data/data.csv", "data.csv")
    zip_file.write("data/text.txt", "text.txt")
    zip_file.close()

    return zip_file


class TestZipfile(unittest.TestCase):

    def test_create(self):
        create_zip()

    def test_namelist(self):
        zip_file = create_zip()

        files = zip_file.namelist()
        self.assertEqual(files.sort(), ['data.csv', 'text.txt'].sort())

    def test_infolist(self):
        zip_file = create_zip()
        info_list = zip_file.infolist()

    def test_getinfo(self):
        zip_file = create_zip()

        zip_info = zip_file.getinfo("text.txt")
        self.assertEqual(zip_info.filename, "text.txt")

    def test_read(self):
        create_zip()

        zip_file = zipfile.ZipFile("tmp/zip_file.zip", "r")
        res = zip_file.read("text.txt").decode()
        zip_file.close()
        self.assertTrue(res.startswith("Lorem"))

    def test_extract(self):
        create_zip()

        zip_file = zipfile.ZipFile("tmp/zip_file.zip", "r")
        zip_file.extract("text.txt", "tmp")
        zip_file.close()


if __name__ == '__main__':
    unittest.main()
