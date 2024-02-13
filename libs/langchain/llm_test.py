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

    def test_input_str_and_output_str(self):
        text = "This is a test!"
        res = self._llm.invoke("Say " + text)
        self.assertIs(type(res), str)

    def test_invoke(self):
        text = "This is a test!"
        res = self._llm.invoke("Say " + text)
        self.assertEqual(res.strip(), text)


if __name__ == '__main__':
    unittest.main()
