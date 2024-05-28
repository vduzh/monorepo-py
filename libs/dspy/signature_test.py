import unittest
from unittest import TestCase

import dspy
from pydantic import BaseModel, Field

from libs.dspy.utils.model import get_lm

QUESTION = "What is the capital of Germany?"


# A signature is a declarative specification of input/output behavior of a DSPy module
#
# Signatures tell the LM what it needs to do, rather than specify how we should ask the LM to do it.
class TestSignature(TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the LM
        lm = get_lm()
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

    def test_typed_predictors(self):
        class Input(BaseModel):
            context: str = Field(description="The context for the question")
            query: str = Field(description="The question to be answered")

        class Output(BaseModel):
            answer: str = Field(description="The answer for the question")
            confidence: float = Field(ge=0, le=1, description="The confidence score for the answer")

        class QASignature(dspy.Signature):
            """
            Answer the question based on the context and query provided, and on the scale of 10 tell how confident
            you are about the answer.
            """

            input: Input = dspy.InputField()
            output: Output = dspy.OutputField()

        # define typed predictor
        predictor = dspy.TypedPredictor(QASignature)

        # the same thing
        # predictor = dspy.TypedPredictor("input:Input -> output:Output")

        # testing out
        doc_query_pair = Input(
            context="The quick brown fox jumps over the lazy dog",
            query="What does the fox jumps over?",
        )

        prediction = predictor(input=doc_query_pair)
        output = prediction.output

        # unpack
        answer, confidence = output

        print(f"Prediction: {prediction}\n")
        print(f"Answer: {answer}, Answer Type: {type(answer)}")
        print(f"Confidence Score: {confidence}, Confidence Score Type: {type(confidence)}")


if __name__ == '__main__':
    unittest.main()
