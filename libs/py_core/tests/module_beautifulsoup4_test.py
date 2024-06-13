import unittest

from bs4 import BeautifulSoup


class TestBeautifulSoup(unittest.TestCase):
    def test_file_to_dict(self):
        with open("data/data.xml", 'r') as file:
            xml_content = file.read()
            soup = BeautifulSoup(xml_content, "xml")
            # print(soup.prettify())

            self.assertEqual("1", soup.id.string)
            self.assertEqual("foo", soup.title.string)
            self.assertEqual("bar", soup.body.string)

    def test_dict_to_file(self):
        data = {"id": 1, "title": "Foo"}

        root = BeautifulSoup(features="xml").new_tag("data")

        for key, value in data.items():
            element = BeautifulSoup(features="xml").new_tag(key)
            element.string = str(value)
            root.append(element)

        xml_string = root.prettify()
        # print(xml_string)

        with open("tmp/data.xml", 'w') as file:
            file.write(xml_string)


if __name__ == '__main__':
    unittest.main()
