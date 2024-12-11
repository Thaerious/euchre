from euchre import *
import socket
import pickle

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def connect():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)
        snap = pickle.loads(data)
        print(pickle)

if __name__ == "__main__":
    connect()