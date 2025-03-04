from euchre.card import *
from .tools.Query import Query
from .Bot_0 import Bot_0
from .Bot_2 import Bot_2

# ["♠", "♥", "♣", "♦"]

def report_query(query, snap, all = []):
    print(f"{query}, {snap.down_card}, [{snap.hand}]:{snap.trump}, {all}")

class Bot_3(Bot_0):
    def setup(self):
        super().setup()

        self.prepend({
            "state_1":[],
            "state_2":[],
            "state_3":[],
            "state_4":[],
            "state_5":[],
        })         
