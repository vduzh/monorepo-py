import unittest

import dspy
from dspy.datasets import HotPotQA

from libs.dspy.model import get_lm


class TestRetrieve(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the LM
        lm = get_lm()

        # Set up the retrieval model
        colbert_v2_wiki17_abstracts = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')

        # Configure the DSPy
        dspy.settings.configure(lm=lm, rm=colbert_v2_wiki17_abstracts)

        # Load the dataset
        dataset = HotPotQA(train_seed=1, train_size=20, eval_seed=2023, dev_size=50, test_size=0)

        # Tell DSPy that the 'question' field is the input. Any other fields are labels and/or metadata.
        cls.train_set = [x.with_inputs('question') for x in dataset.train]
        cls.dev_set = [x.with_inputs('question') for x in dataset.dev]

    def test_retrieve(self):
        # Get an example
        dev_example = self.dev_set[18]
        question = dev_example.question

        # Create a retriever
        retrieve = dspy.Retrieve(k=3)

        # Extract the data for the question
        prediction = retrieve(question)
        print("Prediction:", prediction)

        # Get the passages from the prediction
        top_k_passages = prediction.passages

        # Print out the results
        print(f"Top {retrieve.k} passages for question: \"{question}\" \n {'-' * 30}\n")
        for i, passage in enumerate(top_k_passages):
            print(f"{i}]: {passage}\n")


if __name__ == '__main__':
    unittest.main()
