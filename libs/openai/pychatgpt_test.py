import os
import unittest

from dotenv import load_dotenv
from pyChatGPT import ChatGPT

# Load environment variables from .env file
load_dotenv()


# Not sure that this lib is OK. It uses a browser to login.
class TestPyChatGPT(unittest.TestCase):

    def test_send_message(self):
        api = ChatGPT(os.getenv("SESSION_TOKEN"))

        test_value = "This is a test!"
        resp = api.send_message(test_value)
        print(resp)

        api.reset_conversation()
        api.clear_conversations()
        api.refresh_chat_page()


if __name__ == '__main__':
    unittest.main()
