import unittest

from langchain_community.vectorstores.chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings


class TestSelectors(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # examples of antonyms
        cls._examples = [
            {"input": "happy", "output": "sad"},
            {"input": "tall", "output": "short"},
            {"input": "energetic", "output": "lethargic"},
            {"input": "sunny", "output": "gloomy"},
            {"input": "windy", "output": "calm"},
        ]

    def test_create_semantic_similarity_example_selector(self):
        example_selector = SemanticSimilarityExampleSelector.from_examples(
            # the list of examples available to select from
            self._examples,
            # the embedding class used to produce embeddings which are used to measure semantic similarity
            OpenAIEmbeddings(),
            # VectorStore class that is used to store the embeddings and do a similarity search over
            Chroma,
            # This is the number of examples to produce.
            k=2,
        )

        # select the most similar example to the input.
        input_text = "worried"
        selected_examples = example_selector.select_examples({"input": input_text})

        print(f"Examples most similar to the input: {input_text}")
        self.print_selected_examples(selected_examples)

    def test_add_example_to_semantic_similarity_example_selector(self):
        example_selector = SemanticSimilarityExampleSelector.from_examples(
            self._examples, OpenAIEmbeddings(), Chroma, k=2)
        # add new example to the selector
        example_selector.add_example(
            {"input": "anxious", "output": "calm"}
        )

        # select the most similar example to the input.
        input_text = "worried"
        selected_examples = example_selector.select_examples({"input": input_text})

        print(f"Examples most similar to the input: {input_text}")
        self.print_selected_examples(selected_examples)

    @staticmethod
    def print_selected_examples(examples):
        for example in examples:
            print("== Example ==\n")
            for k, v in example.items():
                print(f"{k}: {v}")


if __name__ == '__main__':
    unittest.main()
