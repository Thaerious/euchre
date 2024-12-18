from euchre import *
from euchre.Euchre import EuchreException
from euchre.bots.Bot import Bot
import pickle
import random
import asyncio

class GameServer:
    def __init__(this):
        this.isRunning = True

    async def connect(this, reader, writer):
        this.reader = reader
        this.writer = writer

        this.initGame()
        await this.initIO()
        this.sendSnaps()

    def initGame(this, seed = 5589):
        random.seed(seed)
        this.bot = Bot()
        names = ["Adam", "T100", "Skynet", "Robocop"]
        random.shuffle(names)
        this.euchre = Euchre(names)        
        this.game = Game(this.euchre)        
        this.game.input(None, "start", None)     
        this.history = [("seed", seed), ("start", None)]

    async def initIO(this):
        async with asyncio.TaskGroup() as tg:
            t1 = tg.create_task(this.readStdin())
            t2 = tg.create_task(this.readSocket())

    async def readStdin(this):
        while this.isRunning:
            line = await reader.readline()
            if not line: break
            parts = line.split()

            if parts[0] == "print":
                print(euchre)
            elif parts[0] == "exit":
                this.isRunning = False           

    async def readSocket(this):
        try:
            with this.conn:  # Automatically close the connection when done
                while this.running:
                    await this.receivePacket()
        except ConnectionResetError:
            this.running = False
            print(f"Connection with {this.addr} was reset by the client.")
            return false

        print(f"Connection with {this.addr} has been closed.") 

    async def receivePacket(this):
        print("---------------------------------------")  
        print(f" current player {this.euchre.getCurrentPlayer().name}")
        if this.euchre.getCurrentPlayer().name == "Adam":
            await this.getNextPacket()
        else:
            snap = Snapshot(this.game, this.euchre.getCurrentPlayer())
            (action, data) = this.bot.decide(snap)
            print(f"bot {this.euchre.getCurrentPlayer().name}: {action} {data}")
            this.history.append((action, data))                
            this.game.input(this.euchre.getCurrentPlayer(), action, data)

        this.sendSnaps()

    # Translate raw bytes from input stream into a python object (snapshot).
    async def getNextPacket(this):
        data = await this.reader.read(1024) # Receive data from the client
        if not data:                 # Client has closed the connection
            print("connection terminated")
            this.running = False
            return

        print(f"Data received: {len(data)}") 
        packet = pickle.loads(data)
        print(packet) 
        this.hndPacket(packet)

    async def sendSnaps(this):
        snap = Snapshot(this.game, this.euchre.players.getPlayer("Adam"))
        this.writer.write(pickle.dumps(snap))           
        await this.writer.drain()

        print(f"data sent hash : {this.game.hash}")

        data = await this.reader.read(1024)  # Receive ack from client
        if not data:                   # Client has closed the connection
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

    def hndPacket(this, packet):
        action = packet[0]
        data = packet[1]

        if action == "save":
            this.saveHistory()
        elif action == "load":
            this.loadHistory()
        else:
            try:
                this.game.input(this.euchre.players.getPlayer("Adam"), action, data)
                this.history.append(packet) 
            except EuchreException as ex:
                print(ex)


    def loadHistory(this):
        print("--- Loading History -------------------")
        this.history = []

        with open('history.txt', 'r') as file:
            for line in file:
                if line == None: continue                
                line = line.strip()
                parsed = line.split()
                print(f"{line} -> {parsed}")
                this.loadAction(parsed)
        print("---------------------------------------")                

    def loadAction(this, parsed):        
        action = parsed[0] if len(parsed) > 0 else ""
        data = parsed[1] if len(parsed) > 1 else ""
        if action == "": return

        this.history.append((action, data))

        if action == "seed":
            random.seed(int(data))
        elif action == "start":
            names = ["Adam", "T100", "Skynet", "Robocop"]
            random.shuffle(names)
            this.euchre = Euchre(names)  
            this.game = Game(this.euchre)
            this.game.input(None, "start", None)  
        else:
            this.game.input(this.euchre.getCurrentPlayer(), action, data)


    def saveHistory(this):
        with open('history.txt', 'w') as file:
            for line in this.history:
                if line == None: continue
                file.write(f"{line[0]} {line[1]}\n") 
                       