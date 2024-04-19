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
        # 1. Define the signature.
        signature = "question -> answer"

        # 2. Declare the Predict module with the signature.
        predict_module = dspy.Predict(signature)

        # 3. Call the module with input argument(s).
        res = predict_module(question=QUESTION)
        print(res)

        # 4. Access the output.
        answer = res.answer

        # there is no auxiliary information just
        self.assertEqual(1, len(res))
        self.assertEqual("Berlin", answer)

    def test_configuration_keys(self):
        module = dspy.Predict(
            "question -> answer",
            # number of completions
            n=5
        )

        res = module(question="What are the largest cities in Germany?")
        print(res)

        # Access the outputs.
        answer_lst = res.completions.answer
        # print(answer)

        self.assertEqual(5, len(answer_lst))
        for one_answer in answer_lst:
            self.assertTrue(one_answer.find("Berlin") > -1)

    def test_chain_of_thought(self):
        qa_module = dspy.ChainOfThought("question -> answer")

        res = qa_module(question=QUESTION)
        print(res)

        self.assertEqual(2, len(res))
        self.assertIsNotNone(res.rationale)
        self.assertEqual("Berlin", res.answer)

    def test_program_of_thought(self):
        module = dspy.ProgramOfThought("question -> answer")

        # TODO:implement
        raise NotImplementedError()

    def test_re_act(self):
        module = dspy.ReAct("question -> answer")

        # TODO:implement
        raise NotImplementedError()

    def test_multi_chain_comparison(self):
        module = dspy.MultiChainComparison("question -> answer")

        # TODO:implement
        raise NotImplementedError()


if __name__ == '__main__':
    unittest.main()
