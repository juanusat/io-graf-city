# extract_map.py
# Extrae y guarda el grafo vial de Chiclayo, Lambayeque, Perú, y lo dibuja.

import osmnx as ox
import matplotlib.pyplot as plt

# 1. Definir lugar y descargar grafo de carreteras
place = "Chiclayo, Lambayeque, Peru"
G = ox.graph_from_place(place, network_type="drive")

# 2. Simplificar y proyectar el grafo para dibujo en coordenadas planas
G_proj = ox.project_graph(G)

# 3. Dibujar y guardar la figura
fig, ax = ox.plot_graph(G_proj,
                        node_size=5,
                        edge_color="gray",
                        edge_linewidth=0.7,
                        show=False,
                        close=False)
plt.title("Grafo vial de Chiclayo")
plt.savefig("chiclayo_graph.png", dpi=300)
plt.show()

# 4. Guardar el grafo en formato GraphML para reutilizar
ox.save_graphml(G_proj, "chiclayo_graph.graphml")
