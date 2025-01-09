from euchre.delString import delString
from euchre.Card import Card, CardList, Hand    

class Player:
    def __init__(this, name):
        this.name = name        
        this.partner = None
        this.clear()             

    def clear(this):
        this.cards = Hand()
        this.played = CardList() # cards this player has played in the current trick
        this.tricks = 0
        this.alone = False   

    def copy(this):
        newPlayer = Player(this.name)
        for card in this.cards:
            newPlayer.cards.append(card)

        return newPlayer

    def __str__(this):     
        sb = f"{this.name}[{delString(this.cards)}][{delString(this.played)}] {this.tricks}"
        return sb

class PlayerList(list):
    def __init__(this, names = []):
        if (len(names) != 4): return

        for name in names:
            this.append(Player(name))

        this[0].partner = this[2]
        this[1].partner = this[3]
        this[2].partner = this[0]
        this[3].partner = this[1]

    def get_player(this, name):
        for player in this:
            if player.name == name: return player

        return None

    def copy(this):
        copiedList = PlayerList()
        for player in this: copiedList.append(player)
        return copiedList 

    def clear(this):
        for player in this: player.clear()

    # Move the first player to the end
    # Repeat until the first player is the player specified as 'player'.
    def rotate(this, player = None):
        this.append(this.pop(0))
        if player == None: return

        while this[0] != player:
            this.append(this.pop(0))

    # Return the next next player in this list
    # If there is no next player, returns None
    def activate_next_player(this, afterThis):
        returnNext = False

        for player in this:
            if returnNext: return player
            if player == afterthis: returnNext = True

        return None

    def __str__(this):     
        names = []
        for player in this: names.append(player.name)
        return f"[{delString(names)}]"
