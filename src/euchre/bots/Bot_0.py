from typing import List, Dict, Optional, Tuple
from euchre.card import Card
from euchre import Snapshot
from .tools.Query import Query
from .tools.Query_Result import Query_Result
from .tools.Query_Exception import Query_Exception
from .tools.Query_Base import Query_Base
from .tools.Query_Collection import Query_Collection

# ["♠", "♥", "♣", "♦"]

class Default_Suit(Query_Base):
    def __init__(self, name: str = "default 4") -> None:
        super().__init__(name)

    def decide(self, snap: Snapshot):
        down_suit = snap.down_card.suit
        down_suit_index = Card.suits.index(down_suit)
        next_suit_index = (down_suit_index + 1) % 4
        return Query_Result("make", Card.suits[next_suit_index], Query_Collection(snap.hand), "default")

class Bot_0:
    def __init__(self) -> None:
        self.last_query = None
        self.state_counts: Dict[str, int] = {f"state_{i}": 0 for i in range(1, 6)}

        # Initialize queries for each state as an empty list.
        self.queries: Dict[str, List[Query]] = {f"state_{i}": [] for i in range(1, 6)} 
        self.setup()       

    def setup(self):
        self.prepend({
            "state_1":[Query('~', 'default 1').do("pass")],
            "state_2":[Query('~', 'default 2').do("down")],
            "state_3":[Query('~', 'default 3').do("pass")],
            "state_4":[Default_Suit()],
            "state_5":[Query('~', 'default 5').playable().do("play")],
        })

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
                q = queries[s]
                self.queries[s].extend(q)

        for query in self.queries["state_5"]:
            query.playable()

    def prepend(self, queries: Dict[str, List[Query]]) -> None:        
        for i in range(1, 6):
            s: str = f"state_{i}"
            if s in queries:
                q = queries[s].copy()
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

    # query each result for the state, return the first one that doesn't result in rejected or no action
    def decide_state(self, state: str, snap: Snapshot) -> Tuple[str, Query_Collection]:
        self.state_counts[state] += 1

        for query in self.queries[state]:
            self.last_query = query            
            query_result = query.decide(snap)
            if query_result.action == "rejected": continue
            if query_result.action == "no action": continue
            return (query_result.action, query_result.data)

        raise Exception(f"Sanity check failed, last query ({self.last_query.name}) must return a valid result ({action}).")
