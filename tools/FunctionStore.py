import sys
import re

class Line:
    def __init__(self, line_no, contents):
        self.line_no = line_no
        self.contents = contents.strip()
        self.split = re.findall(r'\[.*?\]|\S+', contents)

    def __getitem__(self, key):
        return self.split[key]
    
    def __str__(self):
        return self.contents
    
    def __len__(self):
        return len(self.split)

class FunctionStore:
    def __init__(self, filename):
        self.functions = {}
        self.tests = {}
        self.line_no = 0
        self.parse(filename)

    def parse(self, filename):
        current_function = None

        with open(filename) as f:
            for line in f:
                self.line_no += 1
                line = line.strip()
                if line == "": continue
                if line.startswith("#"): continue
                line = Line(self.line_no, line)

                if line[0][-1] == ":":
                    name, lines = self.build_function(line)
                    self.functions[name] = lines
                    current_function = lines
                elif line[0] == "test":
                    name, lines, desc = self.build_test(line)
                    self.functions[name] = lines
                    self.tests[name] = desc
                    current_function = lines
                elif current_function is None:
                    continue
                else:
                    current_function.append(line)

    def build_function(self, line):
        name = line[0][:-1]
        return (name, [])
    
    def build_test(self, line):
        name = line[1][:-1]
        if len(line) < 3: return (name, [], "")        
        description = " ".join(line[2:])
        return (name, [], description)

if __name__ == "__main__":    
    filename = sys.argv[1]
    ft = FunctionStore(filename)
    
    for name in ft.functions.keys():
        if name in ft.tests:
            print(f"{name}: {ft.tests[name]}")
        else:
            print(f"{name}:")

        for line in ft.functions[name]:
            print("    ", line)
