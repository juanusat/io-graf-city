import osmnx as ox
import matplotlib.pyplot as plt

place = "Chiclayo, Lambayeque, Peru"
G = ox.graph_from_place(place, network_type="drive")

G_proj = ox.project_graph(G)
fig, ax = ox.plot_graph(G_proj,
                        node_size=5,
                        edge_color="gray",
                        edge_linewidth=0.7,
                        show=False,
                        close=False)
plt.title("Grafo vial de Chiclayo")
plt.savefig("chiclayo_graph.png", dpi=300)
# plt.show()

ox.save_graphml(G_proj, "chiclayo_graph.graphml")