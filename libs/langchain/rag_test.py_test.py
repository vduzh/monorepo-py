import unittest

from langchain_community.vectorstores.docarray import DocArrayInMemorySearch
from langchain_openai import OpenAIEmbeddings


class TestRetrievalAugmentedGeneration(unittest.TestCase):

    def test_(self):
        vectorstore = DocArrayInMemorySearch.from_texts(
            ["harrison worked at kensho", "bears like to eat honey"],
            embedding=OpenAIEmbeddings(),
        )

        retriever = vectorstore.as_retriever()


if __name__ == '__main__':
    unittest.main()
