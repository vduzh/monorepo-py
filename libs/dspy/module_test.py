import unittest
from unittest import TestCase

import dspy

from libs.dspy.utils.model import get_lm

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

        prediction = qa_module(question=QUESTION)
        print("rationale:", prediction.rationale)
        print("answer:", prediction.answer)

        self.assertEqual(2, len(prediction))
        self.assertIsNotNone(prediction.rationale)
        self.assertEqual("Berlin", prediction.answer)

    def test_built_in_chain_of_thought_with_hint(self):
        generate_answer = dspy.ChainOfThoughtWithHint("question -> answer")

        # Call the predictor on a particular input alongside a hint.
        prediction = generate_answer(
            question="What is the color of the sky?",
            hint="It's what you often see during a sunny day."
        )
        print(prediction)

        self.assertEqual(2, len(prediction))
        self.assertIsNotNone(prediction.rationale)
        self.assertIsNotNone(prediction.answer)

    def test_built_in_program_of_thought_module(self):
        pot = dspy.ProgramOfThought("question -> answer")

        prediction = pot(
            question="Sarah has 5 apples. She buys 7 more apples from the store. How many apples does Sarah have now?"
        )
        print(prediction)

        self.assertEqual(2, len(prediction))
        self.assertIsNotNone(prediction.rationale)
        self.assertIsNotNone(prediction.answer)

    def test_built_in_re_act_module(self):
        react_module = dspy.ReAct("question -> answer")

        prediction = react_module(
            question='Sarah has 5 apples. She buys 7 more apples from the store. How many apples does Sarah have now?'
        )
        print(prediction)

        self.assertEqual(2, len(prediction))
        self.assertIsNotNone(prediction.rationale)
        self.assertIsNotNone(prediction.answer)

    def test_built_in_multi_chain_comparison_module(self):
        module = dspy.MultiChainComparison("question -> answer")

        # TODO:implement
        raise NotImplementedError()

    def test_custom_module(self):
        # 1. Define the module (a custom program)
        class CustomModule(dspy.Module):
            def __init__(self):
                super().__init__()
                # Start with just a single dspy.ChainofThought module
                self.prog = dspy.ChainOfThought("question -> answer")

                # Add complexity incrementally as you go
                # some other llm calls

            def forward(self, question):
                return self.prog(question=question)

        # 2. Create an instance of the module
        custom_module = CustomModule()

        # 3. Call the module with input argument(s).
        prediction = custom_module(question=QUESTION)
        # print(prediction)

        # Inspect the Model's History
        dspy.settings.lm.inspect_history(n=1)

        # 4. Access the output.
        answer = prediction.answer

        # Assert the answer
        self.assertEqual("Berlin", answer)


if __name__ == '__main__':
    unittest.main()
