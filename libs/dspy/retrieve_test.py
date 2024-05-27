import unittest

import dspy

from libs.dspy.model import get_lm


class TestRetrieve(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the LM
        lm = get_lm()

        # Set up the retrieval model
        retrieval_model = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')

        # Configure the DSPy
        dspy.settings.configure(lm=lm, rm=retrieval_model)

    def test_retrieve(self):
        # Question
        question = """ Who conducts the draft in which Marc-Andre Fleury was drafted to the Vegas Golden Knights for 
        the 2017-18 season?"""

        # Create a retriever
        retrieve = dspy.Retrieve(k=3)

        # Search for the top-k passages that match a given query
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
