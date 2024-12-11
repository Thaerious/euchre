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
        this.sendSnaps()
        this.listen()      

    def sendSnaps(this):
        snap = Snapshot(this.game, this.euchre.players.getPlayer("Adam"))
        this.conn.sendall(pickle.dumps(snap))   
        print(this.euchre)
        print(f"state : {this.game.currentState()}")
        print("---------------------------------------")             

    def loop(this):
        this.running = True
        while this.running:
            if this.euchre.getCurrentPlayer().name == "Adam":
                this.listen()
            else:
                snap = Snapshot(this.game, this.euchre.getCurrentPlayer())
                (action, data) = this.bot.decide(snap)
                this.game.input(this.euchre.getCurrentPlayer(), action, data)
                this.sendSnaps()


    def listen(this):
        with this.conn:  # Automatically close the connection when done
            while True:
                print(f"Waiting for data...")  
                try:
                    data = this.conn.recv(1024)  # Receive data from the client
                    if not data:  # Client has closed the connection
                        this.running = False
                        print(f"Client {this.addr} disconnected")
                        break

                    print(f"Data received: {len(data)}") 
                    packet = pickle.loads(packet)
                    this.hndPacket(packet)

                except ConnectionResetError:
                    this.running = False
                    print(f"Connection with {this.addr} was reset by the client.")
                    break

        print(f"Connection with {this.addr} has been closed.")        

    def hndPacket(this, packet):
        print(packet)
        
