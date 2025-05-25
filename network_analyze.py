import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from build_power_grid_with_load import G

def draw_network(G, title="Network Visualization"):
    pos = nx.spring_layout(G, k=0.15, seed=42)
    plt.figure(figsize=(12, 12))

    nx.draw_networkx_nodes(G, pos, node_size=300, node_color='skyblue')
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8)

    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def analyze_network(G):
    print("===== Basic Network Properties =====")
    print(f"Number of nodes: {G.number_of_nodes()}")
    print(f"Number of edges: {G.number_of_edges()}")
    print(f"Density: {nx.density(G):.4f}")
    print(f"Is connected? {nx.is_connected(G)}")

    if nx.is_connected(G):
        diameter = nx.diameter(G)
        avg_shortest_path = nx.average_shortest_path_length(G)
        print(f"Diameter: {diameter}")
        print(f"Average shortest path length: {avg_shortest_path:.4f}")
    else:
        largest_cc = max(nx.connected_components(G), key=len)
        subG = G.subgraph(largest_cc)
        diameter = nx.diameter(subG)
        avg_shortest_path = nx.average_shortest_path_length(subG)
        print("Graph is not connected. Analyzing largest connected component...")
        print(f"Diameter (LCC): {diameter}")
        print(f"Avg. shortest path length (LCC): {avg_shortest_path:.4f}")

    print("\n===== Degree & Distribution =====")
    degrees = [deg for _, deg in G.degree()]
    avg_degree = np.mean(degrees)
    print(f"Average degree: {avg_degree:.2f}")

    print("\n===== Centrality Measures =====")
    deg_cent = nx.degree_centrality(G)
    bet_cent = nx.betweenness_centrality(G)
    clo_cent = nx.closeness_centrality(G)
    eig_cent = nx.eigenvector_centrality(G, max_iter=1000)

    print(f"Top 5 nodes by degree centrality:")
    print(sorted(deg_cent.items(), key=lambda x: -x[1])[:5])

    print(f"\nTop 5 nodes by betweenness centrality:")
    print(sorted(bet_cent.items(), key=lambda x: -x[1])[:5])

    print(f"\nTop 5 nodes by closeness centrality:")
    print(sorted(clo_cent.items(), key=lambda x: -x[1])[:5])

    print(f"\nTop 5 nodes by eigenvector centrality:")
    print(sorted(eig_cent.items(), key=lambda x: -x[1])[:5])

    print("\n===== Clustering & Connectivity =====")
    avg_clust = nx.average_clustering(G)
    assort = nx.degree_assortativity_coefficient(G)
    print(f"Average clustering coefficient: {avg_clust:.4f}")
    print(f"Assortativity (degree correlation): {assort:.4f}")

    print("\n===== Component Analysis =====")
    components = list(nx.connected_components(G))
    print(f"Number of connected components: {len(components)}")
    print(f"Size of largest component: {len(max(components, key=len))}")

    # Return computed properties for reuse
    return {
        'degree_centrality': deg_cent,
        'betweenness_centrality': bet_cent,
        'closeness_centrality': clo_cent,
        'eigenvector_centrality': eig_cent,
        'average_clustering': avg_clust,
        'assortativity': assort,
        'diameter': diameter,
        'average_shortest_path_length': avg_shortest_path,
        'average_degree': avg_degree,
        'connected_components': components
    }

if __name__ == "__main__":
    draw_network(G, "Power Grid Network Texas dataset")
    network_props = analyze_network(G)