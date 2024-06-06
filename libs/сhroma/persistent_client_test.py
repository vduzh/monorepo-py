import os
import unittest

import chromadb
from chromadb import DEFAULT_TENANT, DEFAULT_DATABASE, Settings


class TestCPersistentClient(unittest.TestCase):
    test_collection = "test_collection"

    @classmethod
    def setUpClass(cls):
        path = os.path.join(os.path.dirname(__file__), "tmp")
        cls._persistent_client = chromadb.PersistentClient(
            path=path,
            settings=Settings(),
            tenant=DEFAULT_TENANT,
            database=DEFAULT_DATABASE,
        )

    def setUp(self):
        try:
            self._persistent_client.delete_collection(self.test_collection)
        except ValueError:
            pass

    def test_create_collection(self):
        collection = self._persistent_client.create_collection(name=self.test_collection)

    def test_load_collection(self):
        collection = self._persistent_client.get_or_create_collection(name=self.test_collection)


if __name__ == '__main__':
    unittest.main()
