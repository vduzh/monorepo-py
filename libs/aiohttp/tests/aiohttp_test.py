import asyncio
import unittest

import aiohttp

from libs.py_core.tests.module_asyncio_test import async_timed, log_calls


class TestAioHttp(unittest.TestCase):
    URL = 'https://www.example.com/'

    def test_template(self):
        async def async_main():
            pass

        asyncio.run(async_main())

    def test_create_session(self):
        async def async_main():
            async with aiohttp.ClientSession() as session:
                pass

        asyncio.run(async_main())

    def test_session_get(self):
        async def async_main():
            async with aiohttp.ClientSession() as session:
                async with session.get(self.URL) as response:
                    status = response.status
                    self.assertEqual(200, status)

        asyncio.run(async_main())

    def test_timeout(self):
        async def async_main():
            session_timeout = aiohttp.ClientTimeout(total=1, connect=.91)
            async with aiohttp.ClientSession(timeout=session_timeout) as session:
                # use the timeout from the session
                async with session.get(self.URL) as response:
                    pass

                # specify the timeout from the connection
                connection_timeout = aiohttp.ClientTimeout(total=5.01)
                async with session.get("https://www.google.com", timeout=connection_timeout) as response:
                    pass

                # simulate connection timeout
                connection_timeout = aiohttp.ClientTimeout(total=.01)
                try:
                    async with session.get("https://www.artezion.com", timeout=connection_timeout) as response:
                        pass
                except TimeoutError:
                    print("Timeout")

        asyncio.run(async_main())

    def test_spread_gather(self):
        count = 10
        target_urls = [self.URL for _ in range(count)]

        @log_calls()
        async def make_request(session, url):
            async with session.get(url) as response:
                return response.status

        @async_timed()
        async def async_main():
            async with aiohttp.ClientSession() as session:
                requests = [make_request(session, url) for url in target_urls]
                return await asyncio.gather(*requests)

        result = asyncio.run(async_main())
        self.assertEqual([200 for _ in range(count)], result)


if __name__ == '__main__':
    unittest.main()
