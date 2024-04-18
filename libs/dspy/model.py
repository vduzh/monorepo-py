import dspy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_llm():
    # Initialize the model
    # return dspy.OpenAI(model='gpt-3.5-turbo-instruct', max_tokens=250)
    return dspy.OpenAI(max_tokens=250)
