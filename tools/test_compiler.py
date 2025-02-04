import sys
import re
import os
from euchre.del_string import del_string

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
    actions = ["start", "continue", "pass", "order", "alone", "down", "up", "make", "play"]

    def __init__(self):
        self.routines = [Header()]
        self.names = []
    
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

                if len(split) == 0: self.append("")
                elif line.startswith("#"): self.append(f"{line}")
                elif line.startswith("seed"): self.append(f"random.seed({split[1]})")
                elif self.process_fixture(line): pass
                elif self.process_test(line): pass
                elif self.process_names(line): pass 
                elif self.process_set(line): pass 
                elif self.process_assert(line): pass
                elif line.startswith("print"): self.append(f"print(game)")
                elif line.startswith("@"): self.append(f"pytest.raises({line[1:]}):\n")
                elif self.process_player_action(line): pass
                elif self.process_actions(line): pass

                elif line.startswith("play"):
                    for s in split[1:]:
                        self.append(f"game.input(game.current_player.name, 'play', '{s}')")

               

                else:
                    self.append(f"{line}")

        return self
    
    def process_names(self, line):
        if not line.startswith("names"): return False

        matches = re.findall(r"\[(.*?)\]", line) 
        self.append(f"game = Game([{matches[0]}])")
        self.names = re.findall(r'"([^"]+)"', matches[0])
        return True
    
    def process_set(self, line):
        if not line.startswith("set"): return False
        (target, source) = re.match(r'set ([\da-zA-Z_]+)[ ]*=[ ]*(.+)', line).groups()
        
        if target in self.names:
            cards = re.findall(r'[910JQKAL]+[♠♥♣♦]', source)
            cards = del_string(cards, ",", "'")
            self.append(f"game.set_cards('{target}', [{cards}])")
        elif target == "up_card":
            self.append(f"game.up_card = '{source}'")

        return True
    
    def process_fixture(self, line):
        if not line.startswith("fixture"): return False
        split = line.split()
        self.enter_routine(f"return {split[1]}")                                     
        self.append(f"@pytest.fixture\ndef {split[1]}():")
        return True

    def process_test(self, line):
        if not line.startswith("test"): return False
        split = line.split()        
        self.enter_routine()  

        if len(split) > 2:
            args = del_string(split[2:])
            self.append(f"def test_{split[1]}({args}):")
        else:
            self.append(f"def test_{split[1]}():")
        return True      

    def process_assert(self, line):
        if not line.startswith("assert"): return False
        modified_line = re.sub(r'^(assert)\s+', r'\1 game.', line)
        self.append(f"{modified_line}")         
        return True

    def process_player_action(self, line):
        split = line.split()
        if not split[0] in self.names: return False        

        if len(split) == 2:
            self.append(f"game.input('{split[0]}', '{split[1]}', None)")
        elif len(split) == 3:
            self.append(f"game.input('{split[0]}', '{split[1]}', '{split[2]}')")             
        return True

    def process_actions(self, line):        
        split = line.split()
        if not split[0] in Compiler.actions: return False

        for i, action in enumerate(split):
            if not action in Compiler.actions: continue

            if action in ["start", "continue"]:
                self.append(f"game.input(None, '{action}', None)")        
            elif action in ["play", "up", "make"]:
                self.append(f"game.input(game.current_player.name, '{action}', '{split[i+1]}')") 
            else: 
                self.append(f"game.input(game.current_player.name, '{action}', None)")
        
        return True


# python test_compiler.py <filename>.test
# input path only
# will output to tests/<filename>.py
if len(sys.argv) == 2:
    filename = os.path.basename(sys.argv[1])
    if not filename.startswith("test_"):
        filename = "test_" + filename
    destpath = filename.replace(".test", ".py")
    sys.argv.append(f"./tests/{destpath}")

# python test_compiler.py <full_input_path>.test <full_output_path>
# input path only
if len(sys.argv) != 3:
    print("usage: python test_compiler.py <source_file> <dest_file>")
    exit()

c = Compiler().run(sys.argv[1]).write_out(sys.argv[2])
        


