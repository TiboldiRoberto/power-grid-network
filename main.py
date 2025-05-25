from build_power_grid_with_load import G
from independndent_cascade_model import independent_cascade, SeedSelection

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
# G_with_status, activated_nodes_with_status, nodes_removed, llc_size = independent_cascade(G, 0.3, 0.05, SeedSelection.HIGH_BETWEENNESS)
# print(nodes_removed)
# print(llc_size)

G_betw, _, removed_betw, llc_betw = independent_cascade(G, alpha=0.3, seed_fraction=0.05, seed_selection=SeedSelection.HIGH_BETWEENNESS)
G_deg, _, removed_deg, llc_deg = independent_cascade(G, alpha=0.3, seed_fraction=0.05, seed_selection=SeedSelection.HIGH_DEGREE)
G_rand, _, removed_rand, llc_rand = independent_cascade(G, alpha=0.3, seed_fraction=0.05, seed_selection=SeedSelection.RANDOM)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(removed_betw, llc_betw, marker='o', label='High Betweenness')
plt.plot(removed_deg, llc_deg, marker='s', label='High Degree')
plt.plot(removed_rand, llc_rand, marker='^', label='Random')

plt.xlabel('% of Nodes Activated')
plt.ylabel('LLC Size (Active Subgraph)')
plt.title('ICM Spread: % of Nodes Activated vs. LLC Size')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("nodes_removed_vs_llc.png", dpi=300)
print("✅ Saved nodes_removed_vs_llc.png")

# # Return summary
# len(activated_nodes_with_status), G_with_status.number_of_nodes(), G_with_status.number_of_edges()
#
# # Optional: Layout for visualization (spring layout spreads nodes out nicely)
# pos = nx.spring_layout(G_with_status, k=0.15, seed=42)
#
# # Map node status to color
# node_colors = [
#     'red' if G_with_status.nodes[n]['status'] == 'active' else 'skyblue'
#     for n in G_with_status.nodes()
# ]
#
# plt.figure(figsize=(10, 10))
#
# # Draw nodes and edges
# nx.draw_networkx_nodes(G, pos, node_size=300, node_color=node_colors)
# nx.draw_networkx_edges(G, pos, alpha=0.5)
#
# # Draw node labels (Bus IDs)
# labels = {node: node for node in G.nodes()}
# nx.draw_networkx_labels(G, pos, labels, font_size=10)
#
# plt.title("Independent Cascade Model: Active vs Inactive Nodes")
# plt.axis('off')
# plt.tight_layout()
# plt.savefig("independent_cascade_model_1i.png", dpi=300)
# print("✅ Saved independent_cascade_model_1i.png")