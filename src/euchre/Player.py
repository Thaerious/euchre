from euchre.del_string import del_string
from euchre.card import *

class Player:
    def __init__(self, name, index):
        self.name = name        
        self.partner = None
        self.index = index
        self.clear()             

    def clear(self):
        self.cards = Hand()
        self.played = [] # cards self player has played in the current trick
        self.tricks = 0
        self.alone = False   

    def copy(self):
        newPlayer = Player(self.name)
        for card in self.cards:
            newPlayer.cards.append(card)

        return newPlayer

    def __str__(self):     
        sb = f"{self.name}[{del_string(self.cards)}][{del_string(self.played)}] {self.tricks}"
        return sb

class PlayerList(list):
    def __init__(self, names = []):
        if (len(names) != 4): return

        for i, name in enumerate(names):
            self.append(Player(name, i))

        self[0].partner = self[2]
        self[1].partner = self[3]
        self[2].partner = self[0]
        self[3].partner = self[1]

    def get_player(self, name):
        for player in self:
            if player.name == name: return player

        return None

    def copy(self):
        copiedList = PlayerList()
        for player in self: copiedList.append(player)
        return copiedList 

    def clear(self):
        for player in self: player.clear()

    # Move the first player to the end
    # Repeat until the first player is the player specified as 'player'.
    def rotate(self, player = None):
        self.append(self.pop(0))
        if player == None: return

        while self[0] != player:
            self.append(self.pop(0))

    # Return the next next player in self list
    # If there is no next player, returns None
    def activate_next_player(self, afterThis):
        returnNext = False

        for player in self:
            if returnNext: return player
            if player == afterself: returnNext = True

        return None

    def __str__(self):     
        names = []
        for player in self: names.append(player.name)
        return f"[{del_string(names)}]"
