import os
from pathlib import Path

import chromadb
from chromadb import Settings


# create a vectorstore from the list of documents


def get_in_memory_client():
    return chromadb.Client()


def get_persistent_client():
    path = os.path.join(os.path.expanduser('~'), "llm_rag_facts_store_chromadb_langchain", "chroma_db")
    print("path", path)
    return chromadb.PersistentClient(path=path)


def get_http_client():
    HOST_NAME = "localhost"
    PORT = 8000

    client = chromadb.HttpClient(host=HOST_NAME, port=PORT, settings=Settings(allow_reset=True))
    client.reset()  # resets the database
    return client


def get_chroma_client():
    return get_in_memory_client()
    # return get_persistent_client()
    # return get_http_client()
