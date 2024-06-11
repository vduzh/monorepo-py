import os

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma

from projects.llm_rag_facts_store_chromadb_langchain.chroma_client import get_chroma_client
from projects.llm_rag_facts_store_chromadb_langchain.embeddings import get_embeddings


def load_documents():
    print("load_documents:", "starting...")
    # configure splitter
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=200,
        chunk_overlap=0
    )

    # create text loader
    path = os.path.join(os.path.dirname(__file__), "data", "facts.txt")
    loader = TextLoader(path)

    # load documents
    docs = loader.load_and_split(text_splitter)
    # pprint(docs)

    # init a chroma client
    client = get_chroma_client()

    # create chroma
    chroma = Chroma(
        client=client,
        collection_name="facts_collection",
        embedding_function=get_embeddings(),
    )
    # add documents
    chroma.add_documents(docs)
    print("load_documents:", "finished")
