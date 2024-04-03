import unittest

from langchain.text_splitter import HTMLHeaderTextSplitter, CharacterTextSplitter


class TestTextSplitter(unittest.TestCase):

    def test_split_by_character(self):
        with open("./data/some_text.txt") as f:
            external_text = f.read()

        spliter = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=200,
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False,
        )

        docs = spliter.create_documents([external_text])

    def test_split_by_character_with_metadata(self):
        with open("./data/some_text.txt") as f:
            external_text = f.read()

        with open("./data/some_data.csv") as f2:
            external_text_2 = f2.read()

        spliter = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=200,
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False,
        )

        metadatas = [{"document": 1}, {"document": 2}]
        docs = spliter.create_documents([external_text, external_text_2], metadatas=metadatas)

    def test_html_header_text_splitter(self):
        headers_to_split_on = [
            ("h1", "Header 1"),
            ("h2", "Header 2"),
            ("h3", "Header 3"),
        ]

        splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        html_header_splits = splitter.split_text_from_file("./data/some_html.html")

        # for split in html_header_splits:
        #     print(split)

        # print(len(html_header_splits))


if __name__ == '__main__':
    unittest.main()
