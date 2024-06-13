import unittest

import requests
from requests import ConnectTimeout

BASE_URL = "https://jsonplaceholder.typicode.com"


class TestRequestsModule(unittest.TestCase):

    def test_get(self):
        res = requests.get(f"{BASE_URL}/todos/1")
        self.assertEqual(200, res.status_code)
        print(res.json())
        print(res.text)

    def test_response(self):
        res = requests.get(f"{BASE_URL}/todos/1")

        self.assertEqual(200, res.status_code)
        self.assertEqual({"userId": 1, "id": 1, "title": "delectus aut autem", "completed": False}, res.json())
        print(res.text)

    def test_timeout(self):
        with self.assertRaises(ConnectTimeout):
            requests.get(f"{BASE_URL}/todos", timeout=0.0001)

    def test_get_params(self):
        res = requests.get(f"{BASE_URL}/todos", params={"userId": 1})
        self.assertEqual(200, res.status_code)
        print(res.text)

    def test_headers(self):
        headers = {
            "Authorization": "Bearer: test_token"
        }
        res = requests.get(f"{BASE_URL}/todos/1", headers=headers)
        self.assertEqual(200, res.status_code)
        print(res.text)

    def test_post(self):
        payload = {
            "userId": 1,
            "title": "Test Title",
            "completed": False
        }

        res = requests.post(f"{BASE_URL}/todos", data=payload)
        self.assertEqual(201, res.status_code)
        print(res.text)

    def test_post_file(self):
        # TODO: use anther endpoint
        res = None

        with open("data/todo_new.json") as f:
            files = {
                "text_file": f
            }

            res = requests.post(f"{BASE_URL}/todos", files=files)

        # self.assertEqual(201, res.status_code)
        print(res.text)

    def test_session(self):
        session = requests.Session()

        res = session.get(f"{BASE_URL}/todos/1")
        print(res.text)
        res = session.get(f"{BASE_URL}/todos/2")
        print(res.text)


if __name__ == '__main__':
    unittest.main()
