import unittest
from concurrent.futures import ThreadPoolExecutor, Future
from time import sleep


def task(code=0):
    print(f"Function: Task {code} is being started...")
    sleep(1)
    print(f"Function: Task {code} finished!")
    return code * 10


class TestConcurrent(unittest.TestCase):

    def test_thread_pool_executor_submit(self):
        with ThreadPoolExecutor() as executor:
            feature_1: Future = executor.submit(task, 20)
            feature_2: Future = executor.submit(task, 21)

            print("submit: ", feature_1.result())
            print("submit: ", feature_2.result())

    def test_thread_pool_executor_map(self):
        with ThreadPoolExecutor() as executor:
            results_iterator = executor.map(task, [30, 31])
            print("map: ", list(results_iterator))


if __name__ == '__main__':
    unittest.main()
