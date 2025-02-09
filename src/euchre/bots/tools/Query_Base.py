from euchre.Snapshot import Snapshot

class Query_Base:
    name = "N/A"

    def __str__(self):
        return f"[{self.name}]"
    
    def all(self, _snap: Snapshot):
        raise NotImplemented
    
    def playable(self, snap):
        return self.all(snap).playable(snap)