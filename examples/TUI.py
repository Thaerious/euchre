from euchre import *
from euchre.Card import Hand
import curses
import random



class View:
    def __init__(this, stdscr, server):
        this.stdscr = stdscr
        this.server = server

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
            this.mock.input(None, "start", None)

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

    def printUpCard(this, snap):
        printCard(this.stdscr, 5, 10, snap.upCard)
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
    server = MockServer()
    view = View(stdscr, server)
    server.addAgent("Adam", view)
    view.start()

if __name__ == "__main__":
    curses.wrapper(Main)