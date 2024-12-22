import socket
import pickle
import curses
import threading
import struct
import time
from datetime import datetime
from euchre import *
from euchre.Card import Hand
from euchre.Snapshot import Snapshot
from euchre.bots.tools import *

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
        this.paintLock = threading.Lock()

        stdscr.keypad(True)
        curses.start_color()
        curses.curs_set(0)

        curses.init_color(8, 400, 400, 400)  # RGB values (0-1000)

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Default color
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Highlight color
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Current player color
        curses.init_pair(4, 8, curses.COLOR_BLACK)  # Gray text on black background

        height, width = stdscr.getmaxyx()
        this.stdscr = stdscr
        this.boardscr = stdscr.subwin(height - 1, width, 0, 0) 
        this.statscr = stdscr.subwin(1, width, height - 1, 0)

        this.running = True
        this.snaps = []
        this.handView = None
        this.actionOptions = None
        this.dataOptions = None
        this.infoScreen = False
        this.options = []
        this.selectedOption = -1

    def connect(this):
        this.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this.socket.connect((HOST, PORT))

        # retrieve one snapshot before continuing
        this.loadNextSnapshot()
        this.updateUIState()
        this.paintBoard()

        this.socket.settimeout(1)

        this.socketThead = threading.Thread(target=this.listenSocket)
        this.socketThead.daemon = True  # Ensure threads close when the main program exits
        this.socketThead.start()

        this.stdinThead = threading.Thread(target=this.listenStdin)
        this.stdinThead.daemon = True  # Ensure threads close when the main program exits
        this.stdinThead.start()

        this.socketThead.join()
        this.stdinThead.join()

    # Load the snapshot queue with incoming packets
    def listenSocket(this):
        while this.running == True:
            try:
                this.loadNextSnapshot()
                this.updateUIState()
                if this.snaps[-1].lastPlayer != this.snaps[-1].forPlayer: 
                    time.sleep(0.75)

                if not this.paintTrickOver():
                    this.paintBoard()
            except socket.timeout:
                # Timeout allows us to check this.running periodically
                continue
            except Exception as e:
                curses.endwin()
                raise e  # Re-raise exceptions to ensure proper cleanup

    # retreive the next packet from the socket and translate it into a snapshot    
    def loadNextSnapshot(this):
        len_b = this.socket.recv(4)
        len = struct.unpack("!I", len_b)[0]
        data = this.socket.recv(len)
        if not data: raise Exception("Remotely Closed Socket")
        dataObject = pickle.loads(data)

        if isinstance(dataObject, Snapshot):
            this.snaps.append(dataObject)
            this.updateStatus(f"{len} {dataObject.hash} {datetime.now().strftime("%H:%M:%S")}")
        else:
            raise Exception("Expected Snapshot")


    def listenStdin(this):
        try:
            while this.running == True:
                key = this.stdscr.getch()

                if this.infoScreen: # when 'any key' clears screen
                    this.infoScreen = False
                    this.paintBoard()
                elif key == ord('x'):
                    this.running = False
                elif key == ord('p'):
                    this.paintSnap()                 
                elif key == curses.KEY_UP:
                    this.prevOption()
                    this.paintBoard()
                elif key == curses.KEY_DOWN:
                    this.nextOption()
                    this.paintBoard()
                elif key == curses.KEY_RIGHT:
                    this.currentOptions().next()
                    this.paintBoard()
                elif key == curses.KEY_LEFT:
                    this.currentOptions().prev()
                    this.paintBoard()
                elif key == 10:
                    this.send()
                    this.paintBoard()
            
        except Exception as e:
            curses.endwin()
            raise e  # Re-raise exceptions to ensure proper cleanup

    def shutdown(this, exception):
        this.boardscr.cl

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
        this.boardscr.clear()

        this.boardscr.addstr(0, 0, f"┌─────────────────────────┐", curses.color_pair(1))
        this.boardscr.addstr(1, 0, f"│Press Enter to Start Game│", curses.color_pair(1))
        this.boardscr.addstr(2, 0, f"└─────────────────────────┘", curses.color_pair(1))

        key = this.boardscr.getch()
        if key == 10:  # Enter key
            this.connect()

    def send(this, snap = None):
        if snap == None and len(this.snaps) == 0: return
        if snap == None: snap = this.snaps[-1]
        
        action = "play"
        data = None

        if this.actionOptions != None:
            action = this.actionOptions.get().lower()

        if this.dataOptions != None:
            data = this.dataOptions.get()

        if snap.state == 5 or snap.state == 2:
            data = str(this.handView.get())

        serialized = pickle.dumps((action, data))
        len_b = struct.pack("!I", len(serialized))
        this.socket.sendall(len_b + serialized)

    # Retrieve the next snap from the queue
    # Enable / disable UI components based on the state
    def updateUIState(this, snap = None):
        if snap == None and len(this.snaps) == 0: return
        if snap == None: snap = this.snaps[-1]

        this.handView = HandView(snap.hand)

        if snap.state == 1:
            this.actionOptions = OptionList(["Pass", "Order", "Alone"])
            this.dataOptions = None
            this.options = [this.actionOptions]
            this.selectOption(0)

        elif snap.state == 2:
            this.actionOptions = OptionList(["Up", "Down"])
            this.dataOptions = None
            this.options = [this.handView, this.actionOptions]
            this.selectOption(1)

        elif snap.state == 3:
            this.actionOptions = OptionList(["Pass", "Make", "Alone"])
            this.dataOptions = OptionList(this.allowedSuits())
            this.options = [this.dataOptions, this.actionOptions]
            this.selectOption(1)

        elif snap.state == 4:
            this.actionOptions = OptionList(["Make", "Alone"])
            this.dataOptions = OptionList(this.allowedSuits())
            this.options = [this.dataOptions, this.actionOptions]
            this.selectOption(1)

        elif snap.state == 5:
            this.actionOptions = None
            this.dataOptions = None
            this.options = [this.handView]
            this.selectOption(0)

        return snap

    def paintMenu(this, x = 22, snap = None):
        if snap == None and len(this.snaps) == 0: return
        if snap == None: snap = this.snaps[-1]

        if snap.active == snap.forPlayer:
            this.paintActiveMenu(x)
        else:
            this.paintIdleMenu(x)

    def paintActiveMenu(this, x = 21, snap = None):
        if snap == None and len(this.snaps) == 0: return
        if snap == None: snap = this.snaps[-1]

        this.boardscr.addstr(x + 0, 0, stateLabels[snap.state])
        x = x + 1

        if this.dataOptions != None:
            x = this.dataOptions.paint(this.boardscr, x)

        if this.actionOptions != None:
            x = this.actionOptions.paint(this.boardscr, x)

        this.boardscr.addstr(x + 1, 0, "[p] Print snapshot")
        this.boardscr.addstr(x + 2, 0, "[x] Exit")

    def paintIdleMenu(this, x = 21):
        this.boardscr.addstr(x + 0, 0, "[p] Print snapshot")
        this.boardscr.addstr(x + 1, 0, "[x] Exit")

    def paintSnap(this, snap = None):
        if snap == None and len(this.snaps) == 0: return
        if snap == None: snap = this.snaps[-1]

        this.infoScreen = True
        this.boardscr.clear()
        string = str(snap)
        this.boardscr.addstr(string)
        this.boardscr.addstr(string.count('\n') + 1, 0, "Press any key to continue")
        this.boardscr.refresh()

    def updateStatus(this, string):
        with this.paintLock:
            this.statscr.erase()
            this.statscr.addstr(0, 0, string, curses.color_pair(1))
            this.statscr.refresh()

    def paintTrickOver(this, snap = None):
        if snap == None or len(this.snaps) < 2: return False
        if snap == None: snap = this.snaps[-2]

        this.updateStatus(f"{snap.state} {snap.lastAction[snap.lastPlayer]}")

        if len(this.snaps) < 2: return False
        if this.snaps[-2].state != 5: return False
        if snap.state != 1: return False
        
        this.infoScreen = True

        with this.paintLock:
            this.boardscr.clear()
            if snap != None:
                trick = snap.tricks[-2]
                this.paintUpCard(snap)
                this.paintSouth(snap)
                this.paintWest(snap)
                this.paintNorth(snap)
                this.paintEast(snap)

                trick = snap.tricks[-1] if len(snap.tricks) > 0 else None
                winner = snap.names[trick.winner()]

                this.boardscr.addstr(24, 0, f"The winner of this trick is {winner}")
                this.boardscr.addstr(25, 0, "Press any key to continue")
            this.boardscr.refresh()
        return True

    def paintBoard(this, snap = None):
        if snap == None and len(this.snaps) == 0: return
        if snap == None: snap = this.snaps[-1]

        with this.paintLock:
            this.boardscr.clear()
            if snap != None:
                this.paintUpCard()
                this.paintSouth()
                this.paintWest()
                this.paintNorth()
                this.paintEast()
                this.paintTeam1()
                this.paintTeam2()
                this.paintMenu()
                this.paintScore()
            this.boardscr.refresh()

    def paintUpCard(this, snap = None):
        if snap == None and len(this.snaps) == 0: return
        if snap == None: snap = this.snaps[-1]

        if snap.upCard is not None:
            paintCard(this.boardscr, 6, 10, snap.upCard)
        else:
            paintCard(this.boardscr, 6, 10, Card("X"))
        paintCard(this.boardscr, 6, 18, Card("  "))

    def paintScore(this, snap = None):
        if snap == None and len(this.snaps) == 0: return
        if snap == None: snap = this.snaps[-1]

        x =  13
        y = 1
        team = teamOf(snap.forPlayer)
        other = otherTeam(team)
        this.boardscr.addstr(x+0, y, f"f:a", 1)
        this.boardscr.addstr(x+1, y, f"{snap.score[team]}:{snap.score[other]}", 1)

    def paintTeam1(this, snap = None):
        if snap == None and len(this.snaps) == 0: return
        if snap == None: snap = this.snaps[-1]

        x = 12
        y = 21

        for trick in snap.tricks:
            if len(trick) < len(snap.order): break
            winner = trick.winner()
            partner = (snap.forPlayer + 2) % 4

            if winner == snap.forPlayer or winner == partner:
                this.boardscr.addstr(x+0, y, f"*", 1)
                x = x + 1

    def paintTeam2(this, snap = None):
        if snap == None and len(this.snaps) == 0: return
        if snap == None: snap = this.snaps[-1]

        x = 7
        y = 35

        for trick in snap.tricks:
            if len(trick) < len(snap.order): break
            winner = trick.winner()
            partner = (snap.forPlayer + 2) % 4

            if winner != snap.forPlayer and winner != partner:
                this.boardscr.addstr(x+0, y, f"*", 1)
                x = x + 1

    def paintSouth(this):
        if this.handView != None: this.handView.paint(this.boardscr, 17)
        this.paintPlayer(0, 11, 14)

    def paintWest(this):
        this.paintPlayer(1, 6, 0)

    def paintNorth(this):
        this.paintPlayer(2, 0, 14)

    def paintEast(this):
        this.paintPlayer(3, 6, 28)

    # snap : snapshot
    # chair : chair position at table (s, w, n, e) = (0, 1, 2, 3)
    # x : x offset
    # y : y offset
    # trick : current trick
    def paintPlayer(this, chair, x, y, snap = None):
        if snap == None and len(this.snaps) == 0: return
        if snap == None: snap = this.snaps[-1]

        # index = the index of the player in the snap.names array
        # the same that is used in: active, dealer, forPlayer, maker, and order[]
        pIndex = (snap.forPlayer + chair) % 4

        if (pIndex in snap.order) == False:
            paintBox(this.boardscr, x, y, "", curses.color_pair(4))
            this._paintPlayerName(pIndex, x, y, curses.color_pair(4))
        elif pIndex == snap.active:
            this._paintPlayer(pIndex, x, y, curses.color_pair(3))
            this._paintPlayerName(pIndex, x, y, curses.color_pair(3))
        else:
            this._paintPlayer(pIndex, x, y, curses.color_pair(1))
            this._paintPlayerName(pIndex, x, y, curses.color_pair(1))

    def _paintPlayer(this, pIndex, x, y, color, snap = None):
        if snap == None and len(this.snaps) == 0: return
        if snap == None: snap = this.snaps[-1]

        trick = snap.tricks[-1] if len(snap.tricks) > 0 else None

        if trick == None:
            paintBox(this.boardscr, x, y, snap.lastAction[pIndex], color)
        else:
            card = trick.getCardByPlayer(pIndex)
            paintCard(this.boardscr, x, y, card, color)

    def _paintPlayerName(this, pIndex, x, y, color, snap = None):
        if snap == None and len(this.snaps) == 0: return
        if snap == None: snap = this.snaps[-1]

        # Put name in parens if dealer, append trump to maker
        name = snap.names[pIndex]
        if snap.dealer == pIndex: name = f"({name})"
        if snap.maker == pIndex: name = f"{name} {snap.trump}"
        this.boardscr.addstr(x+5, y, f"{name}", color)

    def allowedSuits(this):
        suits = ["♠", "♣", "♥", "♦"]
        suits.remove(snap.upCard.suit)
        return suits

def paintCard(screen, x, y, card, color = None):
    if color == None: color = curses.color_pair(1)
    if card == None: return paintBox(screen, x, y, "", color)

    l = card.value.ljust(2)
    s = card.suit
    r = card.value.rjust(2)

    screen.addstr(x+0, y, f"┌─────┐", color)
    screen.addstr(x+1, y, f"│{l}   │", color)
    screen.addstr(x+2, y, f"│  {s}  │", color)
    screen.addstr(x+3, y, f"│   {r}│", color)
    screen.addstr(x+4, y, f"└─────┘", color)
    return x + 5

def paintBox(screen, x, y, text, color = None):
    if color == None: curses.color_pair(1)
    if text == None: text = ""
    text = text.center(5)

    screen.addstr(x+0, y, f"┌─────┐", color)
    screen.addstr(x+1, y, f"│     │", color)
    screen.addstr(x+2, y, f"│{text}│", color)
    screen.addstr(x+3, y, f"│     │", color)
    screen.addstr(x+4, y, f"└─────┘", color)
    return x + 5

def Main(stdscr):
    try:
        view = View(stdscr)
        view.connect()
    except Exception as e:
        raise e  # Re-raise exceptions to ensure proper cleanup
    finally:
        curses.endwin()  # Restore terminal to normal state

if __name__ == "__main__":
    curses.wrapper(Main)
