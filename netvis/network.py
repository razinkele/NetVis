from pyvis.network import Network
import networkx as nx
from IPython.display import display, HTML
from browser import display_html
import pandas as pd
class NetworkVS(Network):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.net = nx.Graph()
    legend = list()
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
    #' Add a legend on a Graph object
    #' 
    #' @param graph : a graph object
    #' @param enabled : Boolean. Default to TRUE.
    #' @param useGroups : use groups options in legend ? Default to TRUE.
    #' @param addNodes : a data.frame or a list for adding custom node(s)
    #' @param addEdges : a data.frame or a list for adding custom edges(s)
    #' @param width : Number, in [0,...,1]. Default to 0.2
    #' @param position : one of "left" (Default) or "right"
    #' @param main : For add a title. Character or a named list.
    def VisLegend(self, enabled=True, useGroups=True, addNodes=None, addEdges=None, width=0.2, position="left", main=None, ncol=1, stepX=100, stepY=100, zoom=True):
         if(enabled):
            # initialize legend vaariable as an empty list
            legend = list()
            if not (0 <= width <= 1):
                raise ValueError("'width' must be between 0 and 1")
            legend['width'] = width
            
            if not isinstance(useGroups, bool):
                raise ValueError("useGroups must be logical (True/False)")
            legend['useGroups'] = useGroups
            
            if position not in ["left", "right"]:
                raise ValueError("position must be one of 'left' or 'right'")
            legend['position'] = position
            
            if not isinstance(ncol, int) or ncol < 1:
                raise ValueError("ncol must be an integer >= 1")
            legend['ncol'] = ncol
            
            legend['stepX'] = stepX
            legend['stepY'] = stepY
            
            legend['zoom'] = zoom
            
            if addEdges is not None:
                legend['edges'] = addEdges
                if isinstance(addEdges, pd.DataFrame):
                    legend['edgesToDataframe'] = True
                elif isinstance(addEdges, list):
                    legend['edgesToDataframe'] = True
                else:
                    raise ValueError("addEdges must be a pandas DataFrame or a list")
            if addNodes is not None:
                legend['nodes'] = addNodes
                if isinstance(addNodes, pd.DataFrame):
                    legend['nodesToDataframe'] = True
                elif isinstance(addNodes, list):
                    legend['nodesToDataframe'] = False
                else:
                    raise ValueError("addNodes must be a pandas DataFrame or a list")
             # main
            if main is not None:
                if isinstance(main, dict):
                    if any(key not in ["text", "style"] for key in main.keys()):
                        raise ValueError("Invalid 'main' argument")
                    if "text" not in main:
                        raise ValueError("Needed a 'text' value using a list for 'main'")
                    if "style" not in main:
                        main["style"] = 'font-family:Georgia, Times New Roman, Times, serif;font-weight:bold;font-size:14px;text-align:center;'
                elif not isinstance(main, str):
                    raise ValueError("Invalid 'main' argument. Not a character")
                else:
                    main = {
                        "text": main,
                        "style": 'font-family:Georgia, Times New Roman, Times, serif;font-weight:bold;font-size:14px;text-align:center;'
                    }
                legend["main"] = main
            self.legend = legend
                    
            
            return """
            <div style="position: absolute; right: 0; top: 0; z-index: 1000; background-color: white; padding: 10px; border: 1px solid black;">
                <h3>Legend</h3>
                <ul>
                    <li><span style="color: red;">Red</span> - High Degree Centrality</li>
                    <li><span style="color: green;">Green</span> - Low Degree Centrality</li>
                </ul>
            </div>
            """
        
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