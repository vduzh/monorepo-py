import unittest

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize the model
llm = ChatOpenAI()

# convert the chat message to a string
output_parser = StrOutputParser()


class TestPromptTemplates(unittest.TestCase):

    def test_basic_chain(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are world class technical documentation writer."),
            ("user", "{input}")
        ])

        chain = prompt | llm | output_parser

        s = chain.invoke({"input": "how can langsmith help with testing?"})


if __name__ == '__main__':
    unittest.main()
