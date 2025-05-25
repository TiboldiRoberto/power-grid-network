import pandas as pd
import networkx as nx

# === 1. Cargar datos de buses y ramas ===
bus_df = pd.read_csv("bus.csv")         # <-- aquí se cargan los datos de buses
branch_df = pd.read_csv("branch.csv")   # <-- aquí se cargan los datos de ramas (conexiones)

# === 2. Usar MW Load como carga inicial (L_i) ===
# bus_df['Load_MW'] = bus_df['MW Load']

# === 3. Definir parámetro alpha (20% de margen de tolerancia) ===
# alpha = 0.1
# bus_df['Capacity_MW'] = bus_df['Load_MW'] * (1 + alpha)

# === 4. Crear el grafo de la red eléctrica ===
G = nx.Graph()

# Añadir nodos con carga y capacidad
for _, row in bus_df.iterrows():
    G.add_node(row['Bus ID'])

# Añadir aristas entre buses
for _, row in branch_df.iterrows():
    from_bus = row['From Bus']
    to_bus = row['To Bus']
    G.add_edge(from_bus, to_bus)

# === 5. Mostrar resumen ===
print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
