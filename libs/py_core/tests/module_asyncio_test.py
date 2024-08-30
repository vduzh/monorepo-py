import asyncio
import unittest
from asyncio import CancelledError


async def my_coroutine() -> None:
    print("My coroutine!")


async def coroutine_add_one(number: int) -> int:
    return number + 1


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


if __name__ == '__main__':
    unittest.main()
