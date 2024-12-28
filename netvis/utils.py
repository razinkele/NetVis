def format_graph_data(graph):
    """Format the graph data for visualization."""
    nodes = [{'id': node, 'label': str(node)} for node in graph.nodes()]
    edges = [{'from': edge[0], 'to': edge[1]} for edge in graph.edges()]
    return {'nodes': nodes, 'edges': edges}

def save_graph_to_file(graph, filename):
    """Save the graph data to a file."""
    data = format_graph_data(graph)
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_graph_from_file(filename):
    """Load graph data from a file."""
    with open(filename, 'r') as f:
        data = json.load(f)
    return data