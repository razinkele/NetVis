from shiny import App, render, ui, reactive
import networkx as nx
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'netvis')))
from pyvis.network import Network
from network import NetworkVS
import html
import json
import pandas as pd


PYVIS_SHAPES = [
    "ellipse",
    "circle",
    "database",
    "box",
    "text",
    "diamond",
    "dot",
    "star",
    "triangle",
    "triangleDown",
    "square",
    "hexagon",
]

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h3("SESTool", style="color: #10276a; margin-bottom: 10px;"),  # Add title

        
        # Replace the tooltip and file input section with:
        ui.tooltip(
            ui.div(
                ui.input_file(
                    "excel_file", 
                    "Upload Excel file", 
                    accept=[".xlsx"],
                ),
                style=" padding: 0px; height: 30px; margin-bottom: 28px;"

            ),
            ("Excel file should have two sheets:\n"
             "'nodes' with columns: id, label, shape, color, size\n"
             "'edges' with columns: from, to")
        ),
        ui.input_action_button(
            "load_excel",
            "Load from Excel",
            class_="btn-sm btn-primary",
            style="margin-bottom: -8px;",
        ),
        ui.input_action_button(
            "display",
            "Display Network",
            class_="btn-sm btn-primary",
            style="margin-bottom: -12px;",
        ),
        ui.input_action_button(
            "get_data",
            "Get Data from Network",
            class_="btn-sm btn-primary",
            style="margin-bottom: 8px;",
        ),
        ui.input_action_button(
            "generate",
            "Generate New Network",
            class_="btn-sm btn-primary",
            style="margin-bottom: -10px;",
        ),
        ui.panel_conditional(
            "true",
            ui.accordion(
                ui.accordion_panel(
                    "Generation Parameters",
                    ui.input_slider(
                        "num_nodes", "Number of nodes", min=3, max=15, value=8
                    ),
                    ui.input_select(
                        "layout",
                        "Layout algorithm",
                        choices=["spring", "circular", "random"],
                        selected="spring",
                    ),
                    #id="gen_params",
                ),
                id="main_accordion",
                selected=None  # This makes all panels collapsed by default
            ),
        ),
        ui.output_text_verbatim("network_data"),
    ),
    ui.navset_tab(
        ui.nav_panel(
            "Network View",
            ui.output_ui("network_output"),
        ),
        ui.nav_panel(
            "Node Data",
            ui.row(
                ui.column(
                    3,
                    ui.input_select(
                        "selected_node",
                        "Select Node:",
                        choices=[],
                    ),
                ),
                ui.column(
                    3,
                    ui.input_text(
                        "node_label",
                        "Node Label:",
                        value="",
                    ),
                ),
                ui.column(
                    3,
                    ui.input_select(
                        "node_shape",
                        "Node Shape:",
                        choices=PYVIS_SHAPES,
                        selected="dot",
                    ),
                ),
                ui.column(
                    3,
                    ui.div(
                        ui.div(
                            "Node Color:",
                            class_="control-label",
                        ),
                        ui.tags.input(
                            id="node_color",
                            type="color",
                            value="#97c2fc",
                            style="width: 100%; height: 38px; margin-top: 5px;",
                            oninput="Shiny.setInputValue('node_color', this.value)",
                        ),
                        class_="form-group",
                    ),
                ),
                ui.column(
                    3,
                    ui.input_slider(
                        "node_size", "Node Size:", min=10, max=50, value=25
                    ),
                ),
            ),
            ui.row(
                ui.column(
                    12,
                    ui.input_action_button(
                        "apply_changes",
                        "Apply Changes",
                        class_="btn-primary",
                        width="100%",
                    ),
                )
            ),
            ui.output_data_frame("node_table"),
        ),
        ui.nav_panel(
            "Edge Data",
            ui.output_data_frame("edge_table"),
        ),
    ),
    ui.tags.script(
        """
        $(document).on('click', '#get_data', function() {
            var iframe = document.querySelector('#networkIframe');
            if (iframe && iframe.contentWindow) {
                setTimeout(function() {
                    try {
                        var network = iframe.contentWindow.network;
                        if (network) {
                            var nodes = network.body.data.nodes.get();
                            var edges = network.body.data.edges.get();
                            Shiny.setInputValue('network_data', JSON.stringify({
                                nodes: nodes,
                                edges: edges
                            }));
                        } else {
                            Shiny.setInputValue('network_data', JSON.stringify({
                                error: "Network object not found"
                            }));
                        }
                    } catch (e) {
                        Shiny.setInputValue('network_data', JSON.stringify({
                            error: "Error accessing network data: " + e.message
                        }));
                    }
                }, 500);
            } else {
                Shiny.setInputValue('network_data', JSON.stringify({
                    error: "Iframe not found"
                }));
            }
        });
        
        Shiny.addCustomMessageHandler('update-node-properties', function(message) {
            document.getElementById('node_color').value = message.color;
            Shiny.setInputValue('node_color', message.color);
            Shiny.setInputValue('node_size', message.size);
        });
    """
    ),
)


def server(input, output, session):
    network_data_rv = reactive.value(None)
    cached_html = reactive.value(None)
    last_button = reactive.value(None)
    node_data = reactive.value(None)
    edge_data = reactive.value(None)

    @reactive.effect
    @reactive.event(input.generate)
    def _():
        last_button.set("generate")

    @reactive.effect
    @reactive.event(input.display)
    def _():
        last_button.set("display")

    @reactive.effect
    @reactive.event(input.load_excel)
    def load_excel_data():
        if not input.excel_file():
            return

        file_path = input.excel_file()[0]["datapath"]
        try:
            # Read nodes data
            nodes_df = pd.read_excel(file_path, sheet_name="nodes")
            nodes_list = nodes_df.to_dict("records")

            # Read edges data
            edges_df = pd.read_excel(file_path, sheet_name="edges")
            edges_list = edges_df.to_dict("records")

            # Set the data
            node_data.set(nodes_list)
            edge_data.set(edges_list)

            # Force redraw
            last_button.set("generate")
            cached_html.set(None)

            # Update node choices
            choices = [str(node["id"]) for node in nodes_list]
            ui.update_select("selected_node", choices=choices)

        except Exception as e:
            ui.notification_show(f"Error loading Excel file: {str(e)}", type="error")

    @reactive.effect
    @reactive.event(input.network_data)
    async def update_node_choices():
        if input.network_data() is not None:
            try:
                data = json.loads(input.network_data())
                if "nodes" in data:
                    nodes = data["nodes"]
                    choices = [str(node["id"]) for node in nodes]
                    ui.update_select("selected_node", choices=choices)

                    if nodes and len(nodes) > 0:
                        first_node = nodes[0]
                        await session.send_custom_message(
                            "update-node-properties",
                            {
                                "color": first_node.get("color", "#97c2fc"),
                                "size": first_node.get("size", 25),
                            },
                        )
            except:
                pass

    @reactive.effect
    @reactive.event(input.selected_node)
    async def update_node_properties():
        if node_data.get() is not None and input.selected_node():
            nodes = node_data.get()
            selected_id = input.selected_node()
            
            for node in nodes:
                if str(node["id"]) == selected_id:
                    await session.send_custom_message(
                        "update-node-properties",
                        {
                            "color": node.get("color", "#97c2fc"),
                            "size": node.get("size", 25),
                        },
                    )
                    ui.update_select("node_shape", selected=node.get("shape", "dot"))
                    ui.update_text("node_label", value=node.get("label", str(selected_id)))
                    break

    @reactive.effect
    @reactive.event(input.apply_changes)
    def apply_node_changes():
        if node_data.get() is not None and input.selected_node():
            nodes = node_data.get()
            selected_id = input.selected_node()
            
            updated_nodes = []
            for node in nodes:
                node_copy = node.copy()
                if str(node_copy["id"]) == selected_id:
                    node_copy["shape"] = input.node_shape()
                    node_copy["color"] = input.node_color()
                    node_copy["size"] = input.node_size()
                    node_copy["label"] = input.node_label() or str(selected_id)  # Use ID if label is empty
                updated_nodes.append(node_copy)
            
            node_data.set(updated_nodes)
            last_button.set("generate")
            cached_html.set(None)
            
            # Force redraw of the network
            html_content = generate_network_html()
            cached_html.set(html_content)

    @render.text
    @reactive.event(input.network_data)
    def network_data():
        if input.network_data() is not None:
            try:
                data = json.loads(input.network_data())
                if "error" in data:
                    return f"Error: {data['error']}"
                node_data.set(data["nodes"])
                edge_data.set(data["edges"])
                return (
                    f"Nodes: {json.dumps(data['nodes'], indent=2)}\n"
                    f"Edges: {json.dumps(data['edges'], indent=2)}"
                )
            except json.JSONDecodeError:
                return "Error parsing network data"
            except Exception as e:
                return f"Unexpected error: {str(e)}"
        return "No data received yet. Click 'Get Data from Network' after generating a network."

    @render.data_frame
    def node_table():
        if node_data.get() is None:
            return pd.DataFrame()
        df = pd.DataFrame(node_data.get())
        cols = ["id", "label", "shape", "color", "size", "x", "y"]
        existing_cols = [col for col in cols if col in df.columns]
        other_cols = [col for col in df.columns if col not in cols]
        return df[existing_cols + other_cols]

    @render.data_frame
    def edge_table():
        if edge_data.get() is None:
            return pd.DataFrame()
        df = pd.DataFrame(edge_data.get())
        cols = ["id", "from", "to", "color", "width"]
        existing_cols = [col for col in cols if col in df.columns]
        other_cols = [col for col in df.columns if col not in cols]
        return df[existing_cols + other_cols]

    def generate_network_html():
        if node_data.get() is not None and edge_data.get() is not None:
            net = NetworkVS(height="600px", width="100%", bgcolor="#ffffff")

            for node in node_data.get():
                net.add_node(
                    node["id"],
                    label=str(node["id"]),
                    shape=node.get("shape", "dot"),
                    color=node.get("color", "#97c2fc"),
                    group = node.get("group", 1),
                    size=node.get("size", 25),
                    **{
                        k: v
                        for k, v in node.items()
                        if k not in ["id", "label", "shape", "color", "size"]
                    },
                )

            for edge in edge_data.get():
                net.add_edge(edge["from"], edge["to"])
        else:
            G = nx.erdos_renyi_graph(input.num_nodes(), 0.3)
            net = NetworkVS(height="600px", width="100%", bgcolor="#ffffff")
            net.from_nx(G)

        net.set_options(
            """
        {
            "physics": {
                "solver": "%s"
            }
        }
        """
            % input.layout()
        )
        custom_options = {
            "nodes": {
                "shape": "box",
                "size": 30,
                "font": {
                    "size": 16
                }
            },
            "physics": {
                "barnesHut": {
                    "gravitationalConstant": -3000,
                    "springLength": 250
                }
            }
        }
        # Configure the network
        #net = configure_network_options(net)
        print("BEFORE GENERATING HTML")
        test=False
        if test:
            print(net.options['manipulation']['enabled'])
            print(net.options['manipulation']['editNode'])
            net.options['manipulation']['editNode'] =True
            print(net.options['manipulation']['initiallyActive'])
        return net.generate_html()

    @render.ui
    @reactive.event(input.generate, input.display, input.apply_changes)
    def network_output():
        if (
            last_button.get() == "generate"
            or cached_html.get() is None
            or input.apply_changes()
        ):
            html_content = generate_network_html()
            cached_html.set(html_content)
        else:
            html_content = cached_html.get()

        return ui.div(
            ui.HTML(
                f"""
                <iframe id="networkIframe" srcdoc='{html.escape(html_content)}'
                        style='width: 100%; height: 600px; border: 1px solid lightgray;'
                        sandbox='allow-scripts allow-same-origin'>
                </iframe>
                """
            )
        )


app = App(app_ui, server)