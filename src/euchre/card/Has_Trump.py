from euchre.card.Card import Card
from cffi import FFI

class Has_Trump():
    def __init__(self):
        self.ffi = FFI()
        self.trump_ptr = self.ffi.new("int *", 0)

    @property
    def trump(self):
        i = self.trump_ptr[0]
        if i == -1: return None
        return Card.suits[i]

    @trump.setter
    def trump(self, trump):
        if trump is None:
            self.trump_ptr = self.ffi.new("int *", -1)
        else:
            i = Card.suits.index(trump)
            self.trump_ptr = self.ffi.new("int *", i)