import unittest

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from model import get_chat_model


class TestLCEL(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._model = get_chat_model()

    @classmethod
    def tearDownClass(cls):
        cls._model = None

    # basic example: prompt + model + output parser
    def test_pipeline_without_lcel(self):
        user_input = {"topic": "ice cream"}

        # constructs a PromptValue
        template = "tell me a short joke about {topic}"
        prompt = ChatPromptTemplate.from_template(template)
        prompt_value = prompt.invoke(user_input)

        # passes the generated prompt into the model for evaluation
        message = self._model.invoke(prompt_value)

        # takes in a message and transforms this into a string
        output_parser = StrOutputParser()
        out_str = output_parser.invoke(message)

        print(out_str)

    # basic example: prompt + model + output parser
    def test_pipeline_with_lcel(self):
        user_input = {"topic": "ice cream"}

        # create a chain components
        prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
        output_parser = StrOutputParser()

        # feeds the output from one component as input into the next component
        chain = prompt | self._model | output_parser

        # invoke the chain
        out = chain.invoke({"topic": "ice cream"})
        print(out)


if __name__ == '__main__':
    unittest.main()
