import asyncio
import functools
import signal
import socket
import time
import unittest
from asyncio import CancelledError, Future, InvalidStateError, Task, AbstractEventLoop
from typing import Awaitable, Callable, Any

import multiprocess as mp  # Note that we are importing "multiprocess", no "ing"!
import requests


# a decorator to log method calls
def log_calls():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f'{func.__name__} started with arguments: {args}, {kwargs}.')
            try:
                return await func(*args, **kwargs)
            finally:
                print(f'{func.__name__} finished.')

        return wrapped

    return wrapper


# a decorator to measure the execution time
def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f'async_timed: Function {func.__name__} has started with arguments: {args}, {kwargs}.')
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f'async_timed: Function {func.__name__} has finished. It took {total:.4f} seconds.')

        return wrapped

    return wrapper


async def coroutine_add_one(number: int) -> int:
    return number + 1


@async_timed()
async def cpu_bound_work(size=100_000_000) -> int:
    counter = 0
    for i in range(size):
        counter += 1
    return counter


@async_timed()
async def delay(delay_seconds: int) -> int:
    print(f'delay: Sleeping for {delay_seconds} sec. ...')
    await asyncio.sleep(delay_seconds)
    print(f'delay: Waking up after {delay_seconds} sec. of sleep.')
    return delay_seconds


class TestAsyncio(unittest.TestCase):
    def test_create_coroutine(self):
        async def my_coroutine() -> int:
            return 2

        coroutine_obj = my_coroutine()
        print(f"Type is: {type(coroutine_obj)}\nResult is: {coroutine_obj}")

    def test_execute_coroutine_on_event_loop(self):
        # create a coroutine object
        coroutine_obj = coroutine_add_one(2)

        # put the coroutine object on an event loop to execute it
        result_num = asyncio.run(coroutine_obj)

        self.assertEqual(3, result_num)

    def test_await(self):
        async def async_main():
            # stop async_main and wait for the end of the coroutine_add_one
            one_plus_one = await coroutine_add_one(1)
            # stop async_main and wait for the end of the coroutine_add_one
            two_plus_one = await coroutine_add_one(2)

            return one_plus_one, two_plus_one

        # Execute the async_main coroutine
        result = asyncio.run(async_main())
        self.assertEqual((2, 3), result)

    def test_awaitable(self):
        async def async_main():
            coroutine = coroutine_add_one(1)
            task = asyncio.create_task(coroutine_add_one(2))
            future = Future()

            self.assertIsInstance(coroutine, Awaitable)
            self.assertIsInstance(task, Awaitable)
            self.assertIsInstance(future, Awaitable)

        asyncio.run(async_main())

    def test_sleep(self):
        async def hello_world_message() -> str:
            await asyncio.sleep(1)
            return "Hello World!"

        async def async_main():
            message = await hello_world_message()
            print(message)

        asyncio.run(async_main())

    def test_simulate_long_term_operation(self):

        async def async_main():
            await delay(2)
            return 'hello world!'

        res = asyncio.run(async_main())
        self.assertEqual('hello world!', res)

    def test_create_task(self):
        async def async_main():
            # schedules the execution of the coroutine object
            task = asyncio.create_task(delay(2))
            print(f'The type of the task id: {type(task)}')

            # ...
            # some code might be here
            # ...

            # suspends async_main until the task ends and returns the result
            result = await task
            return result

        res = asyncio.run(async_main())
        self.assertEqual(2, res)

    def test_create_several_tasks(self):
        async def async_main():
            task_1 = asyncio.create_task(delay(2))
            task_2 = asyncio.create_task(delay(3))
            task_3 = asyncio.create_task(delay(1))

            res_1 = await task_1
            res_2 = await task_2
            res_3 = await task_3

            return res_1, res_2, res_3

        res = asyncio.run(async_main())
        self.assertEqual((2, 3, 1), res)

    def test_gather(self):
        async def async_main():
            delay_list = [delay(i) for i in [2, 3, 1]]
            return await asyncio.gather(*delay_list)

        res = asyncio.run(async_main())
        self.assertEqual((2, 3, 1), res)

    def test_execute_code_while_other_operations_work(self):
        async def some_code():
            for i in range(5):
                await asyncio.sleep(1)
                print("While i'm waiting, the other code is working...!")

        async def async_main():
            task_1 = asyncio.create_task(delay(2))
            task_2 = asyncio.create_task(delay(3))

            await some_code()
            await task_1
            await task_2

        asyncio.run(async_main())

    def test_cancel_task_from_other_code(self):
        async def async_main():
            # execute a long running task
            long_task = asyncio.create_task(delay(10))

            # wait for 5 sec for the task to finish
            seconds_elapsed = 0
            while not long_task.done():
                print(f"The task is still running. Nex check in 1 sec.")
                await asyncio.sleep(1)
                seconds_elapsed += 1
                if seconds_elapsed == 5:
                    long_task.cancel()

            try:
                await long_task
            except CancelledError:
                print(f"The task has been cancelled.")

        asyncio.run(async_main())

    def test_cancel_task_with_wait_for(self):
        async def async_main():
            delay_task = asyncio.create_task(delay(5))

            try:
                result = await asyncio.wait_for(delay_task, timeout=2)
                print(result)
            except asyncio.TimeoutError:
                print("Timeout occurred.")
                print(f"Has the task been cancelled? {delay_task.cancelled()}!")

        asyncio.run(async_main())

    def test_shield_task(self):
        async def async_main():
            task = asyncio.create_task(delay(5))

            try:
                result = await asyncio.wait_for(asyncio.shield(task), timeout=2)
                print(result)
            except asyncio.TimeoutError:
                print("The task has been running more than 2 sec. It will finish soon.")

        asyncio.run(async_main())

    def test_create_future(self):
        # create an object
        future = Future()

        # check if the status is false
        self.assertFalse(future.done())
        # check for an exception if the result is not set
        with self.assertRaises(InvalidStateError):
            future.result()

        # set the result
        future.set_result(123)
        # check for a true status
        self.assertTrue(future.done())
        # check if the result is 123
        self.assertEqual(123, future.result())

        future = Future()
        future.set_exception(BaseException("Some exception occurred"))
        # check for an exception if the result is not set
        with self.assertRaises(BaseException):
            future.result()

    def test_await_future(self):
        @log_calls()
        async def set_future_value(future):
            await asyncio.sleep(2)
            future.set_result(100)

        def make_request() -> Future:
            future = Future()
            asyncio.create_task(set_future_value(future))
            return future

        @log_calls()
        @async_timed()
        async def async_main():
            # create request
            future = make_request()
            # wait for the result
            value = await future
            # assert the result
            self.assertEqual(100, value)

        asyncio.run(async_main())

    def test_future_is_superclass_of_task(self):
        self.assertIsInstance(Future(), Task)

    def test_timing(self):
        @async_timed()
        async def async_main():
            task = asyncio.create_task(delay(3))
            await task

        asyncio.run(async_main())

    def test_improper_use_wih_cpu_bound(self):

        @async_timed()
        async def async_main():
            task_1 = asyncio.create_task(cpu_bound_work(100_000_000))
            task_2 = asyncio.create_task(cpu_bound_work(90_000_000))
            task_3 = asyncio.create_task(delay(4))

            await task_1
            await task_2
            await task_3

        asyncio.run(async_main())

    def test_improper_use_of_sync_api(self):
        @async_timed()
        async def call_sync_api(code) -> int:
            # here is a synchronous api call as the get method blocks code execution
            return requests.get("http://example.com").status_code

        @async_timed()
        async def async_main():
            task_1 = asyncio.create_task(call_sync_api(1))
            task_2 = asyncio.create_task(call_sync_api(2))
            task_3 = asyncio.create_task(call_sync_api(3))

            await task_1
            await task_2
            await task_3

        asyncio.run(async_main())

    def test_create_event_loop_manually(self):
        @async_timed()
        async def async_main():
            await asyncio.sleep(1)

        # manually create an event loop
        loop = asyncio.new_event_loop()

        try:
            # gets a coroutine and executes and wait it until completion
            loop.run_until_complete(async_main())
        finally:
            loop.close()

    def test_access_event_loop(self):
        def call_later():
            print("call_later: I got called!")

        @async_timed()
        async def async_main():
            # get an event loop
            loop = asyncio.get_running_loop()

            # do some stuff with the look
            loop.call_soon(call_later)

            # call a coroutine
            await delay(2)

        asyncio.run(async_main())

    def test_debug_mode(self):
        asyncio.run(cpu_bound_work(), debug=True)

    def test_debug_callback_duration(self):
        async def async_main():
            loop = asyncio.get_event_loop()
            loop.slow_callback_duration = .250

        asyncio.run(async_main(), debug=True)

    def test_handle_signals(self):

        def handle_signal():
            print(f'Received the signal.')

        async def async_main():
            loop: AbstractEventLoop = asyncio.get_running_loop()
            loop.add_signal_handler(signal.SIGINT, handle_signal)

            await delay(10)

        asyncio.run(async_main())

    def test_async_server(self):
        def run_server():

            async def process_request(client_socket: socket, loop: AbstractEventLoop):
                print("Server:", "Processing data from the client socket...")

                # wait for data from the infinite loop
                while data := await loop.sock_recv(client_socket, 1024):
                    print("Server:", f'I got data: {data}!')

                    # send data back to the client
                    print("Server:", "Writing data back to a client...")
                    await loop.sock_sendall(client_socket, data)
                    print("Server:", "The data has been sent!")

            async def async_main():
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_socket.setblocking(False)
                server_socket.bind(('127.0.0.1', 8000))
                server_socket.listen()

                event_loop: AbstractEventLoop = asyncio.get_event_loop()

                while True:
                    # wait for the user connection
                    client_socket, client_address = await event_loop.sock_accept(server_socket)
                    client_socket.setblocking(False)
                    print("Server:", f'I got a connection from {client_address}!')

                    # handle the clients request
                    await asyncio.create_task(process_request(client_socket, event_loop))

            asyncio.run(async_main())

        def run_client():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                print("Client:", "Creating connection...")
                # connect to a remote socket at the address
                client_socket.connect(("127.0.0.1", 8000))
                # write data to the server
                print("Client:", "Writing data to the server...")
                client_socket.sendall(b"Hello, world\r\n")
                # receive up to 1024 bytes from the server
                print("Client:", "Receiving the response...")
                data = client_socket.recv(1024)
                print("Client:", f"Received {data!r}")

        # create a process for each task
        process_1 = mp.Process(target=run_server)
        process_2 = mp.Process(target=run_client)

        # run processes
        process_1.start()
        process_2.start()

        # wait for the end of the  processes
        process_1.join()
        process_2.join()


if __name__ == '__main__':
    unittest.main()
