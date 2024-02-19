import logging
import unittest

from langchain.retrievers import MultiQueryRetriever
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.faiss import FAISS

from libs.langchain.model import get_embeddings, get_chat_model


class TestRetriever(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._llm = get_chat_model()
        cls._embeddings = get_embeddings()

        cls._db = FAISS.from_documents(
            CharacterTextSplitter(chunk_size=1000, chunk_overlap=0).split_documents(
                TextLoader("./data/some_text.txt").load()),
            cls._embeddings
        )

    def test_create_retriever(self):
        # construct a retriever
        retriever = self._db.as_retriever()
        print(retriever)

    def test_get_relevant_documents(self):
        query = "What is LangChain?"

        retriever = self._db.as_retriever()
        docs = retriever.get_relevant_documents(query)

        retriever = self._db.as_retriever(search_type="mmr")
        docs = retriever.get_relevant_documents(query)

        retriever = self._db.as_retriever(search_kwargs={"k": 1})
        docs = retriever.get_relevant_documents(query)

    def test_multi_query_retriever(self):
        logging.basicConfig()
        logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

        retriever = MultiQueryRetriever.from_llm(retriever=self._db.as_retriever(), llm=self._llm)
        unique_docs = retriever.get_relevant_documents(query="What is LangChain?")
        len(unique_docs)

    def test_contextual_compression(self):
        pass


if __name__ == '__main__':
    unittest.main()
