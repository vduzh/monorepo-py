import unittest

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from model import get_model


class TestPromptTemplates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the model
        cls._llm = get_model()

        # convert the chat message to a string
        cls._output_parser = StrOutputParser()

    @classmethod
    def tearDownClass(cls):
        cls._llm = None

    def test_basic_chain(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are world class technical documentation writer."),
            ("user", "{input}")
        ])

        chain = prompt | self._llm | self._output_parser

        s = chain.invoke({"input": "how can langsmith help with testing?"})


if __name__ == '__main__':
    unittest.main()
