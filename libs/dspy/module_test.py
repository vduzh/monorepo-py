import unittest
from unittest import TestCase

import dspy

from model import get_lm

QUESTION = "What is the capital of Germany?"


class TestModule(TestCase):

    @classmethod
    def setUpClass(cls):
        lm = get_lm()
        dspy.settings.configure(lm=lm)

    def test_built_in_predict_module(self):
        # 1. Define the signature.
        signature = "question -> answer"

        # 2. Declare the Predict module with the signature.
        predict_module = dspy.Predict(signature)

        # 3. Call the module with input argument(s).
        res = predict_module(question=QUESTION)

        # Inspect the last prompt for the LM
        dspy.settings.lm.inspect_history(n=1)
        print("Response:", res)

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
        print("Prediction:", res)

        # Access the outputs.
        answer_lst = res.completions.answer
        # print(answer)

        self.assertEqual(5, len(answer_lst))
        for a in answer_lst:
            self.assertIn("Berlin", a)

    def test_built_in_chain_of_thought_module(self):
        qa_module = dspy.ChainOfThought("question -> answer")

        res = qa_module(question=QUESTION)
        print("rationale:", res.rationale)
        print("answer:", res.answer)

        self.assertEqual(2, len(res))
        self.assertIsNotNone(res.rationale)
        self.assertEqual("Berlin", res.answer)

    def test_built_in_program_of_thought_module(self):
        module = dspy.ProgramOfThought("question -> answer")

        # TODO:implement
        raise NotImplementedError()

    def test_built_in_re_act_module(self):
        module = dspy.ReAct("question -> answer")

        # TODO:implement
        raise NotImplementedError()

    def test_built_in_multi_chain_comparison_module(self):
        module = dspy.MultiChainComparison("question -> answer")

        # TODO:implement
        raise NotImplementedError()

    def test_custom_module(self):
        class CustomModule(dspy.Module):
            def __init__(self):
                super().__init__()
                self.prog = dspy.Predict("question -> answer")

            def forward(self, question):
                return self.prog(question=question)

        custom_module = CustomModule()
        prediction = custom_module(question=QUESTION)
        # print(prediction)

        self.assertEqual(1, len(prediction))
        self.assertEqual("Berlin", prediction.answer)


if __name__ == '__main__':
    unittest.main()
