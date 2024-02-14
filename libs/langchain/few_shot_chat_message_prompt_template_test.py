import sys
import unittest

from langchain_community.vectorstores.chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import OpenAIEmbeddings


class TestFewShotChatMessagePromptTemplate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._examples = [
            {"input": "2+2", "output": "4"},
            {"input": "2+3", "output": "5"},
        ]

        cls._examples_ext = cls._examples + [
            {"input": "2+4", "output": "6"},
            {"input": "What did the cow say to the moon?", "output": "nothing at all"},
            {
                "input": "Write me a poem about the moon",
                "output": "One for the moon, and one for me, who are we to talk about the moon?",
            },
        ]

        # print(cls._examples_ext)

        # create a formatter to format the few-shot examples to a string
        cls.example_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "{input}"),
                ("ai", "{output}"),
            ]
        )
        # print(cls.example_prompt.format(**cls._examples[0]))

    def test_create_few_shot_prompt_template_from_example_set(self):
        few_shot_prompt_template = FewShotChatMessagePromptTemplate(examples=self._examples,
                                                                    example_prompt=self.example_prompt)
        prompt_text = few_shot_prompt_template.format()
        print(sys._getframe().f_code.co_name, "->")
        print(prompt_text)

    def test_create_few_shot_prompt_template_with_semantic_similarity_example_selector(self):
        # create a vectorstore and populate it
        to_vectorize = [" ".join(example.values()) for example in self._examples_ext]
        # print(to_vectorize)
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=self._examples_ext)

        # create the example selector
        example_selector = SemanticSimilarityExampleSelector(vectorstore=vectorstore, k=2)
        # The prompt template will load examples by passing the input do the `select_examples` method
        examples = example_selector.select_examples({"input": "horse"})
        # print(examples)

        # Define how each example will be formatted.
        # In this case, each example will become 2 messages:
        # 1 human, and 1 AI
        example_prompt = ChatPromptTemplate.from_messages([("human", "{input}"), ("ai", "{output}")])

        # Create prompt template
        few_shot_prompt_template = FewShotChatMessagePromptTemplate(
            # The input variables select the values to pass to the example_selector
            input_variables=["input"],
            example_selector=example_selector,
            example_prompt=example_prompt,
        )

        prompt_text = few_shot_prompt_template.format(input="What's 3+3?")
        print(sys._getframe().f_code.co_name, "->")
        print(prompt_text)

    def test_create_chat_prompt_template_for_model(self):
        few_shot_prompt_template = FewShotChatMessagePromptTemplate(examples=self._examples,
                                                                    example_prompt=self.example_prompt)

        chat_prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a wondrous wizard of math."),
                few_shot_prompt_template,
                ("human", "{input}")
            ]
        )

        prompt_text = chat_prompt_template.format(input="What's the square of a triangle?")
        print(sys._getframe().f_code.co_name, "->")
        print(prompt_text)


if __name__ == '__main__':
    unittest.main()
