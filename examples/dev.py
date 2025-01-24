from euchre import Game, Snapshot
from euchre.bots import Bot
from euchre.card import *
from euchre.class_getter import *

class Snafu:

    @class_getter
    def hello():
        print("Hello method invoked")

Snafu.hello

