import selectors
import socket
import unittest

import multiprocess as mp  # Note that we are importing "multiprocess", no "ing"!


class TestSocket(unittest.TestCase):
    def test_create_server_socket(self):
        with socket.socket(
                # type of address our socket will be able to interact with
                socket.AF_INET,  # hostname and a port number
                # TCP protocol for our communication
                socket.SOCK_STREAM
        ) as server_socket:
            # reuse the port number after we stop and restart the application
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def test_bind_socket_to_address(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # set our socket up at the address 127.0.0.1:8000
            address = ("127.0.0.1", 8000)
            server_socket.bind(address)

    def test_listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(("127.0.0.1", 8000))

            # listen for connections from clients
            server_socket.listen()

    def test_accept(self):

        def server_task():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_socket.bind(("127.0.0.1", 8000))
                server_socket.listen()

                # wait for a connection with a blocking method accept
                client_socket, client_address = server_socket.accept()
                print(f'I got a connection from {client_address}!')

                buffer = b''
                while buffer[-2:] != b'\r\n':
                    data = client_socket.recv(2)
                    if not data:
                        break
                    else:
                        print(f'I got data: {data}!')
                    buffer = buffer + data
                print(f"All the data is: {buffer}")

                # write data back to a client
                client_socket.sendall(buffer)

        def client_task():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                # connect to a remote socket at the address
                client_socket.connect(("127.0.0.1", 8000))
                # write data to the server
                client_socket.sendall(b"Hello, world\r\n")
                # receive up to 1024 bytes from the server
                data = client_socket.recv(1024)
                print(f"Received {data!r}")

        # create a process for each task
        process_1 = mp.Process(target=server_task)
        process_2 = mp.Process(target=client_task)

        # run processes
        process_1.start()
        process_2.start()

        # wait for the end of the  processes
        process_1.join()
        process_2.join()

    def test_async_with_selectors(self):

        def server_task():
            # create a selector specific fot the OS
            selector = selectors.DefaultSelector()

            # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            with socket.socket() as server_socket:
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_socket.bind(("127.0.0.1", 8000))
                server_socket.listen()

                # register the server socket for read events
                selector.register(server_socket, selectors.EVENT_READ)
                print("Server:", "Registered the server socket.")

                while True:
                    # select events
                    events: list[tuple[selectors.SelectorKey, int]] = selector.select(timeout=1)

                    if len(events) == 0:
                        print("Server:", "No events yet, I'll wait a bit longer!")

                    for event, _ in events:
                        # get the socket for which the event occurred
                        event_socket: socket = event.fileobj

                        if event_socket == server_socket:
                            # If the event occurred with the server socket, it indicates a connection attempt
                            client_socket, client_address = server_socket.accept()
                            client_socket.setblocking(False)
                            print("Server:", f'I got a connection from {client_address}!')

                            # register the connected client socket for read events
                            selector.register(client_socket, selectors.EVENT_READ)
                            print("Server:", "Registered the client socket.")
                        else:
                            print("Server:", "Processing data from the client socket...")
                            # get data from the client and store in the buffer
                            buffer = b''
                            while buffer[-2:] != b'\r\n':
                                data = event_socket.recv(2)
                                if not data:
                                    break
                                else:
                                    print("Server:", f'I got data: {data}!')
                                buffer = buffer + data

                            print("Server:", f"Received from the the client socket: {buffer}")

                            if buffer:
                                print("Server:", "Writing data back to a client...")
                                # write data back to a client
                                event_socket.send(buffer)
                            else:
                                print("Server:", f"All data processed. Closing socket.")
                                selector.unregister(event_socket)
                                event_socket.close()

        def client_task():
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
        process_1 = mp.Process(target=server_task)
        process_2 = mp.Process(target=client_task)

        # run processes
        process_1.start()
        process_2.start()

        # wait for the end of the  processes
        process_1.join()
        process_2.join()


if __name__ == '__main__':
    unittest.main()
