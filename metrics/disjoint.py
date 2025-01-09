from metrics.cohesionx import *

def find_disjoint_hypergraphs(hypergraph):
    """
    Determines and groups disjoint hypergraphs.

    :param hypergraph: A dictionary where keys are hyperedges and values are lists of nodes.
    :return: A list of disjoint hypergraphs, each represented as a set of hyperedges.
    """
    # Build a graph where hyperedges are connected if they share nodes
    hyperedge_graph = defaultdict(set)

    for hyperedge1, nodes1 in hypergraph.items():
        for hyperedge2, nodes2 in hypergraph.items():
            if hyperedge1 == hyperedge2: continue
            if not set(nodes1) & set(nodes2): continue
            hyperedge_graph[hyperedge1].add(hyperedge2)
            hyperedge_graph[hyperedge2].add(hyperedge1)

    # Find connected components (disjoint sub-hypergraphs)
    visited = set()
    disjoint_hypergraphs = []

    def dfs(hyperedge, component):
        """Depth-First Search to find connected components."""
        visited.add(hyperedge)
        component.add(hyperedge)
        for neighbor in hyperedge_graph[hyperedge]:
            if neighbor not in visited:
                dfs(neighbor, component)

    for hyperedge in hypergraph:
        if hyperedge not in visited:
            component = set()
            dfs(hyperedge, component)
            disjoint_hypergraphs.append(component)

    return disjoint_hypergraphs

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <path_to_python_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    with open(file_path, "r") as file:
        code = file.read()
    
    tree = ast.parse(code)
    assign_parents(tree)
    analyzer = ClassCohesionAnalyzer()
    analyzer.visit(tree)

    nodes = analyzer.record.as_dictionary()
    edges = invert_graph(nodes)
    clusters = find_disjoint_hypergraphs(edges)

    print(clusters)