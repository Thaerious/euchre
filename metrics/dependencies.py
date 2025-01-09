from metrics.cohesionx import *

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dependencies.py <path_to_python_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    with open(file_path, "r") as file:
        code = file.read()
    
    tree = ast.parse(code)
    assign_parents(tree)
    analyzer = ClassCohesionAnalyzer()
    analyzer.visit(tree)

    nodes = analyzer.record
    edges = invert_graph(nodes)
    
    for attribute, methods in edges.items():
        print(f"{attribute} {type(attribute)}")
