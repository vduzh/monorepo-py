import unittest
from concurrent.futures import ThreadPoolExecutor, Future, ProcessPoolExecutor
from time import sleep


def task(code=0):
    print(f"Function: Task {code} is being started...")
    sleep(1)
    print(f"Function: Task {code} finished!")
    return code * 10


def long_running_task(code=1, n=100_000_000):
    print(f"Long running task # {code} is being started...")
    while n:
        n -= 1
    print(f"Long running task # {code} finished!")


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

    def test_thread_process_executor_submit(self):
        with ProcessPoolExecutor() as executor:
            feature_1: Future = executor.submit(long_running_task, code=100, n=100_000_000)
            feature_2: Future = executor.submit(long_running_task, code=50, n=50_000_000)

            print("ProcessPoolExecutor::submit:result ", feature_1.result())
            print("ProcessPoolExecutor::submit:result ", feature_2.result())

    def test_thread_process_executor_map(self):
        with ProcessPoolExecutor() as executor:
            results_iterator = executor.map(
                long_running_task,
                [30, 50],
                [30_000_000, 50_000_000]
            )
            print("map: ", list(results_iterator))


if __name__ == '__main__':
    unittest.main()
