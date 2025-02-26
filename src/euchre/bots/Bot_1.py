from euchre.card import *
from euchre import Snapshot
from .tools.Query import Query
from .Bot_0 import Bot_0
from .tools.Query_Base import Query_Base
from .tools.Query_Collection import Query_Collection

# ["♠", "♥", "♣", "♦"]

class Print_Query(Query_Base):
    name = "print"

    def decide(self, snap: Snapshot):
        print(snap)
        return Query_Collection([]) 

class Bot_1(Bot_0):
    def setup(self):
        super().setup()

        self.prepend({
            "state_1":[],
            "state_2":[],
            "state_3":[],
            "state_4":[],
            "state_5":[
                Query("~", "beats").lead("123").wins().worst().do("play"),
                Query("~", "loses").lead("123").loses().worst().do("play"),            
                Query("♥").lead("0").best().do("play"),
                Query("♦").lead("0").best().do("play"),
                Query("♣").lead("0").best().do("play"),
                Query("♠").lead("0").best().do("play"),
            ],
        })