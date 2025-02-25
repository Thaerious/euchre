from euchre.Snapshot import Snapshot

class Stats:
    _call_count = 0 # the number of times this query was invoked
    _activated = 0 # the number of times a non-empty result was returned
    _flag_activation = False # set when activated, clear when scored
    _score = 0 # add winning scores, subtract losing scores
    _state_count = 0 # the number of times the state this query belongs to was invoked

    @property
    def state_count(self):
        return self._state_count

    @state_count.setter
    def state_count(self, value):
        self._state_count = value

    def called(self):
        self._call_count = self._call_count + 1

    def activate(self):
        self._activated = self._activated + 1
        self._flag_activation = True

    def score(self, value):
        if self._flag_activation: 
            self._score = self._score + value
        self._flag_activation = False            

    def __str__(self):
        pct_activated = 0.0
        if self.state_count != 0:
            pct_activated = self._activated / self.state_count * 100

        points_per_activation = 0.0
        if self._activated != 0:
            points_per_activation = self._score / self._activated

        return f"{self._activated} {pct_activated:.1f} {self._score} {points_per_activation:.2f}"

class Query_Base:
    def __init__(self, name):
        self.name = name
        self._stats = Stats()
        self._action = ""

    @property
    def stats(self):
        return self._stats

    @property
    def action(self):
        return self._action

    def do(self, value):  
        if not isinstance(value, str): raise TypeError(f"Expected str, found {type(value)}")
        self._action = value
        return self

    def __str__(self):
        return f"{self.name}"
    
    def __repr__(self):
        return f"{self.name}"    
    
    def all(self, _snap: Snapshot):
        raise NotImplemented
    
    def playable(self, snap):
        return self.all(snap).playable(snap)