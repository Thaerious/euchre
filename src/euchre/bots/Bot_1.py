from euchre.card import *
from euchre import Snapshot
from .tools.Query import Query
from .Bot_0 import Bot_0
from .tools.Query_Base import Query_Base
from .tools.Query_Result import Query_Result

import random

# ["♠", "♥", "♣", "♦"]

class Print_Query(Query_Base):
    name = "print"

    def all(self, snap: Snapshot):
        print(snap)    
        return Query_Result([]) 

class Bot_1(Bot_0):
    queries = {
        "state_1":[],
        "state_2":[],
        "state_3":[],
        "state_4":[],
        "state_5":[
            (Query("♥").lead("0").best(), "play"),
            (Query("♦").lead("0").best(), "play"),
            (Query("♣").lead("0").best(), "play"),
            (Query("♠").lead("0").best(), "play"),
            (Query("~", "beats").lead("123").beats().worst(), "play"),
            (Print_Query(), "play"),
            (Query("~", "loses").lead("123"), "play"),
        ],
    }     

    def __init__(self):
        super().__init__(Bot_1.queries)
