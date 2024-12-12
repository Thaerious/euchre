import socket
import pickle
import curses
import queue
import threading
from euchre import *
from euchre.Card import Hand

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

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

        this.options = []
        this.selectedOption = -1
        this.selectedCard = -1

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
                snap = pickle.loads(data)
                this.snapQ.put(snap)

                with this.paintLock:                
                    this.statscr.addstr(0, 0, f"packets waiting: {this.snapQ.qsize()}", curses.color_pair(1))
                    this.statscr.refresh()                    
            except socket.timeout:
                # Timeout allows us to check this.running periodically
                continue
            except Exception as e:
                print(f"Error: {e}")
                break                
            
    def send(this):
        data = None
        action = this.options[this.selectedOption].lower()

        if this.selectedCard != -1:
            data = this.snap.cards[this.selectedCard]

        this.socket.sendall(pickle.dumps((action, data)))            

    def startUILoop(this):
        this.getNextSnap() 

        while this.running == True:
            this.printBoard(this.snap)            
            key = this.stdscr.getch()   

            if key == ord('x'):
                this.stdscr.clear()                
                this.stdscr.refresh()
                this.running = False        
            elif key == ord('p'):
                this.printSnap(this.snap)
                this.printBoard(this.snap)
            elif key == ord('n'):
                this.getNextSnap()                                             
            elif key == curses.KEY_RIGHT:
                this.selectedOption = this.selectedOption + 1
                if this.selectedOption >= len(this.options): this.selectedOption = len(this.options) - 1
            elif key == curses.KEY_LEFT:
                this.selectedOption = this.selectedOption - 1
                if this.selectedOption < 0: this.selectedOption = 0
            elif key == 10:  
                this.send()   
                this.getNextSnap()

    def getNextSnap(this):
        this.snap = this.snapQ.get() 

        if this.snap.state == 1:
            this.options = ["Pass", "Order", "Alone"]
            this.selectedOption = 0   
            this.selectedCard = -1         

        elif this.snap.state == 2:
            this.options = ["Up", "Down"]
            this.selectedOption = 0            
            this.selectedCard = -1

        elif this.snap.state == 3:
            this.options = ["Pass", "Make", "Alone"]
            this.selectedOption = 0
            this.selectedCard = -1   

        elif this.snap.state == 4:
            this.options = ["Make", "Alone"]
            this.selectedOption = 0
            this.selectedCard = -1       

        else:
            this.options = []
            this.selectedOption = 0                   
            this.selectedCard = -1

    def printMenu(this, snap, x = 21):
        if snap.active == snap.forPlayer:
            this.printActiveMenu(snap, x)
        else:
            this.printIdleMenu(snap, x)

    def printActiveMenu(this, snap, x = 20):
        if snap.state != 5: this.printOptions(x)        
        this.stdscr.addstr(x + 1, 0, "[p] Print snapshot")
        this.stdscr.addstr(x + 2, 0, "[x] Exit")    

    def printIdleMenu(this, snap, x = 20):
        this.stdscr.addstr(x + 0, 0, "[n] Next")
        this.stdscr.addstr(x + 1, 0, "[p] Print snapshot")
        this.stdscr.addstr(x + 2, 0, "[x] Exit")

    def printEuchre(this):
        this.stdscr.clear()
        string = str(this.euchre)
        this.stdscr.addstr(string)
        this.stdscr.addstr(string.count('\n') + 1, 0, "Press any key to continue")
        this.stdscr.getch()

    def printSnap(this, snap):
        this.stdscr.clear()        
        string = str(snap)
        this.stdscr.addstr(string)
        this.stdscr.addstr(string.count('\n') + 1, 0, "Press any key to continue")
        this.stdscr.refresh()
        this.stdscr.getch()      

    def printOptions(this, x):
        y = 0
        for i, option in enumerate(this.options):
            if i == this.selectedOption:
                this.stdscr.addstr(x, y, f"[{option}]", curses.color_pair(2))
            else:
                this.stdscr.addstr(x, y, f"[{option}]", curses.color_pair(1))

            y = y + len(option) + 3

    def printBoard(this, snap):
        with this.paintLock:
            this.stdscr.clear()
            if snap != None:
                this.printUpCard(snap)
                this.printSouth(snap)
                this.printWest(snap)
                this.printNorth(snap)
                this.printEast(snap)
                this.printMenu(snap)       
            this.statscr.addstr(0, 0, f"packets waiting: {this.snapQ.qsize()}", curses.color_pair(1))
            this.stdscr.refresh()

    def printUpCard(this, snap):
        if snap.upCard is not None:
            printCard(this.stdscr, 5, 10, snap.upCard)
        else:
            printCard(this.stdscr, 5, 10, Card("X"))
        printCard(this.stdscr, 5, 18, Card("  "))

    def printSouth(this, snap):
        x = 16
        y = 0
        w = (len(this.snap.hand) * 4) + 1
        offy = (21 - w) / 2
        y = y + 6 + offy
        y = int(y)

        for i, card in enumerate(this.snap.hand):
            if i == this.selectedCard:
                printCard(this.stdscr, x, y, card, 2)
            else:
                printCard(this.stdscr, x, y, card, 1)
            y = y + 4

        playPosition = snap.forPlayer % 4
        if playPosition == snap.active:
            printCard(this.stdscr, 10, 14, Card("  "), 3)
        else:
            printCard(this.stdscr, 10, 14, Card("  "), 1)            

    def printWest(this, snap):
        playPosition = (snap.forPlayer + 1) % 4
        if playPosition == snap.active:
            printCard(this.stdscr, 5, 0, Card("  "), 3)
        else:
            printCard(this.stdscr, 5, 0, Card("  "), 1)    

    def printNorth(this, snap):
        playPosition = (snap.forPlayer + 2) % 4
        if playPosition == snap.active:
            printCard(this.stdscr, 0, 14, Card("  "), 3)
        else:
            printCard(this.stdscr, 0, 14, Card("  "), 1)

    def printEast(this, snap):
        playPosition = (snap.forPlayer + 3) % 4
        if playPosition == snap.active:
            printCard(this.stdscr, 5, 27, Card("  "), 3)
        else:
            printCard(this.stdscr, 5, 27, Card("  "), 1)      

def printCard(stdscr, x, y, card, color = 1):
    l = card.value.ljust(2)
    s = card.suit
    r = card.value.rjust(2)

    stdscr.addstr(x+0, y, f"┌─────┐", curses.color_pair(color))
    stdscr.addstr(x+1, y, f"│{l}   │", curses.color_pair(color))
    stdscr.addstr(x+2, y, f"│  {s}  │", curses.color_pair(color))
    stdscr.addstr(x+3, y, f"│   {r}│", curses.color_pair(color))
    stdscr.addstr(x+4, y, f"└─────┘", curses.color_pair(color))

def Main(stdscr):
    view = View(stdscr)
    view.connect()

if __name__ == "__main__":
    curses.wrapper(Main)
    # view = TestView()
    # view.connect()