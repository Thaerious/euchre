from euchre.delString import delString
import Card

class CardList(list):
    def __init__(self, stringList = []):
        for string in stringList:
            self.append(Card(string))

    def randomItem(self):
        if len(self) == 0: return None
        index = random.randint(0, len(self)) - 1
        return self[index]     

    def __str__(self):
        return delString(self)