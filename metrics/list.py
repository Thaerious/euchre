from metrics.cohesionx import *

class Test():
    def foo(self):
        self.f = self.f + 1

    def bar(self):
        self.b += 1        

    def foobar(self):
        self.b = 0
        self.f = 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python side_effects.py <path_to_python_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    with open(file_path, "r") as file:
        code = file.read()
    
    tree = ast.parse(code)
    assign_parents(tree)
    analyzer = ClassCohesionAnalyzer()
    analyzer.visit(tree)

    methods = analyzer.record
    inverse = invert_graph(methods)

    for method, attrs in methods.items():
        context = ContextRecord()

        for attr in attrs:
            if methods[method][attr].write:
                context.write = True
            if methods[method][attr].read:
                context.read = True

        print(f"# {method}() {context}")
