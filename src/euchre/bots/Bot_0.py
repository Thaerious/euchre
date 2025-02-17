from euchre.card import *
from euchre import Snapshot
from .tools.Query import Query
from .tools.Query_Base import Query_Base
from .tools.Query_Result import Query_Result
import random

# ["♠", "♥", "♣", "♦"]

class Default_Suit(Query_Base):
    name = "default_suit"

    def all(self, snap: Snapshot):
        options = []
        suits = Card.suits
        suits.remove(snap.down_card.suit)

        for card in snap.hand:
            if card.suit in suits: 
                options.append(card)

        return Query_Result([random.choice(options)])

class Random_Suit(Query_Base):
    name = "random_suit"

    def all(self, snap: Snapshot):
        options = []
        suits = Card.suits
        suits.remove(snap.down_card.suit)
        random_suit = [random.choice(options)]
        return Card(snap.deck, f"A{random_suit}")

class Bot_0:
    def print_stats(self):
        for state in self.queries:
            print(f"{state}: {self.state_counts[state]}")
            for query in self.queries[state]:
                percent_activated = 0 

                if self.state_counts[state] != 0:
                    percent_activated = query.stats.activated / self.state_counts[state] * 100

                print(f" - {query} {percent_activated:.1f}")

    def __init__(self, queries: list[Query] = None):
        self.trick_count = 0
        self.last_query = None

        self.state_counts = {
            "state_1": 0,
            "state_2": 0,
            "state_3": 0,
            "state_4": 0,
            "state_5": 0,
        }

        self.queries = {
            "state_1": [],
            "state_2": [],
            "state_3": [],
            "state_4": [],
            "state_5": [],
        }

        if queries is not None:
            self.append(queries)

        self.queries["state_1"].append(Query('~', 'default').do("pass"))
        self.queries["state_2"].append(Query('~', 'default').do("down"))
        self.queries["state_3"].append(Query('~', 'default').do("pass"))
        self.queries["state_4"].append(Default_Suit().do("make"))
        self.queries["state_4"].append(Random_Suit().do("make"))
        self.queries["state_5"].append(Query('~', 'default').playable().do("play"))

    def append(self, queries: list[Query] = None):
        for i in range(1, 5):
            s = f"state_{i}"
            if s in queries:
                q = queries[s].copy()
                q.reverse()
                self.queries[s].extend(q)

        for query in self.queries["state_5"]:
            if query.action == "and": continue
            query.playable()

    def decide(self, snap: Snapshot):
        self.last_query = None
        state = f"state_{snap.current_state}"
        (action, result) = self.do_state(state, snap)

        if not isinstance(action, str): raise TypeError(f"{type(action)}")
        if len(result) == 0: raise Exception("Result must contain at least one card.")

        if snap.current_state in [3, 4]:
            return (action, result.get().suit)
        else:
            return (action, result.get())

    def do_state(self, state, snap):
        self.state_counts[state] += 1
        stack = self.queries[state].copy()

        while len(stack) > 0:
            query = stack.pop()
            self.last_query = query
            query.stats.call_count += 1
            result = query.all(snap)

            if len(result) == 0:
                while query.action == "and":
                    query = stack.pop()

            if len(result) > 0:
                query.stats.activated += 1
                if query.action == "and":
                    continue
                else:
                    return (query.action, result)

        raise Exception("Sanity check failed, last query must return a result.")