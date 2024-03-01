import unittest
from pprint import pprint

from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableParallel


# https://python.langchain.com/docs/expression_language/how_to/functions
class TestRunnableLambda(unittest.TestCase):
    def test_(self):
        print("passed:")


if __name__ == '__main__':
    unittest.main()
