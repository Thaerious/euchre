from euchre.card.Card import Card
import random

class Bot:
    def decide(self, snap):
        method_name = f"state_{snap.state}"
        method = getattr(self, method_name)
        method(snap)

    def state_1(self, snap):
        options = ["pass", "order", "alone"]
        random_item = random.choice(options)
        return random_item, None

    def state_2(self, snap):
        pass

    def state_3(self, snap):
        pass

    def state_4(self, snap):
        pass

    def state_5(self, snap):
        pass

