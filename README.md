# NetVis Documentation

## Overview
NetVis is a Python library that combines the powerful analytic capabilities of NetworkX with the interactive visualization features of PyVis. It provides a seamless way to create, analyze, and visualize complex networks.

## Features
- Create and manipulate graphs using NetworkX.
- Visualize graphs interactively with PyVis.
- Easy-to-use interface for network analysis and visualization.

## Installation
You can install NetVis using pip. Run the following command in your terminal:

```
pip install netvis
```

## Usage
Here is a simple example of how to use the NetVis library:

```python
from netvis.network import Network

# Create a new network
net = Network()

# Add nodes and edges
net.add_node('A')
net.add_node('B')
net.add_edge('A', 'B')

# Visualize the network
net.visualize('my_network.html')
```

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.