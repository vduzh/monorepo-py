import asyncio
import functools
import time
import unittest
from asyncio import CancelledError, Future, InvalidStateError, Task
from typing import Awaitable, Callable, Any

import requests


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


async def my_coroutine() -> None:
    print("My coroutine!")


async def coroutine_add_one(number: int) -> int:
    return number + 1


@async_timed()
async def delay(delay_seconds: int) -> int:
    print(f'delay: Sleeping for {delay_seconds} sec. ...')
    await asyncio.sleep(delay_seconds)
    print(f'delay: Waking up after {delay_seconds} sec. of sleep.')
    return delay_seconds


class TestAsyncio(unittest.TestCase):
    def test_create_coroutine(self):
        result_coroutine = my_coroutine()
        print(type(result_coroutine))
        # self.assertIsInstance(result_coroutine, coroutine)

    def test_execute_coroutine(self):
        # Execute the coroutine_add_one coroutine
        result_num = asyncio.run(coroutine_add_one(2))
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
        asyncio.run(asyncio.sleep(1))

    def test_simulate_long_term_operation(self):
        async def async_main():
            await delay(2)
            return 'hello world!'

        res = asyncio.run(async_main())
        self.assertEqual('hello world!', res)

    def test_create_task(self):
        async def async_main():
            # schedules the execution of the coroutine object
            sleep_for_three_task = asyncio.create_task(delay(2))

            # ... some code might be here ...
            print(f'The type of the task id: {type(sleep_for_three_task)}')

            # suspends async_main until the task ends and returns the result
            result = await sleep_for_three_task

            return result

        res = asyncio.run(async_main())
        self.assertEqual(2, res)

    def test_create_several_tasks(self):
        async def async_main():
            task_1 = asyncio.create_task(delay(2))
            task_2 = asyncio.create_task(delay(3))
            task_3 = asyncio.create_task(delay(1))

            return await task_1, await task_2, await task_3

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
        async def cpu_bound_work(size=100_000_000) -> int:
            counter = 0
            for i in range(size):
                counter += 1
            return counter

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


if __name__ == '__main__':
    unittest.main()
