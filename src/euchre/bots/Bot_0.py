from typing import List, Dict, Optional, Tuple
from euchre.card import Card
from euchre import Snapshot
from .tools.Query import Query
from .tools.Query_Exception import Query_Exception
from .tools.Query_Base import Query_Base
from .tools.Query_Result import Query_Result
import random

# ["♠", "♥", "♣", "♦"]

class Default_Suit(Query_Base):
    def __init__(self, name: str = "default suit") -> None:
        super().__init__(name)

    def all(self, snap: Snapshot):
        down_suit = snap.down_card.suit
        down_suit_index = Card.suits.index(down_suit)
        next_suit_index = (down_suit_index + 1) % 4
        return ("make", Card.suits[next_suit_index])

class Bot_0:
    def __init__(self, queries: Optional[Dict[str, List[Query]]] = {}) -> None:
        self.last_query: Optional[Query] = None

        self.state_counts: Dict[str, int] = {f"state_{i}": 0 for i in range(1, 6)}
        # Initialize queries for each state as an empty list.
        self.queries: Dict[str, List[Query]] = {f"state_{i}": [] for i in range(1, 6)}
        self.append(queries)

        # Build default queries for each state.
        self.queries["state_1"].append(Query('~', 'default state 1').do("pass"))
        self.queries["state_2"].append(Query('~', 'default state 2').do("down"))
        self.queries["state_3"].append(Query('~', 'default state 3 ').do("pass"))
        self.queries["state_4"].append(Default_Suit())
        self.queries["state_5"].append(Query('~', 'default state 5').playable().do("play"))

    def print_stats(self) -> None:
        for state in self.queries:
            print(f"{state}: {self.state_counts[state]}")
            for query in self.queries[state]:
                query.stats.state_count = self.state_counts[state]
                name = str(query)[:10].ljust(10, '.')
                print(f"  {name}: {query.stats}")

    def score(self, value: int) -> None:
        for state in self.queries:
            for query in self.queries[state]:   
                query.stats.score(value)

    def append(self, queries: Dict[str, List[Query]]) -> None:        
        for i in range(1, 6):
            s: str = f"state_{i}"
            if s in queries:
                q: List[Query] = queries[s].copy()
                self.queries[s].extend(q)                

        for query in self.queries["state_5"]:
            query.playable()

    def prepend(self, queries: Dict[str, List[Query]]) -> None:        
        for i in range(1, 6):
            s: str = f"state_{i}"
            if s in queries:
                q: List[Query] = queries[s].copy()
                self.queries[s][:0] = q                

        for query in self.queries["state_5"]:
            query.playable()            

    def decide(self, snap: Snapshot) -> Tuple[str, object]:
        """
        Returns a tuple of action and either a Card or a suit (str) depending on state.
        """
        self.last_query = None
        state: str = f"state_{snap.current_state}"
        (action, data) = self.decide_state(state, snap)

        if snap.current_state in [3, 4]:
            if isinstance(data, Card):
                data = data.suit

        return (action, data)

    # query each result for the state, return the first one that doesn't result in "skip"
    def decide_state(self, state: str, snap: Snapshot) -> Tuple[str, Query_Result]:
        self.state_counts[state] += 1

        for query in self.queries[state]:
            self.last_query = query            
            (action, data) = query.all(snap)
            if action != "skip": return (action, data)

        raise Exception(f"Sanity check failed, last query ({self.last_query.name}) must return a valid result ({action}).")
