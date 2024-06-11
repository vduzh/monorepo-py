import os

from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

# Load environment variables from .env file
load_dotenv()

# get the environment variables
_embedding_model_name = os.getenv("OPENAI_API_EMBEDDING_MODEL")


def get_embeddings() -> Embeddings:
    print("Embedding model:", _embedding_model_name)
    return OpenAIEmbeddings(model=_embedding_model_name)
