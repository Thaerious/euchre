# HasTrump.py
class HasTrump:
    def __init__(self):
        self._trump = None

    @property
    def trump(self):
        return self._trump

    @trump.setter
    def trump(self, trump):
        self._trump = trump
