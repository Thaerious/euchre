from euchre.Card import Card
import random

class Bot:
    def decide(this, snap):
        print(snap)
        this.snap = snap
        getattr(this, f"state{snap.state}")()

    def state1(this):
        return ("pass", None)

    def state2(this):
        return ("down", None)

    def state3(this):
        return ("pass", None)

    def state4(this):
        return ("x", None)

    def state5(this):
        return ("x", None)

