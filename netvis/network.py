from pyvis.network import Network
import networkx as nx
from IPython.display import display, HTML
from browser import display_html

class NetworkVS(Network):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.net = nx.Graph()

    def add_node(self, node, **attr):
        self.net.add_node(node, **attr)

    def add_edge(self, u, v, **attr):
        self.net.add_edge(u, v, **attr)

    def analyze(self):
        nx.set_node_attributes(self.net, nx.degree_centrality(self.net), 'degree_centrality')
        return {
            'number_of_nodes': self.net.number_of_nodes(),
            'number_of_edges': self.net.number_of_edges(),
            'degree_centrality': nx.degree_centrality(self.net),
            'clustering_coefficient': nx.clustering(self.net)
        }

    class Graph(Network):
        def __init__(self, notebook=False):
            super().__init__(notebook=notebook)

    def visualize(self, filename='graph.html', notebook=False):
        net = self.Graph(notebook=notebook)
        #net.select_menu('physics')
        net.widget_height = '1000px'
        net.widget_width = '100%'
        net.directed = nx.is_directed(self.net)
        # net.get_network_data(self.net)
        #net.neighborhood_highlight(True)
        net.shapes = 'dot'
        net.options = {
            "nodes": {
                "borderWidth": 0,
                "borderWidthSelected": 0,
                "color": {
                    "highlight": {
                        "background": "rgba(255,255,255,1)"
                    }
                },
                "font": {
                    "size": 14,
                    "face": "tahoma"
                },
                "scaling": {
                    "label": {
                        "enabled": True
                    }
                },
                "shadow": {
                    "enabled": True
                },
                "shape": "dot",
                "size": 25
            },
            "edges": {
                "arrows": {
                    "to": {
                        "enabled": True
                    }
                },
                "color": {
                    "color": "rgba(50,50,50,0.5)",
                    "highlight": "rgba(0,0,0,1)"
                },
                "font": {
                    "size": 10,
                    "face": "tahoma"
                },
                "scaling": {
                    "label": {
                        "enabled": True
                    }
                },
                "shadow": {
                    "enabled": True
                },
                "smooth": {
                    "enabled": True
                }
            },
            "interaction": {
                "hover": True,
                "navigationButtons": True,
                "keyboard": True
            },
            "manipulation": {
                "enabled": True,
                "initiallyActive": False,
                "addNode": True,
                "editNode": """function (data, callback) {
                        data.label = prompt("Edit Node Label", data.label) || data.label;
                        callback(data);""",
                "deleteNode": True,
                "addEdge": True,
                "editEdge": True
            },
        }
        if False:  
            net.set_options("""
            {
                "manipulation": {
                    "enabled": true,
                    "initiallyActive": true,
                    "addNode": function (data, callback) {
                        data.label = "New Node";
                        callback(data);
                    },
                    "editNode": function (data, callback) {
                        data.label = prompt("Edit Node Label", data.label) || data.label;
                        callback(data);
                    },
                    "deleteNode": true,
                    "addEdge": true,
                    "editEdge": true,
                    "deleteEdge": true
                }
            }
            """)
        for node in self.net.nodes(data=True):
            net.add_node(node[0], **node[1])
        for edge in self.net.edges(data=True):
            net.add_edge(edge[0], edge[1], **edge[2])
        #net.force_atlas_2based()
        net.show(filename)
        display_html(filename)
        

# Example usage
if __name__ == "__main__":
    net_vs = NetworkVS()
    net_vs.add_node(1)
    net_vs.add_node(2)
    net_vs.add_node(3)
    net_vs.add_edge(1, 2)
    net_vs.add_edge(3, 2)
    net_vs.add_edge(1, 3)
    print(net_vs.analyze())
    net_vs.visualize('graph.html', notebook=True)