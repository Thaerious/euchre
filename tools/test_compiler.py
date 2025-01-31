import sys
import re
import os
from euchre.del_string import del_string

if len(sys.argv) == 2:
    filename = os.path.basename(sys.argv[1])
    if not filename.startswith("test_"):
        filename = "test_" + filename
    destpath = filename.replace(".test", ".py")
    sys.argv.append(f"./tests/{destpath}")

if len(sys.argv) != 3:
    print("usage: python test_compiler.py <source_file> <dest_file>")
    exit()

destpath = [
    "import pytest",
    "from euchre.Euchre import *",
    "from euchre.Game import *",
    ""
]

indent = "    "
after = None

def add_after():
     global after
     if after is not None:
         destpath.append(after)
         destpath.append("")
         after = None

with open(sys.argv[1], "r") as file:
    for _line in file:
        line = _line.strip()       
        split = line.split()

        if line.startswith("#"):
            destpath.append(f"{indent}{line}")

        elif line.startswith("fixture"):
            add_after()
            destpath.append(f"@pytest.fixture")
            destpath.append(f"def {split[1]}():")
            after = f"{indent}return {split[1]}"

        elif line.startswith("test"):
            add_after()
            if len(split) > 2:
                args = del_string(split[2:])
                destpath.append(f"def test_{split[1]}({args}):")
            else:
                destpath.append(f"def test_{split[1]}():")

        elif line.startswith("names"):
            matches = re.findall(r"\[(.*?)\]", line) 
            destpath.append(f"{indent}game = Game([{matches[0]}])")
        
        elif line.startswith("seed"):
            destpath.append(f"{indent}random.seed({split[1]})")

        elif line.startswith("assert"):
            modified_line = re.sub(r'^(assert)\s+', r'\1 game.', line)
            destpath.append(f"{indent}{modified_line}")

        elif line.startswith("print"):
            destpath.append(f"{indent}print(game)")

        elif line.startswith("@"):
            destpath.append(f"{indent}print(game)")
            destpath.append(f"{indent}pytest.raises({line[1:]}):\n{indent}")

        elif line.startswith("play"):
            for s in split[1:]:
                destpath.append(f"{indent}game.input(game.current_player.name, 'play', '{s}')")

        else:
            if len(split) == 0:
                destpath.append("")
            elif len(split) == 1:
                destpath.append(f"{indent}game.input(None, '{split[0]}', None)")            
            elif len(split) == 2:
                destpath.append(f"{indent}game.input('{split[0]}', '{split[1]}', None)")
            elif len(split) == 3:
                destpath.append(f"{indent}game.input('{split[0]}', '{split[1]}', '{split[2]}')")

with open(sys.argv[2], "w") as file:
    for line in destpath:
        file.write(line + "\n")
