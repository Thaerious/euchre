from euchre.Card import Card
import random

class Bot:
    def decide(this, snap):
        print(snap)
        this.snap = snap
        getattr(this, f"state{snap.state}")()

    def state1(this):
        print("State 1")

    def state2(this):
        print("State 2")

    def state3(this):
        print("State 3")

    def state4(this):
        print("State 4")

    def state5(this):
        print("State 5")

