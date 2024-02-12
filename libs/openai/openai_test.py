import os
import unittest

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_API_KEY"),
)

model = "gpt-3.5-turbo"
model_with_embedding = "text-embedding-3-small"


class TestOpenAI(unittest.TestCase):

    def test_create_completion(self):
        test_value = "This is a test!"
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say " + test_value,
                }
            ],
            model=model,
        )
        self.assertTrue(len(chat_completion.choices), 1)

        choice = chat_completion.choices[0]
        self.assertTrue(choice.finish_reason, 'stop')
        self.assertTrue(choice.message.content, test_value)

    def test_create_completion_with_2_choices(self):
        test_value = "This is a test!"
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say " + test_value,
                }
            ],
            model=model,
            n=2
        )
        self.assertTrue(len(chat_completion.choices), 2)

    def test_create_embedding(self):
        test_text = "This is a test!"
        res = client.embeddings.create(input=test_text, model=model_with_embedding)
        embedding = res.data[0].embedding
        self.assertTrue(len(embedding) > 0)


if __name__ == '__main__':
    unittest.main()
