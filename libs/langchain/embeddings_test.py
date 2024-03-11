import unittest

from chromadb import Embeddings
from langchain_openai import OpenAIEmbeddings


class TestEmbeddings(unittest.TestCase):

    def test_embeddings(self):
        embeddings = OpenAIEmbeddings()

        print("Testing foo", embeddings)


if __name__ == '__main__':
    unittest.main()
