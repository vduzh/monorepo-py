import unittest

from langchain_core.runnables import RunnableLambda, Runnable


class TestRunnable(unittest.TestCase):

    def test_runnable(self):
        # create a Runnable
        runnable: Runnable = RunnableLambda(lambda x: x + 1)
        # transform a single input into an output
        out = runnable.invoke(1)
        # assert the result
        self.assertEqual(2, out)

    def test_runnable_chain(self):
        # create two Runnables
        first_runnable: Runnable = RunnableLambda(lambda x: x + 1)
        second_runnable: Runnable = RunnableLambda(lambda x: x * 10)
        # build a chain
        out = second_runnable.invoke(first_runnable.invoke(1))
        # assert the result
        self.assertEqual(20, out)

    def test_runnable_chain_as_lcel(self):
        # build a chain of 2 runables
        chain = RunnableLambda(lambda x: x + 1) | RunnableLambda(lambda x: x * 10)
        # transform a single input into an output
        out = chain.invoke(1)
        # assert the result
        self.assertEqual(20, out)



if __name__ == '__main__':
    unittest.main()
