from euchre.card import *
from euchre import Snapshot
from .tools.Query import Query
from .Bot_0 import Bot_0
from .tools.Query_Base import Query_Base
from .tools.Query_Result import Query_Result

# ["♠", "♥", "♣", "♦"]

class Print_Query(Query_Base):
    name = "print"

    def all(self, snap: Snapshot):
        snap = snap.normalize_order()
        print(snap)
        return Query_Result([]) 

class Bot_1(Bot_0):
    queries = {
        "state_1":[],
        "state_2":[],
        "state_3":[],
        "state_4":[],
        "state_5":[
            (Query("~", "beats").lead("123").wins().worst().do("play")),
            (Query("~", "loses").lead("123").loses().worst().do("play")),            
            (Query("♥").lead("0").best().do("play")),
            (Query("♦").lead("0").best().do("play")),
            (Query("♣").lead("0").best().do("play")),
            (Query("♠").lead("0").best().do("play")),
        ],
    }     

    def __init__(self):
        super().__init__(Bot_1.queries)
