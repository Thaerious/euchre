import socket
import threading
from .GameServer import GameServer

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

class ConnectionServer:
    def start(this):
        this.running = True

        this.server = await asyncio.start_server(handle_connection, HOST, PORT)

        this.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        this.socket.bind((HOST, PORT))
        this.socket.listen()
        this.socket.settimeout(1.0)  # Set a 1-second timeout on accept()
        print(f"Server is listening on {HOST}:{PORT}")

        # Listen for incoming connections
        while this.running:
            try:
                conn, addr = this.socket.accept()
                print(f"Accepted connection from {addr}")
                gameServer = GameServer(conn, addr)
                client_thread = threading.Thread(target=gameServer.onConnect)
                client_thread.daemon = True  # Ensure threads close when the main program exits
                client_thread.start()
            except socket.timeout:
                # Timeout occurred, check if we should still run
                continue        

        if this.socket:
            this.socket.close()
            print("Socket closed. Goodbye!")