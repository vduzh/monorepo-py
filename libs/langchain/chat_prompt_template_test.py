import unittest
from pprint import pprint

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompt_values import ChatPromptValue
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder


class TestChatPromptTemplates(unittest.TestCase):

    def test_create_prompt_from_template_with_type_and_content(self):
        template = "You are a helpful assistant that translates {input_language} to {output_language}."
        human_template = "{text}"
        chat_prompt_template = ChatPromptTemplate.from_messages([
            ("system", template),
            ("human", human_template)
        ])

        message_list = chat_prompt_template.format_messages(
            input_language="English",
            output_language="French",
            text="I love programming."
        )

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
        chat_prompt_value = chat_prompt_template.invoke({
            "input_language": "English",
            "output_language": "French",
            "text": "I love programming."
        })

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

    def test_create_prompt_with_messages_placeholder(self):
        # to be inserted into a message list by the MessagesPlaceholder
        chat_history_lst = [
            HumanMessage(content='How many letters in the word educa? Return the result as a number.'),
            AIMessage(content='The word "educa" has 5 letters.')
        ]

        chat_prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a very powerful assistant but not great at calculating word lengths."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
        ])

        message_list = chat_prompt_template.format_messages(
            input="Really?",
            chat_history=chat_history_lst
        )
        pprint(message_list)

        self.assertEqual(4, len(message_list))
        self.assertIsInstance(message_list[0], SystemMessage)
        self.assertIsInstance(message_list[1], HumanMessage)
        self.assertIsInstance(message_list[2], AIMessage)
        self.assertEqual('The word "educa" has 5 letters.', message_list[2].content)
        self.assertIsInstance(message_list[3], HumanMessage)


if __name__ == '__main__':
    unittest.main()
