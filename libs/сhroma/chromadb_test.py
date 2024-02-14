import unittest

import chromadb


class TestChromaDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._chroma_client = chromadb.Client()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_create_collection(self):
        self._chroma_client.create_collection(name="my_collection")

    def test_add_text_document_to_collection(self):
        collection = self._chroma_client.create_collection(name="text_documents")
        collection.add(
            documents=["This is a document", "This is another document"],
            metadatas=[{"source": "my_source"}, {"source": "my_source"}],
            ids=["id1", "id2"]
        )

    def test_query_collection(self):
        collection = self._chroma_client.create_collection(name="text_documents")
        collection.add(
            documents=["This is a document", "This is another document"],
            metadatas=[{"source": "my_source"}, {"source": "my_source"}],
            ids=["id1", "id2"]
        )

        # return the n most similar results
        results = collection.query(query_texts=["This is a query document"], n_results=2)
        print(results)


if __name__ == '__main__':
    unittest.main()
