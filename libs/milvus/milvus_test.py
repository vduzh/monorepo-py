import os
import unittest
from inspect import currentframe

from dotenv import load_dotenv
from milvus_model import DefaultEmbeddingFunction
from pymilvus import MilvusClient

# Load environment variables from .env file
load_dotenv()


class TestMilvus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize Milvus client
        cls._milvus_client = MilvusClient(
            uri=os.getenv("MILVUS_ENDPOINT"),
            token=os.getenv("MILVUS_API_KEY"),
        )

    def tearDown(self):
        for collection_name in self._milvus_client.list_collections():
            self._milvus_client.drop_collection(collection_name=collection_name)

    def test_drop_collection(self):
        # collection_name = currentframe().f_code.co_name
        embedding_fn = DefaultEmbeddingFunction()

        # Text strings to search from.
        docs = [
            "Artificial intelligence was founded as an academic discipline in 1956.",
            "Alan Turing was the first person to conduct substantial research in AI.",
            "Born in Maida Vale, London, Turing was raised in southern England.",
        ]

        vectors = embedding_fn.encode_documents(docs)

    def test_create_collection(self):
        collection_name = currentframe().f_code.co_name

        self._milvus_client.create_collection(
            collection_name,
            # The vectors we will use in this demo has 768 dimensions
            dimension=768
        )

        # Define collection parameters
        # collection_params = {
        #     'fields': [
        #         {
        #             'name': 'text',
        #             'type': DataType.FLOAT_VECTOR,
        #             'params': {
        #                 'dim': 768
        #             },
        #             'indexes': [
        #                 {
        #                     'index_type': IndexType.IVF_FLAT,
        #                     'metric_type': MetricType.L2
        #                 }
        #             ]
        #         },
        #         {
        #             'name': 'id',
        #             'type': DataType.INT64,
        #             'auto_id': True
        #         }
        #     ]
        # }

        # Create collection if it doesn't exist
        # if not self._milvus_client.has_collection(collection_name):
        # self._milvus_client.create_collection(collection_name, collection_params)


if __name__ == '__main__':
    unittest.main()
