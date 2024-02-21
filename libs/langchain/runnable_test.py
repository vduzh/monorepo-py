import unittest

from langchain_core.runnables import RunnableLambda, Runnable


class TestRunnable(unittest.TestCase):

    def test_runnable(self):
        runnable: Runnable = RunnableLambda(lambda x: x + 1)

        # transforms a single input into an output
        out = runnable.invoke(1)

        self.assertEqual(2, out)

    def test_runnable_chain(self):
        first_runnable: Runnable = RunnableLambda(lambda x: x + 1)
        second_runnable: Runnable = RunnableLambda(lambda x: x * 10)

        out = second_runnable.invoke(first_runnable.invoke(1))

        self.assertEqual(20, out)



if __name__ == '__main__':
    unittest.main()
