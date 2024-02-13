import unittest

from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from model import get_llm


class TestLLMChain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._llm = get_llm()
        cls._output_parser = StrOutputParser()

    @classmethod
    def tearDownClass(cls):
        cls._llm = None

    def test_create_chain(self):
        prompt = PromptTemplate.from_template("What is a good name for a company that makes ${product}?")
        chain = LLMChain(llm=self._llm, prompt=prompt)
        print(chain)

        # execute chain
        # res = chain.run(product="colorful socks")

    def test_create_chain_with_lcel(self):
        prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
        chain = prompt | self._llm | self._output_parser
        print(chain)

        # out = chain.invoke({"product": "colorful socks"})

    # def test_basic_chain(self):
    #     prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
    #     chain = prompt | self._llm | self._output_parser
    #     # out = chain.invoke({"product": "colorful socks"})



if __name__ == '__main__':
    unittest.main()
