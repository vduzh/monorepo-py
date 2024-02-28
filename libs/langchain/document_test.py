import unittest
from pprint import pprint

from langchain_core.documents import Document


class TestDocument(unittest.TestCase):

    def test_doc(self):
        doc = Document(
            page_content="some text",
            metadata={
                "foo": "bar"
            }
        )
        pprint("Testing foo")


if __name__ == '__main__':
    unittest.main()
