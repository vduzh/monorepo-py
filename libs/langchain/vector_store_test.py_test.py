import unittest

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings


class TestVectorStore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.embeddings_model = OpenAIEmbeddings()

    @staticmethod
    def _get_documents():
        text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
        return text_splitter.split_documents(TextLoader('./data/some_text.txt').load())

    def test_create_db(self):
        db = Chroma.from_documents(self._get_documents(), self.embeddings_model)
        # print(db)

    def test_create_similarity_search(self):
        query = "What is LangChain?"
        db = Chroma.from_documents(self._get_documents(), self.embeddings_model)
        docs = db.similarity_search(query)
        print("test_create_similarity_search:", docs[0].page_content)

    def test_create_similarity_search_by_vector(self):
        query = "What is LangChain?"
        embedding_vector = self.embeddings_model.embed_query(query)

        db = Chroma.from_documents(self._get_documents(), self.embeddings_model)
        docs = db.similarity_search_by_vector(embedding_vector)

        print("test_create_similarity_search_by_vector:", docs[0].page_content)


if __name__ == '__main__':
    unittest.main()
