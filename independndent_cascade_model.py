import random
import numpy as np
import networkx as nx
from enum import Enum

class SeedSelection(Enum):
    RANDOM = 'random'
    HIGH_DEGREE = 'high_degree'
    HIGH_BETWEENNESS = 'high_betweenness'

# Function to implement the Independent Cascade Model
def independent_cascade(G_original, alpha=0.1, seed_fraction=0.05, seed_selection=SeedSelection.RANDOM):
    """
    Simulates the Independent Cascade Model on a directed graph.

    Parameters:
    - G_original: Directed networkx graph.
    - alpha: Influence probability per edge.
    - seed_fraction: Fraction of nodes to use as random seeds.

    Returns:
    - Set of all activated nodes.
    """

    G = G_original.copy()

    nx.set_node_attributes(G, 'inactive', name='status')

    # Initialize
    nodes = list(G.nodes())
    seed_count = max(1, int(len(nodes) * seed_fraction))

    # === Seed selection strategies ===
    if seed_selection == SeedSelection.RANDOM:
        seeds = set(random.sample(nodes, seed_count))
    elif seed_selection == SeedSelection.HIGH_DEGREE:
        degree_sorted = sorted(G.degree, key=lambda x: x[1], reverse=True)
        seeds = set([node for node, _ in degree_sorted[:seed_count]])
    elif seed_selection == SeedSelection.HIGH_BETWEENNESS:
        betweenness = nx.betweenness_centrality(G)
        sorted_nodes = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
        seeds = set([node for node, _ in sorted_nodes[:seed_count]])
    else:
        raise ValueError("Unsupported seed_selection strategy")

    activated = set(seeds)
    newly_activated = set(seeds)

    nodes_removed = []
    nodes_removed.append(0)
    llc_size = []
    llc_size.append(calculate_llc_size(G))

    # Mark seed nodes as 'active'
    for seed in seeds:
        G.nodes[seed]['status'] = 'active'

    # Propagation loop
    while newly_activated:
        llc_size.append(calculate_llc_size(G))
        nodes_removed.append(len(activated)/len(nodes) * 100)
        next_activated = set()
        for node in newly_activated:
            for neighbor in G.neighbors(node):
                if G.nodes[neighbor]['status'] == 'inactive' and random.random() <= alpha:
                    G.nodes[neighbor]['status'] = 'active'
                    next_activated.add(neighbor)
        newly_activated = next_activated
        activated.update(newly_activated)

    return G, activated, nodes_removed, llc_size


def calculate_llc_size(G):
    # Filter only active nodes
    active_nodes = [n for n, attr in G.nodes(data=True) if attr.get('status') == 'inactive']

    # Create subgraph of active nodes
    G_active = G.subgraph(active_nodes)

    # Get connected components (for undirected graphs)
    if isinstance(G_active, nx.DiGraph):
        G_active = G_active.to_undirected()

    components = list(nx.connected_components(G_active))

    if not components:
        return 0  # No active component

    llc = max(components, key=len)
    return len(llc)