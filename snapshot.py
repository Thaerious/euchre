def snapshot(game, forPlayer):
    primitive_types = (int, float, str, bool, type(None), bytes)
    snap = {}

    snap["state"] = game.state.__name__
    snap["forPlayer"] = forPlayer.name
    snap["activePlayer"] = game.activePlayer.name if game.activePlayer != None else ""
    snap["upcard"] = str(game.euchre.upcard)
    snap["trump"] = game.euchre.trump
    snap["maker"] = game.euchre.maker.name
    snap["dealer"] = game.euchre.dealer().name

    if forPlayer == game.euchre.dealer():
        snap["downcard"] = str(game.euchre.downcard)
    else:
        snap["downcard"] = None

    snap["players"] = []
    for player in game.euchre.players: 
        snap["players"].append(player.name)

    snap["playing"] = []
    for player in game.euchre.playing: 
        snap["playing"].append(player.name)

    snap["cards"] = []
    for card in forPlayer.cards: 
        snap["cards"].append(str(card))

    return snap