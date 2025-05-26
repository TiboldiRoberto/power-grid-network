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

    G = G_original.copy()

    nx.set_node_attributes(G, 'functional', name='status')

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

    failed = set(seeds)
    newly_failed = set(seeds)

    nodes_removed = []
    nodes_removed.append(0)
    llc_size = []
    llc_size.append(calculate_llc_size(G))

    # Mark seed nodes as 'failed'
    for seed in seeds:
        G.nodes[seed]['status'] = 'failed'

    # Propagation loop
    while newly_failed:
        llc_size.append(calculate_llc_size(G))
        nodes_removed.append(len(failed)/len(nodes) * 100)
        next_failed = set()
        for node in newly_failed:
            for neighbor in G.neighbors(node):
                if G.nodes[neighbor]['status'] == 'functional' and random.random() <= alpha:
                    G.nodes[neighbor]['status'] = 'failed'
                    next_failed.add(neighbor)
        newly_failed = next_failed
        failed.update(newly_failed)

    return G, failed, nodes_removed, llc_size


def calculate_llc_size(G):
    # Filter only functional nodes
    failed_nodes = [n for n, attr in G.nodes(data=True) if attr.get('status') == 'functional']

    # Create subgraph of failed nodes
    G_failed = G.subgraph(failed_nodes)

    # Get connected components (for undirected graphs)
    if isinstance(G_failed, nx.DiGraph):
        G_failed = G_failed.to_undirected()

    components = list(nx.connected_components(G_failed))

    if not components:
        return 0  # No failed component

    llc = max(components, key=len)
    return len(llc)