import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'netvis')))
print(f'System path {sys.path}')
from network import NetworkVS
import networkx as nx
from browser import display_html

def test_network_creation():
    net = NetworkVS()
    net.add_node(1)
    net.add_node(2)
    net.add_edge(1, 2)
    
    assert len(net.net.nodes) == 2
    assert len(net.net.edges) == 1

def test_graph_visualization():
    net = NetworkVS()
    net.add_node(1)
    net.add_node(2)
    net.add_node(3)
    net.add_node(4)
    net.add_edge(1, 2)
    net.add_edge(1, 2)
    net.add_edge(1, 3)
    net.add_edge(1, 4)
    net.add_edge(2, 3)
    net.add_edge(2, 4)
    net.add_edge(3, 4)
    
 
    graph_html = net.generate_html()
    # Save the HTML to a file
    html_file_path = os.path.join(os.getcwd(), "network.html")
    with open(html_file_path, "w") as file:
        file.write(graph_html)
    
    # Call the function to display the graph
    display_html("network.html")

def test_graph_analysis():
    net = NetworkVS()
    net.add_node(1)
    net.add_node(2)
    net.add_edge(1, 2)
    
    analysis = net.analyze()
    assert analysis['number_of_nodes'] == 2
    assert analysis['number_of_edges'] == 1
    assert analysis['degree_centrality'][1] == 1.0
    assert analysis['degree_centrality'][2] == 1.0

def test_empty_graph():
    net = NetworkVS()
    
    assert len(net.net.nodes) == 0
    assert len(net.net.edges) == 0

def test_add_multiple_nodes():
    net = NetworkVS()
    nodes = [1, 2, 3, 4, 5]
    for node in nodes:
        net.add_node(node)
    
    assert len(net.net.nodes) == len(nodes)

def test_add_multiple_edges():
    net = NetworkVS()
    edges = [(1, 2), (2, 3), (3, 4), (4, 5)]
    for u, v in edges:
        net.add_edge(u, v)
    
    assert len(net.net.edges) == len(edges)

if __name__ == "__main__":
    test_network_creation()
    test_graph_visualization()
    test_graph_analysis()
    test_empty_graph()
    test_add_multiple_nodes()
    test_add_multiple_edges()
    print("All tests passed!")