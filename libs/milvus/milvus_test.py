import os
import unittest

from dotenv import load_dotenv
from pymilvus import MilvusClient

# Load environment variables from .env file
load_dotenv()


class TestMilvus(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print(os.getenv("MILVUS_ENDPOINT"))

        # Initialize Milvus client
        cls._milvus_client = MilvusClient(
            uri=os.getenv("MILVUS_ENDPOINT"),
            token=os.getenv("MILVUS_API_KEY"),
        )

    @classmethod
    def tearDownClass(cls):
        pass

    def test_create_collection(self):
        # self._chroma_client.create_collection(name="my_collection")
        #
        # # Define collection parameters
        # collection_name = 'my_collection'
        # collection_params = {
        #     'fields': [
        #         {'name': 'text', 'type': DataType.FLOAT_VECTOR, 'params': {'dim': 768},
        #          'indexes': [{'index_type': IndexType.IVF_FLAT, 'metric_type': MetricType.L2}]},
        #         {'name': 'id', 'type': DataType.INT64, 'auto_id': True}
        #     ]
        # }
        #
        # # Create collection if it doesn't exist
        # if not milvus_client.has_collection(collection_name):
        #     milvus_client.create_collection(collection_name, collection_params)
        print(111)

    # def test_add_text_document_to_collection(self):
    #     collection = self._chroma_client.create_collection(name="text_documents")
    #     collection.add(
    #         documents=["This is a document", "This is another document"],
    #         metadatas=[{"source": "my_source"}, {"source": "my_source"}],
    #         ids=["id1", "id2"]
    #     )
    #
    # def test_query_collection(self):
    #     collection = self._chroma_client.create_collection(name="text_documents")
    #     collection.add(
    #         documents=["This is a document", "This is another document"],
    #         metadatas=[{"source": "my_source"}, {"source": "my_source"}],
    #         ids=["id1", "id2"]
    #     )
    #
    #     # return the n most similar results
    #     results = collection.query(query_texts=["This is a query document"], n_results=2)
    #     print(results)


if __name__ == '__main__':
    unittest.main()
