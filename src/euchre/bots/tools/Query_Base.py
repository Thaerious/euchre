from euchre.Snapshot import Snapshot

class Stats:
    call_count = 0 # the number of times this query was invoked
    activated = 0 # the number of times a non-empty result was returned

    def __str__(self):
        if self.call_count == 0: return "NaN"
        return f" - {(self.activated / self.call_count * 100):.1f}%"

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
        return f"'{self.name}'"
    
    def __repr__(self):
        return f"'{self.name}'"    
    
    def all(self, _snap: Snapshot):
        raise NotImplemented
    
    def playable(self, snap):
        return self.all(snap).playable(snap)