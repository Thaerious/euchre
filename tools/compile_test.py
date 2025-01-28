import sys
import re

if len(sys.argv) != 3:
    print("usage: python compile_test.py <source_file> <dest_file>")
    exit()

output = [
    "import pytest",
    "from euchre.Euchre import *",
    "from euchre.Game import *",
    ""
]

with open(sys.argv[1], "r") as file:
    for _line in file:
        line = _line.strip()       
        split = line.split()

        if line.startswith("test"):
            output.append(f"def test_{split[1]}()")

        elif line.startswith("names"):
            matches = re.findall(r"\[(.*?)\]", line) 
            output.append(f"\tgame = Game({matches[0]})")
        
        elif line.startswith("seed"):
            output.append(f"\tgame.debug_seed = {split[1]}")

        elif line.startswith("assert"):
            output.append(f"\t{line}")

        else:
            if len(split) == 1:
                output.append(f"\tgame.input(None, {split[0]}, None)")            
            elif len(split) == 2:
                output.append(f"\tgame.input({split[0]}, {split[1]}, None)")
            elif len(split) == 3:
                output.append(f"\tgame.input({split[0]}, {split[1]}, {split[2]})")

for line in output:
    print(line)            