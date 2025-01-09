from metrics.cohesionx import *

class Foo():
    def __init__(self):
        pass
    
    def method():
        pass

class Test():
    def __init__(self):
        self.l = []

    def size(self):
        len(self.l)

    def foo(self):
        self.l.append(0)

    def bar(self):
        self.foo = Foo()

