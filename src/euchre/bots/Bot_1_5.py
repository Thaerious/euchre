from euchre.card import *
from euchre import Snapshot
from .tools.Query import Query
from .Bot_0 import Bot_0
from .Bot_1 import Bot_1
from .tools.Query_Base import Query_Base
from .tools.Query_Collection import Query_Collection
from .tools.Query import normalize_value

# ["♠", "♥", "♣", "♦"]

def report_query(query, snap: Snapshot, result):
        print(snap.current_player.name, snap.seed, snap.hand_count)

class Bot_1_5(Bot_1):
    def setup(self):
        super().setup()

        self.prepend({
            "state_1":[
                Query("J♥ J♦ A♥").up_card("♥").count("3").do("order").hook("on_match", report_query),
                Query("J♦ J♥ A♦").up_card("♦").count("3").do("order"),
                Query("J♣ J♠ A♣").up_card("♣").count("3").do("order"),
                Query("J♠ J♣ A♠").up_card("♠").count("3").do("order"),
            ],
            "state_2":[
                Query("910JQK♥").count("1").worst().do("up"),
                Query("~♠ 910JQK").count("12345").worst().do("up"),                  
            ],
            "state_3":[],
            "state_4":[],
            "state_5":[],
        })