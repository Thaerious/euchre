from pyvis.network import Network

def visualize_hypergraph_interactively(hypergraph):
    """
    Visualize a hypergraph with interactive, draggable nodes using pyvis.

    :param hypergraph: A dictionary where keys are hyperedges and values are lists of nodes in each hyperedge.
    """
    # Create a Pyvis Network object
    net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white", directed=False)
    net.barnes_hut()

    # Add nodes and edges to the network
    for hyperedge, nodes in hypergraph.items():
        # Add hyperedge as a node
        net.add_node(hyperedge, label=hyperedge, color="pink", shape="circle")

        for node in nodes:
            # Add node if it doesn't exist
            net.add_node(node, label=node, color="lightblue", shape="dot")
            # Connect the hyperedge to the node
            net.add_edge(hyperedge, node)

    # Show the interactive visualization in a browser
    net.show("hypergraph.html", notebook=False)

# Example hypergraph
hypergraph = {
    "E1": ["A", "B", "C"],
    "E2": ["A", "B"],
    "E3": ["D", "E"],
    "E4": ["E", "F", "G"]
}

visualize_hypergraph_interactively(hypergraph)
