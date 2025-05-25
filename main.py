from build_power_grid_with_load import G
from independndent_cascade_model import independent_cascade

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# Optional: Layout for visualization (spring layout spreads nodes out nicely)
pos = nx.spring_layout(G, k=0.15, seed=42)

plt.figure(figsize=(10, 10))

# Draw nodes and edges
nx.draw_networkx_nodes(G, pos, node_size=300, node_color='skyblue')
nx.draw_networkx_edges(G, pos, alpha=0.5)

# Draw node labels (Bus IDs)
labels = {node: node for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels, font_size=10)

plt.title("Power Grid Network with Bus IDs")
plt.axis('off')
plt.tight_layout()
plt.savefig("power_grid_network.png", dpi=300)
print("✅ Saved power_nodes_plot.png")

# Run the model with default alpha and random seeds
G_with_status, activated_nodes_with_status = independent_cascade(G, 0.5)

# Return summary
len(activated_nodes_with_status), G_with_status.number_of_nodes(), G_with_status.number_of_edges()

# Optional: Layout for visualization (spring layout spreads nodes out nicely)
pos = nx.spring_layout(G_with_status, k=0.15, seed=42)

# Map node status to color
node_colors = [
    'red' if G_with_status.nodes[n]['status'] == 'active' else 'skyblue'
    for n in G_with_status.nodes()
]

plt.figure(figsize=(10, 10))

# Draw nodes and edges
nx.draw_networkx_nodes(G, pos, node_size=300, node_color=node_colors)
nx.draw_networkx_edges(G, pos, alpha=0.5)

# Draw node labels (Bus IDs)
labels = {node: node for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels, font_size=10)

plt.title("Independent Cascade Model: Active vs Inactive Nodes")
plt.axis('off')
plt.tight_layout()
plt.savefig("independent_cascade_model_1i.png", dpi=300)
print("✅ Saved independent_cascade_model_1i.png")