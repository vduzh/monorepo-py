import unittest

import dspy
from dspy.datasets import HotPotQA
from dspy.evaluate import answer_exact_match, answer_passage_match
from dspy.teleprompt import BootstrapFewShot

from libs.dspy.model import get_lm


class TestRag(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the LM
        lm = get_lm()
        lm.inspect_history(n=1)

        # Set up the retrieval model
        colbert_v2_wiki17_abstracts = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')

        # Configure the DSPy
        dspy.settings.configure(lm=lm, rm=colbert_v2_wiki17_abstracts)

        # Load the dataset
        dataset = HotPotQA(train_seed=1, train_size=20, eval_seed=2023, dev_size=50, test_size=0)

        # Tell DSPy that the 'question' field is the input. Any other fields are labels and/or metadata.
        cls.train_set = [x.with_inputs('question') for x in dataset.train]
        cls.dev_set = [x.with_inputs('question') for x in dataset.dev]

    def test_rag(self):
        # Define the signature
        class GenerateAnswer(dspy.Signature):
            """Answer questions with short factoid answers."""

            context = dspy.InputField(desc="may contain relevant facts")
            question = dspy.InputField()

            answer = dspy.OutputField(desc="often between 1 and 5 words")

        # Build the Pipeline as a DSPy module
        class RAG(dspy.Module):
            def __init__(self, num_passages=3):
                super().__init__()

                self.retrieve = dspy.Retrieve(k=num_passages)
                self.generate_answer = dspy.ChainOfThought(GenerateAnswer)

            def forward(self, question):
                # search for the top-num_passages relevant passages
                context = self.retrieve(question).passages

                # generate the answer
                prediction = self.generate_answer(context=context, question=question)

                # return the answer
                return dspy.Prediction(context=context, answer=prediction.answer)

        # Optimize the Pipeline

        # Validation logic: check that the predicted answer is correct.
        # Also check that the retrieved context does actually contain that answer.
        def validate_context_and_answer(example, pred, trace=None):
            answer_em = answer_exact_match(example, pred)
            answer_pm = answer_passage_match(example, pred)
            return answer_em and answer_pm

        # Set up a basic teleprompter, which will compile our RAG program.
        teleprompter = BootstrapFewShot(metric=validate_context_and_answer)

        # Compile!
        compiled_rag = teleprompter.compile(RAG(), trainset=self.train_set)

        # Ask any question you like to this simple RAG program.
        my_question = "What castle did David Gregory inherit?"

        # Get the prediction. This contains `pred.context` and `pred.answer`.
        prediction = compiled_rag(my_question)

        # Print the contexts and the answer.
        print(f"Question: {my_question}")
        print(f"Predicted Answer: {prediction.answer}")
        print(f"Retrieved Contexts (truncated): {[c[:200] + '...' for c in prediction.context]}")


if __name__ == '__main__':
    unittest.main()
