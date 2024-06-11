import os

import dspy
from dotenv import load_dotenv
from dspy.retrieve.chromadb_rm import ChromadbRM

from projects.llm_rag_facts_dspy.embeddings import get_embedding_function

# Load environment variables from .env file
load_dotenv()


def get_colbert_rm():
    # Set up the retrieval model
    return dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')


def get_chromadb_rm():
    path = os.path.join(os.path.expanduser('~'), "llm_rag_facts_store_chromadb_langchain", "chroma_db")

    return ChromadbRM(
        collection_name="facts_collection",
        persist_directory=path,
        embedding_function=get_embedding_function(),
        k=3
    )


def get_rm():
    # Set up the retrieval model
    return get_chromadb_rm()
    # return get_colbert_rm()
