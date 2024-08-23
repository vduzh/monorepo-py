import unittest
from queue import Empty, Queue
from threading import Thread, Lock
from time import sleep


def task(code=0):
    print(f"Function: Task {code} is being started...")
    sleep(1)
    print(f"Function: Task {code} finished!")


counter = 0


class TestThreading(unittest.TestCase):
    def test_thread_with_target(self):
        thread = Thread(target=task, args=(1,))
        thread.start()
        thread.join()

    def test_thread_run(self):
        class CustomThread(Thread):
            def __init__(self, code):
                super().__init__()
                self.code = code

            def run(self):
                print(f"CustomThread: Task {self.code} is being started...")
                sleep(1)
                print(f"CustomThread: Task {self.code} finished!")

        thread = CustomThread(100)
        thread.start()
        thread.join()

    def test_daemon(self):
        daemon = Thread(target=task, args=(1,), daemon=True)

    def test_communicate_threads(self):
        def producer(queue: Queue):
            for i in range(6):
                print(f'Adding element {i} the queue...')
                sleep(1)
                queue.put(i)

        def consumer(queue: Queue):
            while True:
                try:
                    item = queue.get()
                except Empty:
                    continue
                else:
                    print(f'Processing element {item} from the queue...')
                    sleep(2)
                    queue.task_done()

        task_queue = Queue()

        producer_thread = Thread(target=producer, args=(task_queue,))
        consumer_thread = Thread(target=consumer, args=(task_queue,))

        producer_thread.start()
        consumer_thread.start()

        # waiting for the tasks being added to the queue
        producer_thread.join()

        # дожидаемся, пока все задачи в очереди будут завершены
        task_queue.join()

    def test_lock(self):
        lock = Lock()
        lock.acquire()
        # ...
        lock.release()

    def test_lock_race_condition_with_lock(self):
        def increase(lock, value):
            lock.acquire()
            global counter
            counter += value
            lock.release()

        test_lock = Lock()

        t1 = Thread(target=increase, args=(test_lock, 1))
        t2 = Thread(target=increase, args=(test_lock, -2))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        print(f"Counter: {counter}")

    def test_lock_race_condition_with_lock_in_class(self):
        class Counter:

            def __init__(self, initial_value: int):
                self.value = initial_value
                self.__lock = Lock()

            def increase(self, value: int):
                self.__lock.acquire()
                self.value += value
                self.__lock.release()

        counter_obj = Counter(0)

        t1 = Thread(target=counter_obj.increase, args=(5,))
        t2 = Thread(target=counter_obj.increase, args=(-10,))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        print(f"Counter in class: {counter_obj.value}")


if __name__ == '__main__':
    unittest.main()
