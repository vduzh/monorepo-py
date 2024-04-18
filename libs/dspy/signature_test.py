import unittest
from unittest import TestCase

import dspy

from model import get_lm


class TestSignature(TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the LM
        lm = get_lm()
        lm.inspect_history(n=1)
        dspy.settings.configure(lm=lm)

    def test_lm(self):
        # Define the signature (return an answer, given a question)
        signature_str = "question -> answer"
        # Create a module (ChainOfThought) and assign it the signature.
        qa_module = dspy.ChainOfThought(signature_str)

        # Run with the default LM configured with `dspy.configure` above.
        response_as_prediction = qa_module(question="What is the capital of Germany?")
        print(response_as_prediction)

        self.assertEqual("Berlin", response_as_prediction.answer)


if __name__ == '__main__':
    unittest.main()
