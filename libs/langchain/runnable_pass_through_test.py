import unittest
from pprint import pprint

from langchain_core.runnables import RunnablePassthrough, RunnableLambda


class TestRunnablePassthrough(unittest.TestCase):

    def test_pass_through_without_prm(self):
        runnable = (
                {"passed": RunnablePassthrough()}
                |
                RunnableLambda(lambda data: data.get('passed'))
        )

        res = runnable.invoke({"foo": "data 1", "bar": "data 2"})
        print("passed:", res)

    def test_pass_through_with_assign(self):
        runnable = (
            {"extra": RunnablePassthrough.assign(bar=lambda x: x["foo"] + "???!")}
            |
            RunnableLambda(lambda data: data.get('extra'))
        )

        res = runnable.invoke({"foo": "10"})
        print("extra:", res)

    def test_pass_through_mix(self):
        runnable = (
            {"passed": RunnablePassthrough()}
            |
            {"extra": RunnablePassthrough.assign(bar=lambda x: x["foo"] + "???!")}
            |
            RunnableLambda(lambda data: data)
        )

        res = runnable.invoke({"foo": "10"})
        print("mix:", res)


if __name__ == '__main__':
    unittest.main()
