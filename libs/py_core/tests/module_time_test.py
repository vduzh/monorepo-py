import time
import unittest


class TestTime(unittest.TestCase):
    def test_time(self):
        t = time.time()
        print(t)

    def test_sleep(self):
        print("Start. Going to sleep")
        time.sleep(1)
        print("Woken up!")

    def test_execution_time(self):
        start = time.perf_counter()
        time.sleep(1)
        finish = time.perf_counter()
        print(finish - start)

    if __name__ == '__main__':
        unittest.main()
