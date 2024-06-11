import os

from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# get the environment variables
_embedding_model_name = os.getenv("OPENAI_API_EMBEDDING_MODEL")


def get_embedding_function():
    # print("Embedding model:", _embedding_model_name)
    embedding_function = OpenAIEmbeddingFunction(
        api_key=os.environ.get('OPENAI_API_KEY'),
        # model_name="text-embedding-ada-002"
        model_name=_embedding_model_name
    )
    # embedding_function = OpenAIEmbeddingFunction()
    return embedding_function
