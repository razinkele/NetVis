from pyvis.network import Network
from pyvis.utils import check_html
import networkx as nx
from IPython.display import display, HTML
from browser import display_html
import pandas as pd
import os
from jinja2 import Environment, FileSystemLoader

class NetworkVS(Network):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nxnet = nx.Graph()
        self.legend = list()
        # Override the set_template_dir method of the parent class
        
        # Set the path for the network  visualization template file
        # changing the original name in PyVis to the new name in this class
        self.path = "VisTemplate.html"
        
        # Set the directory for the templates
        self.template_dir = os.path.dirname(__file__) + "/templates/"
        
        # Initialize the Jinja2 environment with the template directory
        self.templateEnv = Environment(loader=FileSystemLoader(self.template_dir))
    
    def set_template_dir(self, template_directory, template_file='VisTemplate.html'):
        """
            Path to template directory along with the location of the template file.
            :template_directory path: template directory
            :template_file path: name of the template file that is going to be used to generate the html doc.

        """
        self.path = template_file
        self.template_dir = template_directory
        self.templateEnv = Environment(loader=FileSystemLoader(self.template_dir))
    '''
    This method generates an HTML file that visualizes a network graph using the data structures supporting the nodes, edges, and options.

    Explanation:
    Method Definition:

    def generate_html(self, name="index.html", local=True, notebook=False):
    This method generates an HTML file for visualizing the network graph.
    Parameters:
    name: The name of the HTML file to be generated (default is "index.html").
    local: A boolean indicating whether to use local resources (default is True).
    notebook: A boolean indicating whether the output is for a Jupyter notebook (default is False).

    Check HTML File:

    check_html(name): This function checks if the provided HTML file name is valid.

    Check for Links in Hover Data:

    The method iterates through the nodes to check if any node's title contains an href attribute. If so, it sets use_link_template to True to indicate that the template should override the default hover mechanic.

    Load Template:

    If not notebook, the method loads the template from the file specified by self.path using the Jinja2 environment (self.templateEnv).
    If notebook is True, it uses the template stored in self.template.

    Get Network Data:

    nodes, edges, heading, height, width, options = self.get_network_data(): This method retrieves the data structures for nodes, edges, heading, height, width, and options.

    Check Physics Enabled:

    The method checks if physics is enabled in the options. If the options are a dictionary, it checks for the 'physics' key and its 'enabled' status. If not, it directly checks the self.options.physics.enabled attribute.

    Render HTML:

    The method renders the HTML using the template and the retrieved data. It passes various parameters to the template, including height, width, nodes, edges, heading, options, physics_enabled, and other configuration options.

    Return HTML:

    return self.html: The method returns the generated HTML as a string.

    Summary:
    The generate_html method in the Network class generates an HTML file for visualizing a network graph. It checks for links in the hover data, loads the appropriate template, retrieves the network data, checks if physics is enabled, and renders the HTML using the template and the retrieved data. The generated HTML is then returned as a string.
    '''
    
    def generate_html(self, name="index.html", local=True, notebook=False):
        # check if the name is valid
        check_html(name)
        # check if there are links in the hover data
        use_link_template = False
        for n in self.nodes:
            title = n.get("title", None)
            if title:
                if "href" in title:
                    """
                    this tells the template to override default hover
                    mechanic, as the tooltip would move with the mouse
                    cursor which made interacting with hover data useless.
                    """
                    use_link_template = True
                    break
        # load the template
        if not notebook:
            template = self.templateEnv.get_template(self.path)
            print(f'Template is {template}')
        else:
            template = self.template
        # get the network data
        nodes, edges, heading, height, width, options = self.get_network_data()
        # check if physics is enabled
        if isinstance(options, dict):
            physics_enabled = options.get("physics", {}).get("enabled", False)
        else:
            # use the default physics_enabled attribute
            # physics_enabled = self.options.physics.enabled
            physics_enabled = False
        # render the HTML
        self.html = template.render(height=height,
                                    width=width,
                                    nodes=nodes,
                                    edges=edges,
                                    heading=heading,
                                    options=options,
                                    physics_enabled=physics_enabled,
                                    use_DOT=self.use_DOT,
                                    dot_lang=self.dot_lang,
                                    legend=self.legend,
                                    widget=self.widget,
                                    bgcolor=self.bgcolor,
                                    conf=self.conf,
                                    tooltip_link=use_link_template,
                                    neighborhood_highlight=self.neighborhood_highlight,
                                    select_menu=self.select_menu,
                                    filter_menu=self.filter_menu,
                                    notebook=notebook,
                                    cdn_resources=self.cdn_resources
                                    )
        return self.html
    # Changing the write method - needed to upgrade to vis-9.1.9
    def write_html(self, name, local=True, notebook=False):
        import shutil
        import webbrowser
        from IPython.display import IFrame
        import tempfile
        """
        This method gets the data structures supporting the nodes, edges,
        and options and updates the template to write the HTML holding
        the visualization.
        :type name_html: str
        """
        check_html(name)
        self.html = self.generate_html(notebook=notebook)
        # write the class internal HTML to a file
        with open(name, "w+") as out:
            out.write(self.html)
        # return the IFrame to display the HTML
        if notebook:
            with open(name, "w+") as out:
                out.write(self.html)
            return IFrame(name, width=self.width, height=self.height)
        elif notebook and local:
            if not os.path.exists("lib"):
                os.makedirs(os.path.dirname("lib"))
            if not os.path.exists("lib/bindings"):
                shutil.copytree(f"{os.path.dirname(__file__)}/templates/lib/bindings", "lib/bindings")
            if not os.path.exists("lib/tom-select"):
                shutil.copytree(f"{os.path.dirname(__file__)}/templates/lib/tom-select", "lib/tom-select")
            if not os.path.exists("lib/bindings"):
                shutil.copytree(f"{os.path.dirname(__file__)}/templates/lib/vis-9.1.2", "lib/vis-9.1.2")
            with open(name, "w+") as out:
                out.write(self.html)
            return IFrame(name, width=self.width, height=self.height)
        else:
            if local:
                print("Tempdir is the current directory.")
                tempdir = "."
            else:
                print("tempdir is a temporary directory.")
                tempdir = tempfile.mkdtemp()
                print(f"tempdir is {tempdir}")
            # with tempfile.mkdtemp() as tempdir:
            # copy the lib directory to the tempdir - not clear why this is necessary
            if os.path.exists(f"{tempdir}/lib"):
                print(f'Trying to remove {tempdir}/lib as it is already there')
                shutil.rmtree(f"{tempdir}/lib")
            # copy the lib directory from  to the temp directory
            print(f'Copying {os.path.dirname(__file__)}/templates/lib to {tempdir}/lib')
            shutil.copytree(f"{os.path.dirname(__file__)}/templates/lib", f"{tempdir}/lib")
            
            with open(f"{tempdir}/{name}", "w+") as out:
                out.write(self.html)
                webbrowser.open(f"{tempdir}/{name}")
    def initialise_nxnet(self):
        """
        Initialize the nxnet graph from the network structure in self.
        """
        # Clear the existing nxnet graph
        self.nxnet.clear()
        
        # Add nodes to nxnet
        for node in self.nodes:
            self.nxnet.add_node(node["id"], **node)  # Use ** to unpack node attributes

        # Add edges to nxnet
        for edge in self.edges:
            self.nxnet.add_edge(edge["from"], edge["to"], **edge)  # Use ** for edge attributes

    def analyse(self):
        self.initialise_nxnet()
        # Calculate degree centrality and clustering coefficient
        nx.set_node_attributes(self.nxnet, nx.degree_centrality(self.nxnet), 'degree_centrality')
        return {
            'number_of_nodes': self.nxnet.number_of_nodes(),
            'number_of_edges': self.nxnet.number_of_edges(),
            'degree_centrality': nx.degree_centrality(self.nxnet),
            'clustering_coefficient': nx.clustering(self.nxnet)
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
    def AddLegend(self, enabled=True, useGroups=True, addNodes=None, addEdges=None, width=0.2, position="left", main=None, ncol=1, stepX=100, stepY=100, zoom=True):
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
          
   
    def visualize(self, filename='graph.html', notebook=False):
        #net.select_menu('physics')
        self.widget_height = '1000px'
        self.widget_width = '100%'
        #self.directed = nx.is_directed(self.net)
        # net.get_network_data(self.net)
        self.neighborhood_highlight(True)
        self.shapes = 'dot'
        self.options = {
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
                "navigationButtons": False,
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
        
        #net.force_atlas_2based()
        #self.prep_notebook()
        # Add the legend after it is implemented
        # self.add_legend(self.legend)
        # be aware that the path is relative to the current working directory
        # if you want to save the file in a specific directory, make sure to use the full path
        # be aware the write_html uses hardcoded Visjs version (9.1.2)
        # netw.show also uses write_html, so it will also use the hardcoded version
        
        self.write_html(filename)
        self.generate_html(filename)
        #self.generate_html2(filename)
        display_html(filename)
        return self.html
    # Analyze loops in the network
    def analyse_loops(self):
        if not self.nxnet:
            self.initialise_nxnet()
        cycles = list(nx.simple_cycles(self.nxnet))
        loop_details = []
        for cycle in cycles:
            cycle_length = len(cycle)
            strengths = [self.nxnet[cycle[i]][cycle[(i + 1) % len(cycle)]]['strength'] for i in range(len(cycle))]
            total_strength = sum(strengths)
            avg_strength = total_strength / cycle_length
            loop_details.append({
                'cycle': cycle,
                'length': cycle_length,
                'total_strength': total_strength,
                'average_strength': avg_strength,
                'is_reinforcing': all(s > 0 for s in strengths) or all(s < 0 for s in strengths)
            })
        return loop_details
    # Identify leverage points and bottlenecks
    def analyse_influence_dependency(self):
        if not self.nxnet:
            self.initialise_nxnet()
        graph = self.nxnet
        in_degrees = dict(graph.in_degree())
        out_degrees = dict(graph.out_degree())
        influence_dependency = []

        for node in graph.nodes:
            influence = out_degrees[node]  # Number of outgoing edges
            dependency = in_degrees[node]  # Number of incoming edges
            influence_dependency.append({
                'node': node,
                'influence': influence,
                'dependency': dependency,
                'type': 'leverage point' if influence > dependency else 'bottleneck' if dependency > influence else 'neutral'
            })

        return influence_dependency
    def save_as_pajek(self, filename):
        """
        Save the network as a .pajek file.
        :param filename: The name of the file to save the network to.
        """
        if not self.nxnet:
            self.initialise_nxnet()
        # conver all the attributes to strings
        for u, v, d in self.nxnet.edges(data=True):
            for k, v in d.items():
                if not isinstance(v, str):
                    d[k] = str(v)
        for n, d in self.nxnet.nodes(data=True):
            for k, v in d.items():
                if not isinstance(v, str):
                    d[k] = str(v)
        nx.write_pajek(self.nxnet, filename)
        print(f"Network saved as {filename}")
    def style_edges_based_on_attributes(self):
        """
        Styles edges in a pyvis network based on confidence and strength.

        Parameters:
        - net: The pyvis.Network object.
        - edges: List of edges with attributes. Each edge should be a dictionary with:
        * 'from': Source node ID.
        * 'to': Target node ID.
        * 'confidence': Confidence level (0 to 1).
        * 'strength': Strength value (positive or negative).

        Example:
        edges = [
            {'from': 1, 'to': 2, 'confidence': 0.8, 'strength': -5},
            {'from': 2, 'to': 3, 'confidence': 0.5, 'strength': 3},
        ]
        """
        for edge in self.edges:
            confidence = edge.get("confidence", 1)
            print(f'Confidence is {confidence}')
            strength = edge.get("strength", 0)
            print(f'Strength is {strength}')
            

            # Set color based on strength
            color = "red" if strength < 0 else "green"

            # Set transparency (opacity) based on confidence
            opacity = min(max(confidence * 1.5, 0.1), 1)  # Scale up confidence
            rgba_color = f"rgba({255 if strength < 0 else 0}, {255 if strength > 0 else 0}, 0, {opacity})"
            print(f'rgba_color is {rgba_color}')
            # Set width based on strength magnitude
            width = max(abs(strength) * 3, 1)  # Multiply by 3 to make differences more prominent
            print(f'width is {width}')
            # add arrows to the edges
            edge["arrows"] = "to"           
            # update the edge with the new style
            # add a new property to the edge
            edge["color"] = rgba_color
            edge["width"] = width
            
# Example usage
if __name__ == "__main__":
    
    
    import os
    import random
    
    def is_shiny_environment():
        # Example: Check for a custom environment variable set by your Shiny app
        return "SHINY_APP_CONTEXT" in os.environ

    net_vs = NetworkVS()
    # Add 20 nodes
    for i in range(1, 21):
        net_vs.add_node(i, label=f"Node {i}", group = "undefined")
    # Add 35 random edges
    for _ in range(35):
        net_vs.add_edge(random.randint(1, 20), random.randint(1, 20), 
                        strength = random.randint(-5, 5),confidence = random.uniform(0, 10))
    
    net_vs.style_edges_based_on_attributes()
    for edge in net_vs.edges:
        print(f'Color: Width')
        # print edge width and colot attributes
        print(f'{edge["width"]}: {edge["color"]}')
        
        

    # Check whether the net_vs is of class NetworkVS
    if (isinstance(net_vs, NetworkVS)):
        analysis_results = net_vs.analyse()
        for key, value in analysis_results.items():
            print(f"{key}: {value}")
    else:
        # Set the template directory and file
        template_dir = os.path.dirname(__file__) + "/templates/"
        net_vs.set_template_dir(template_directory=template_dir , template_file='VisTemplate.html')
    
    filename = 'graph2try.html'
    # Check whether the environment is a Shiny environment
    if is_shiny_environment():
        print("Running in a Python Shiny environment.")
    else:
        print("Not running in a Shiny environment.")
    my_html = net_vs.generate_html(name=filename)
    net_vs.write_html(filename, local=False)
    net_vs.save_as_pajek("network.pajek")