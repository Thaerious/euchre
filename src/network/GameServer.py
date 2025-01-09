from euchre import *
from euchre.Euchre import EuchreException
from euchre.bots.Bot import Bot
import pickle
import random
import asyncio
import sys
import struct
import traceback

class GameServer:
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
            tg.create_task(this.readStdin())
            tg.create_task(this.readSocket())

    async def readStdin(this):
        this.stdinRunning = True

        loop = asyncio.get_running_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        while this.stdinRunning:
            try:
                print("\b\b> ", end="", flush=True)
                line = await reader.readline()
                if not line: break

                line = line.decode().strip()
                parts = line.split()
                await this.processInput(parts)
            except Exception as ex:                
                this.socketRunning = False
                traceback.print_exc()

    async def processInput(this, parts):
        if len(parts) == 0:
            return
        elif parts[0] == "print":
            print(this.euchre)
            print(f"hash: {this.game.hash}")
        elif parts[0] == "refresh":
            await this.sendSnaps()
        elif parts[0] == "exit":
            exit()       
        elif parts[0] == "save":
            this.saveHistory()
        elif parts[0] == "load":
            await this.loadHistory()
        elif parts[0] == "history":
            for entry in this.history:
                print(entry)
                
    async def readSocket(this):
        this.socketRunning = True

        while this.socketRunning:
            try:
                await this.receivePacket()
            except ConnectionResetError:
                this.isRunning = False
                print(f"Connection was reset by the client.")
                return False
            except Exception as ex:
                this.socketRunning = False
                traceback.print_exc()

        print(f"Connection with client has been closed.") 

    async def receivePacket(this):
        if this.euchre.getCurrentPlayer().name == "Adam":
            await this.getNextPacket()
        else:
            snap = Snapshot(this.game, this.euchre.getCurrentPlayer())
            (action, data) = this.bot.decide(snap)
            (action, data) = (action.lower(), data)

            name = this.euchre.getCurrentPlayer().name
            print(f"\b\b{name} : ('{action}', {data})")
            print("> ", end="", flush=True)                             
            this.game.input(this.euchre.getCurrentPlayer(), action, data)
            this.history.append((name, action, data, this.game.hash))

        await this.sendSnaps()

    # Translate raw bytes from input stream into a python object (snapshot).
    async def getNextPacket(this):        
        len_b = await this.reader.readexactly(4)
        len = struct.unpack("!I", len_b)[0]
        data = await this.reader.readexactly(len) # Receive data from the client

        if not data:                 # Client has closed the connection
            print("connection terminated")
            this.running = False
            return

        packet = pickle.loads(data)
        print(f"\b\bAdam : {packet}") 
        print("> ", end="", flush=True)
        this.hndPacket(packet)

    async def sendSnaps(this):
        snap = Snapshot(this.game, this.euchre.players.get_player("Adam"))
        serialized = pickle.dumps(snap)
        len_b = struct.pack("!I", len(serialized))

        this.writer.write(len_b + serialized)             
        await this.writer.drain()      
        print(f"\b\bsent {len(serialized)} {snap.hash}")       

    def hndPacket(this, packet):
        (action, data) = (packet[0].lower(), packet[1])

        try:
            this.game.input(this.euchre.players.get_player("Adam"), action, data)
            this.history.append(("Adam", action, data, this.game.hash))
        except EuchreException as ex:
            print(ex)


    async def loadHistory(this):
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

        await this.sendSnaps()

        while this.euchre.getCurrentPlayer().name != "Adam":
            snap = Snapshot(this.game, this.euchre.getCurrentPlayer())
            (action, data) = this.bot.decide(snap)
            (action, data) = (action.lower(), data)

            name = this.euchre.getCurrentPlayer().name
            print(f"\b\b{name} : ('{action}', {data})")
            print("> ", end="", flush=True)                             
            this.game.input(this.euchre.getCurrentPlayer(), action, data)
            this.history.append((name, action, data, this.game.hash))
            await this.sendSnaps()          

    def loadAction(this, parsed):        
        action = parsed[0] if len(parsed) > 0 else ""
        data = parsed[1] if len(parsed) > 1 else ""
        if action == "": return

        if action == "seed":
            this.initGame(seed = int(data))
        elif action == "start":
            pass
        else:
            this.game.input(this.euchre.getCurrentPlayer(), action, data)
            this.history.append((this.euchre.getCurrentPlayer().name, action, data, this.game.hash))   


    def saveHistory(this):
        with open('history.txt', 'w') as file:
            for line in this.history:
                if line == None: continue
                file.write(f"{line[1]} {line[2]}\n") 
                       