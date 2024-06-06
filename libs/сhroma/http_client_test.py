import unittest
from time import sleep

import chromadb
import docker
import requests
from docker import DockerClient
from docker.errors import NotFound


def wait_for_container(container, timeout=120, stop_time=3):
    print("wait_for_container:", "waiting for the container...")

    elapsed_time = 0
    while container.status != 'running' and elapsed_time < timeout:
        print("wait_for_container:", "the container status:", container.status)
        sleep(stop_time)
        container.reload()
        elapsed_time += stop_time
        continue
    print("wait_for_container:", "the container is ready")


def wait_for_chroma_server(url, timeout=120, stop_time=3):
    print("wait_for_chroma_server:", "waiting for the chroma db server...")

    elapsed_time = 0

    while elapsed_time < timeout:
        print("wait_for_chroma_server:", "still waiting...")

        sleep(stop_time)

        try:
            response = requests.head(url)

            if response.status_code == 200:
                print("wait_for_chroma_server:", "the chroma server is ready!")
                return

            print("wait_for_chroma_server:", f"the chroma server returned status code: {response.status_code}")
        except requests.exceptions.ConnectionError:
            pass

        elapsed_time += stop_time

    print("could not connect to the chroma server.")


class TestHttpClient(unittest.TestCase):
    IMAGE_NAME = "chromadb/chroma"

    CONTAINER_NAME = "chromadb"

    HOST_NAME = "localhost"
    PORT = 8000

    ENVIRONMENT = {
        "IS_PERSISTENT": True,
        "ANONYMIZED_TELEMETRY": True,
    }

    docker_client: DockerClient = None
    # ssh_client: SSHClient = None

    test_collection = "test_collection"

    @classmethod
    def setUpClass(cls):
        # create a docker client
        cls.docker_client = docker.from_env()

        # init container
        container = None
        try:
            # getting a container if any
            container = cls.docker_client.containers.get(cls.CONTAINER_NAME)
            print("getting the existing container...")

            if container.status != 'running':
                print("starting the existing container...")
                container.start()
                wait_for_container(container)

            print("the existing container started.")
        except NotFound as e:
            print("running a new container...")
            container = cls.docker_client.containers.run(
                cls.IMAGE_NAME,
                detach=True,
                # added --rm
                auto_remove=True,
                ports={f"{cls.PORT}/tcp": cls.PORT},
                name=cls.CONTAINER_NAME,
                volumes=["./chroma:/chroma/chroma"],
                environment=cls.ENVIRONMENT
            )

            wait_for_container(container)
            print("the new container started.")

            # Wait for Chroma
            wait_for_chroma_server(f"http://{cls.HOST_NAME}:{cls.PORT}/docs")
            print("the chroma db server started.")

        # creating a http client
        print("creating a chroma db HttpClient...")
        cls._http_client = chromadb.HttpClient(host=cls.HOST_NAME, port=cls.PORT)
        print("created the chroma db HttpClient")

    @classmethod
    def tearDownClass(cls):
        # close the connection to the container
        # cls.ssh_client.close()

        # stop the container
        try:
            container = cls.docker_client.containers.get(cls.CONTAINER_NAME)
            container.stop()
            # container.remove()
        except NotFound as e:
            pass

    def test_create_collection(self):
        collection = self._http_client.get_or_create_collection(name=self.test_collection)

        self.assertEqual(self.test_collection, collection.name)


if __name__ == '__main__':
    unittest.main()
