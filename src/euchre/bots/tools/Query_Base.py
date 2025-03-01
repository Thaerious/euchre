from euchre.Snapshot import Snapshot

class Query_Stats:
    _call_count = 0          # the number of times this query was invoked
    _activated = 0           # the number of times a non-empty result was returned
    _wins = 0                # the number of times a positive score was recorded when activated
    _flag_activation = False # set when activated, clear when scored
    _score = 0               # add winning scores, subtract losing scores
    _state_count = 0         # the number of times the state this query belongs to was invoked

    @property
    def state_count(self):
        return self._state_count

    @state_count.setter
    def state_count(self, value):
        self._state_count = value

    def called(self):
        self._call_count += 1

    def activate(self):
        self._activated += 1
        self._flag_activation = True

    def score(self, value):
        if self._flag_activation: 
            self._score = self._score + value
            if value > 0: self._wins += 1

        self._flag_activation = False            

    def __str__(self):
        pct_activated = 0.0
        if self.state_count != 0:
            pct_activated = self._activated / self.state_count * 100

        points_per_activation = 0.0
        if self._activated != 0:
            points_per_activation = self._score / self._activated

        pct_wins = 0.0
        if self._activated != 0:
            pct_wins = self._wins / self._activated * 100

        return f"{pct_activated:.1f} {self._activated} {self._wins} {pct_wins:.1f}"

class Query_Base:
    def __init__(self, name):
        self.name = name
        self._stats = Query_Stats()
        self._action = "no_action"
        self._data = None

    @property
    def stats(self):
        return self._stats

    @property
    def action(self):
        return self._action
    
    @property
    def data(self):
        return self._data

    def do(self, action, data = None):  
        if not isinstance(action, str): raise TypeError(f"Expected str, found {type(action)}")
        self._action = action
        self._data = data
        return self

    def __str__(self):
        return f"{self.name}"
    
    def __repr__(self):
        return f"{self.name}"    
    
    def decide(self, _snap: Snapshot):
        raise NotImplemented
    
    def playable(self, snap):
        return self.decide(snap).playable(snap)