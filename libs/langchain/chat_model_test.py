import json
import unittest

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.utils.function_calling import convert_to_openai_tool

from model import get_chat_model


def multiply(a: int, b: int) -> int:
    """Multiply two integers together.

    Args:
        a: First integer
        b: Second integer
    """
    return a * b


class TestChatModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the model
        cls.chat_model = get_chat_model()

    @classmethod
    def tearDownClass(cls):
        cls.chat_model = None

    def test_create_ai_message(self):
        content = "The purpose of model regularization is to ..."
        message = AIMessage(content=content)

        self.assertEqual(message.type, "ai")
        self.assertEqual(message.content, content)

    def test_create_human_message(self):
        content = "What is the purpose of model regularization?"
        message = HumanMessage(content=content)

        self.assertEqual(message.type, "human")
        self.assertEqual(message.content, content)

    def test_create_system_message(self):
        content = "You're a helpful assistant"
        message = SystemMessage(content=content)

        self.assertEqual(message.type, "system")
        self.assertEqual(message.content, content)

    def test_create_function_message(self):
        pass

    def test_create_chat_message(self):
        pass

    def test_input_messages_and_output_message(self):
        messages = [HumanMessage(content="This is a test!")]
        res = self.chat_model.invoke(messages)
        self.assertIs(type(res), AIMessage)

    def test_invoke(self):
        # list of messages
        input_messages = [
            SystemMessage(content="You're a helpful assistant"),
            HumanMessage(content="What is the purpose of model regularization?"),
        ]
        out_message = self.chat_model.invoke(input_messages)
        print(out_message)

    # def test_invoke(self):
    #     text = "This is a test!"
    #     messages = [HumanMessage(content="Say " + text)]
    #     message = self.chat_model.invoke(messages)
    #     self.assertEqual(message.content, text)

    def test_invoke_coerced_objects(self):
        # TODO: implement
        pass

    def test_stream(self):
        input_messages = [
            SystemMessage(content="You're a helpful assistant"),
            HumanMessage(content="What is the purpose of model regularization?"),
        ]

        for chunk in self.chat_model.stream(input_messages):
            print(chunk.content, end="", flush=True)

    def test_batch(self):
        input_messages = [
            SystemMessage(content="You're a helpful assistant"),
            HumanMessage(content="What is the purpose of model regularization?"),
        ]
        out_message = self.chat_model.batch([input_messages])
        print(out_message)

    # unittest doesn't support async code
    # async def test_a_invoke(self):
    #     input_messages = [
    #         SystemMessage(content="You're a helpful assistant"),
    #         HumanMessage(content="What is the purpose of model regularization?"),
    #     ]
    #     out_message = await self.chat_model.ainvoke(input_messages)
    #     print(out_message)

    def test_python_function_calling(self):
        # define function
        tool = convert_to_openai_tool(multiply)
        # print(json.dumps(tool, indent=2))

        # out_message = self.chat_model.invoke(
        #     "what's 5 times three",
        #     tools=[convert_to_openai_tool(multiply)]
        # )
        # print(out_message)

        # chat_model_with_tool = self.chat_model.bind(tools=[convert_to_openai_tool(multiply)])
        # chat_model_with_tool.invoke("what's 5 times three")

        pass


if __name__ == '__main__':
    unittest.main()
