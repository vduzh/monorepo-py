import unittest
from queue import Empty, Queue
from threading import Thread
from time import sleep

def task(code=0):
    print(f"Function: Task {code} is being started...")
    sleep(1)
    print(f"Function: Task {code} finished!")


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


if __name__ == '__main__':
    unittest.main()
