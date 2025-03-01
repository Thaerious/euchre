from euchre.card import *
from .tools.Query import Query
from .Bot_1 import Bot_1
from typing import List, Dict, Optional, Tuple

# ["♠", "♥", "♣", "♦"]

def report_query(query, snap, all):
    print(query, snap.up_card, f"[{snap.hand}]", all)

class Bot_2(Bot_1):
    def setup(self):
        super().setup()

        self.prepend({
            "state_1":[],
            "state_2":[],
            "state_3":[],
            "state_4":[],
            "state_5":[],
        })
