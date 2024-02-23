import unittest
from pprint import pprint

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.vectorstores.docarray import DocArrayInMemorySearch

from libs.langchain.model import get_embeddings


class TestVectorStore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.embeddings_model = get_embeddings()

    @staticmethod
    def _get_documents_from_file(name: str = "some_text.txt"):
        return CharacterTextSplitter(chunk_size=200, chunk_overlap=50).split_documents(
            TextLoader("./data/" + name).load()
        )

    def test_create_db(self):
        db = Chroma.from_documents(self._get_documents_from_file(), self.embeddings_model)

    def test_create_similarity_search(self):
        query = "What is LangChain?"
        db = Chroma.from_documents(self._get_documents_from_file(), self.embeddings_model)
        docs = db.similarity_search(query)
        print("test_create_similarity_search:", docs[0].page_content)

    def test_create_similarity_search_by_vector(self):
        query = "What is LangChain?"
        embedding_vector = self.embeddings_model.embed_query(query)

        db = Chroma.from_documents(self._get_documents_from_file(), self.embeddings_model)
        docs = db.similarity_search_by_vector(embedding_vector)

        print("test_create_similarity_search_by_vector:", docs[0].page_content)

    def test_doc_array_in_memory_search(self):
        db = DocArrayInMemorySearch.from_documents(self._get_documents_from_file("state_of_the_union.txt"),
                                                   self.embeddings_model)

        query = "What did the president say about Ketanji Brown Jackson"
        docs = db.similarity_search(query)

        pprint(docs)


if __name__ == '__main__':
    unittest.main()
