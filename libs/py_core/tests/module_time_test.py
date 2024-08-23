import unittest
from time import perf_counter, sleep, time


class TestTime(unittest.TestCase):
    def test_time(self):
        t = time()
        print("Now: ", t)

    def test_sleep(self):
        print("Start. Going to sleep")
        sleep(1)
        print("Woken up!")

    def test_perf_counter(self):
        start = perf_counter()

        print("Task is being started...")
        sleep(1)
        print("Task finished!")

        finish = perf_counter()

        print(f"Execution time: {finish - start} sec.")


if __name__ == '__main__':
    unittest.main()
