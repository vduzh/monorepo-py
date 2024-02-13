import unittest

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from model import get_llm


class TestPromptTemplates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._llm = get_llm()
        cls._output_parser = StrOutputParser()

    @classmethod
    def tearDownClass(cls):
        cls._llm = None

    def test_create_prompt_from_template(self):
        prompt = PromptTemplate.from_template("What is a good name for a company that makes colorful socks?")

    def test_format_prompt(self):
        prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
        text = prompt.format(product="colorful socks")
        self.assertEqual(text, "What is a good name for a company that makes colorful socks?")

    def test_basic_chain(self):
        prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
        chain = prompt | self._llm | self._output_parser
        out = chain.invoke({"product": "colorful socks"})

if __name__ == '__main__':
    unittest.main()
