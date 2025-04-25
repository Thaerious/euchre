# Player.py
from euchre.card import Hand
from euchre.del_string import del_string


class Team:
    def __init__(self, players):
        self._players = players
        self._score = 0

    def __str__(self):
        return del_string([p.name for p in self._players])

    def __repr__(self):
        return del_string([p.name for p in self._players])

    @property
    def is_alone(self):
        for player in self._players:
            if player.alone:
                return True
        return False

    @property
    def tricks(self):
        tricks = 0
        for player in self._players:
            tricks = tricks + player.tricks
        return tricks

    @property
    def players(self):
        return self._players.copy()

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

class Player:
    def __init__(self, name, index):
        self.name = name
        self.partner = None
        self.index = index
        self.team = None
        self.clear()

    def __json__(self):
        return {
            "name": self.name,
            "tricks": self.tricks,
            "played": self.played,
            "hand": self.hand,
            "alone": self.alone,
        }

    def clear(self):
        self.hand = Hand()
        self.played = []  # cards self player has played in the current trick
        self.tricks = 0
        self.alone = False

    def copy(self):
        new_player = Player(self.name)
        for card in self.hand:
            new_player.hand.append(card)

        return new_player

    def __str__(self):
        sb = f"({self.name}, {del_string(self.hand)}, [{del_string(self.played)}], T{self.tricks})"
        return sb

class PlayerList(list):
    def __init__(self, names=[]):
        if len(names) != 4:
            return

        for i, name in enumerate(names):
            self.append(Player(name, i))

        self[0].partner = self[2]
        self[1].partner = self[3]
        self[2].partner = self[0]
        self[3].partner = self[1]

    def get_player(self, name):
        for player in self:
            if player.name == name:
                return player

        return None

    def copy(self):
        copied_list = PlayerList()
        for player in self:
            copied_list.append(player)
        return copied_list

    def clear(self):
        for player in self:
            player.clear()

    # Move the first player to the end
    # Repeat until the first player is the player specified as 'player'.
    def rotate(self, player=None):
        self.append(self.pop(0))
        if player is None:
            return

        while self[0] != player:
            self.append(self.pop(0))

    # Return the next next player in self list
    # If there is no next player, returns None
    def activate_next_player(self, after_this):
        return_next = False

        for player in self:
            if return_next:
                return player
            if player == after_this:
                return_next = True

        return None

    def __str__(self):
        names = []
        for player in self:
            names.append(player.name)
        return f"[{del_string(names)}]"
