from euchre.card import *
from euchre import Snapshot
from .tools.Query import Query
from .tools.Query_Base import Query_Base
from .tools.Query_Result import Query_Result
import random

# ["♠", "♥", "♣", "♦"]

class Default_Suit(Query_Base):
    name = "default"

    def all(self, snap: Snapshot):
        options = []
        for card in snap.hand:
            if not card.suit in options: 
                options.append(card.suit)

        if snap.down_card.suit in options:
            options.remove(snap.down_card.suit)
        
        #todo what happens if they only have the turned down suit?
        return Query_Result([random.choice(options)])        

class Stat:
    call_count = 0 # the number of times this query was invoked
    activated = 0 # the number of times a non-empty result was returned

    def __str__(self):
        return f" - {(self.activated / self.call_count * 100):.1f}%"

class Bot_0:
    def print_stats(self):
        for state in self.queries:
            print(f"{state}: {self.state_counts[state]}")
            for pair in self.queries[state]:
                query = pair[0]
                percent_activated = 0 

                if self.state_counts[state] != 0:
                    percent_activated = self.stats[query].activated / self.state_counts[state] * 100

                print(f" - {query} {percent_activated:.1f}")

    def __init__(self, queries = None):
        self.trick_count = 0

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

        self.stats: list[Stat] = {
            # Query -> Stat dictionary
        }

        if queries is not None:
            self.queries["state_1"].extend(queries["state_1"])
            self.queries["state_2"].extend(queries["state_2"])
            self.queries["state_3"].extend(queries["state_3"])
            self.queries["state_4"].extend(queries["state_4"])
            self.queries["state_5"].extend(queries["state_5"])           

        self.queries["state_1"].append((Query('~', 'default'), "pass"))
        self.queries["state_2"].append((Query('~', 'default'), "down"))
        self.queries["state_3"].append((Query('~', 'default'), "pass"))
        self.queries["state_4"].append((Default_Suit(), "make"))
        self.queries["state_5"].append((Query('~', 'default'), "play"))

        for state in self.queries:
            for query in self.queries[state]:
                self.stats[query[0]] = Stat()

    def decide(self, snap: Snapshot):
        method_name = f"state_{snap.state}"
        method = getattr(self, method_name)
        return method(snap)

    def do_state(self, state, snap, eval):
        self.state_counts[state] += 1

        for query in self.queries[state]:
            self.stats[query[0]].call_count += 1
            
            result = eval(query[0]).get()

            if result is not None:
                self.stats[query[0]].activated += 1
                return (query[1], result)  

        raise Exception("Sanity check failed")

    def state_1(self, snap): # pass / order / alone  
        return self.do_state("state_1", snap, lambda q: q.all(snap))

    def state_2(self, snap): # dealer up / down
        return self.do_state("state_2", snap, lambda q: q.all(snap))

    def state_3(self, snap): # pass / make / alone
        return self.do_state("state_3", snap, lambda q: q.all(snap))

    def state_4(self, snap): # Dealer make / alone
        return self.do_state("state_4", snap, lambda q: q.all(snap))

    def state_5(self, snap):        
        return self.do_state("state_5", snap, lambda q: q.playable().all(snap))        
