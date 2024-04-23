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

    def test_lm(self):
        # Define the signature (return an answer, given a question)
        signature_str = "question -> answer"
        # Create a module (ChainOfThought) and assign it the signature.
        qa_module = dspy.ChainOfThought(signature_str)

        # Run with the default LM configured with `dspy.configure` above.
        response_as_prediction = qa_module(question=QUESTION)
        print(response_as_prediction)

        self.assertEqual("Berlin", response_as_prediction.answer)

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
        # call the module
        classify = dspy.Predict(signature)

        response = classify(sentence=sentence)
        print(response)

        self.assertEqual("Positive", response.sentiment)

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

    def test_inline_signatures_rag_question_answering(self):
        # TODO: implement
        raise NotImplementedError("Retrieval-Augmented Question Answering not implemented yet")

        signature = "context, question -> answer"
        # rag_qa = dspy.Predict(signature)
        #
        # response = rag_qa(context="", question=QUESTION)
        # print(response)
        #
        # self.assertEqual("Berlin", response.answer)

    def test_inline_signatures_multiple_choice_question_answering_with_reasoning(self):
        # TODO: implement
        raise NotImplementedError("Multiple-Choice Question Answering with Reasoning not implemented yet")

        signature = "question, choices -> reasoning, selection"
        # rag_qa = dspy.Predict(signature)
        #
        # response = rag_qa(context="", question=QUESTION)
        # print(response)
        #
        # self.assertEqual("Berlin", response.answer)

    def test_class_based_signatures_sentiment_classification(self):
        class Emotion(dspy.Signature):
            """Classify emotion among sadness, joy, love, anger, fear, surprise."""

            sentence = dspy.InputField()
            sentiment = dspy.OutputField()

        # example from dair-ai/emotion
        sentence = "i started feeling a little vulnerable when the giant spotlight started blinding me"

        classify = dspy.Predict(Emotion)

        response = classify(sentence=sentence)
        print(response)

        self.assertEqual("fear", response.sentiment)

    def test_class_based_signatures_evaluate_faithfulness_to_citations(self):
        class CheckCitationFaithfulness(dspy.Signature):
            """Verify that the text is based on the provided context."""

            context = dspy.InputField(desc="facts here are assumed to be true")
            text = dspy.InputField()
            faithfulness = dspy.OutputField(desc="True/False indicating if text is faithful to context")

        # build the context
        context = """
            The 21-year-old made seven appearances for the Hammers and netted his only goal for them in a Europa League
            qualification round match against Andorran side FC Lustrains last season. Lee had two loan spells in League 
            One last term, with Blackpool and then Colchester United. He scored twice for the U's but was 
            unable to save them from relegation. The length of Lee's contract with the promoted Tykes has not been 
            revealed. Find all the latest football transfers on our dedicated page.
        """

        # specify text to evaluate
        text = "Lee scored 3 goals for Colchester United."

        # create a module
        faithfulness = dspy.ChainOfThought(CheckCitationFaithfulness)

        # run the program
        response = faithfulness(context=context, text=text)
        print(response)

        # assert the result
        self.assertFalse(eval(response.faithfulness))


if __name__ == '__main__':
    unittest.main()
