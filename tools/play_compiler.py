import sys
import re

if len(sys.argv) != 3:
    print("usage: python play_compiler.py <source_file> <dest_file>")
    exit()

output = [
    "import pytest",
    "from euchre.Euchre import *",
    "from euchre.Game import *",
    ""
]

indent = "    "

with open(sys.argv[1], "r") as file:
    for _line in file:
        line = _line.strip()       
        split = line.split()

        if line.startswith("#"):
            output.append(f"{indent}{line}")

        elif line.startswith("test"):
            output.append(f"def test_{split[1]}():")

        elif line.startswith("names"):
            matches = re.findall(r"\[(.*?)\]", line) 
            output.append(f"{indent}game = Game([{matches[0]}])")
        
        elif line.startswith("seed"):
            output.append(f"{indent}game.seed = {split[1]}")

        elif line.startswith("assert"):
            modified_line = re.sub(r'^(assert)\s+', r'\1 game.', line)
            output.append(f"{indent}{modified_line}")

        elif line.startswith("print"):
            output.append(f"{indent}print(game)")

        elif line.startswith("@"):
            #with pytest.raises(EuchreException, match="Card 'Q♠' must follow suit '♥'."):  
            output.append(f"{indent}print(game)")
            output.append(f"{indent}pytest.raises({line[1:]}):\n{indent}")

        elif line.startswith("play"):
            for s in split[1:]:
                output.append(f"{indent}game.input(game.current_player.name, 'play', '{s}')")

        else:
            if len(split) == 0:
                output.append("")
            elif len(split) == 1:
                output.append(f"{indent}game.input(None, '{split[0]}', None)")            
            elif len(split) == 2:
                output.append(f"{indent}game.input('{split[0]}', '{split[1]}', None)")
            elif len(split) == 3:
                output.append(f"{indent}game.input('{split[0]}', '{split[1]}', '{split[2]}')")

with open(sys.argv[2], "w") as file:
    for line in output:
        file.write(line + "\n")
