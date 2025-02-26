from euchre.card import *
from euchre import Snapshot
from .tools.Query import Query
from .Bot_0 import Bot_0
from .tools.Query_Base import Query_Base
from .tools.Query_Collection import Query_Collection

# ["♠", "♥", "♣", "♦"]

def report_query(query, snap: Snapshot, all = []):
    # print(f"{query}, {snap.tricks[-1]}:{snap.tricks[-1].best_card}, [{snap.hand}]:{snap.trump}, {all}")
    print(f"{query}, {snap.lead_index}:{snap.for_index}, [{snap.hand}]:{snap.trump}, {all}")

class Bot_1_5(Bot_0):
    def setup(self):
        super().setup()

        self.prepend({
            "state_1":[],
            "state_2":[],
            "state_3":[],
            "state_4":[],
            "state_5":[
                Query("~", "O-W").lead("123").winner("13").wins().best().do("play").register_hook("on_match", report_query),
                Query("~", "O-W").winner("13").wins().worst().do("play"),
                Query("~", "P-W").winner("2").link("910JQK♥").count("1").do("play"),
                Query("~", "P-W").winner("2").link("910JQK♦").count("1").do("play"),
                Query("~", "P-W").winner("2").link("910JQK♣").count("1").do("play"),
                Query("~", "P-W").winner("2").worst().do("play"),
                Query("~", "L").lead("123").loses().worst().do("play"),
                Query("♥").lead("0").best().do("play"),
                Query("♦").lead("0").best().do("play"),
                Query("♣").lead("0").best().do("play"),
                Query("♠").lead("0").best().do("play"),
            ],
        })