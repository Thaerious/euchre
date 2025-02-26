

class Query_Result():
    def __init__(self, action, data, collection):
        self.action = action
        self.data = data
        self.all = collection

    def __str__(self):
        return f"QueryResult({self.action}, {self.data}, {self.all})"
    
    def __repr__(self):
        return str(self)