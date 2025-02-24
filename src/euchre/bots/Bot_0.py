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

    def all(self, snap: Snapshot) -> Query_Result:
        options: List[Card] = []
        suits: List[str] = Card.suits # new copy provided on each call
        suits.remove(snap.down_card.suit)

        for card in snap.hand:
            if card.suit in suits: 
                options.append(card)

        qr: Query_Result = Query_Result(self)
        qr.extend([random.choice(options)])
        return qr    

class Random_Suit(Query_Base):
    def __init__(self, name: str = "random suit") -> None:
        super().__init__(name)

    def all(self, snap: Snapshot) -> Query_Result:
        suits: List[str] = Card.suits # new copy provided on each call
        suits.remove(snap.down_card.suit)
        random_suit: str = random.choice(suits)
        qr: Query_Result = Query_Result(self)

        qr.extend([Card(snap.deck, random_suit, "A")])
        return qr        

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
        self.queries["state_4"].append(Default_Suit().do("make"))
        self.queries["state_4"].append(Random_Suit().do("make"))
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
        (action, result) = self.decide_state(state, snap)

        if not isinstance(action, str): 
            raise TypeError(f"{type(action)}")

        if len(result) == 0: 
            raise Exception("Result must contain at least one card.")

        # For states 3 and 4, we assume result.get() returns a Card, and we return its suit.
        if snap.current_state in [3, 4]:
            return (action, result.get().suit)
        else:
            return (action, result.get())

    def decide_state(self, state: str, snap: Snapshot) -> Tuple[str, Query_Result]:
        try:
            self.state_counts[state] += 1

            for query in self.queries[state]:
                self.last_query = query
                result: Query_Result = query.all(snap)

                if not isinstance(result, Query_Result): 
                    raise TypeError(f"Expected Query_Result found {type(result).__name__}")
                
                if len(result) > 0:
                    return (query.action, result)
                
        except Exception as e:
            # Here, `query` is expected to be defined in the loop;
            # if not, you might want to adjust the error handling.
            raise Query_Exception(query, e) from e

        raise Exception("Sanity check failed, last query must return a result.")
