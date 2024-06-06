import unittest
from inspect import currentframe
from pprint import pprint

import chromadb
from chromadb import EmbeddingFunction, Documents, Embeddings
from chromadb.utils import embedding_functions


class TestClientAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Use the in-memory mode
        cls._client_api = chromadb.Client()

    def test_create_collection(self):
        collection_name = currentframe().f_code.co_name

        # Create a collection using default embedding function
        self._client_api.create_collection(name=collection_name)
        self._client_api.get_or_create_collection(name=collection_name)

    def test_create_collection_with_specific_embedding_function(self):
        collection_name = currentframe().f_code.co_name

        # Use the default function with all-MiniLM-L6-v2 model for creating embeddings
        embedding_function = embedding_functions.DefaultEmbeddingFunction()

        # Create a collection
        self._client_api.create_collection(
            name=collection_name,
            embedding_function=embedding_function
        )

    def test_create_collection_with_custom_embedding_function(self):
        collection_name = currentframe().f_code.co_name

        # Custom embedding function
        class CustomEmbeddingFunction(EmbeddingFunction):
            def __call__(self, docs: Documents) -> Embeddings:
                # Embed the input documents somehow
                embedding_function = embedding_functions.DefaultEmbeddingFunction()
                return embedding_function(docs)

        # Create a collection
        self._client_api.create_collection(
            name=collection_name,
            embedding_function=CustomEmbeddingFunction()
        )

    def test_list_collections(self):
        collection_name = currentframe().f_code.co_name
        collection_names = [collection_name + str(i) for i in range(2)]

        for name in collection_names:
            self._client_api.create_collection(name=name)

        collection_sequence = self._client_api.list_collections()
        # pprint(collection_sequence)

        self.assertEqual(2, len(collection_sequence))
        self.assertTrue(all([collection.name in collection_names for collection in collection_sequence]))

    def test_modify_collection(self):
        collection_name = currentframe().f_code.co_name
        collection = self._client_api.create_collection(name=collection_name)

        collection.modify(name="modified")

        self.assertEqual("modified", collection.name)

    def test_delete_collection(self):
        collection_name = currentframe().f_code.co_name
        self._client_api.create_collection(name=collection_name)

        self._client_api.delete_collection(name=collection_name)

    def test_get_existing_collection(self):
        collection_name = currentframe().f_code.co_name
        self._client_api.create_collection(name=collection_name)

        collection = self._client_api.get_collection(name=collection_name)

        self.assertEqual("get_existing_collection", collection.name)

    def test_get_or_create_collection(self):
        collection_name = currentframe().f_code.co_name

        self._client_api.get_or_create_collection(name=collection_name)

    def test_add_data_to_collection(self):
        collection_name = currentframe().f_code.co_name
        collection = self._client_api.create_collection(name=collection_name)

        # Automatically tokenizes, embeds, and stores the data
        collection.add(
            # Raw texts for automatic conversion
            documents=[
                "Lorem Ipsum is simply dummy text",
                "Lorem Ipsum is simply random text"
            ],
            # an optional field but recommended for later querying
            metadatas=[
                {"type": "recipe", "source": "kitchen"},
                {"type": "article", "source": "newspaper"}
            ],
            # required field
            ids=["100", "200"]
        )

    def test_count_data(self):
        collection_name = currentframe().f_code.co_name
        collection = self._client_api.create_collection(name=collection_name)
        collection.add(
            documents=["Foo", "Bar"],
            ids=["100", "200"]
        )

        self.assertEqual(2, collection.count())

    def test_get_data(self):
        collection_name = currentframe().f_code.co_name
        collection = self._client_api.create_collection(name=collection_name)
        collection.add(
            documents=["Lorem Ipsum is simply dummy text", "Lorem Ipsum is simply random text"],
            ids=["100", "200"]
        )

        # get all documents
        get_result = collection.get()
        # pprint(get_result

        # get documents by id
        get_result = collection.get(ids=["100"])
        pprint(get_result)

    def test_update_data(self):
        collection_name = currentframe().f_code.co_name
        collection = self._client_api.create_collection(name=collection_name)
        collection.add(
            documents=["Lorem Ipsum is simply dummy text", "Lorem Ipsum is simply random text"],
            ids=["100", "200"]
        )

        # update
        collection.update(
            documents=["Foo"],
            ids=["100"]
        )

        # get documents by id
        get_result = collection.get(ids=["100"])
        # pprint(get_result)

        self.assertEqual("Foo", get_result["documents"][0])

    def test_upsert_data(self):
        collection_name = currentframe().f_code.co_name
        collection = self._client_api.create_collection(name=collection_name)
        collection.add(
            documents=["Lorem Ipsum is simply dummy text", "Lorem Ipsum is simply random text"],
            ids=["100", "200"]
        )

        # update
        collection.upsert(
            documents=["Foo", "Bar"],
            ids=["100", "300"]
        )
        pprint(collection.get())

        self.assertEqual(3, collection.count())
        self.assertEqual("Foo", collection.get(ids=["100"]).get("documents")[0])
        self.assertEqual("Bar", collection.get(ids=["300"]).get("documents")[0])

    def test_delete_data(self):
        collection_name = currentframe().f_code.co_name
        collection = self._client_api.create_collection(name=collection_name)
        collection.add(
            documents=["Lorem Ipsum is simply dummy text", "Lorem Ipsum is simply random text"],
            ids=["100", "200"]
        )

        # update
        collection.delete(ids=["100"])

        self.assertEqual(1, collection.count())

    def test_query_data_in_collection(self):
        collection_name = currentframe().f_code.co_name
        collection = self._client_api.create_collection(name=collection_name)
        collection.add(
            documents=[
                "Chroma is an AI-native open-source vector database.",
                "Milvus is a powerful vector database tailored for processing and searching extensive vector data.",
                "Weaviate is a fast, flexible and reliable vector database."
            ],
            metadatas=[{"source": "foo"}, {"source": "bar"}, {"source": "foo"}],
            ids=["100", "200", "300"]
        )

        # return the n most similar results
        query_result = collection.query(
            # raw string, which is automatically processed using the embedding function
            query_texts=[
                "What is a vector database?"
            ],
            # number of results to retrieve
            n_results=2
        )
        # pprint(query_result)

        # return the filtered results
        query_result = collection.query(
            query_texts=["What is a vector database?"],
            n_results=2,
            # metadata-based filtering
            where={"source": "foo"}
        )

        # return the results filtered with an operator
        query_result = collection.query(
            query_texts=["What is a vector database?"],
            n_results=2,
            where={
                "source": {
                    "$eq": "foo"
                }
            }
        )

        # return the results filtered with an operator and document content
        query_result = collection.query(
            query_texts=["What is a vector database?"],
            n_results=2,
            where={"source": "foo"},
            where_document={"$contains": "open-source"}
        )
        pprint(query_result)

    if __name__ == '__main__':
        unittest.main()
