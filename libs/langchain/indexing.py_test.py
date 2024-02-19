import unittest

from langchain.indexes import SQLRecordManager, index
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents import Document

from libs.langchain.model import get_embeddings


class TestIndexing(unittest.TestCase):

    def setUp(self):
        self._db = FAISS.from_texts([""], get_embeddings())

        self.record_manager = SQLRecordManager("some_vector_store/test_index", db_url="sqlite://")
        self.record_manager.create_schema()

        self.doc1 = Document(page_content="kitty", metadata={"source": "kitty.txt"})
        self.doc2 = Document(page_content="doggy", metadata={"source": "doggy.txt"})

    def test_none_deletion_mode(self):
        indexing_result = index(
            [self.doc1, self.doc1, self.doc2],
            self.record_manager,
            self._db,
            cleanup=None,
            source_id_key="source"
        )
        self.assertEqual(indexing_result, {'num_added': 2, 'num_updated': 0, 'num_skipped': 0, 'num_deleted': 0})

    def test_incremental_deletion_mode(self):
        indexing_result = index(
            [self.doc1, self.doc1, self.doc2],
            self.record_manager,
            self._db,
            cleanup="incremental",
            source_id_key="source"
        )
        self.assertEqual(indexing_result, {'num_added': 2, 'num_updated': 0, 'num_skipped': 0, 'num_deleted': 0})

        indexing_result = index(
            [self.doc1, self.doc1, self.doc2],
            self.record_manager,
            self._db,
            cleanup="incremental",
            source_id_key="source"
        )
        self.assertEqual(indexing_result, {'num_added': 0, 'num_updated': 0, 'num_skipped': 2, 'num_deleted': 0})

        changed_doc_2 = Document(page_content="puppy", metadata={"source": "doggy.txt"})
        indexing_result = index(
            [self.doc1, self.doc1, changed_doc_2],
            self.record_manager,
            self._db,
            cleanup="incremental",
            source_id_key="source"
        )
        self.assertEqual(indexing_result, {'num_added': 1, 'num_updated': 0, 'num_skipped': 1, 'num_deleted': 1})

    def test_full_deletion_mode(self):
        indexing_result = index(
            [self.doc1, self.doc2],
            self.record_manager,
            self._db,
            cleanup="full",
            source_id_key="source"
        )
        self.assertEqual(indexing_result, {'num_added': 2, 'num_updated': 0, 'num_skipped': 0, 'num_deleted': 0})

        indexing_result = index(
            [self.doc1],
            self.record_manager,
            self._db,
            cleanup="full",
            source_id_key="source"
        )
        self.assertEqual(indexing_result, {'num_added': 1, 'num_updated': 0, 'num_skipped': 0, 'num_deleted': 1})


if __name__ == '__main__':
    unittest.main()
