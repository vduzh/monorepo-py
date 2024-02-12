import unittest

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize the model
llm = ChatOpenAI()

# convert the chat message to a string
output_parser = StrOutputParser()


class TestPromptTemplates(unittest.TestCase):

    def test_basic(self):
        test_value = "This is a test!"
        s = llm.invoke("Say " + test_value)
        self.assertTrue(s.content, test_value)


if __name__ == '__main__':
    unittest.main()
