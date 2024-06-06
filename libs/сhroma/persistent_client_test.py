import os
import unittest

import chromadb
from chromadb import DEFAULT_TENANT, DEFAULT_DATABASE, Settings


class TestPersistentClient(unittest.TestCase):
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

    def test_create_collection(self):
        self._persistent_client.get_or_create_collection(name=self.test_collection)


if __name__ == '__main__':
    unittest.main()
