import unittest
from pprint import pprint

from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableParallel


# https://python.langchain.com/docs/expression_language/how_to/map
class TestRunnableParallel(unittest.TestCase):

    # TODO: move tests to TestLCEL

    def test_(self):
        setup_and_retrieval = RunnableParallel(
            {
                "context": "some text",
                "question": RunnablePassthrough()
            }
        )

        res = setup_and_retrieval.invoke("test")
        print(res)

        print("passed:")


if __name__ == '__main__':
    unittest.main()
