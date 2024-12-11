from euchre import *
import pickle

class GameServer:
    def __init__(this, conn, addr):
        this.conn = conn
        this.addr = addr

    def onConnect(this):
        # todo: read first packet and do validation
        
        this.euchre = Euchre(["Adam", "T100", "Skynet", "Robocop"])
        this.game = Game(this.euchre)
        this.game.input(None, "start")

        snap = Snapshot(this.game, this.euchre.players.getPlayer("Adam"))
        this.conn.sendall(pickle.dumps(snap))
        print(this.euchre)
        print(f"state : {this.game.currentState()}")
        print("---------------------------------------")

        this.listen()      

    def listen(this):
        with this.conn:  # Automatically close the connection when done
            while True:
                try:
                    data = this.conn.recv(1024)  # Receive data from the client
                    if not data:  # Client has closed the connection
                        print(f"Client {this.addr} disconnected")
                        break

                    packet = pickle.loads(packet)
                    this.hndPacket(packet)

                except ConnectionResetError:
                    print(f"Connection with {this.addr} was reset by the client.")
                    break

        print(f"Connection with {this.addr} has been closed.")        

    def hndPacket(this, packet):
        print(packet)
        
