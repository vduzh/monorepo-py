import unittest

from langchain_community.vectorstores.chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_openai import OpenAIEmbeddings


class TestFewShotPromptTemplate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # create the example set
        cls._examples = [
            # each example is a dictionary
            {
                # the question is an input variable, the value is its value
                "question": "Who lived longer, Muhammad Ali or Alan Turing?",
                "answer": """
        Are follow up questions needed here: Yes.
        Follow up: How old was Muhammad Ali when he died?
        Intermediate answer: Muhammad Ali was 74 years old when he died.
        Follow up: How old was Alan Turing when he died?
        Intermediate answer: Alan Turing was 41 years old when he died.
        So the final answer is: Muhammad Ali
                            """,

            },
            {
                "question": "When was the founder of craigslist born?",
                "answer": """
        Are follow up questions needed here: Yes.
        Follow up: Who was the founder of craigslist?
        Intermediate answer: Craigslist was founded by Craig Newmark.
        Follow up: When was Craig Newmark born?
        Intermediate answer: Craig Newmark was born on December 6, 1952.
        So the final answer is: December 6, 1952
                """,
            },
            {
                "question": "Who was the maternal grandfather of George Washington?",
                "answer": """
        Are follow up questions needed here: Yes.
        Follow up: Who was the mother of George Washington?
        Intermediate answer: The mother of George Washington was Mary Ball Washington.
        Follow up: Who was the father of Mary Ball Washington?
        Intermediate answer: The father of Mary Ball Washington was Joseph Ball.
        So the final answer is: Joseph Ball
                """,
            },
            {
                "question": "Are both the directors of Jaws and Casino Royale from the same country?",
                "answer": """
        Are follow up questions needed here: Yes.
        Follow up: Who is the director of Jaws?
        Intermediate Answer: The director of Jaws is Steven Spielberg.
        Follow up: Where is Steven Spielberg from?
        Intermediate Answer: The United States.
        Follow up: Who is the director of Casino Royale?
        Intermediate Answer: The director of Casino Royale is Martin Campbell.
        Follow up: Where is Martin Campbell from?
        Intermediate Answer: New Zealand.
        So the final answer is: No
                """,
            },
        ]

        # create a formatter to format the few-shot examples to a string
        cls.example_prompt = PromptTemplate(input_variables=["question", "answer"],
                                            template="Question: {question}\n{answer}")
        # print(cls.example_prompt.format(**cls.examples[0]))

    def test_create_prompt_template_from_example_set(self):
        # feed examples and formatter to FewShotPromptTemplate
        few_shot_prompt_template = FewShotPromptTemplate(
            examples=self.examples,
            example_prompt=self.example_prompt,
            suffix="Question: {input}",
            input_variables=["input"]
        )

        # generate the text of the prompt
        prompt_text = few_shot_prompt_template.format(input="Who was the father of Mary Ball Washington?")
        print(prompt_text)

    def test_create_prompt_template_with_semantic_similarity_example_selector(self):
        example_selector = SemanticSimilarityExampleSelector.from_examples(
            self._examples, OpenAIEmbeddings(), Chroma, k=1
        )

        question = "Who was the father of Mary Ball Washington?"
        selected_examples = example_selector.select_examples({"question": question})

        few_shot_prompt_template = FewShotPromptTemplate(
            example_selector=example_selector,
            example_prompt=self.example_prompt,
            suffix="Question: {input}",
            input_variables=["input"],
        )

        # generate the text of the prompt
        prompt_text = few_shot_prompt_template.format(input="Who was the father of Mary Ball Washington?")
        print(prompt_text)


if __name__ == '__main__':
    unittest.main()
