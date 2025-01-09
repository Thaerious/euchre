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

    if len(sys.argv) == 2:
        for method, attrs in methods.items():
            print(f"# {method}()")

            for attr in attrs:
                print(f"  - {attr} {methods[method][attr]}")
            for method2 in inverse[attr]:
                if method2 != method:
                    print(f"  - {method2}() {inverse[attr][method]}")
            print("")
    else:
        method = sys.argv[2]
        print(f"# {method}()")
        attrs = methods[method]

        for attr in attrs:
            print(f"  {methods[method][attr]} {attr}")
        for method2 in inverse[attr]:
            # if method2 != method:
            print(f"  - {method2}() {methods[method2][attr]}")
        print("")