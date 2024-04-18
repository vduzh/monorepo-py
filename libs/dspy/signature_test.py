import unittest
from unittest import TestCase

import dspy

from model import get_lm

QUESTION = "What is the capital of Germany?"


# A signature is a declarative specification of input/output behavior of a DSPy module
#
# Signatures tell the LM what it needs to do, rather than specify how we should ask the LM to do it.
class TestSignature(TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the LM
        lm = get_lm()
        lm.inspect_history(n=1)
        dspy.settings.configure(lm=lm)

    def test_inline_signatures_qa(self):
        signature = "question -> answer"
        qa = dspy.Predict(signature)

        response = qa(question=QUESTION)
        print(response)

        self.assertEqual("Berlin", response.answer)

    def test_lm(self):
        # Define the signature (return an answer, given a question)
        signature_str = "question -> answer"
        # Create a module (ChainOfThought) and assign it the signature.
        qa_module = dspy.ChainOfThought(signature_str)

        # Run with the default LM configured with `dspy.configure` above.
        response_as_prediction = qa_module(question=QUESTION)
        print(response_as_prediction)

        self.assertEqual("Berlin", response_as_prediction.answer)


if __name__ == '__main__':
    unittest.main()
