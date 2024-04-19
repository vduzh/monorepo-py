import unittest
from unittest import TestCase

import dspy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class TestLanguageModels(TestCase):
    __QUESTION = "What is the capital of Germany?"

    def test_lm_client(self):
        lm = dspy.OpenAI(max_tokens=250)
        dspy.configure(lm=lm)

    def test_call_lm(self):
        # not recommended way to interact
        lm = dspy.OpenAI(max_tokens=250)
        dspy.configure(lm=lm)

        res_lst = lm(self.__QUESTION)
        res_str = str(res_lst[0])
        print(res_str)

        self.assertIn("Berlin", res_str)

    def test_multiple_lm(self):
        default_lm = dspy.OpenAI(max_tokens=250)
        dspy.configure(lm=default_lm)

        # Run with the default model
        qa_module = dspy.ChainOfThought('question -> answer')
        res = qa_module(question=self.__QUESTION)
        print("Default LM:", res)
        self.assertEqual("Berlin", res.answer)

        # Run with GPT-4
        another_lm = dspy.OpenAI(model='gpt-4-1106-preview', max_tokens=300)
        with dspy.context(lm=another_lm):
            res = qa_module(question=self.__QUESTION)
            print("Another LM:", res)
            self.assertEqual("Berlin", res.answer)

    def test_remote_lm_open_ai(self):
        # lm = dspy.{provider_listed_below}(model="your model", model_request_kwargs="...")
        lm = dspy.OpenAI(model="your model", model_request_kwargs="...")
        raise NotImplementedError("Not implemented yet")

    def test_remote_lm_cohere(self):
        # lm = dspy.{provider_listed_below}(model="your model", model_request_kwargs="...")
        lm = dspy.Cohere(model="your model", model_request_kwargs="...")
        raise NotImplementedError("Not implemented yet")

    def test_remote_lm_anyscale(self):
        # lm = dspy.{provider_listed_below}(model="your model", model_request_kwargs="...")
        lm = dspy.Anyscale(model="your model", model_request_kwargs="...")
        raise NotImplementedError("Not implemented yet")

    def test_remote_lm_together(self):
        # lm = dspy.{provider_listed_below}(model="your model", model_request_kwargs="...")
        lm = dspy.Together(model="your model", model_request_kwargs="...")
        raise NotImplementedError("Not implemented yet")

    def test_local_lm_hf_client_tgi(self):
        # tgi_mistral = dspy.HFClientTGI(
        #     model="mistralai/Mistral-7B-Instruct-v0.2",
        #     port=8080,
        #     url="http://localhost"
        # )
        raise NotImplementedError("Not implemented yet")


if __name__ == '__main__':
    unittest.main()
