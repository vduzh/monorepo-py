import os

from dotenv import load_dotenv
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings

# Load environment variables from .env file
load_dotenv()

# get the environment variables
model_name = os.getenv("OPENAI_API_MODEL")
chat_model_name = os.getenv("OPENAI_API_MODEL")
embedding_model_name = os.getenv("OPENAI_API_EMBEDDING_MODEL")


def get_llm():
    print("LLM model:", model_name)
    return OpenAI(model_name=model_name)


def get_chat_model():
    print("Chat model:", chat_model_name)
    return ChatOpenAI(model_name=chat_model_name)


def get_embeddings():
    print("Embedding model:", embedding_model_name)
    return OpenAIEmbeddings(model=embedding_model_name)
