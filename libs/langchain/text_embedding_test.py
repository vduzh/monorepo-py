import unittest

from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore, InMemoryByteStore
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings


class TestTextEmbedding(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.embeddings_model = OpenAIEmbeddings()

    def test_create_embedding_model(self):
        print("embeddings_model:", self.embeddings_model)

    def test_create_embed_documents(self):
        embeddings = self.embeddings_model.embed_documents(
            [
                "Hi there!",
                "Oh, hello!",
                "What's your name?",
                "My friends call me World",
                "Hello World!"
            ]
        )
        print("embeddings: number of embeddings:", len(embeddings))
        print("embeddings: length of one embedding:", len(embeddings[0]))

    def test_create_embed_query(self):
        embedded_query = self.embeddings_model.embed_query("What was the name mentioned in the conversation?")
        print("embedded query: length", len(embedded_query))
        print("embedded query: five first items:", embedded_query[:5])

    def test_caching_embedding(self):
        local_embeddings_model = OpenAIEmbeddings()

        store = LocalFileStore("./cache/")
        keys = list(store.yield_keys())[:5]
        print("FileStore:keys", keys)

        cached_embedder = CacheBackedEmbeddings.from_bytes_store(
            local_embeddings_model,
            store,
            namespace=self.embeddings_model.model
        )

        row_documents = TextLoader("./data/some_text.txt").load()
        splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0)
        documents = splitter.split_documents(row_documents)

        db = FAISS.from_documents(documents, cached_embedder)

        embedded_query = local_embeddings_model.embed_query("What was the name mentioned in the conversation?")

    def test_caching_embedding_with_in_memory_byte_store(self):
        local_embeddings_model = OpenAIEmbeddings()

        store = InMemoryByteStore()

        cached_embedder = CacheBackedEmbeddings.from_bytes_store(
            local_embeddings_model,
            store,
            namespace=self.embeddings_model.model
        )

        row_documents = TextLoader("./data/some_text.txt").load()
        splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0)
        documents = splitter.split_documents(row_documents)

        db = FAISS.from_documents(documents, cached_embedder)

        embedded_query = local_embeddings_model.embed_query("What was the name mentioned in the conversation?")


if __name__ == '__main__':
    unittest.main()
