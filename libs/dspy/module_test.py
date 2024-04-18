import unittest
from unittest import TestCase

import dspy

from model import get_lm

QUESTION = "What is the capital of Germany?"


class TestModule(TestCase):

    @classmethod
    def setUpClass(cls):
        lm = get_lm()
        # lm.inspect_history(n=1)
        dspy.settings.configure(lm=lm)

    def test_predict(self):
        predict_module = dspy.Predict("question -> answer")

        res = predict_module(question=QUESTION)
        print(res)

        # there is no auxiliary information just
        self.assertEqual(1, len(res))
        self.assertEqual("Berlin", res.answer)

    def test_chain_of_thought(self):
        qa_module = dspy.ChainOfThought("question -> answer")

        res = qa_module(question=QUESTION)
        print(res)

        self.assertEqual(2, len(res))
        self.assertIsNotNone(res.rationale)
        self.assertEqual("Berlin", res.answer)

    def test_chain_of_thought_num_of_outputs(self):
        qa_module = dspy.ChainOfThought("question -> answer", n=5)

        res = qa_module(question="What are the largest cities in Germany?")
        print(res)
        self.assertTrue(res.answer.find("Berlin") > -1)


if __name__ == '__main__':
    unittest.main()
