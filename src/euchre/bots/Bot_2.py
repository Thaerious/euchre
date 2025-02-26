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
            "state_5":[],
        })
