from euchre.card.Card import Card
from euchre import Snapshot
import random

class Bot:
    def decide(self, snap: Snapshot):
        method_name = f"state_{snap.state}"
        method = getattr(self, method_name)
        return method(snap)

    def state_1(self, snap):
        if snap.hand.count_suit(snap.trump, snap.trump) > 3:
            return ("order", None)

        options = ["pass", "order", "alone"]
        random_item = random.choice(options)
        return (random_item, None)

    def state_2(self, snap):
        pass

    def state_3(self, snap):
        pass

    def state_4(self, snap):
        pass

    def state_5(self, snap):
        pass

