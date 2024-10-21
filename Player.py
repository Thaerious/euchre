from delString import delString

class Team:
    def __init__(this, player1, player2):
        this.player1 = player1
        this.player2 = player2
        this.score = 0
        this.otherTeam = None

    def tricks(this):
        return this.player1.tricks + this.player2.tricks

    def isAlone(this):
        return this.player1.alone | this.player2.alone

class Player:
    def __init__(this, name):
        this.name = name        
        this.partner = None
        this.team = None
        this.clear()             

    def clear(this):
        this.cards = []
        this.played = [] # cards played in the current trick
        this.tricks = 0
        this.alone = False   

    def copy(this):
        newPlayer = Player(this.name)
        for card in this.cards:
            newPlayer.cards.append(card)

        return newPlayer

    def __str__(this):     
        sb = this.name + "[" + delString(this.cards) + "]"
        if (this.alone): sb = sb + "A"
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

        this[0].team = Team(this[0], this[2])
        this[2].team = this[0].team
        this[1].team = Team(this[1], this[3])
        this[3].team = this[1].team

        this[0].team.otherTeam = this[1].team
        this[1].team.otherTeam = this[0].team

    def copy(this):
        copiedList = PlayerList()
        for player in this: copiedList.append(player)
        return copiedList 

    def clear(this):
        for player in this: player.clear()

    # Move the first player to the end
    # Repeate unil the first player is the player specified as 'player'.
    def rotate(this, player = None):
        print(f"Rotate {str(player)}")

        this.append(this.pop(0))
        if player == None: return

        while this[0] != player:
            this.append(this.pop(0))

    def nextPlayer(this, afterThis, circular = False):
        returnNext = False

        for player in this:
            if returnNext: return player
            if player == afterThis: returnNext = True

        if circular: return this[0]
        else: return None

    def __str__(this):     
        names = []
        for player in this: names.append(player.name)
        return "[" + delString(names) + "]"
