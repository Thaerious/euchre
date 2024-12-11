import socket
import pickle
import curses
import queue
import threading
from euchre import *
from euchre.Card import Hand

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def connect():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)
        snap = pickle.loads(data)
        return snap

class View:
    def __init__(this, stdscr):
        this.stdscr = stdscr

    def update(this, snap):
        x = 0
        # running = True
        # while running:
        #     key = this.stdscr.getch()
        #     if key ==  ord('x'): 
        #         running = False
        #     elif key == ord('p'):
        #         this.printEuchre()
        #     elif key == ord('z'):
        #         this.printSnap()     
            
        #     snap = Snapshot(this.game, this.euchre.players.getPlayer("Adam"))
        #     this.printBoard(snap)

    def start(this):
        this.stdscr.clear()
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Default color
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Highlight color
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Current player color

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
        this.snapQ = queue.Queue()
        
        this.listenThread = threading.Thread(target=this.listenLoop)
        this.listenThread.daemon = True  # Ensure threads close when the main program exits
        this.listenThread.start()

    def listenLoop(this):
        while this.running == True:
            data = this.socket.recv(4096)
            snap = pickle.loads(data)
            this.queue.put(snap)

    def gameLoop(this):
        this.running = True
        while this.running == True:
            data = this.socket.recv(4096)
            snap = pickle.loads(data)
            this.printBoard(snap)

    def printMenu(this, x = 20):
        this.stdscr.addstr(x, 0, "[x] Exit")
        this.stdscr.addstr(x + 1, 0, "[p] Print euchre object")
        this.stdscr.addstr(x + 2, 0, "[z] Print snapshot")

    def printEuchre(this):
        this.stdscr.clear()
        string = str(this.euchre)
        this.stdscr.addstr(string)
        this.stdscr.addstr(string.count('\n') + 1, 0, "Press any key to continue")
        this.stdscr.getch()

    def printSnap(this):
        this.stdscr.clear()
        snap = Snapshot(this.game, this.euchre.players.getPlayer("Adam"))
        string = str(snap)
        this.stdscr.addstr(string)
        this.stdscr.addstr(string.count('\n') + 1, 0, "Press any key to continue")
        this.stdscr.getch()      

    def printBoard(this, snap):
        this.stdscr.clear()
        this.printUpCard(snap)
        this.printSouth(snap)
        this.printEast(snap)
        this.printNorth(snap)
        this.printWest(snap)
        this.printMenu()
        this.stdscr.refresh()

    def printUpCard(this, snap):
        if snap.upCard is not None:
            printCard(this.stdscr, 5, 10, snap.upCard)
        else:
            printCard(this.stdscr, 5, 10, Card("X"))
        printCard(this.stdscr, 5, 18, Card("  "))

    def printSouth(this, snap):
        printHandHz(this.stdscr, 15, 0, snap.hand, 0)

    def printEast(this, snap):
        playPosition = (snap.forPlayer + 1) % 4
        if playPosition == snap.active:
            printCard(this.stdscr, 0, 14, Card("  "), 3)
        else:
            printCard(this.stdscr, 0, 14, Card("  "), 1)

    def printNorth(this, snap):
        playPosition = (snap.forPlayer + 2) % 4
        if playPosition == snap.active:
            printCard(this.stdscr, 5, 0, Card("  "), 3)
        else:
            printCard(this.stdscr, 5, 0, Card("  "), 1)

    def printWest(this, snap):
        playPosition = (snap.forPlayer + 3) % 4
        if playPosition == snap.active:
            printCard(this.stdscr, 5, 27, Card("  "), 3)
        else:
            printCard(this.stdscr, 5, 27, Card("  "), 1)            

def printEuchre(stdscr, euchre):
    stdscr.clear()
    printCard(stdscr, 0, 14, Card("  "), 3)
    printCard(stdscr, 5, 0, Card("  "))
    printCard(stdscr, 5, 10, Card("K♦"))
    printCard(stdscr, 5, 18, Card("  "))
    printCard(stdscr, 5, 27, Card("  "))
    printCard(stdscr, 10, 14, Card("  "))
    printHandHz(stdscr, 15, 0, Hand(["A♣", "A♣", "Q♥", "Q♥"]), 0)
    printMenu(stdscr)

    stdscr.refresh()

def printMenu(stdscr):
    stdscr.addstr(20, 0, "[x] Exit")
    stdscr.addstr(21, 0, "[p] Print euchre object")
    stdscr.addstr(22, 0, "[s] Print snapshot")

def printCard(stdscr, x, y, card, color = 1):
    l = card.value.ljust(2)
    s = card.suit
    r = card.value.rjust(2)

    stdscr.addstr(x+0, y, f"┌─────┐", curses.color_pair(color))
    stdscr.addstr(x+1, y, f"│{l}   │", curses.color_pair(color))
    stdscr.addstr(x+2, y, f"│  {s}  │", curses.color_pair(color))
    stdscr.addstr(x+3, y, f"│   {r}│", curses.color_pair(color))
    stdscr.addstr(x+4, y, f"└─────┘", curses.color_pair(color))

def printHandHz(stdscr, x, y, hand, highlight = -1):
    w = (len(hand) * 4) + 1
    offy = (21 - w) / 2
    y = y + 6 + offy
    y = int(y)

    for i, card in enumerate(hand):
        color = 2 if i == highlight else 1
        printCard(stdscr, x, y, card, color)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        y = y + 4



def Main(stdscr):
    view = View(stdscr)
    view.start()

if __name__ == "__main__":
    curses.wrapper(Main)