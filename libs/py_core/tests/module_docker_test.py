import unittest
from pprint import pprint

import docker
from docker.errors import NotFound

IMAGE_NAME = "docker/getting-started"
CONTAINER_NAME = "getting-started"


def is_container_running(name=CONTAINER_NAME):
    return len(docker.from_env().containers.list(filters={"name": name})) > 0


class TestDocker(unittest.TestCase):
    def test_connect(self):
        client = docker.from_env()

    def test_images(self):
        client = docker.from_env()
        lst = client.images.list()
        for img in lst:
            # print(i., type(i))
            pprint(img.attrs)
            # Image

        # print(lst)

    def test_containers_list(self):
        containers = docker.from_env().containers

        lst = containers.list()
        res = [container.name for container in lst]
        # print(res)

        lst = containers.list(filters={"name": CONTAINER_NAME})
        res = [container.name for container in lst]
        # print(res)

    def test_container_stop(self):
        client = docker.from_env()
        try:
            container = client.containers.get(CONTAINER_NAME)
            container.stop()
        except docker.errors.NotFound as e:
            pass

    def test_container_remove(self):
        client = docker.from_env()
        try:
            container = client.containers.get(CONTAINER_NAME)
            container.stop()
            container.remove()
        except docker.errors.NotFound as e:
            pass

    def test_container_run(self):
        client = docker.from_env()

        try:
            container = client.containers.get(CONTAINER_NAME)
            container.stop()
            container.remove()
        except NotFound:
            pass

        client.containers.run(IMAGE_NAME, detach=True, name=CONTAINER_NAME)

        # client.containers.run("docker/getting-started", "echo hello world")
        # container = client.containers.run(
        #     'alpine',
        #     'echo hello world'
        # )
        # print(type(container))
        # print(container)


if __name__ == '__main__':
    unittest.main()
