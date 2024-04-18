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

    def test_inline_signatures_question_answering(self):
        signature = "question -> answer"
        qa = dspy.Predict(signature)

        response = qa(question=QUESTION)
        print(response)

        self.assertEqual("Berlin", response.answer)

    def test_inline_signatures_sentiment_classification(self):
        # example from the SST-2 dataset.
        sentence = "it's a charming and often affecting journey."

        signature = "sentence -> sentiment"
        classify = dspy.Predict(signature)

        response = classify(sentence=sentence)
        print(response)

        # self.assertEqual("Positive", response.sentiment)

    def test_inline_signatures_summarization(self):
        # Example from the XSum dataset.
        document = """
            The 21-year-old made seven appearances for the Hammers and netted his only goal for them in a Europa League 
            qualification round match against Andorran side FC Lustrains last season. 
            Lee had two loan spells in League One last term, with Blackpool and then Colchester United. 
            He scored twice for the U's but was unable to save them from relegation. 
            The length of Lee's contract with the promoted Tykes has not been revealed. 
            Find all the latest football transfers on our dedicated page.
        """

        signature = "document -> summary"
        summarize = dspy.Predict(signature)

        response = summarize(document=document)
        print(response.summary)

        # self.assertEqual("Neutral", response.sentiment)

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
