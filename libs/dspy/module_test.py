import unittest
from unittest import TestCase

import dspy

from model import get_lm


class TestModule(TestCase):
    __QUESTION = "What is the capital of Germany?"

    @classmethod
    def setUpClass(cls):
        lm = get_lm()
        # lm.inspect_history(n=1)
        dspy.settings.configure(lm=lm)

    def test_chain_of_thought_num_of_outputs(self):
        qa_module = dspy.ChainOfThought("question -> answer", n=5)

        res = qa_module(question="What are the largest cities in Germany?")
        print(res)
        self.assertTrue(res.answer.find("Berlin") > -1)


if __name__ == '__main__':
    unittest.main()
