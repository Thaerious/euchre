from euchre import *
from euchre.Euchre import EuchreException
from euchre.bots.Bot import Bot
import pickle
import random

class GameServer:
    def __init__(this, conn, addr):
        # seed = random.randint(1, 10000)
        seed = 5589
        print(f"seed {seed}")
        random.seed(seed)
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

        print(f"data sent hash : {this.game.hash}")

        data = this.conn.recv(1024)  # Receive ack from client
        if not data:                 # Client has closed the connection
            print("connection terminated")
            this.running = False
            return

        packet = pickle.loads(data)   

        if packet[0] != "ack":
            print(f"expected 'ack', received '{packet[0]}'")
            this.running = False
            return             
        else:
            print(packet)          

    def loop(this):
        try:
            this.running = True
            with this.conn:  # Automatically close the connection when done
                while this.running:
                    this.step()
        except ConnectionResetError:
            this.running = False
            print(f"Connection with {this.addr} was reset by the client.")
            return false

        print(f"Connection with {this.addr} has been closed.") 

    def step(this):
        try:
            print("---------------------------------------")  
            print(f" current player {this.euchre.getCurrentPlayer().name}")
            if this.euchre.getCurrentPlayer().name == "Adam":
                this.getNextPacket()
            else:
                snap = Snapshot(this.game, this.euchre.getCurrentPlayer())
                (action, data) = this.bot.decide(snap)
                print(f"bot {this.euchre.getCurrentPlayer().name}: {action} {data}")
                this.game.input(this.euchre.getCurrentPlayer(), action, data)
        except EuchreException as e:
            print(e)
        finally:
            this.sendSnaps()

    def getNextPacket(this):
        print("waiting for next packet")

        data = this.conn.recv(1024)  # Receive data from the client
        if not data:                 # Client has closed the connection
            print("connection terminated")
            this.running = False
            return

        print(f"Data received: {len(data)}") 
        packet = pickle.loads(data)
        print(packet) 
        this.hndPacket(packet)

    def hndPacket(this, packet):
        action = packet[0]
        data = packet[1]

        this.game.input(this.euchre.players.getPlayer("Adam"), action, data)
        this.sendSnaps()
        print(f"state : {this.game.getState()}")
