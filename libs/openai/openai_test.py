import unittest
from pprint import pprint

from libs.openai.model import get_llm, get_model_name, get_embedding_model_name


class TestOpenAI(unittest.TestCase):
    def setUp(self):
        self.client = get_llm()

    def test_create_completion(self):
        test_value = "This is a test!"
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "user", "content": "Say " + test_value}
            ],
            model=get_model_name(),
        )
        pprint(chat_completion)

        self.assertTrue(len(chat_completion.choices), 1)

        choice = chat_completion.choices[0]
        self.assertTrue(choice.finish_reason, 'stop')
        self.assertTrue(choice.message.content, test_value)

    def test_create_completion_with_2_choices(self):
        test_value = "This is a test!"
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "user", "content": "Say " + test_value}
            ],
            model=get_model_name(),
            n=2
        )
        pprint(chat_completion)

        self.assertTrue(len(chat_completion.choices), 2)

    def test_create_embedding(self):
        test_text = "This is a test!"
        res = self.client.embeddings.create(
            input=test_text,
            model=get_embedding_model_name(),
        )

        embedding = res.data[0].embedding
        pprint(embedding[:10])

        self.assertTrue(len(embedding) > 0)


if __name__ == '__main__':
    unittest.main()
