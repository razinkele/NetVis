
from pyvis.network import Network
from netvis.browser import display_html
import os


def create_and_display_graph():
    net = Network(directed=True)

    # Add nodes to the graph
    nodes = ["Node A", "Node B", "Node C", "Node D"]
    for node in nodes:
        net.add_node(node, label=node)

    # Add edges to the graph
    edges = [("Node A", "Node B"), ("Node B", "Node C"), ("Node C", "Node D"), ("Node D", "Node A")]
    for edge in edges:
        net.add_edge(edge[0], edge[1])

    # Customize appearance
    net.toggle_physics(True)  # Enable physics for layout dynamics
    net.toggle_stabilization(True)  # Stabilize the graph after adding nodes and edges  
    net.show_buttons(filter_=['physics'])  # Show only the physics button
    # Generate the HTML for the graph
    graph_html = net.generate_html()

    # Save the HTML to a file
    html_file_path = os.path.join(os.getcwd(), "network.html")
    with open(html_file_path, "w") as file:
        file.write(graph_html)

    # Open the HTML file in VSCode
    #vscode.open(html_file_path)

# Call the function to create and display the graph
display_html("network.html")