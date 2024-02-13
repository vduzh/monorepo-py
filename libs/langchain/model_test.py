import unittest

from model import get_model


class TestPromptTemplates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the model
        cls._llm = get_model()

    @classmethod
    def tearDownClass(cls):
        cls._llm = None

    def test_basic(self):
        test_value = "This is a test!"
        s = self._llm.invoke("Say " + test_value)
        self.assertTrue(s.content, test_value)


if __name__ == '__main__':
    unittest.main()
