import socket
import pickle
import curses
import queue
import threading
import time
import traceback
from euchre import *
from euchre.Card import Hand
from euchre.Snapshot import Snapshot

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

stateLabels = [
    "Game not started",
    "Order up dealer?",
    "Pick up card?",
    "Make suit?",
    "Dealer make suit.",
    "Play a card."
]

class OptionList:
    def __init__(this, options = []):
        this.options = options
        this.index = -1
        this.active = False

    def activate(this):
        if this.index == -1: this.index = 0
        this.active = True

    def deactivate(this):
        this.active = False

    def len(this):
        return len(this.options)

    def next(this):
        this.index = this.index + 1
        if this.index >= len(this.options):
            this.index = len(this.options) - 1

    def prev(this):
        this.index = this.index - 1
        if this.index < 0:
            this.index = 0

    def get(this):
        if len(this.options) == 0: return None
        return this.options[this.index]

    def paint(this, stdscr, x):
        if x is None: raise Exception
        if len(this.options) == 0: return x

        y = 0
        for i, option in enumerate(this.options):
            if i == this.index:
                if this.active:
                    stdscr.addstr(x, y, f"[{option}]", curses.color_pair(2) | curses.A_BOLD)
                else:
                    stdscr.addstr(x, y, f" {option} ", curses.color_pair(2))
            else:
                stdscr.addstr(x, y, f" {option} ", curses.color_pair(1))

            y = y + len(option) + 3

        return x + 1

class HandView(OptionList):
    def paint(this, stdscr, x):
        y = 0
        w = (this.len() * 4) + 1
        offy = (21 - w) / 2
        y = y + 6 + offy
        y = int(y)

        for i, card in enumerate(this.options):
            if i == this.index:
                if this.active:
                    paintCard(stdscr, x, y, card, curses.color_pair(2) | curses.A_BOLD)
                else:
                    paintCard(stdscr, x, y, card, curses.color_pair(2))
            else:
                paintCard(stdscr, x, y, card, curses.color_pair(1))

            y = y + 4    

        return x + 5        

class View:
    def __init__(this, stdscr):
        this.stdscr = stdscr
        this.paintLock = threading.Lock()

        stdscr.keypad(True)
        curses.start_color()
        curses.curs_set(0)

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Default color
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Highlight color
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Current player color

        height, width = stdscr.getmaxyx()
        this.statscr = this.stdscr.subwin(1, width, height - 1, 0)

        this.handView = None
        this.actionOptions = None
        this.dataOptions = None       
        this.options = []
        this.selectedOption = -1

        this.snap = None
        this.history = []

    def currentOptions(this):
        if this.selectedOption >= 0:
            return this.options[this.selectedOption]
        return None

    def selectOption(this, index):
        if this.selectedOption >= 0 and this.selectedOption < len(this.options):
            this.options[this.selectedOption].deactivate()

        this.selectedOption = index
        this.options[index].activate()

    def nextOption(this):
        next = this.selectedOption + 1
        if next >= len(this.options): next = len(this.options) - 1
        this.selectOption(next)
        

    def prevOption(this):
        prev = this.selectedOption - 1
        if prev < 0: prev = 0
        this.selectOption(prev)

    def start(this):
        this.stdscr.clear()

        this.stdscr.addstr(0, 0, f"┌─────────────────────────┐", curses.color_pair(1))
        this.stdscr.addstr(1, 0, f"│Press Enter to Start Game│", curses.color_pair(1))
        this.stdscr.addstr(2, 0, f"└─────────────────────────┘", curses.color_pair(1))

        key = this.stdscr.getch()
        if key == 10:  # Enter key                       
            this.connect()

    def connect(this):
        this.running = True

        this.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this.socket.connect((HOST, PORT))     
        this.socket.settimeout(1.0)   
        this.snapQ = queue.Queue()

        this.listenThread = threading.Thread(target=this.listen)
        this.listenThread.daemon = True  # Ensure threads close when the main program exits
        this.listenThread.start()        
        this.startUILoop()    
        this.listenThread.join()

    def listen(this):
        while this.running == True:
            try:
                data = this.socket.recv(4096)
                if not data: break # Handle the case where the connection is closed

                with this.paintLock:
                    dataObject = pickle.loads(data)

                    if isinstance(dataObject, Snapshot): 
                        snap = dataObject                   
                        this.snapQ.put(snap)
                        this.history.append(snap.hash)
                        this.socket.sendall(pickle.dumps(("ack", snap.hash)))                              
                        this.statscr.addstr(0, 0, f"packets waiting: {this.snapQ.qsize()}", curses.color_pair(1))
                        this.statscr.refresh()                    
                    else:
                        this.paintException(dataObject)
            except socket.timeout:
                # Timeout allows us to check this.running periodically
                continue            
            
    def send(this):
        action = "play"
        data = None

        if this.actionOptions != None:
            action = this.actionOptions.get().lower()

        if this.dataOptions != None:
            data = this.dataOptions.get()

        if this.snap.state == 5:
            data = str(this.handView.get())

        this.socket.sendall(pickle.dumps((action, data)))            

    def continueLoop(this):
        while this.snapQ.qsize() > 0:
            this.getNextSnap()
            this.paintTrickOver(this.snap)
            this.paintBoard(this.snap)
            time.sleep(0.75)    

    def startUILoop(this):
        this.getNextSnap(True) 

        while this.running == True:
            this.paintBoard(this.snap)            
            key = this.stdscr.getch()   

            print(key)

            if key == ord('x'):
                this.stdscr.clear()                
                this.stdscr.refresh()
                this.running = False        
            elif key == ord('p'):
                this.paintSnap(this.snap)
                this.paintBoard(this.snap)
            elif key == ord('s'):
                this.socket.sendall(pickle.dumps(("save", None))) 
            elif key == ord('l'):
                this.socket.sendall(pickle.dumps(("load", None)))
            elif key == ord('n'):
                this.continueLoop()
            elif key == curses.KEY_UP:
                this.prevOption()
            elif key == curses.KEY_DOWN:
                this.nextOption()
            elif key == curses.KEY_RIGHT:
                this.currentOptions().next()
            elif key == curses.KEY_LEFT:
                this.currentOptions().prev()
            elif key == 10:  
                if this.snap.active == this.snap.forPlayer:                    
                    this.send()
                    # this.getNextSnap(True)
                    this.continueLoop()

    def getNextSnap(this, wait = False):
        if wait == True:
            this.snap = this.snapQ.get() 
        if this.snapQ.qsize() > 0:
            this.snap = this.snapQ.get() 

        if this.snap == None: return
        this.handView = HandView(this.snap.hand)

        if this.snap.state == 1:
            this.actionOptions = OptionList(["Pass", "Order", "Alone"])
            this.dataOptions = None
            this.options = [this.actionOptions]
            this.selectOption(0)

        elif this.snap.state == 2:
            this.actionOptions = OptionList(["Up", "Down"])
            this.dataOptions = None            
            this.options = [this.handView, this.actionOptions]
            this.selectOption(1)

        elif this.snap.state == 3:
            this.actionOptions = OptionList(["Pass", "Make", "Alone"])
            this.dataOptions = OptionList(allowedSuits(this.snap))         
            this.options = [this.dataOptions, this.actionOptions]
            this.selectOption(1)

        elif this.snap.state == 4:
            this.actionOptions = OptionList(["Make", "Alone"])
            this.dataOptions = OptionList(allowedSuits(this.snap))  
            this.options = [this.dataOptions, this.actionOptions]
            this.selectOption(1)

        elif this.snap.state == 5:
            this.actionOptions = None
            this.dataOptions = None
            this.options = [this.handView]
            this.selectOption(0)

    def paintMenu(this, snap, x = 22):
        if snap.active == snap.forPlayer:
            this.paintActiveMenu(snap, x)
        else:
            this.paintIdleMenu(snap, x)

    def paintActiveMenu(this, snap, x = 21):        
        this.stdscr.addstr(x + 0, 0, stateLabels[snap.state])
        x = x + 1

        if this.dataOptions != None: 
            x = this.dataOptions.paint(this.stdscr, x)

        if this.actionOptions != None: 
            x = this.actionOptions.paint(this.stdscr, x)

        this.stdscr.addstr(x + 1, 0, "[p] Print snapshot")
        this.stdscr.addstr(x + 2, 0, "[x] Exit")    

    def paintIdleMenu(this, snap, x = 21):
        this.stdscr.addstr(x + 0, 0, "[p] Print snapshot")
        this.stdscr.addstr(x + 1, 0, "[x] Exit")

    def paintException(exception):   
        this.stdscr.clear()
        print(exception.message)
        this.stdscr.addstr(x + 1, 0, "Press any key to continue")
        this.stdscr.refresh()
        this.stdscr.getch()

    def paintSnap(this, snap):
        this.stdscr.clear()        
        string = str(snap)
        this.stdscr.addstr(string)
        this.stdscr.addstr(string.count('\n') + 1, 0, "Press any key to continue")
        this.stdscr.refresh()
        this.stdscr.getch()      

    def paintTrickOver(this, snap):
        if this.snap.state != 5: return
        if len(this.snap.tricks) < 2: return
        if len(this.snap.tricks[-1]) > 0: return

        with this.paintLock:
            this.stdscr.clear()
            if snap != None:
                trick = snap.tricks[-2]
                this.paintUpCard(snap)
                this.paintSouth(snap, trick)
                this.paintWest(snap, trick)
                this.paintNorth(snap, trick)
                this.paintEast(snap, trick)

                winner = snap.names[trick.winner(snap.trump)]
                this.stdscr.addstr(24, 0, f"The winner of this trick is {winner}")
                this.stdscr.addstr(25, 0, "Press any key to continue")
            this.statscr.addstr(0, 0, f"packets waiting: {this.snapQ.qsize()}", curses.color_pair(1))
            this.stdscr.refresh()
        this.stdscr.getch()
        

    def paintBoard(this, snap):
        with this.paintLock:
            this.stdscr.clear()
            if snap != None:
                trick = snap.tricks[-1]
                this.paintUpCard(snap)
                this.paintSouth(snap, trick)
                this.paintWest(snap, trick)
                this.paintNorth(snap, trick)
                this.paintEast(snap, trick)
                this.paintMenu(snap)       
            this.statscr.addstr(0, 0, f"packets waiting: {this.snapQ.qsize()}", curses.color_pair(1))
            this.stdscr.refresh()

    def paintUpCard(this, snap):
        if snap.upCard is not None:
            paintCard(this.stdscr, 6, 10, snap.upCard)
        else:
            paintCard(this.stdscr, 6, 10, Card("X"))
        paintCard(this.stdscr, 6, 18, Card("  "))

    def paintSouth(this, snap, trick):
        if this.handView != None: this.handView.paint(this.stdscr, 17)
        this.paintPlayer(snap, 0, 11, 14, trick)           

    def paintWest(this, snap, trick):
        this.paintPlayer(snap, 1, 6, 0, trick) 

    def paintNorth(this, snap, trick):
        this.paintPlayer(snap, 2, 0, 14, trick)

    def paintEast(this, snap, trick):
        this.paintPlayer(snap, 3, 6, 27, trick)

    def paintPlayer(this, snap, i, x, y, trick):
        playPosition = (snap.forPlayer + i) % 4

        # paint the player box yellow if active else white
        name = snap.names[playPosition]
        if snap.dealer == playPosition: name = f"({name})"
        if snap.maker == playPosition: name = f"{name} {snap.trump}"

        card = None
        t = (playPosition - trick.lead) % 4
        if len(trick) > t: card = trick[t]

        if playPosition == snap.active:
            x = paintCard(this.stdscr, x, y, card, 3)
            this.stdscr.addstr(x, y, f"{name}", 3)
        else:
            x = paintCard(this.stdscr, x, y, card, 1)              
            this.stdscr.addstr(x, y, f"{name}", 1)

def allowedSuits(snap):
    suits = ["♠", "♣", "♥", "♦"]
    suits.remove(snap.upCard.suit)
    return suits

def paintCard(stdscr, x, y, card, color = 255):
    if card == None: return paintBox(stdscr, x, y, color)

    l = card.value.ljust(2)
    s = card.suit
    r = card.value.rjust(2)

    stdscr.addstr(x+0, y, f"┌─────┐", color)
    stdscr.addstr(x+1, y, f"│{l}   │", color)
    stdscr.addstr(x+2, y, f"│  {s}  │", color)
    stdscr.addstr(x+3, y, f"│   {r}│", color)
    stdscr.addstr(x+4, y, f"└─────┘", color)
    return x + 5

def paintBox(stdscr, x, y, color = 255):
    if color == None: curses.color_pair(1)

    stdscr.addstr(x+0, y, f"┌─────┐", color)
    stdscr.addstr(x+1, y, f"│     │", color)
    stdscr.addstr(x+2, y, f"│     │", color)
    stdscr.addstr(x+3, y, f"│     │", color)
    stdscr.addstr(x+4, y, f"└─────┘", color)
    return x + 5

def Main(stdscr):
    view = View(stdscr)
    view.connect()
    

if __name__ == "__main__":
    curses.wrapper(Main)
    # view = TestView()
    # view.connect()