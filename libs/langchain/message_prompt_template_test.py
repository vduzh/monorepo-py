import unittest

from langchain_core.prompts import HumanMessagePromptTemplate, AIMessagePromptTemplate, SystemMessagePromptTemplate


class TestMessagePromptTemplate(unittest.TestCase):

    def test_system_message_prompt_template(self):
        template = "System template text will go here.."
        system_message_prompt_template = SystemMessagePromptTemplate.from_template(template)
        print(system_message_prompt_template)

    def test_ai_message_prompt_template(self):
        template = "AI template text will go here.."
        ai_message_prompt_template = AIMessagePromptTemplate.from_template(template)
        print(ai_message_prompt_template)

    def test_human_message_prompt_template(self):
        template = "Summarize our conversation so far in {word_count} words."
        human_message_prompt_template = HumanMessagePromptTemplate.from_template(template)
        print(human_message_prompt_template)


if __name__ == '__main__':
    unittest.main()
