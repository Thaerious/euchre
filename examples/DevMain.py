from euchre.bots.evals.CountSuitInHand import CountSuitInHand
from euchre.Euchre import Hand
from types import SimpleNamespace

rulepart = CountSuitInHand()
rulepart.genotype["suit"] = "♠"
rulepart.genotype["operator"] = "="
rulepart.genotype["count"] = 0

snap = SimpleNamespace()
snap.cards = Hand(["9♣", "K♣", "Q♥", "Q♣"])

print(rulepart.genotype)
print(rulepart.evaluate(snap))
