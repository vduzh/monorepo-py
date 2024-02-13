import unittest

from langchain_core.messages import HumanMessage, AIMessage

from model import get_chat_model


class TestLLM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the model
        cls.chat_model = get_chat_model()

    @classmethod
    def tearDownClass(cls):
        cls.chat_model = None

    def test_input_messages_and_output_message(self):
        messages = [HumanMessage(content="This is a test!")]
        res = self.chat_model.invoke(messages)
        self.assertIs(type(res), AIMessage)

    def test_invoke(self):
        text = "This is a test!"
        messages = [HumanMessage(content="Say " + text)]
        message = self.chat_model.invoke(messages)
        self.assertEqual(message.content, text)


if __name__ == '__main__':
    unittest.main()
