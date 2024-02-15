import unittest

from model import get_llm


class TestLLM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the model
        cls._llm = get_llm()

    @classmethod
    def tearDownClass(cls):
        cls._llm = None

    def test_invoke(self):
        input_text = "This is a test!"
        output_str = self._llm.invoke("Say " + input_text)
        self.assertEqual(output_str.strip(), input_text)

    def test_stream(self):
        for chunk_str in self._llm.stream("What is a good name for a company that makes colorful socks?"):
            print(chunk_str, end="", flush=True)

    def test_batch(self):
        messages = [
            "What is a good name for a company that makes colorful socks?",
            "What are some theories about the relationship between unemployment and inflation?",
        ]

        result_list = self._llm.batch(messages)
        print(result_list)


if __name__ == '__main__':
    unittest.main()
