import unittest

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from model import get_chat_model


class TestChatPromptTemplates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._llm = get_chat_model()
        cls._output_parser = StrOutputParser()

    @classmethod
    def tearDownClass(cls):
        cls._llm = None

    def test_create_prompt_from_template(self):
        template = "You are a helpful assistant that translates {input_language} to {output_language}."
        human_template = "{text}"
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", template),
            ("human", human_template)
        ])
        messages = chat_prompt.format_messages(input_language="English", output_language="French",
                                               text="I love programming.")

        message1 = messages[0]
        self.assertIs(type(message1), SystemMessage)
        self.assertEqual(message1.content, "You are a helpful assistant that translates English to French.")

        message2 = messages[1]
        self.assertIs(type(message2), HumanMessage)
        self.assertEqual(message2.content, "I love programming.")

    def test_basic_chain(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are world class technical documentation writer."),
            ("user", "{input}")
        ])
        chain = prompt | self._llm | self._output_parser
        out = chain.invoke({"input": "how can langsmith help with testing?"})


if __name__ == '__main__':
    unittest.main()
