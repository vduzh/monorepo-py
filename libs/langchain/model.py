from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()


def get_model():
    # Initialize the model
    return ChatOpenAI()
