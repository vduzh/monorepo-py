import unittest
from time import sleep

import docker
import paramiko
from docker import DockerClient
from docker.errors import NotFound
from paramiko.client import SSHClient

"""
1 Info: 
1.1 docker run -d -p 2222:2222 --name=openssh-server -e PUID=1000 -e PGID=1000 -e PASSWORD_ACCESS=true -e USER_PASSWORD=test -e USER_NAME=test lscr.io/linuxserver/openssh-server
1.2 docker ps
1.3 ssh -p 2222 user@localhost  
"""

# set variables
IMAGE_NAME = "lscr.io/linuxserver/openssh-server"
CONTAINER_NAME = "openssh-server"

HOST_NAME = "localhost"
PORT = 2222
USER_NAME = "test"
PASSWORD = "test"

ENVIRONMENT = {"PUID": 1000, "PGID": 1000, "PASSWORD_ACCESS": True, "USER_PASSWORD": PASSWORD, "USER_NAME": USER_NAME}


# ENVIRONMENT = ["PUID=1000", "PGID=1000", "PASSWORD_ACCESS=true", f"USER_PASSWORD=test", "USER_NAME=test"]

class TestParamiko(unittest.TestCase):
    docker_client: DockerClient = None
    ssh_client: SSHClient = None

    @staticmethod
    def wait_for_container(container):
        print("waiting for the container...")
        timeout = 120
        stop_time = 3
        elapsed_time = 0
        while container.status != 'running' and elapsed_time < timeout:
            print("the container status:", container.status)
            sleep(stop_time)
            container.reload()
            elapsed_time += stop_time
            continue
        print("the container is ready")

    @classmethod
    def setUpClass(cls):
        # create a docker client
        cls.docker_client = docker.from_env()

        # init container
        container = None
        try:
            # getting a container if any
            container = cls.docker_client.containers.get(CONTAINER_NAME)
            print("getting the existing container...")

            if container.status != 'running':
                print("starting the existing container...")
                container.start()
                cls.wait_for_container(container)
        except NotFound as e:
            print("running a new container...")
            container = cls.docker_client.containers.run(
                IMAGE_NAME,
                detach=True,
                ports={f"{PORT}/tcp": PORT},
                name=CONTAINER_NAME,
                environment=ENVIRONMENT
            )

            cls.wait_for_container(container)

        # connect to the SSH server in the container
        cls.ssh_client = SSHClient()
        cls.ssh_client.load_system_host_keys(filename="./data/known_hosts")
        cls.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        cls.ssh_client.connect(hostname=HOST_NAME, port=PORT, username=USER_NAME, password=PASSWORD)

    @classmethod
    def tearDownClass(cls):
        # close the connection to the container
        cls.ssh_client.close()

        # stop the container
        try:
            container = cls.docker_client.containers.get(CONTAINER_NAME)
            container.stop()
            # container.remove()
        except NotFound as e:
            pass

    def test_(self):
        pass

    def test_connect(self):
        with paramiko.SSHClient() as ssh_client:
            # authorize the host
            # ssh_client.load_system_host_keys()
            ssh_client.load_system_host_keys(filename="./data/known_hosts")
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

            ssh_client.connect(
                hostname=HOST_NAME,
                port=PORT,
                username=USER_NAME,
                password=PASSWORD
            )

            std_in, std_out, std_err = ssh_client.exec_command("ls -ls /")
            print(std_out.read().decode("utf-8"))

    def test_invoke_shell(self):
        raise NotImplementedError()

    def test_exec_command(self):
        # std_in, std_out, std_err = self.ssh_client.exec_command("ls -ls /")
        std_in, std_out, std_err = self.ssh_client.exec_command("echo 'Hello, world!'")

        # output = std_out.read().decode("utf-8")
        output = std_out.read().decode().strip()
        error = std_err.read().decode().strip()
        # print(output)

        self.assertEqual(output, "Hello, world!")
        self.assertEqual(error, "")


if __name__ == '__main__':
    unittest.main()
