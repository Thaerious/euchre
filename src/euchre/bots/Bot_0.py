from euchre.card import *
from euchre import Snapshot
from .tools.Query import Query
from .tools.Query_Exception import Query_Exception
from .tools.Query_Base import Query_Base
from .tools.Query_Result import Query_Result
import random

# ["♠", "♥", "♣", "♦"]

class Default_Suit(Query_Base):
    def __init__(self, name="default suit"):
        super().__init__(name)

    def all(self, snap: Snapshot):
        options = []
        suits = Card.suits
        suits.remove(snap.down_card.suit)

        for card in snap.hand:
            if card.suit in suits: 
                options.append(card)

        qr = Query_Result(self)
        qr.extend([random.choice(options)])
        return qr    

class Random_Suit(Query_Base):
    def __init__(self, name="random suit"):
        super().__init__(name)

    def all(self, snap: Snapshot):
        suits = Card.suits
        suits.remove(snap.down_card.suit)
        random_suit = random.choice(suits)
        qr = Query_Result(self)
        qr.extend([Card(snap.deck, random_suit, "A")])
        return qr        

class Bot_0:
    def print_stats(self):
        for state in self.queries:
            print(f"{state}: {self.state_counts[state]}")
            for query in self.queries[state]:
                percent_activated = 0 

                if self.state_counts[state] != 0:
                    percent_activated = query.stats.activated / self.state_counts[state] * 100

                print(f" - {query}: {percent_activated:.1f}")

    def __init__(self, queries: list[Query] = []):
        self.trick_count = 0
        self.last_query = None

        self.state_counts = {f"state_{i}": 0 for i in range(1,6)}
        self.queries = {f"state_{i}": [] for i in range(1,6)}
        self.append(queries)

        self.queries["state_1"].append(Query('~', 'default state 1').do("pass"))
        self.queries["state_2"].append(Query('~', 'default state 2').do("down"))
        self.queries["state_3"].append(Query('~', 'default state 3 ').do("pass"))
        self.queries["state_4"].append(Default_Suit().do("make"))
        self.queries["state_4"].append(Random_Suit().do("make"))
        self.queries["state_5"].append(Query('~', 'default state 5').playable().do("play"))

    def append(self, queries: list[Query] = []):
        for i in range(1, 6):
            s = f"state_{i}"
            if s in queries:
                q = queries[s].copy()
                self.queries[s].extend(q)

        for query in self.queries["state_5"]:
            query.playable()

    def decide(self, snap: Snapshot):
        self.last_query = None
        state = f"state_{snap.current_state}"
        (action, result) = self.decide_state(state, snap)

        if not isinstance(action, str): 
            raise TypeError(f"{type(action)}")

        if len(result) == 0: 
            raise Exception("Result must contain at least one card.")

        if snap.current_state in [3, 4]:
            return (action, result.get().suit)
        else:
            return (action, result.get())

    def decide_state(self, state, snap):
        try:
            self.state_counts[state] += 1

            for query in(self.queries[state]):
                self.last_query = query
                result = query.all(snap)

                if not isinstance(result, Query_Result): 
                    raise TypeError(f"Expected Query_Result found {type(result).__name__}")
                
                if len(result) > 0:
                    return (query.action, result)
                
        except Exception as e:
            raise Query_Exception(query, e) from e            

        raise Exception("Sanity check failed, last query must return a result.") 
