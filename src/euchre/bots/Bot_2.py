from euchre.card import *
from .tools.Query import Query
from .Bot_0 import Bot_0
from typing import List, Dict, Optional, Tuple

# ["♠", "♥", "♣", "♦"]

def report_query(query, snap, all):
    print(query, snap.up_card, f"[{snap.hand}]", all)

#.register_hook("after", report_query)

class Bot_2(Bot_0):
    queries = {
        "state_1":[
            Query("♥", name="RB♥").up_card("J♥").dealer("02").count("2345").do("order"),
            Query("♦", name="RB♦").up_card("J♦").dealer("02").count("2345").do("order"),
            Query("♣", name="RB♣").up_card("J♣").dealer("02").count("2345").do("order"),
            Query("♠", name="RB♠").up_card("J♠").dealer("02").count("2345").do("order"),
            Query("♥", name="♥>2").up_card("♥").count("345").do("order"),
            Query("♦", name="♦>2").up_card("♦").count("345").do("order"),
            Query("♣", name="♣>2").up_card("♣").count("345").do("order"),
            Query("♠", name="♠>2").up_card("♠").count("345").do("order"),
            Query("J♥ J♦ A♥").up_card("♥").count("23").do("order"),
            Query("J♦ J♥ A♦").up_card("♦").count("23").do("order"),
            Query("J♣ J♠ A♣").up_card("♣").count("23").do("order"),
            Query("J♠ J♣ A♠").up_card("♠").count("23").do("order"),             
        ],
        "state_2":[
            Query("910JQK♥").count("1").worst().do("up"),
            Query("~♠ 910JQK").count("12345").worst().do("up"),
        ],
        "state_3":[
            Query("~♥").down_card("♥").count("5").do("make"),
            Query("~♦").down_card("♦").count("5").do("make"),
            Query("~♣").down_card("♣").count("5").do("make"),
            Query("~♠").down_card("♠").count("5").do("make"),
        ],
        "state_4":[
            Query("~♥").down_card("♥").count("345").do("make"),
            Query("~♦").down_card("♦").count("345").do("make"),
            Query("~♣").down_card("♣").count("345").do("make"),
            Query("~♠").down_card("♠").count("345").do("make"),
        ],
        "state_5":[
            Query("~", "beats").lead("123").wins().worst().do("play"),
            Query("~", "loses").lead("123").loses().worst().do("play"),            
            Query("♥", name="play ♥").lead("0").best().do("play"),
            Query("♦", name="play ♦").lead("0").best().do("play"),
            Query("♣", name="play ♣").lead("0").best().do("play"),
            Query("♠", name="play ♠").lead("0").best().do("play"),
        ],
    }     

    def __init__(self, queries: Optional[Dict[str, List[Query]]] = {}):
        super().__init__(Bot_2.queries)
