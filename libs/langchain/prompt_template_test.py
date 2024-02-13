import unittest

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import StringPromptValue
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
        text = "What is a good name for a company that makes colorful socks?"
        prompt_template = PromptTemplate.from_template(text)
        self.assertEqual(prompt_template.template, text)

    def test_create_prompt_with_string_prompt_composition(self):
        template = "What is a good name for a company that makes colorful socks?"
        text = ", make it funny and in {language}"
        prompt_template = PromptTemplate.from_template(template) + text
        self.assertEqual(prompt_template.template, template + text)
        self.assertEqual(prompt_template.input_variables, ["language"])

    def test_format_prompt(self):
        prompt_template = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
        text = prompt_template.format(product="colorful socks")
        self.assertEqual(text, "What is a good name for a company that makes colorful socks?")

    def test_invoke_string_prompt_value(self):
        prompt_template = PromptTemplate.from_template("Test {foo}")

        string_prompt_value = prompt_template.invoke({"foo": "Foo"})

        self.assertIs(type(string_prompt_value), StringPromptValue)
        self.assertEqual(string_prompt_value.to_string(), "Test Foo")

        message_list = string_prompt_value.to_messages();
        self.assertEqual(len(message_list), 1)
        message = message_list[0]
        self.assertIs(type(message), HumanMessage)
        self.assertEqual(len(message_list), 1)

    def test_basic_chain(self):
        prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
        # chain = prompt | self._llm | self._output_parser
        # out = chain.invoke({"product": "colorful socks"})


if __name__ == '__main__':
    unittest.main()
