from euchre import Game, Snapshot
from euchre.bots import Bot
from euchre.card import *
from euchre.class_getter import *
import json

deck = Deck()
card = deck[0]

print(card)

def custom_json_serializer(obj):
    """ Custom JSON serializer that looks for __json__() """
    if hasattr(obj, "__json__"):
        return obj.__json__()  # Call __json__() if it exists
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

print(json.dumps(deck, default = custom_json_serializer))