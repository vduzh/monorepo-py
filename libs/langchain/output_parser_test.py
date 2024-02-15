import unittest

from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from model import get_llm


# Define your desired data structure.
class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")

    # You can add custom validation logic easily with Pydantic.
    # @validator("setup")
    # def question_ends_with_question_mark(self, field):
    #     if field[-1] != "?":
    #         raise ValueError("Badly formed question!")
    #     return field


class TestOutputParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._llm = get_llm()

    @classmethod
    def tearDownClass(cls):
        cls._llm = None

    def test_parse(self):
        output_parser = CommaSeparatedListOutputParser()

        str_list = output_parser.parse("one, two")
        self.assertEqual(str_list, ["one", "two"])

    def test_invoke(self):
        output_parser = CommaSeparatedListOutputParser()

        str_list = output_parser.invoke("one, two")
        self.assertEqual(str_list, ["one", "two"])

    def test_lcel(self):
        # add parser to a Runnable sequence
        output_parser = CommaSeparatedListOutputParser()

        # create prompt
        prompt = PromptTemplate.from_template("Form words one and two in comma separated format")

        # create a chain
        chain = prompt | self._llm | output_parser

        # Transform a single input into an output
        out_str = chain.invoke({})

        self.assertEqual(out_str, ["one", "two"])

    def test_partial_variables(self):
        parser = CommaSeparatedListOutputParser()

        format_instructions = parser.get_format_instructions()
        prompt = PromptTemplate(
            template="List two {subject}.\n{format_instructions}",
            input_variables=["subject"],
            partial_variables={"format_instructions": format_instructions}
        )

        chain = prompt | self._llm | parser
        out_str = chain.invoke({"subject": "numbers in words starting from 1"})

        self.assertEqual(out_str, ["one", "two"])

    def test_comma_separated_list_output_parser(self):
        output_parser = CommaSeparatedListOutputParser()

        str_list = output_parser.parse("one, two")
        self.assertEqual(str_list, ["one", "two"])

    def test_pydantic_output_parser(self):
        # set up a parser + inject instructions into the prompt template
        output_parser = PydanticOutputParser(pydantic_object=Joke)

        prompt = PromptTemplate(
            template="Answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": output_parser.get_format_instructions()},
        )

        # set up a query intended to prompt a language model to populate the data structure
        prompt_and_model = prompt | self._llm
        output = prompt_and_model.invoke({"query": "Tell me a joke."})

        joke = output_parser.invoke(output)
        print(joke)


if __name__ == '__main__':
    unittest.main()
