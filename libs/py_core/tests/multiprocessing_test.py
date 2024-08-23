import unittest
from multiprocessing import Process


def long_running_task(code=1, n=100_000_000):
    print(f"Task {code} is being started...")
    while n:
        n -= 1
    print(f"Task {code} finished!")


class TestMultiprocessing(unittest.TestCase):
    def test_multiprocessing(self):
        # create a process for each task
        process_1 = Process(target=long_running_task, args=(1, 100_000_000))
        process_2 = Process(target=long_running_task, args=(5, 50_000_000))

        # run processes
        process_1.start()
        process_2.start()

        # wait for the end of the  processes
        process_1.join()
        process_2.join()


if __name__ == '__main__':
    unittest.main()
