from .RulePart import RulePart

class CountTrumpInHand(RulePart):
    def __init__(this):
        super().__init__()

        this.alleles = {
            "operator" : ["=", "<", ">", "!=", "<=", ">="],
            "count": [0, 1, 2, 3, 4, 5]
        }

    def evaluate(this, snap):
        count = 0
        for card in snap.cards:
            if card.suit == snap.trump: 
                count = count + 1

        if this.genotype["operator"] == "=": return count == this.genotype["count"]
        if this.genotype["operator"] == ">": return count > this.genotype["count"]
        if this.genotype["operator"] == "<": return count < this.genotype["count"]
        if this.genotype["operator"] == "!=": return count != this.genotype["count"]
        if this.genotype["operator"] == "<=": return count <= this.genotype["count"]
        if this.genotype["operator"] == ">=": return count >= this.genotype["count"]
