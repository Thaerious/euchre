from euchre import *
from euchre.Euchre import EuchreException
from euchre.bots.Bot import Bot
import pickle
import random
import asyncio
import sys

class GameServer:
    def __init__(this):
        this.isRunning = True

    async def connect(this, reader, writer):
        this.reader = reader
        this.writer = writer

        this.initGame()
        await this.initIO()
        await this.sendSnaps()

    def initGame(this, seed = 5589):
        random.seed(seed)
        this.bot = Bot()
        names = ["Adam", "T100", "Skynet", "Robocop"]
        random.shuffle(names)
        this.euchre = Euchre(names)        
        this.game = Game(this.euchre)        
        this.game.input(None, "start", None)     
        this.history = [(None, "seed", seed, None), (None, "start", None, this.game.hash)]

    async def initIO(this):
        async with asyncio.TaskGroup() as tg:
            t1 = tg.create_task(this.readStdin())
            t2 = tg.create_task(this.readSocket())

    async def readStdin(this):
        loop = asyncio.get_running_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        while this.isRunning:
            print("\b\b> ", end="", flush=True)
            line = await reader.readline()
            if not line: break

            line = line.decode().strip()
            parts = line.split()

            if len(parts) == 0:
                continue

            if parts[0] == "print":
                print(" ----- euchre object -----")
                print(this.euchre)
                print(f"hash: {this.game.hash}")
            if parts[0] == "push":
                await this.sendSnaps()
            elif parts[0] == "exit":
                exit()       
            elif parts[0] == "save":
                this.saveHistory()
            elif parts[0] == "load":
                this.loadHistory()
            elif parts[0] == "history":
                for entry in this.history:
                    print(entry)            


    async def readSocket(this):
        try:
            while this.isRunning:
                await this.receivePacket()
        except ConnectionResetError:
            this.isRunning = False
            print(f"Connection was reset by the client.")
            return False

        print(f"Connection with client has been closed.") 

    async def receivePacket(this):
        if this.euchre.getCurrentPlayer().name == "Adam":
            await this.getNextPacket()
        else:
            snap = Snapshot(this.game, this.euchre.getCurrentPlayer())
            (action, data) = this.bot.decide(snap)
            name = this.euchre.getCurrentPlayer().name
            print(f"\b\b{name} : ('{action}', {data})")
            print("> ", end="", flush=True)                             
            this.game.input(this.euchre.getCurrentPlayer(), action, data)
            this.history.append((name, action, data, this.game.hash))

        await this.sendSnaps()

    # Translate raw bytes from input stream into a python object (snapshot).
    async def getNextPacket(this):
        data = await this.reader.read(1024) # Receive data from the client
        if not data:                 # Client has closed the connection
            print("connection terminated")
            this.running = False
            return

        packet = pickle.loads(data)
        print(f"\b\bAdam : {packet}") 
        print("> ", end="", flush=True)
        this.hndPacket(packet)

    async def sendSnaps(this):
        snap = Snapshot(this.game, this.euchre.players.getPlayer("Adam"))
        this.writer.write(pickle.dumps(snap))             
        await this.writer.drain()      
        print(f"\b\bsent {snap.hash}")       

    def hndPacket(this, packet):
        action = packet[0]
        data = packet[1]

        try:
            this.game.input(this.euchre.players.getPlayer("Adam"), action, data)
            this.history.append(("Adam", action, data, this.game.hash))
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
                this.sendSnaps()
        print("---------------------------------------")                

    def loadAction(this, parsed):        
        action = parsed[0] if len(parsed) > 0 else ""
        data = parsed[1] if len(parsed) > 1 else ""
        if action == "": return

        if action == "seed":
            random.seed(int(data))
            this.history.append((None, "seed", data, None))
        elif action == "start":
            names = ["Adam", "T100", "Skynet", "Robocop"]
            random.shuffle(names)
            this.euchre = Euchre(names)  
            this.game = Game(this.euchre)
            this.game.input(None, "start", None)
            this.history.append((None, "start", None, this.game.hash))  
        else:
            this.game.input(this.euchre.getCurrentPlayer(), action, data)
            this.history.append((this.euchre.getCurrentPlayer().name, action, data, this.game.hash))  


    def saveHistory(this):
        with open('history.txt', 'w') as file:
            for line in this.history:
                if line == None: continue
                file.write(f"{line[1]} {line[2]}\n") 
                       