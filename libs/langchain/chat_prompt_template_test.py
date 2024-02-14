import unittest

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import ChatPromptValue
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

from model import get_chat_model


class TestChatPromptTemplates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._llm = get_chat_model()
        cls._output_parser = StrOutputParser()

    @classmethod
    def tearDownClass(cls):
        cls._llm = None

    def test_create_prompt_from_template_with_type_and_content(self):
        template = "You are a helpful assistant that translates {input_language} to {output_language}."
        human_template = "{text}"
        chat_prompt_template = ChatPromptTemplate.from_messages([
            ("system", template),
            ("human", human_template)
        ])
        message_list = chat_prompt_template.format_messages(input_language="English", output_language="French",
                                                            text="I love programming.")

        self.assertIs(type(message_list), list)

        message1 = message_list[0]
        self.assertIs(type(message1), SystemMessage)
        self.assertEqual(message1.content, "You are a helpful assistant that translates English to French.")

        message2 = message_list[1]
        self.assertIs(type(message2), HumanMessage)
        self.assertEqual(message2.content, "I love programming.")

    def test_create_prompt_from_template_with_base_message_and_message_prompt_template(self):
        content = "You are a helpful assistant that translates English to French."
        human_template = "{text}"
        chat_prompt_template = ChatPromptTemplate.from_messages([
            SystemMessage(content=content),
            HumanMessagePromptTemplate.from_template(human_template)
        ])
        message_list = chat_prompt_template.format_messages(text="I love programming.")

        self.assertIs(type(message_list), list)
        self.assertEqual(len(message_list), 2)

        formatted_message = message_list[1]
        self.assertIs(type(formatted_message), HumanMessage)
        self.assertEqual(formatted_message.content, "I love programming.")

    def test_invoke_chat_prompt_value(self):
        template = "You are a helpful assistant that translates {input_language} to {output_language}."
        human_template = "{text}"
        chat_prompt_template = ChatPromptTemplate.from_messages([
            ("system", template),
            ("human", human_template)
        ])
        chat_prompt_value = chat_prompt_template.invoke({"input_language": "English", "output_language": "French",
                                                         "text": "I love programming."})

        self.assertIs(type(chat_prompt_value), ChatPromptValue)

        message_list = chat_prompt_value.to_messages();
        self.assertEqual(len(message_list), 2)

        message1 = message_list[0]
        self.assertIs(type(message1), SystemMessage)
        self.assertEqual(message1.content, "You are a helpful assistant that translates English to French.")

        message2 = message_list[1]
        self.assertIs(type(message2), HumanMessage)
        self.assertEqual(message2.content, "I love programming.")

        self.assertTrue(chat_prompt_value.to_string().startswith("System:"))

    def test_create_prompt_with_chat_prompt_composition(self):
        # good practice to start with a system message
        base_template = SystemMessage(content="You are a nice pirate")
        # create a pipeline
        chat_prompt_template = (
                base_template +
                # use message when there is no variables to be formatted
                HumanMessage(content="hi") +
                AIMessage(content="what?") +
                # a string -> HumanMessagePromptTemplate
                "{input}"
        )
        # print(chat_prompt_template)

        message_list = chat_prompt_template.format_messages(input="i said hi!")
        # print(message_list)

    def test_basic_chain(self):
        chat_prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are world class technical documentation writer."),
            ("user", "{input}")
        ])

        # LangChain Expression Language (LCEL)
        chain = chat_prompt_template | self._llm | self._output_parser

        out = chain.invoke({"input": "how can langsmith help with testing?"})


if __name__ == '__main__':
    unittest.main()
