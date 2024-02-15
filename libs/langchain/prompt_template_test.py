import unittest
from datetime import datetime

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import StringPromptValue
from langchain_core.prompts import PromptTemplate

from model import get_llm


def _get_foo():
    return "Foo"


class TestPromptTemplates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._llm = get_llm()
        cls._output_parser = StrOutputParser()

    @classmethod
    def tearDownClass(cls):
        cls._llm = None

    def test_create_prompt_template(self):
        template = "What is a good name for a company that makes {product}?"
        prompt_template = PromptTemplate(
            template=template,
            input_variables=["product"]
        )
        # print(prompt_template)

    def test_create_prompt_template_from_template(self):
        template = "What is a good name for a company that makes {product}?"
        prompt_template = PromptTemplate.from_template(template)
        print(prompt_template)

        self.assertEqual(prompt_template.template, template)
        self.assertEqual(prompt_template.input_variables, ["product"])

    def test_create_prompt_with_string_prompt_composition(self):
        template = "What is a good name for a company that makes colorful socks?"
        text = ", make it funny and in {language}"
        prompt_template = PromptTemplate.from_template(template) + text

        self.assertEqual(prompt_template.template, template + text)
        self.assertEqual(prompt_template.input_variables, ["language"])

    def test_format_prompt(self):
        template = "What is a good name for a company that makes {product}?"
        prompt_template = PromptTemplate.from_template(template)

        product = "colorful socks"
        prompt_text = prompt_template.format(product=product)

        self.assertEqual(prompt_text, template.replace("{product}", product))

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

    def test_partial_prompt_templates_with_strings(self):
        prompt_template = PromptTemplate.from_template("{foo}{bar}")
        partial_prompt_template = prompt_template.partial(foo="Foo")

        template_text = partial_prompt_template.format(bar="Bar")

        self.assertEqual(template_text, "FooBar")

    def test_partial_prompt_templates_with_functions(self):
        prompt_template = PromptTemplate.from_template("{foo}{bar}")
        partial_prompt_template = prompt_template.partial(foo=_get_foo)

        template_text = partial_prompt_template.format(bar="Bar")

        self.assertEqual(template_text, "FooBar")

    def test_basic_chain(self):
        prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
        # chain = prompt | self._llm | self._output_parser
        # out = chain.invoke({"product": "colorful socks"})


if __name__ == '__main__':
    unittest.main()
