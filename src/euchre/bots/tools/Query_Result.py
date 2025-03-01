

class Query_Result():
    def __init__(self, action, data, collection, reason):
        self.action = action
        self.data = data
        self.all = collection
        self.reason = reason

    def __str__(self):
        return f"QueryResult({self.action}, {self.data}, {self.all}, '{self.reason}')"
    
    def __repr__(self):
        return str(self)