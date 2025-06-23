import re
import sys
import ast
from euchre import Game
from FunctionStore import FunctionStore

class GameTester():
    def __init__(self):
        self.parts = []
        self.game = None
        self.current = None
        self.fstore = None

        self.data = {
            "players": [],
            "seed": None
        }

    def next(self) -> str:
        return self.current.pop(0)
    
    def peek(self) -> str:
        return self.current[0]

    def has_next(self) -> bool:
        return len(self.current) > 0

    def do_test(self, filename):
        self.fstore = FunctionStore(filename)
        
        for name in self.fstore.tests.keys():
            self.game = None
            self.do_function(name)

    def do_function(self, name):
        for line in self.fstore.functions[name]:
            self.current = line.split.copy()    

            while len(self.current) > 0:
                try:
                    next = self.next()
                    if hasattr(self, f"on_{next}"):
                        getattr(self, f"on_{next}")(line)
                    else:
                        print("Warning Line {line.line_no}: parse rule {next} not found.")
                except Exception as ex:
                    raise type(ex)(f"Line {line.line_no}: {ex}") from ex

    def on_exit(self, line):
        exit()

    def on_call(self, line):
        name = self.next()
        self.do_function(name)

    def on_set(self, line):
        lhs = self.lhs()
        self.next()
        rhs = self.rhs()
        lhs.value = rhs

    def lhs(self):
        if not self.has_next():
            return None
        elif re.fullmatch(r'\$.+', self.peek()):
            player = self.game.players.get(self.next()[1:])
            return TrackedField(player.hand, "set")
        else:
            return get_nested_obj(self.game, self.next())

    def rhs(self):
        value = self.parse_value(self.next())
        return value

    def parse_value(self, input):
        if not input:
            return None
        if re.fullmatch(r"\[(.*?)\]", input):
            split = input[1:-1].split(",")
            return [self.parse_value(s.strip()) for s in split]                    
        elif re.fullmatch(r"[910JQKAL]+[♠♥♣♦]", input):
            card = self.game.deck_manager.deck.get_card(input)
            return card
        elif input.isdigit():
            return int(input)
        else:
            return input

    def on_print(self, line):     
        if not self.has_next():
            print(self.game)
        elif  re.fullmatch(r'\$.+', self.peek()):
            name = self.next()[1:]
            if self.game.players.has(name):
                print(self.game.players.get(name))
            else:
                print(name)
        else:
            while self.has_next():
                self.print_field(self.next())

    def print_field(self, field):
        if has_nested_attr(self.game, field):
            value = get_nested_attr(self.game, field)
            print(f"{field} : {value}")
        else:
            print(f"Warning: Field '{field}' not found in '{type(self.game).__name__}'")

    def on_names(self, line):
        self.data["players"] = ast.literal_eval(self.next())
        self.game = Game(self.data["players"], self.data["seed"])
        
    def on_seed(self, line):
        self.data["seed"] = int(self.next())
        self.game = Game(self.data["players"], self.data["seed"])        

    def on_start(self, line):
        self.game.input(None, "start", None)

    def on_pass(self, line):
        self.game.input(self.game.players.current.name, "pass", None)

    def on_order(self, line):
        self.game.input(self.game.players.current.name, "order", None)

    def on_alone(self, line):
        if self.game.state == 1:
            self.game.input(self.game.players.current.name, "alone", None)
        else:
            self.game.input(self.game.players.current.name, "alone", self.rhs())

    def on_continue(self, line):
        self.game.input(self.game.players.current.name, "continue", None)

    def on_down(self, line):
        self.game.input(self.game.players.current.name, "down", None)

    def on_up(self, line):
        self.game.input(self.game.players.current.name, "up", self.rhs())        

    def on_make(self, line):
        self.game.input(self.game.players.current.name, "make", self.rhs())   

    def on_play(self, line):
        while self.has_next():
            self.game.input(self.game.players.current.name, "play", self.rhs())   

    def on_assert(self, line):
        lhs = self.lhs()
        self.next()
        rhs = self.rhs()
        
        if lhs.value == rhs:
            pass
        else:
            print(f"Line {line.line_no} Assert failed: {line}")

class TrackedField:
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name

    @property
    def value(self):
        return getattr(self.owner, self.name)

    @value.setter
    def value(self, val):
        if callable(getattr(self.owner, self.name)):
            getattr(self.owner, self.name)(val)
        else:
            setattr(self.owner, self.name, val)

    def __repr__(self):
        return f"<TrackedField {self.name}={self.value} of {type(self.owner).__name__}>"    

def get_nested_obj(obj, path):
    attrs = path.split(".")
    for attr in attrs[:-1]:
        obj = getattr(obj, attr)
    return TrackedField(obj, attrs[-1])

def get_nested_attr(obj, path):
    for attr in path.split("."):
        obj = getattr(obj, attr)
    return obj

def has_nested_attr(obj, path):
    for attr in path.split("."):
        if not hasattr(obj, attr):
            return False
        
        obj = getattr(obj, attr)
    return True

if __name__ == "__main__":
    gt = GameTester()
    filename = sys.argv[1]
    gt.do_test(filename)
