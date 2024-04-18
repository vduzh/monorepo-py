import unittest
from unittest import TestCase

import dspy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class TestLanguageModels(TestCase):

    def test_llm_client(self):
        llm = dspy.OpenAI(max_tokens=250)
        dspy.configure(llm=llm)

    def test_call_llm(self):
        # not recommended way to interact
        llm = dspy.OpenAI(max_tokens=250)
        dspy.configure(llm=llm)

        res_lst = llm("What is the capital of Germany?")
        res_str = str(res_lst[0])
        print(res_str)

        self.assertTrue(res_str.find("Berlin") > -1)


if __name__ == '__main__':
    unittest.main()
