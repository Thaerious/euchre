import sys
import re
import os
from euchre.del_string import del_string

def is_action(split):
    actions = ["start", "continue", "pass", "order", "alone", "down", "up", "make", "play"]

    if len(split) == 0: return False
    if len(split) == 1 and split[0] in actions: return True
    if len(split) >= 2 and split[1] in actions: return True
    return False

class Header(list):
    def write_out(self, file):
        for line in self:
            file.write(line)
            file.write("\n")

class Routine(list):
    indent = "    "

    def __init__(self, after = ""):
        self.after = after

    def write_out(self, file):                
        file.write(self[0] + "\n")
        for line in self[1:]:
            file.write(Routine.indent + line + "\n")
        file.write(Routine.indent + self.after + "\n")            
        file.write("\n") 
        
class Compiler():
    def __init__(self):
        self.routines = [Header()]
    
        self.append("import pytest")
        self.append("from euchre.Euchre import *")
        self.append("from euchre.Game import *")

    def enter_routine(self, after = ""):
        self.routines.append(Routine(after))

    def append(self, string):
        self.routines[-1].append(string)

    def write_out(self, path):
        with open(path, "w") as file:
            for routine in self.routines:
                routine.write_out(file)                    

    def run(self, path):
        with open(path, "r") as file:
            for _line in file:
                line = _line.strip()       
                split = line.split()

                if len(split) == 0:
                    self.append("")

                elif line.startswith("#"):
                    self.append(f"{line}")

                elif line.startswith("fixture"):   
                    self.enter_routine(f"return {split[1]}")                                     
                    self.append(f"@pytest.fixture\ndef {split[1]}():")

                elif split[0] == "test":
                    self.enter_routine()  

                    if len(split) > 2:
                        args = del_string(split[2:])
                        self.append(f"def test_{split[1]}({args}):")
                    else:
                        self.append(f"def test_{split[1]}():")

                elif line.startswith("names"):
                    matches = re.findall(r"\[(.*?)\]", line) 
                    self.append(f"game = Game([{matches[0]}])")
                
                elif line.startswith("seed"):
                    self.append(f"random.seed({split[1]})")

                elif line.startswith("assert"):
                    modified_line = re.sub(r'^(assert)\s+', r'\1 game.', line)
                    self.append(f"{modified_line}")

                elif line.startswith("print"):
                    self.append(f"print(game)")

                elif line.startswith("@"):
                    self.append(f"print(game)")
                    self.append(f"pytest.raises({line[1:]}):\n")

                elif line.startswith("play"):
                    for s in split[1:]:
                        self.append(f"game.input(game.current_player.name, 'play', '{s}')")

                elif is_action(split):
                    if len(split) == 1:
                        self.append(f"game.input(None, '{split[0]}', None)")            
                    elif len(split) == 2:
                        self.append(f"game.input('{split[0]}', '{split[1]}', None)")
                    elif len(split) == 3:
                        self.append(f"game.input('{split[0]}', '{split[1]}', '{split[2]}')")

                else:
                    self.append(f"{line}")

        return self

if len(sys.argv) == 2:
    filename = os.path.basename(sys.argv[1])
    if not filename.startswith("test_"):
        filename = "test_" + filename
    destpath = filename.replace(".test", ".py")
    sys.argv.append(f"./tests/{destpath}")

if len(sys.argv) != 3:
    print("usage: python test_compiler.py <source_file> <dest_file>")
    exit()

c = Compiler().run(sys.argv[1]).write_out(sys.argv[2])
        


