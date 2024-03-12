import os

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# get the environment variables
model_name = os.getenv("OPENAI_API_MODEL")
embedding_model_name = os.getenv("OPENAI_API_EMBEDDING_MODEL")


def get_model_name():
    print("LLM model:", model_name)
    return model_name


def get_embedding_model_name():
    print("LLM embedding model:", embedding_model_name)
    return embedding_model_name


def get_llm():
    return OpenAI(
        # This is the default and can be omitted
        api_key=os.getenv("OPENAI_API_KEY"),
    )
