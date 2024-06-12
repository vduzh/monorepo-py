from langchain_community.document_loaders import TextLoader
from langchain_core.vectorstores import VectorStore
from langchain_text_splitters import TextSplitter


class DocumentsService:

    def __init__(
            self,
            text_splitter: TextSplitter,
            text_loader: TextLoader,
            vector_store: VectorStore
    ) -> None:
        super().__init__()

        self.text_splitter = text_splitter
        self.text_loader = text_loader
        self.vector_store = vector_store

    def load(self):
        print("DocumentsService:", "load is working...")

        # load documents
        docs = self.text_loader.load_and_split(self.text_splitter)
        print("DocumentsService:docs", docs)

        # add documents to the vector store
        self.vector_store.add_documents(docs)
        print("DocumentsService:", "added docs to the vector store.")
