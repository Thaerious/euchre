from euchre import *
from euchre.bots.Bot import Bot
import pickle

class GameServer:
    def __init__(this, conn, addr):
        this.conn = conn
        this.addr = addr
        this.bot = Bot()

    def onConnect(this):
        # todo: read first packet and do validation
        
        this.euchre = Euchre(["Adam", "T100", "Skynet", "Robocop"])
        this.game = Game(this.euchre)
        this.game.input(None, "start", None)        
        this.sendSnaps()
        this.loop()    

    def sendSnaps(this):
        snap = Snapshot(this.game, this.euchre.players.getPlayer("Adam"))
        this.conn.sendall(pickle.dumps(snap))   

        print("---------------------------------------") 
        print(this.euchre)
        print(f"state : {this.game.currentState()}")
        print("---------------------------------------")             

    def loop(this):
        try:
            this.running = True
            with this.conn:  # Automatically close the connection when done
                while this.running:
                    if this.euchre.getCurrentPlayer().name == "Adam":
                        this.getNextPacket()
                    else:
                        snap = Snapshot(this.game, this.euchre.getCurrentPlayer())
                        (action, data) = this.bot.decide(snap)
                        this.game.input(this.euchre.getCurrentPlayer(), action, data)
                        
                    this.sendSnaps()
        except ConnectionResetError:
            this.running = False
            print(f"Connection with {this.addr} was reset by the client.")
            return false

        print(f"Connection with {this.addr} has been closed.") 

    def getNextPacket(this):
        print(f"Get next packet") 
        data = this.conn.recv(1024)  # Receive data from the client
        if not data:  # Client has closed the connection
            this.running = False

        print(f"Data received: {len(data)}") 
        packet = pickle.loads(data)
        this.hndPacket(packet)   

    def hndPacket(this, packet):
        print(packet)
        action = packet[0]
        data = packet[1]
        this.game.input(this.euchre.players.getPlayer("Adam"), action, data)
        
