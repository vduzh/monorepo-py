import unittest

from dotenv import load_dotenv
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from pyboxen import boxen

# Load environment variables from .env file
load_dotenv()


def boxen_print(*args, **kwargs):
    print(boxen(*args, **kwargs))


class TestDebug(unittest.TestCase):

    def test_boxen_print(self):
        boxen_print("Lorem testing testing", title="Human", color="red")

    def test_on_chat_model_start(self):
        class ChatModelStartHandler(BaseCallbackHandler):

            def on_chat_model_start(self, serialized, messages, **kwargs):
                print("\n\n=============== Sending Messages =================\n\n")
                for message in messages[0]:
                    if message.type == "system":
                        boxen_print(message.content, title=message.type, color="yellow")
                    elif message.type == "human":
                        boxen_print(message.content, title=message.type, color="green")
                    elif message.type == "ai" and "function_call" in message.additional_kwargs:
                        call = message.additional_kwargs["function_call"]
                        boxen_print(f"Running tool {call['name']} with args {call['arguments']}", title=message.type,
                                    color="cyan")
                    elif message.type == "ai":
                        boxen_print(message.content, title=message.type, color="blue")
                    elif message.type == "function":
                        boxen_print(message.content, title=message.type, color="purple")
                    else:
                        boxen_print(message.content, title=message.type)


        chat = ChatOpenAI(callbacks=[ChatModelStartHandler()])

        input_messages = [
            SystemMessage(content="You're a helpful assistant"),
            HumanMessage(content="Hi!"),
        ]

        res = chat.invoke(input_messages)
        print(res.content)


if __name__ == '__main__':
    unittest.main()
