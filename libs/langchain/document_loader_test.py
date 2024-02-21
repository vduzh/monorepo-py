import unittest

from langchain_community.document_loaders import TextLoader, CSVLoader, DirectoryLoader, PyPDFLoader
from langchain_core.documents import Document


# Using with windows:
# poetry add langchain@1.0.6
# pip add langchain-community@0.0.19
# https://github.com/langchain-ai/langchain/issues/17514
class TestDocumentLoader(unittest.TestCase):

    def test_text_loader(self):
        loader = TextLoader("./data/some_text.txt")
        doc_list = loader.load()
        self.assertEqual(type(doc_list[0]), Document)

    def test_csv_loader(self):
        loader = CSVLoader(file_path='./data/some_data.csv')
        doc_list = loader.load()
        self.assertEqual(type(doc_list[0]), Document)

    def test_csv_loader_customized(self):
        loader = CSVLoader(
            file_path='./data/some_data.csv',
            csv_args={
                'fieldnames': ['Year', ',Make', 'Model']
            }
        )
        doc_list = loader.load()
        self.assertEqual(type(doc_list[0]), Document)

    def test_pdf_loader(self):
        loader = PyPDFLoader("./data/textbook.pdf")
        doc_list = loader.load_and_split()
        # print(doc_list)

    def test_pdf_loader_extract_images(self):
        loader = PyPDFLoader("./data/textbook.pdf", extract_images=True)
        doc_list = loader.load()
        print(doc_list)
        # self.assertEqual(type(doc_list[0]), Document)

    def test_directory_loader(self):
        loader = DirectoryLoader("./data/folder/", glob="**/*.txt")
        doc_list = loader.load()
        self.assertEqual(type(doc_list[0]), Document)


if __name__ == '__main__':
    unittest.main()
