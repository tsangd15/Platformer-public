"""Server Functions Module
This module will contain all server related functions, used to connect and
transfer data between the game server."""
import socket
import json


def send(sock, data):
    """Send data using the given socket.
    A fixed size header containing the size of the data (payload) will be sent
    first so the receiver knows how big the data is.
    The actual data (payload) will be sent afterwards.
    The function returns True if it carried out successfully, otherwise False
    is returned."""
    payload = data.encode(ENCODING)  # encode into byte representation
    payload_size = len(payload)  # get length of payload

    # create header
    header = str(payload_size).encode(ENCODING)
    # pad header so its length is the fixed header size (32)
    header += b" " * (HEADER_SIZE - len(header))

    # attempt to send data to recipient
    try:
        # send header containing payload size then payload
        sock.send(header)
        sock.send(payload)
        return True
    # catch connection reset, aborted & refused errors
    except ConnectionError as e:
        print(f"{e}")  # print exception message to console
    return False


def receive(sock):
    """Receive data using the given socket.
    A fixed size header will be received first in order to know the size to
    receive the actual payload (which varies in size).
    The payload is returned."""
    # receive and decode header (containing payload size)
    try:
        header = sock.recv(HEADER_SIZE).decode(ENCODING)
    # catch connection reset, aborted & refused errors
    except ConnectionError as e:
        print(f"{e}")  # print exception message to console
        return None

    if header != "":
        payload_size = int(header)

        # receive and decode payload
        payload = sock.recv(payload_size).decode(ENCODING)
    else:
        print("Receive timed out.")
        payload = None

    return payload


def connect():
    """Start a connection with the server and return the socket object."""
    # create server socket object
    # af_inet means ipv4, sock_stream means tcp
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(SERVER_ADDR)
    # catch connection reset, aborted & refused errors
    except ConnectionError as e:
        print(f"{e}")  # print exception message to console
        return None
    return client_socket


def server_addentry(tag, score):
    """Send the add entry command to the server."""
    client_socket = connect()  # returns none if connectionerror occurs

    if client_socket is None:
        return None  # stop function execution if error in getting socket

    # send function returns bool whether or not it sent successfully or not
    sent = send(client_socket, f"ADD_ENTRY ({tag}, {score})")

    if sent:
        return receive(client_socket)
    return None  # return None if cmd didn't send


def server_getentries():
    """Send the get entries command to the server."""
    client_socket = connect()  # returns none if connectionerror occurs

    if client_socket is None:
        return None  # stop function execution if error in getting socket

    # send returns bool whether or not it sent successfully or not
    sent = send(client_socket, "GET_ENTRIES (10)")

    if sent:
        return json.loads(receive(client_socket))
    return None  # return None if cmd didn't send


HEADER_SIZE = 32
# specify ip to connect to
IP = "127.0.0.1"
# specify port to bind to
PORT = 63632
SERVER_ADDR = (IP, PORT)
ENCODING = "utf-8"
