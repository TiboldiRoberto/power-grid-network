import random
import numpy as np
import networkx as nx

# Function to implement the Independent Cascade Model
def independent_cascade(G_original, alpha=0.1, seed_fraction=0.05):
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
    seeds = set(random.sample(nodes, seed_count))

    # Mark seed nodes as 'active'
    for seed in seeds:
        G.nodes[seed]['status'] = 'active'

    activated = set(seeds)
    newly_activated = set(seeds)

    # Propagation loop
    while newly_activated:
        next_activated = set()
        for node in newly_activated:
            for neighbor in G.neighbors(node):
                if G.nodes[neighbor]['status'] == 'inactive' and random.random() <= alpha:
                    G.nodes[neighbor]['status'] = 'active'
                    next_activated.add(neighbor)
        newly_activated = next_activated
        activated.update(newly_activated)

    return G, activated