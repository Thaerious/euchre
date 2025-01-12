import asyncio
from network.GameServer import GameServer

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

async def handle_connection(reader, writer):
    print("Handling New Connection")
    gameServer = GameServer()
    await gameServer.connect(reader, writer)

async def main():
    server = await asyncio.start_server(handle_connection, HOST, PORT)
    async with server:
            await server.serve_forever()

print("Waiting For Connections...")
asyncio.run(main())
